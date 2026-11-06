
from django.urls import path
from . import views

urlpatterns = [
    path(
        "dashboard/",
        views.audit_dashboard,
        name="audit_dashboard"
    ),
]
