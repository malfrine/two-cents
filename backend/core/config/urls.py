from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from core.apps.onboarding.views import (
    SurveyOnboardingAPIView,
    PublishedPlanOnboardingAPIView,
)
from core.apps.payments.views import StripeWebhookAPIView
from core.apps.users.views import SessionAPIView, WaitlistUserAPIView
from core.config.api import api

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("api/", include(api.urls)),
    path("api/my/session", SessionAPIView.as_view()),
    path("api/waitlist", WaitlistUserAPIView.as_view()),
    path("api/my/account/onboard", SurveyOnboardingAPIView.as_view()),
    path("api/my/account/onboard/from-survey", SurveyOnboardingAPIView.as_view()),
    path(
        "api/my/account/onboard/from-published-plan",
        PublishedPlanOnboardingAPIView.as_view(),
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/stripe-hooks", StripeWebhookAPIView.as_view()),
]
