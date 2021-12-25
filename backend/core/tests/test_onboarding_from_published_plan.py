from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from core.apps.onboarding.views import (
    SurveyOnboardingAPIView,
    PublishedPlanOnboardingAPIView,
)
from core.apps.published_plans.models import PublishedPlan
from core.apps.published_plans.views import PublishedPlansViewset
from core.apps.users.models import User
from core.tests._utilities import delete_firebase_user_if_exists


class FakeAdmin:
    is_anonymous = False


class OnboardingTestCase(TestCase):
    def setUp(self) -> None:
        self.admin_email = "onboard_django_test@email.com"
        delete_firebase_user_if_exists(self.admin_email)
        self.admin_account = {
            "email": self.admin_email,
            "password": "random_password",
            "first_name": "Two Cents User",
        }
        self.pp_user_email = "published_plan@user.ca"
        delete_firebase_user_if_exists(self.pp_user_email)
        self.pp_user_account = {
            "email": self.pp_user_email,
            "password": "random_password",
            "first_name": "Published Plan Onboarded User",
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
        self.admin_onboard_data = {
            "account": self.admin_account,
            "financial_profile": self.financial_profile,
            "goals": self.goals,
            "investments": self.investments,
            "loans": self.loans,
        }

    def onboard_admin_with_survey(self):
        factory = APIRequestFactory()
        request = factory.post(
            "api/my/account/onboard", data=self.admin_onboard_data, format="json"
        )
        request.user = AnonymousUser()
        view = SurveyOnboardingAPIView.as_view()
        response = view(request)
        assert response.status_code == status.HTTP_200_OK, response.data
        user = User.objects.get(email=self.admin_email)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

    def create_published_plan(self, admin_user: User):
        factory = APIRequestFactory()
        request = factory.post("api/published-plan", format="json")
        force_authenticate(request, user=admin_user)
        view = PublishedPlansViewset.as_view({"post": "create"})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK, response.data
        plan_id = response.data.get("id")
        assert plan_id is not None
        plan = PublishedPlan.objects.get(pk=plan_id)
        assert isinstance(plan, PublishedPlan)
        return plan

    def onboard_from_published_plan(self, published_plan: PublishedPlan):
        factory = APIRequestFactory()
        plan_id = published_plan.pk
        data = {"published_plan_id": plan_id, "account": self.pp_user_account}
        request = factory.post(
            "api/my/account/onboard/from-published-plan", data=data, format="json"
        )
        force_authenticate(request, user=None)
        view = PublishedPlanOnboardingAPIView.as_view()
        response = view(request)
        assert response.status_code == status.HTTP_200_OK, response.data
        new_user = User.objects.get(email=self.pp_user_email)
        assert isinstance(new_user, User)
        return new_user

    def test_onboard_post(self):
        admin_user = self.onboard_admin_with_survey()
        published_plan = self.create_published_plan(admin_user)
        new_user = self.onboard_from_published_plan(published_plan)
        equal_length_assertions = [
            (new_user.loans.all(), admin_user.loans.all()),
            (new_user.investments.all(), admin_user.investments.all()),
            (new_user.goals.all(), admin_user.goals.all()),
        ]
        for new, admin in equal_length_assertions:
            assert len(new) == len(admin), (new, admin)
        financial_profile_attrs = (
            "birth_date",
            "risk_tolerance",
            "retirement_age",
            "monthly_salary_before_tax",
            "percent_salary_for_spending",
            "starting_rrsp_contribution_limit"
            # There's more but it's fine
        )
        for attr in financial_profile_attrs:
            admin = getattr(admin_user.financial_profile, attr)
            new = getattr(new_user.financial_profile, attr)
            assert admin == new, (attr, new, admin)
