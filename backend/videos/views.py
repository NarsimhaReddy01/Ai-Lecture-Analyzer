# backend/videos/views.py
import boto3
import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import LectureVideo
from .tasks import process_video  # Celery task
from .serializers import LectureVideoSerializer
from rest_framework.views import APIView

# -------------------------
# 1️⃣ Generate Presigned URL & Upload Video Metadata
# -------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_presigned_url(request):
    file_name = request.data.get('file_name')
    file_type = request.data.get('file_type')

    if not file_name or not file_type:
        return Response({"error": "file_name and file_type are required"}, status=400)

    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=getattr(settings, 'AWS_S3_REGION_NAME', None)
    )

    unique_id = str(uuid.uuid4())
    key = f"uploads/{unique_id}_{file_name}"

    presigned_post = s3.generate_presigned_post(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key,
        Fields={"Content-Type": file_type},
        Conditions=[{"Content-Type": file_type}],
        ExpiresIn=3600
    )

    # Save video metadata in DB with status "pending"
    video = LectureVideo.objects.create(
        user=request.user,
        title=file_name,
        s3_key=key,
        s3_url=f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{key}",
        status='pending',
        transcription_status="pending"
    )

    # Trigger Celery task asynchronously
    process_video.delay(video.id)

    return Response({
        'data': presigned_post,
        'file_url': video.s3_url,
        'video_id': video.id,
        'message': "Presigned URL generated and processing started"
    })


# -------------------------
# 2️⃣ Fetch Video Processing Results
# -------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_video_results(request, video_id):
    try:
        video = LectureVideo.objects.get(id=video_id, user=request.user)
    except LectureVideo.DoesNotExist:
        return Response({"error": "Video not found"}, status=404)

    return Response({
        "video_id": video.id,
        "title": video.title,
        "status": video.status,
        "transcript": video.transcript or "",
        "summary": video.summary or "",
        "quiz": video.quiz_questions or [],
        "s3_url": video.s3_url
    })



# -------------------------
# 4️⃣ Check Video Status
# -------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def video_status(request, video_id):
    try:
        video = LectureVideo.objects.get(id=video_id, user=request.user)
        return Response({
            "status": video.status,
            "transcript": video.transcript or "",
            "summary": video.summary or "",
            "quiz_questions": video.quiz_questions or [],
        })
    except LectureVideo.DoesNotExist:
        return Response({"error": "Video not found"}, status=404)


# -------------------------
# 5️⃣ Optional: APIView for all videos
# -------------------------
class VideoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = LectureVideo.objects.filter(user=request.user).order_by('-uploaded_at')
        serializer = LectureVideoSerializer(videos, many=True)
        return Response(serializer.data)

