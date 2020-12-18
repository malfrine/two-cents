from typing import List

from pydantic.main import BaseModel
from pennies.model.financial_profile import FinancialProfile

from pennies.model.investment import Investment
from pennies.model.loan import Loan


class PenniesRequest(BaseModel):
    financial_profile: FinancialProfile
    loans: List[Loan]
    investments: List[Investment]
    strategies: List[str]
