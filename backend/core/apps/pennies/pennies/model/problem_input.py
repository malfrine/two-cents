from typing import List

from pydantic.main import BaseModel

from pennies.model.financial_profile import FinancialProfile
from pennies.model.portfolio import Portfolio
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.model.request import PenniesRequest


class ProblemInput(BaseModel):
    problem: UserPersonalFinances
    strategies: List[str]

    @classmethod
    def create_from_pennies_request(cls, request: PenniesRequest) -> "ProblemInput":
        instruments = dict()
        for loan in request.loans:
            instruments[loan.name] = loan
        for investment in request.investments:
            instruments[investment.name] = investment
        return ProblemInput(
            problem=UserPersonalFinances(
                financial_profile=FinancialProfile(
                    monthly_allowance=request.financial_profile.monthly_allowance,
                    years_to_retirement=request.financial_profile.years_to_retirement,
                ),
                portfolio=Portfolio(instruments=instruments),
            ),
            strategies=request.strategies,
        )
