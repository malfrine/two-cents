from typing import List

from pydantic.main import BaseModel

from pennies.model.financial_profile import FinancialProfile
from pennies.model.portfolio import Portfolio
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.model.request import PenniesRequest


class ProblemInput(BaseModel):
    user_finances: UserPersonalFinances
    strategies: List[str]
