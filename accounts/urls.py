
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="user_login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.user_logout, name="user_logout"),

    path("create-invitation/", views.create_invitation, name="create_invitation"),
    path("invite/<str:token>/", views.accept_invitation, name="accept_invitation"),
]