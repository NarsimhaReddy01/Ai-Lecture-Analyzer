from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Admin Panel
    path("admin/", admin.site.urls),

    # ✅ API routes stay separated
    path("api/users/", include("users.urls")),
    path("api/videos/", include("videos.urls")),
]

# ✅ All non-admin & non-API routes → return React index.html
urlpatterns += [
    re_path(r"^(?!admin|api).*$", TemplateView.as_view(template_name="index.html")),
]
