from django.urls import path
from django.contrib import admin
from django.conf.urls import include

from core.config.api import api



urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("api/", include(api.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
