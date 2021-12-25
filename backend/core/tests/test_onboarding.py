from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from core.apps.finances.models.goals import FinancialGoal
from core.apps.finances.models.investments import Investment
from core.apps.finances.models.loans import Loan
from core.apps.onboarding.views import SurveyOnboardingAPIView
from core.apps.users.models import User
from core.apps.users.utilities import delete_user
from core.tests._utilities import delete_firebase_user_if_exists


class OnboardingTestCase(TestCase):
    def setUp(self) -> None:
        self.email = "onboard_django_test@email.com"
        delete_firebase_user_if_exists(self.email)
        self.account = {
            "email": self.email,
            "password": "random_password",
            "first_name": "Two Cents User",
        }
        self.financial_profile = {
            "birth_date": "1994-03-11",
            "retirement_age": 65,
            "risk_tolerance": 0.5,
            "monthly_salary_before_tax": 6000,
            "percent_salary_for_spending": 50,
            "starting_rrsp_contribution_limit": 20_000,
            "starting_tfsa_contribution_limit": 20_000,
            "province_of_residence": "AB",
        }
        self.goals = {
            "big_purchase": {"amount": 50_000, "date": "2030-01-01"},
            "current_nest_egg_amount": 10_000,
        }
        self.investments = {"tfsa": 25_000, "rrsp": 22_000, "non_registered": 0}
        self.loans = {
            "Student Loan": {"balance": 30_000, "date": "2030-01-01"},
            "Credit Card": {"balance": 2000, "date": None},
            "Mortgage": {"balance": 300_000, "date": "2050-01-01"},
        }
        self.data = {
            "account": self.account,
            "financial_profile": self.financial_profile,
            "goals": self.goals,
            "investments": self.investments,
            "loans": self.loans,
        }
        self.view = SurveyOnboardingAPIView.as_view()

    def test_onboard_post(self):
        factory = APIRequestFactory()
        request = factory.post("api/my/account/onboard", data=self.data, format="json")
        request.user = AnonymousUser()
        response = self.view(request)
        assert response.status_code == status.HTTP_200_OK, response.data

        user = User.objects.get(email=self.email)
        assert isinstance(user, User)

        try:  # if any of the assertions fail make sure to delete the firebase user
            loans = Loan.objects.filter(financial_data=user.financial_data)
            assert len(loans) == len(self.loans.values())

            investments = Investment.objects.filter(financial_data=user.financial_data)
            assert len(investments) == 4

            goals = FinancialGoal.objects.filter(financial_data=user.financial_data)
            assert len(goals) == 2
        except Exception:
            delete_user(user)
            raise Exception
        delete_user(user)
