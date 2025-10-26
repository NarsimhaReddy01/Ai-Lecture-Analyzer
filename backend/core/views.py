from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage

from videos.tasks import process_video

class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        file_name = default_storage.save(file.name, file)
        file_path = default_storage.path(file_name)

        # Trigger AI processing in background
        process_video.delay(file_path)

        return Response({
            "message": "Upload successful! Processing started.",
            "file_name": file_name
        }, status=status.HTTP_200_OK)

