from django.contrib import admin
from .models import Document, DocumentPermission

admin.site.register(Document)
admin.site.register(DocumentPermission)