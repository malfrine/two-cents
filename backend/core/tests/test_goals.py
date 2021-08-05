from typing import Dict

from django.test import TestCase
from rest_framework.response import Response

from core.apps.finances.models.goals import FinancialGoal
from core.apps.finances.views import FinancialGoalViewset
from core.tests._utilities import ModelCRUDTestCaseMixin


class GoalCRUDTestCaseMixin(ModelCRUDTestCaseMixin, TestCase):

    url = "api/my/finances/goals"
    model = FinancialGoal
    viewset = FinancialGoalViewset

    def get_create_data(self) -> Dict:
        return {
            "name": "test goal",
            "type": "Nest Egg",
            "amount": "500",
            "date": "2022-01-01",
        }

    def get_update_data(self) -> Dict:
        return {
            "id": self.pk,
            "name": "updated test goal",
            "type": "Nest Egg",
            "amount": "500",
            "date": "2022-01-01",
        }

    def run_update_assertions(self, response: Response):
        assert self.get_obj().name == "updated test goal"
