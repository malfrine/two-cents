from typing import Dict

from django.test import TestCase
from rest_framework.response import Response

from core.apps.finances.models.investments import Investment
from core.apps.finances.models.loans import Loan
from core.apps.finances.views import LoanViewset, InvestmentViewset
from core.tests._utilities import ModelCRUDTestCaseMixin


class LoanCRUDTestCaseMixin(ModelCRUDTestCaseMixin, TestCase):

    url = "api/my/finances/loans"
    model = Loan
    viewset = LoanViewset

    def get_create_data(self) -> Dict:
        return {
            "name": "test_loan",
            "loan_type": "Credit Card",
            "loan_interest": {"interest_type": "Fixed", "apr": 3.2},
            "current_balance": 2000,
        }

    def get_update_data(self) -> Dict:
        return {
            "name": "updated test loan",
            "id": self.pk,
            "loan_type": "Credit Card",
            "loan_interest": {"interest_type": "Fixed", "apr": 3.2},
            "current_balance": 2000,
        }

    def run_update_assertions(self, response: Response):
        assert self.get_obj().name == "updated test loan"


class InvestmentCRUDTestCaseMixin(ModelCRUDTestCaseMixin, TestCase):

    url = "api/my/finances/investments"
    model = Investment
    viewset = InvestmentViewset

    def get_create_data(self) -> Dict:
        return {
            "name": "mutual fund investment",
            "current_balance": 0,
            "investment_type": "Mutual Fund",
            "account_type": "Non-Registered",
            "pre_authorized_monthly_contribution": 0,
            "risk_level": "Low",
        }

    def get_update_data(self) -> Dict:
        return {
            "id": self.pk,
            "name": "updated mutual fund investment",
            "current_balance": 0,
            "investment_type": "Mutual Fund",
            "account_type": "Non-Registered",
            "pre_authorized_monthly_contribution": 0,
            "risk_level": "Low",
        }

    def run_update_assertions(self, response: Response):
        assert self.get_obj().name == "updated mutual fund investment"
