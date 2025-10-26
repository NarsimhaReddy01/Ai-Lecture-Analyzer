from django.db import models
from django.contrib.auth.models import User

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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=512, unique=True)
    s3_url = models.URLField()
    duration = models.FloatField(null=True, blank=True)  # seconds
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # --- Processing fields ---
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    transcription_status = models.CharField(max_length=50, choices=TRANSCRIPTION_CHOICES, default='pending')
    transcript = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    quiz_questions = models.JSONField(blank=True, null=True)  # Use models.JSONField for cross-DB support

    def __str__(self):
        return f"{self.title} ({self.user.username})"
