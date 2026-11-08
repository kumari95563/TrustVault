"""from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        OWNER = "OWNER", "Document Owner"
        VIEWER = "VIEWER", "Viewer"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.VIEWER
    )"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        OWNER = "OWNER", "Document Owner"
        VIEWER = "VIEWER", "Viewer"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.VIEWER
    )


class Invitation(models.Model):

    email = models.EmailField()

    role = models.CharField(
        max_length=10,
        choices=User.Role.choices
    )

    token_hash = models.CharField(
        max_length=64,
        unique=True
    )

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        return (
            self.used_at is None
            and timezone.now() < self.expires_at
        )

    def __str__(self):
        return f"{self.email} - {self.role}"