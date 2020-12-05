from typing import List

from pydantic.main import BaseModel

from pennies.model.investment import Investment
from pennies.model.loan import Loan


class PenniesRequest(BaseModel):
    monthly_allowance: float
    loans: List[Loan]
    investments: List[Investment]
    strategies: List[str]
