import logging

from pennies.model.portfolio import Portfolio
from pennies.model.problem_input import ProblemInput
from pennies.model.request import PenniesRequest
from pennies.model.user_personal_finances import UserPersonalFinances


class ProblemInputFactory:
    @classmethod
    def from_request(cls, request: PenniesRequest) -> ProblemInput:
        logging.info(request.json(indent=3))
        instruments = dict()
        for loan in request.loans:
            instruments[loan.id_] = loan
        for investment in request.investments:
            instruments[investment.id_] = investment
        portfolio = Portfolio(instruments=instruments)
        return ProblemInput(
            user_finances=UserPersonalFinances(
                financial_profile=request.financial_profile,
                portfolio=portfolio,
                goals={g.id_: g for g in request.goals},
            ),
            strategies=request.strategies,
        )
