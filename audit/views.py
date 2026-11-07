
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

    chain_valid = AuditLog.verify_chain()

    return render(
        request,
        "audit/audit_dashboard.html",
        {
            "logs": logs,
            "chain_valid": chain_valid
        }
    )
