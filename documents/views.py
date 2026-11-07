
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .forms import DocumentUploadForm, DocumentShareForm
from .models import Document, DocumentPermission
from accounts.decorators import role_required
from audit.models import AuditLog

# Upload Document
@login_required
@role_required("ADMIN", "OWNER")
def upload_document(request):

    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()
            AuditLog.objects.create(
                user=request.user,
                action="UPLOAD",
                document=document,
                details="Document uploaded successfully"
            )

            messages.success(request, "Document uploaded successfully!")
            return redirect("upload_document")

    else:
        form = DocumentUploadForm()

    return render(request, "documents/upload.html", {
        "form": form
    })


# Document List
@login_required
def document_list(request):

    if request.user.role == "ADMIN":
        documents = Document.objects.all()

    elif request.user.role == "OWNER":
        documents = Document.objects.filter(
            owner=request.user
        )

    else:
        documents = Document.objects.filter(
            permissions__user=request.user,
            permissions__access_level__in=["READ", "EDIT"]
        ).distinct()

    return render(request, "documents/document_list.html", {
        "documents": documents
    })


# Share Document
@login_required
@role_required("ADMIN", "OWNER")
def share_document(request, document_id):

    document = get_object_or_404(Document, id=document_id)

    # Owner can share only their own documents
    if request.user.role == "OWNER" and document.owner != request.user:
        raise PermissionDenied

    if request.method == "POST":
        form = DocumentShareForm(
            request.POST,
            owner=document.owner
        )

        if form.is_valid():
            DocumentPermission.objects.update_or_create(
                document=document,
                user=form.cleaned_data["user"],
                defaults={
                    "access_level": form.cleaned_data["access_level"],
                    "granted_by": request.user
                }
            )
            AuditLog.objects.create(
                user=request.user,
                action="SHARE",
                document=document,
                details=f"Shared with {form.cleaned_data['user'].username}"
            )

            messages.success(
                request,
                "Document shared successfully!"
            )

            return redirect("document_list")

    else:
        form = DocumentShareForm(owner=document.owner)

    return render(request, "documents/share.html", {
        "form": form,
        "document": document
    })
# Secure Document Download
@login_required
def download_document(request, document_id):

    document = get_object_or_404(Document, id=document_id)

    # Administrator can download all documents
    if request.user.role == "ADMIN":
        allowed = True

    # Owner can download only their own documents
    elif request.user.role == "OWNER":
        allowed = document.owner == request.user

    # Viewer needs READ or EDIT permission
    else:
        allowed = DocumentPermission.objects.filter(
            document=document,
            user=request.user,
            access_level__in=["READ", "EDIT"]
        ).exists()

    if not allowed:
        AuditLog.objects.create(
            user=request.user,
            action="DENIED_ACCESS",
            document=document,
            details="Unauthorized document download attempt"
        )
        raise PermissionDenied
    AuditLog.objects.create(
        user=request.user,
        action="DOWNLOAD",
        document=document,
        details="Document downloaded successfully"
    )

    from django.http import FileResponse

    return FileResponse(
        document.file.open("rb"),
        as_attachment=True,
        filename=document.file.name.split("/")[-1]
    )

from django.views.decorators.http import require_POST


@login_required
@role_required("ADMIN", "OWNER")
@require_POST
def revoke_document_access(request, document_id, permission_id):

    document = get_object_or_404(Document, id=document_id)

    if request.user.role == "OWNER" and document.owner != request.user:
        raise PermissionDenied

    permission = get_object_or_404(
        DocumentPermission,
        id=permission_id,
        document=document
    )

    viewer_name = permission.user.username

    permission.delete()

    AuditLog.objects.create(
        user=request.user,
        action="REVOKE",
        document=document,
        details=f"Access revoked for {viewer_name}"
    )

    messages.success(request, "Document access revoked successfully!")

    return redirect("document_list")
