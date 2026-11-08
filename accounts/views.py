
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from django.contrib.auth.views import PasswordResetConfirmView
import secrets
import hashlib

from .models import User, Invitation
from audit.models import AuditLog


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "accounts/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "accounts/login.html")


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html", {
        "user": request.user
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect("user_login")


@login_required
def create_invitation(request):

    if request.user.role != "ADMIN":
        return HttpResponseForbidden("Admin access required.")

    error = None
    invitation_link = None

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        role = request.POST.get("role")

        if not email or role not in ["OWNER", "VIEWER"]:
            error = "Enter a valid email and role."

        elif User.objects.filter(email__iexact=email).exists():
            error = "This email already has an account."

        else:
            token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(token.encode()).hexdigest()

            with transaction.atomic():

                Invitation.objects.create(
                    email=email,
                    role=role,
                    token_hash=token_hash,
                    invited_by=request.user,
                    expires_at=timezone.now() + timedelta(hours=24)
                )

                AuditLog.objects.create(
                    user=request.user,
                    action="INVITATION_CREATED",
                    details=f"Invitation created for {email} with role {role}"
                )

            invitation_link = request.build_absolute_uri(
                reverse("accept_invitation", args=[token])
            )

    return render(request, "accounts/create_invitation.html", {
        "error": error,
        "invitation_link": invitation_link
    })


def accept_invitation(request, token):

    token_hash = hashlib.sha256(token.encode()).hexdigest()

    invitation = Invitation.objects.filter(
        token_hash=token_hash
    ).first()

    if not invitation or not invitation.is_valid():
        return render(request, "accounts/invitation_invalid.html")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not password:
            error = "All fields are required."

        elif password != confirm_password:
            error = "Passwords do not match."

        elif User.objects.filter(username__iexact=username).exists():
            error = "Username already exists."

        elif User.objects.filter(email__iexact=invitation.email).exists():
            error = "An account already exists for this email."

        else:
            try:
                validate_password(password)
            except ValidationError as e:
                error = " ".join(e.messages)
            else:
                with transaction.atomic():

                    invitation = get_object_or_404(
                        Invitation.objects.select_for_update(),
                        token_hash=token_hash
                    )

                    if not invitation.is_valid():
                        return render(
                            request,
                            "accounts/invitation_invalid.html"
                        )

                    user = User.objects.create_user(
                        username=username,
                        email=invitation.email,
                        password=password,
                        role=invitation.role
                    )

                    invitation.used_at = timezone.now()
                    invitation.save(update_fields=["used_at"])

                    AuditLog.objects.create(
                        user=user,
                        action="USER_REGISTERED",
                        details=f"User {username} registered with role {invitation.role} through invitation"
                    )

                return redirect("user_login")

        return render(request, "accounts/accept_invitation.html", {
            "invitation": invitation,
            "error": error
        })

    return render(request, "accounts/accept_invitation.html", {
        "invitation": invitation
    })
class CustomPasswordResetConfirmView(PasswordResetConfirmView):

    def form_valid(self, form):
        response = super().form_valid(form)

        AuditLog.objects.create(
            user=self.user,
            action="PASSWORD_RESET",
            details="User successfully reset their password."
        )

        return response