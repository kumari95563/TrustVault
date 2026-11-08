
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import secrets
import hashlib

from .models import User, Invitation


class InvitationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username="testadmin",
            password="TestAdmin@123",
            role="ADMIN"
        )

    def create_invitation(self):
        token = secrets.token_urlsafe(32)
        invitation = Invitation.objects.create(
            email="newuser@example.com",
            role="VIEWER",
            token_hash=hashlib.sha256(token.encode()).hexdigest(),
            invited_by=self.admin,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        return token, invitation

    def test_admin_can_create_invitation(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("create_invitation"),
            {"email": "viewer@example.com", "role": "VIEWER"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Invitation.objects.filter(email="viewer@example.com").exists()
        )

    def test_non_admin_cannot_create_invitation(self):
        owner = User.objects.create_user(
            username="testowner", password="TestOwner@123", role="OWNER"
        )
        self.client.force_login(owner)
        response = self.client.get(reverse("create_invitation"))
        self.assertEqual(response.status_code, 403)

    def test_invitation_registration_assigns_role(self):
        token, invitation = self.create_invitation()
        response = self.client.post(
            reverse("accept_invitation", args=[token]),
            {
                "username": "newviewer",
                "password": "StrongPass@123",
                "confirm_password": "StrongPass@123"
            }
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="newviewer")
        self.assertEqual(user.role, "VIEWER")
        invitation.refresh_from_db()
        self.assertIsNotNone(invitation.used_at)

    def test_used_invitation_cannot_be_reused(self):
        token, invitation = self.create_invitation()
        invitation.used_at = timezone.now()
        invitation.save(update_fields=["used_at"])
        response = self.client.get(
            reverse("accept_invitation", args=[token])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invitation Expired or Invalid")

    def test_expired_invitation_is_rejected(self):
        token, invitation = self.create_invitation()
        invitation.expires_at = timezone.now() - timedelta(hours=1)
        invitation.save(update_fields=["expires_at"])
        response = self.client.get(
            reverse("accept_invitation", args=[token])
        )
        self.assertContains(response, "Invitation Expired or Invalid")
