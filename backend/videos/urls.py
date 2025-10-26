# backend/videos/urls.py
from django.urls import path
from .views import (
    generate_presigned_url,
    get_video_results,
    video_status,
    VideoListView
)

urlpatterns = [
    path('', VideoListView.as_view(), name='video-list'),  # GET /api/videos/
    path('upload-url/', generate_presigned_url, name='generate-presigned-url'),  # POST /api/videos/upload-url/
    # path('list/', list_videos, name='list-videos'),  # GET /api/videos/list/
    path('<int:video_id>/results/', get_video_results, name='video-results'),  # GET /api/videos/1/results/
    path('<int:video_id>/status/', video_status, name='video-status'),  # GET /api/videos/1/status/
]
