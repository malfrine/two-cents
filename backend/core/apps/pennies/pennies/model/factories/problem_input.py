from pennies.model.factories.investment import InvestmentFactory
from pennies.model.factories.loan import LoanFactory
from pennies.model.financial_profile import FinancialProfile
from pennies.model.portfolio import Portfolio
from pennies.model.problem_input import ProblemInput
from pennies.model.request import PenniesRequest
from pennies.model.user_personal_finances import UserPersonalFinances


class ProblemInputFactory:
    @classmethod
    def from_request(cls, request: PenniesRequest) -> ProblemInput:
        instruments = dict()
        for loan in request.loans:
            instruments[loan.name] = LoanFactory.from_request_loan(loan)
        for investment in request.investments:
            instruments[investment.name] = InvestmentFactory.from_request_investment(
                investment
            )
        return ProblemInput(
            user_finances=UserPersonalFinances(
                financial_profile=request.financial_profile,
                portfolio=Portfolio(instruments=instruments),
            ),
            strategies=request.strategies,
        )
