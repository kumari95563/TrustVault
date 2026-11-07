from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('user_login')),
    path('accounts/', include('accounts.urls')),
    path('audit/', include('audit.urls')),
    path('', include('documents.urls')),
]