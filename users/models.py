from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ops', 'Ops User'),
        ('client', 'Client User'),
    )
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name='filesharing_user_set',  # Add unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='filesharing_user_permissions_set',  # Add unique related_name
        blank=True
    )
