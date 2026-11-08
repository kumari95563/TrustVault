from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Invitation


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('TrustVault Role', {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('TrustVault Role', {'fields': ('role',)}),
    )


admin.site.register(User, CustomUserAdmin)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'invited_by', 'created_at', 'expires_at', 'used_at')
    readonly_fields = ('token_hash', 'created_at', 'used_at')
