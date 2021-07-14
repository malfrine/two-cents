from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from core.apps.onboarding.views import OnboardingAPIView
from core.apps.users.views import SessionAPIView, WaitlistUserAPIView

from core.config.api import api

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("api/", include(api.urls)),
    path("api/my/session", SessionAPIView.as_view()),
    path("api/waitlist", WaitlistUserAPIView.as_view()),
    path("api/my/account/onboard", OnboardingAPIView.as_view()),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
