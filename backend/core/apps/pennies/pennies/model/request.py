from typing import List, Optional

from pydantic.main import BaseModel

from pennies.model.financial_profile import FinancialProfile
from pennies.model.goal import AllGoalTypes
from pennies.model.investment import AllInvestmentTypes
from pennies.model.loan import AllLoanTypes


class PenniesRequest(BaseModel):
    financial_profile: FinancialProfile
    loans: List[AllLoanTypes]
    goals: List[AllGoalTypes]
    investments: List[AllInvestmentTypes]
    strategies: Optional[List[str]] = None
