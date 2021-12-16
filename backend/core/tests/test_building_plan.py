import json
from typing import Dict, Callable

from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase
from rest_framework import status

from core.apps.finances.views import (
    LoanViewset,
    InvestmentViewset,
    FinancialGoalViewset,
    FinancialProfileView,
)
from core.apps.plan.views import UserPlanViewSet
from core.apps.users.models import User
from core.apps.users.utilities import delete_user
from core.tests._utilities import create_user

from rest_framework.test import APIRequestFactory, force_authenticate


def post_object_create(
    url: str, user: User, data: Dict, view: Callable,
):
    factory = APIRequestFactory()
    request = factory.post(url, data=data, format="json")
    force_authenticate(request, user=user)
    response = view(request)
    return response


class PlanBuildingTestCase(TestCase):
    def create_loans(self, user):
        loan_view = LoanViewset.as_view({"post": "create"})
        loans = [
            {
                "name": "credit card",
                "loan_type": "Credit Card",
                "loan_interest": {"interest_type": "Fixed", "apr": 20},
                "current_balance": 2000,
            },
            {
                "name": "student loan",
                "loan_type": "Student Loan",
                "loan_interest": {"interest_type": "Fixed", "apr": 3.2},
                "current_balance": 2000,
                "end_date": "2035-01-01",
                "minimum_monthly_payment": "50",
            },
            {
                "name": "mortgage",
                "loan_type": "Mortgage",
                "loan_interest": {"interest_type": "Fixed", "apr": 1.5},
                "current_balance": 300_000,
                "end_date": "2042-01-01",
                "minimum_monthly_payment": "1200",
            },
        ]
        for data in loans:
            post_object_create(
                url="/api/my/finances/loans", user=user, data=data, view=loan_view
            )

    def create_investments(self, user):
        investment_view = InvestmentViewset.as_view({"post": "create"})
        investments = [
            {
                "name": "mutual fund rrsp",
                "current_balance": 0,
                "investment_type": "Mutual Fund",
                "account_type": "RRSP",
                "pre_authorized_monthly_contribution": 0,
                "risk_level": "Low",
            },
            {
                "name": "etf tfsa",
                "current_balance": 0,
                "investment_type": "ETF",
                "account_type": "TFSA",
                "pre_authorized_monthly_contribution": 100,
                "risk_level": "Medium",
            },
            {
                "name": "etf non-registered",
                "current_balance": 0,
                "investment_type": "ETF",
                "account_type": "Non-Registered",
                "pre_authorized_monthly_contribution": 0,
                "risk_level": "Medium",
            },
            {
                "name": "cash savings",
                "current_balance": 0,
                "investment_type": "Cash",
                "account_type": "Non-Registered",
            },
        ]
        for data in investments:
            post_object_create(
                url="/api/my/finances/investments",
                user=user,
                data=data,
                view=investment_view,
            )

    def create_goals(self, user):
        goal_view = FinancialGoalViewset.as_view({"post": "create"})
        goals = [
            {
                "name": "test goal",
                "type": "Nest Egg",
                "amount": "500",
                "date": "2022-01-01",
            },
            {
                "name": "test goal",
                "type": "Big Purchase",
                "amount": "50000",
                "date": "2040-01-01",
            },
        ]
        for data in goals:
            post_object_create(
                url="/api/my/finances/goals", user=user, data=data, view=goal_view
            )

    def update_financial_profile(self, user):
        factory = APIRequestFactory()
        data = {
            "birth_date": "1994-03-11",
            "retirement_age": 65,
            "risk_tolerance": 50,
            "monthly_salary_before_tax": 8000,
            "percent_salary_for_spending": 50,
            "starting_tfsa_contribution_limit": 0,
            "starting_rrsp_contribution_limit": 0,
            "province_of_residence": "AB",
            "death_age": 90,
        }
        view = FinancialProfileView.as_view({"post": "create"})
        request = factory.post("my/finances/profile", data=data, format="json")
        force_authenticate(request, user=user)
        response = view(request)
        return response

    def create_user_finances(self, user):
        self.create_loans(user)
        self.create_investments(user)
        self.create_goals(user)
        self.update_financial_profile(user)

    def setUp(self) -> None:
        self.user = create_user()
        self.create_user_finances(self.user)

    def tearDown(self) -> None:
        delete_user(self.user)

    def test_building_plan(self):
        factory = APIRequestFactory()
        request = factory.get("api/my/plan", format="json")
        force_authenticate(request, user=self.user)
        assert not self.user.is_anonymous
        view = UserPlanViewSet.as_view({"get": "list"})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK, response.data
        json.dumps(response.data, cls=DjangoJSONEncoder)
