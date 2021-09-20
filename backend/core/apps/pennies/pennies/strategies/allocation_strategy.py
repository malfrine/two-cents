from abc import ABC
from typing import Optional

from pennies.model.parameters import Parameters
from pennies.model.solution import FinancialPlan
from pennies.model.user_personal_finances import UserPersonalFinances


class PlanningStrategy(ABC):
    def create_plan(
        self, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> Optional[FinancialPlan]:
        ...
