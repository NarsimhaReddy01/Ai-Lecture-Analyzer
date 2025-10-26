# backend/core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🔗 All video-related API routes under /api/videos/
    path('api/videos/', include('videos.urls')),
    
    # Optional frontend placeholder (React build integration)
    path('app/', TemplateView.as_view(template_name='index.html'), name='app'),
]
