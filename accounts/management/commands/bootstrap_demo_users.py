import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create TrustVault demo users"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        users = [
            ("TV_ADMIN_USERNAME", "TV_ADMIN_PASSWORD", "ADMIN"),
            ("TV_OWNER_USERNAME", "TV_OWNER_PASSWORD", "OWNER"),
            ("TV_VIEWER_USERNAME", "TV_VIEWER_PASSWORD", "VIEWER"),
        ]

        for username_key, password_key, role in users:
            username = os.getenv(username_key)
            password = os.getenv(password_key)

            if not username or not password:
                raise CommandError("Demo user environment variables are missing.")

            user, created = User.objects.get_or_create(
                username=username,
                defaults={"role": role}
            )

            user.role = role

            if role == "ADMIN":
                user.is_staff = True
                user.is_superuser = True

            if created:
                user.set_password(password)

            user.save()

            self.stdout.write(f"{role} account ready.")