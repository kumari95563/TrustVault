from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import AuditLog

User = get_user_model()


class AuditLogTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
            role="ADMIN"
        )

    def test_audit_log_creation(self):
        log = AuditLog.objects.create(
            user=self.user,
            action="UPLOAD",
            details="Test document uploaded"
        )

        self.assertEqual(log.action, "UPLOAD")
        self.assertTrue(log.current_hash)

    def test_hash_chain_verification(self):
        AuditLog.objects.create(
            user=self.user,
            action="UPLOAD",
            details="First log"
        )

        AuditLog.objects.create(
            user=self.user,
            action="SHARE",
            details="Second log"
        )

        self.assertTrue(AuditLog.verify_chain())

    def test_hash_changes_for_different_actions(self):
        log1 = AuditLog.objects.create(
            user=self.user,
            action="UPLOAD",
            details="First log"
        )

        log2 = AuditLog.objects.create(
            user=self.user,
            action="DOWNLOAD",
            details="Second log"
        )

        self.assertNotEqual(
            log1.current_hash,
            log2.current_hash
        )
    # Test 4: Audit record cannot be modified
    def test_audit_log_cannot_be_modified(self):
        log = AuditLog.objects.create(
            user=self.user,
            action="UPLOAD",
            details="Original record"
        )

        log.details = "Modified record"

        with self.assertRaises(ValueError):
            log.save()

    # Test 5: Audit record cannot be deleted
    def test_audit_log_cannot_be_deleted(self):
        log = AuditLog.objects.create(
            user=self.user,
            action="UPLOAD",
            details="Test record"
        )

        with self.assertRaises(ValueError):
            log.delete()
    def test_tampering_is_detected(self):
        log = AuditLog.objects.create(
            user=self.user,
            action="UPLOAD",
            details="Original record"
        )

        AuditLog.objects.filter(pk=log.pk).update(
            details="Tampered record"
        )

        self.assertFalse(AuditLog.verify_chain())