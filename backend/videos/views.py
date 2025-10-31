import boto3
import uuid
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import LectureVideo
from .tasks import process_video
from .serializers import LectureVideoSerializer


# ==========================================================
# 1️⃣ Generate Presigned URL & Create Video Record
# ==========================================================
@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_exempt
def generate_presigned_url(request):
    """
    Generates an AWS S3 presigned URL for uploading a video
    and immediately triggers Celery background processing.
    """
    print("🧾 Incoming data:", request.data)

    file_name = request.data.get("file_name")
    file_type = request.data.get("file_type")

    if not file_name or not file_type:
        return Response({"error": "file_name and file_type are required"}, status=400)

    # Initialize S3 client
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=getattr(settings, "AWS_S3_REGION_NAME", None),
    )

    unique_id = str(uuid.uuid4())
    key = f"uploads/{unique_id}_{file_name}"

    presigned_post = s3.generate_presigned_post(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key,
        Fields={"Content-Type": file_type},
        Conditions=[{"Content-Type": file_type}],
        ExpiresIn=3600,
    )

    # ✅ Safely assign user (if authenticated)
    user = request.user if request.user.is_authenticated else None

    # ✅ Create video record
    video = LectureVideo.objects.create(
        title=file_name,
        s3_key=key,
        s3_url=f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{key}",
        transcription_status="pending",
        user=user,  # <--- important line
    )

    # Trigger background task
    process_video.delay(video.id)

    return Response(
        {
            "data": presigned_post,
            "file_url": video.s3_url,
            "video_id": video.id,
            "message": "✅ Presigned URL generated and video processing started.",
        },
        status=200,
    )



# ==========================================================
# 2️⃣ Get Full Video Analysis Results
# ==========================================================
@api_view(["GET"])
@permission_classes([AllowAny])
@csrf_exempt
def get_video_results(request, video_id):
    """
    Returns the transcript, summary, quiz, and status for a given video.
    """
    try:
        video = LectureVideo.objects.get(id=video_id)
        serializer = LectureVideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except LectureVideo.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==========================================================
# 3️⃣ Check Current Video Processing Status
# ==========================================================
@api_view(["GET"])
@permission_classes([AllowAny])
@csrf_exempt
def video_status(request, video_id):
    """
    Returns the current processing status for a video (polled by frontend).
    """
    try:
        video = LectureVideo.objects.get(id=video_id)
        return Response(
            {
                "video_id": video.id,
                "title": video.title,
                "status": video.transcription_status,
                "progress": getattr(video, "progress", 0),
                "updated_at": video.updated_at,
            },
            status=status.HTTP_200_OK,
        )

    except LectureVideo.DoesNotExist:
        return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)


# ==========================================================
# 4️⃣ List All Uploaded Videos (Admin / Dashboard)
# ==========================================================
@method_decorator(csrf_exempt, name="dispatch")
class VideoListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Returns all videos ordered by most recent upload.
        """
        videos = LectureVideo.objects.all().order_by("-uploaded_at")
        serializer = LectureVideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
