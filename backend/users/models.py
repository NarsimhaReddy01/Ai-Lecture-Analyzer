from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default="student")

    def is_student(self):
        return self.role == "student"

    def is_teacher(self):
        return self.role == "teacher"
