from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.gis.db import models as gis_models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    ]
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='member')
    location = gis_models.PointField(null=True, blank=True)  # Add this field

    def __str__(self):
        return self.username
