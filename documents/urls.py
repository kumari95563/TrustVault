from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_document, name="upload_document"),
    path("documents/", views.document_list, name="document_list"),
    path(
        "share/<int:document_id>/",
        views.share_document,
        name="share_document"
    ),
    path(
        "download/<int:document_id>/",
        views.download_document,
        name="download_document"
    ),
    path(
        "revoke/<int:document_id>/<int:permission_id>/",
        views.revoke_document_access,
        name="revoke_document_access"
    ),
]