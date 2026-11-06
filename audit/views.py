
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import AuditLog


@login_required
@role_required("ADMIN")
def audit_dashboard(request):

    logs = AuditLog.objects.select_related(
        "user",
        "document"
    ).order_by("-timestamp")

    return render(
        request,
        "audit/audit_dashboard.html",
        {"logs": logs}
    )
