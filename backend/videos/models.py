from django.db import models
from django.contrib.auth import get_user_model


class LectureVideo(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('error', 'Error'),
    ]

    TRANSCRIPTION_CHOICES = [
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('error', 'Error'),
    ]

    # ✅ Make user optional for now — later we’ll require authentication
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


    title = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=512, unique=True)
    s3_url = models.URLField()
    duration = models.FloatField(null=True, blank=True)  # in seconds
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # --- Processing fields ---
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    transcription_status = models.CharField(max_length=50, choices=TRANSCRIPTION_CHOICES, default='pending')
    transcript = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    quiz_questions = models.JSONField(blank=True, null=True)  # Cross-DB compatible

    def __str__(self):
        return f"{self.title} ({self.user.username if self.user else 'Anonymous'})"
