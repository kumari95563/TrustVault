
from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "action",
        "document",
        "timestamp"
    )

    list_filter = ("action", "timestamp")

    search_fields = (
        "user__username",
        "action",
        "details"
    )

    readonly_fields = (
        "user",
        "action",
        "document",
        "timestamp",
        "details",
        "previous_hash",
        "current_hash"
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
