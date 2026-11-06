

from django import forms
from django.contrib.auth import get_user_model

from .models import Document, DocumentPermission

User = get_user_model()


class DocumentUploadForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ["title", "description", "category", "file"]

    def clean_file(self):
        import magic
        import zipfile

        file = self.cleaned_data.get("file")
        allowed_extensions = [".pdf", ".docx", ".txt"]

        if file:
            extension = "." + file.name.split(".")[-1].lower()

            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Only PDF, DOCX and TXT files are allowed."
                )

            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "File size must not exceed 5 MB."
                )

            content = file.read(2048)
            file.seek(0)

            if extension == ".pdf":
                valid = content.startswith(b"%PDF-")

            elif extension == ".txt":
                mime = magic.from_buffer(content, mime=True)
                valid = mime.startswith("text/")

            else:
                try:
                    file.seek(0)
                    with zipfile.ZipFile(file) as archive:
                        valid = "word/document.xml" in archive.namelist()
                except zipfile.BadZipFile:
                    valid = False
                finally:
                    file.seek(0)

            if not valid:
                raise forms.ValidationError(
                    "File content does not match its extension."
                )

        return file


class DocumentShareForm(forms.ModelForm):

    class Meta:
        model = DocumentPermission
        fields = ["user", "access_level"]

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop("owner", None)
        super().__init__(*args, **kwargs)

        self.fields["user"].queryset = User.objects.filter(role="VIEWER")

        if owner:
            self.fields["user"].queryset = (
                self.fields["user"].queryset.exclude(pk=owner.pk)
            )
