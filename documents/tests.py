
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Document, DocumentPermission
from .forms import DocumentUploadForm

User = get_user_model()


class DocumentAccessTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="test123",
            role="ADMIN"
        )

        self.owner = User.objects.create_user(
            username="owner",
            password="test123",
            role="OWNER"
        )

        self.viewer = User.objects.create_user(
            username="viewer",
            password="test123",
            role="VIEWER"
        )

        self.document = Document.objects.create(
            title="Test Document",
            description="Testing access",
            category="Personal",
            owner=self.owner,
            file=SimpleUploadedFile(
                "test.txt",
                b"TrustVault test file"
            )
        )

    # Test 1: Owner can download
    def test_owner_can_download(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            f"/download/{self.document.id}/"
        )

        self.assertEqual(response.status_code, 200)

    # Test 2: Admin can download
    def test_admin_can_download(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            f"/download/{self.document.id}/"
        )

        self.assertEqual(response.status_code, 200)

    # Test 3: Viewer without permission cannot download
    def test_viewer_without_permission_cannot_download(self):
        self.client.force_login(self.viewer)

        response = self.client.get(
            f"/download/{self.document.id}/"
        )

        self.assertEqual(response.status_code, 403)

    # Test 4: Viewer with permission can download
    def test_viewer_with_permission_can_download(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            access_level="READ",
            granted_by=self.owner
        )

        self.client.force_login(self.viewer)

        response = self.client.get(
            f"/download/{self.document.id}/"
        )

        self.assertEqual(response.status_code, 200)

    # Test 5: Viewer cannot download after revoke
    def test_viewer_cannot_download_after_revoke(self):
        permission = DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            access_level="READ",
            granted_by=self.owner
        )

        permission.delete()

        self.client.force_login(self.viewer)

        response = self.client.get(
            f"/download/{self.document.id}/"
        )

        self.assertEqual(response.status_code, 403)

    # Test 6: Invalid file extension rejected
    def test_invalid_file_extension_rejected(self):
        uploaded_file = SimpleUploadedFile(
            "malware.exe",
            b"test content"
        )

        form = DocumentUploadForm(
            data={
                "title": "Invalid File",
                "description": "Testing",
                "category": "Personal"
            },
            files={"file": uploaded_file}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)

    # Test 7: File over 5 MB rejected
    def test_file_over_5mb_rejected(self):
        uploaded_file = SimpleUploadedFile(
            "large.txt",
            b"a" * (5 * 1024 * 1024 + 1)
        )

        form = DocumentUploadForm(
            data={
                "title": "Large File",
                "description": "Testing",
                "category": "Personal"
            },
            files={"file": uploaded_file}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)
    # Test 8: Owner cannot download another owner's document
    def test_owner_cannot_download_other_owners_document(self):

        another_owner = User.objects.create_user(
            username="another_owner",
            password="test123",
            role="OWNER"
        )

        other_document = Document.objects.create(
            title="Private Document",
            description="Another owner's document",
            category="Personal",
            owner=another_owner,
            file=SimpleUploadedFile(
                "private.txt",
                b"Private content"
            )
        )

        self.client.force_login(self.owner)

        response = self.client.get(
            f"/download/{other_document.id}/"
        )

        self.assertEqual(response.status_code, 403)
    # Test 9: Fake PDF content rejected
    def test_fake_pdf_content_rejected(self):
        uploaded_file = SimpleUploadedFile(
            "fake.pdf",
            b"This is not a real PDF file"
        )

        form = DocumentUploadForm(
            data={
                "title": "Fake PDF",
                "description": "Testing fake content",
                "category": "Personal"
            },
            files={"file": uploaded_file}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)
    # Test 10: Fake DOCX content rejected
    def test_fake_docx_content_rejected(self):
        uploaded_file = SimpleUploadedFile(
            "fake.docx",
            b"This is not a valid DOCX file"
        )

        form = DocumentUploadForm(
            data={
                "title": "Fake DOCX",
                "description": "Testing fake content",
                "category": "Personal"
            },
            files={"file": uploaded_file}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("file", form.errors)
    # Test 11: Viewer cannot upload documents
    def test_viewer_cannot_upload(self):
        self.client.force_login(self.viewer)

        response = self.client.get("/upload/")

        self.assertEqual(response.status_code, 403)

    # Test 12: Viewer cannot share documents
    def test_viewer_cannot_share(self):
        self.client.force_login(self.viewer)

        response = self.client.get(
            f"/share/{self.document.id}/"
        )

        self.assertEqual(response.status_code, 403)

    # Test 13: Owner cannot see another owner's document
    def test_owner_cannot_see_other_owners_document(self):
        another_owner = User.objects.create_user(
            username="another_owner",
            password="test123",
            role="OWNER"
        )

        other_document = Document.objects.create(
            title="Secret Document",
            description="Private document",
            category="Personal",
            owner=another_owner,
            file=SimpleUploadedFile(
                "secret.txt",
                b"Secret content"
            )
        )

        self.client.force_login(self.owner)

        response = self.client.get("/documents/")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Secret Document")