# backend/core/views.py

import os
import redis
import logging
from django.http import JsonResponse
from django.db import connection
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from celery import Celery
from videos.tasks import process_video

logger = logging.getLogger(__name__)

# Load environment variables
USE_FREE_API = os.getenv("USE_FREE_API", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")


# ===============================
# 🎥 Video Upload + Background Processing
# ===============================
class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        user_mode = request.POST.get("ai_mode", "paid")  # 👈 user-selected mode
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            logger.info(f"📁 Uploading new video: {file.name}")
            file_name = default_storage.save(file.name, file)
            file_path = default_storage.path(file_name)

            # Pass mode to Celery
            process_video.delay(file_path, user_mode)

            mode_label = "Hugging Face (Free)" if user_mode == "free" else "OpenAI (Paid)"
            logger.info(f"🚀 Started AI processing in {mode_label} mode")

            return Response(
                {
                    "message": "Upload successful! Processing started.",
                    "file_name": file_name,
                    "ai_mode": mode_label
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"❌ Error while uploading: {str(e)}", exc_info=True)
            return Response(
                {"error": f"Failed to process video: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



# ===============================
# 🩺 System Health Check Endpoint
# ===============================
def health_check(request):
    """Checks the health of Database, Redis, and Celery services."""
    health = {"database": False, "redis": False, "celery": False}

    # Database check
    try:
        connection.ensure_connection()
        health["database"] = True
    except Exception as e:
        logger.error(f"⚠️ Database check failed: {e}")

    # Redis check
    try:
        r = redis.Redis(host="redis_broker", port=6379, db=0)
        r.ping()
        health["redis"] = True
    except Exception as e:
        logger.error(f"⚠️ Redis check failed: {e}")

    # ✅ Check Celery
    try:
        app = Celery("core")
        app.conf.broker_url = "redis://redis_broker:6379/0"
        insp = app.control.inspect(timeout=3)
        ping_result = insp.ping()
        if ping_result and any("ok" in v for v in ping_result.values()):
            health["celery"] = True
    except Exception as e:
        print(f"Celery health check failed: {e}")

    # ✅ Determine overall status
    status = "healthy" if all(health.values()) else "degraded"
    return JsonResponse(
        {"status": status, "health": health, "mode": "Hugging Face (Free)"}
    )
