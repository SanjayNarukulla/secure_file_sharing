from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Ops', 'Operations User'),
        ('Client', 'Client User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email_verified = models.BooleanField(default=False)

class File(models.Model):
    filename = models.CharField(max_length=100)
    file_path = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    upload_time = models.DateTimeField(default=timezone.now)
