from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from core.apps.onboarding.views import OnboardingAPIView
from core.apps.plan.views import UserPlanViewSet
from core.apps.users.models import User
from core.tests._utilities import delete_firebase_user_if_exists


class Failure1TestCase(TestCase):
    def setUp(self) -> None:
        self.email = "test.failure1@gmail.com"
        delete_firebase_user_if_exists(self.email)
        self.data = {
            "account": {
                "email": self.email,
                "first_name": "Test",
                "password": "XXXYYYZZZ",
            },
            "financial_profile": {
                "birth_date": "1994-03-20",
                "monthly_salary_before_tax": 8000,
                "percent_salary_for_spending": 20,
                "province_of_residence": "BC",
                "retirement_age": 60,
                "risk_tolerance": 50,
                "starting_rrsp_contribution_limit": 77760,
                "starting_tfsa_contribution_limit": 60500,
            },
            "goals": {"current_nest_egg_amount": 10000},
            "investments": {"non_registered": 10000, "rrsp": 0, "tfsa": 3500},
            "loans": {
                "Credit Card": {"balance": 0},
                "Student Loan": {"balance": 98000, "date": "2030-06-01"},
            },
        }

    def tearDown(self) -> None:

        pass

    def test_onboarding_and_plan_building(self):
        onboarding_view = OnboardingAPIView.as_view()
        factory = APIRequestFactory()
        request = factory.post("api/my/account/onboard", data=self.data, format="json")
        request.user = AnonymousUser()
        response = onboarding_view(request)
        assert response.status_code == status.HTTP_200_OK, response.data

        user = User.objects.get(email=self.email)
        factory = APIRequestFactory()
        request = factory.get("api/my/plan", format="json")
        force_authenticate(request, user=user)
        view = UserPlanViewSet.as_view({"get": "list"})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK, response.data
