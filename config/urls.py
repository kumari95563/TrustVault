
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('documents.urls')),
    path('accounts/', include('accounts.urls')),
    path('audit/', include('audit.urls')),
]
