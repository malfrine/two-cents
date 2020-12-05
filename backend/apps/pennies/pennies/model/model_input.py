from typing import List

from pydantic.main import BaseModel

from pennies.model.portfolio import Portfolio
from pennies.model.problem import Problem
from pennies.model.request import PenniesRequest


class ModelInput(BaseModel):
    problem: Problem
    strategies: List[str]

    @classmethod
    def create_from_pennies_request(cls, request: PenniesRequest) -> "ModelInput":
        instruments = dict()
        for loan in request.loans:
            instruments[loan.name] = loan
        for investment in request.investments:
            instruments[investment.name] = investment
        return ModelInput(
            problem=Problem(
                monthly_allowance=request.monthly_allowance,
                portfolio=Portfolio(instruments=instruments)
            ),
            strategies=request.strategies
        )
