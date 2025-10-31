from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    generate_presigned_url,
    get_video_results,
    video_status,
    VideoListView,
)

urlpatterns = [
    path("", VideoListView.as_view(), name="video-list"),  # GET /api/videos/
    path("upload/", csrf_exempt(generate_presigned_url), name="video-upload"),  # ✅ POST /api/videos/upload/
    path("<int:video_id>/status/", video_status, name="video-status"),  # GET /api/videos/<id>/status/
    path("<int:video_id>/results/", get_video_results, name="video-results"),  # GET /api/videos/<id>/results/
]
