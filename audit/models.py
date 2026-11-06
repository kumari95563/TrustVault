


import hashlib
import json

from django.conf import settings
from django.db import models, transaction


class AuditLog(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    action = models.CharField(max_length=100)

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    previous_hash = models.CharField(
        max_length=64,
        default="0" * 64
    )

    current_hash = models.CharField(
        max_length=64,
        blank=True
    )

    def generate_hash(self):
        data = {
            "user_id": self.user_id,
            "action": self.action,
            "document_id": self.document_id,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
            "previous_hash": self.previous_hash
        }

        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()

    def save(self, *args, **kwargs):

        if self.pk:
            raise ValueError("Audit records cannot be modified.")

        with transaction.atomic():

            last_log = (
                AuditLog.objects
                .select_for_update()
                .order_by("-id")
                .first()
            )

            if last_log:
                self.previous_hash = last_log.current_hash

            super().save(*args, **kwargs)

            self.current_hash = self.generate_hash()

            super().save(update_fields=["current_hash"])

    def delete(self, *args, **kwargs):
        raise ValueError("Audit records cannot be deleted.")

    @classmethod
    def verify_chain(cls):

        logs = cls.objects.order_by("id")
        previous_hash = "0" * 64

        for log in logs:

            if log.previous_hash != previous_hash:
                return False

            if log.current_hash != log.generate_hash():
                return False

            previous_hash = log.current_hash

        return True

    def __str__(self):
        return f"{self.user} - {self.action}"
