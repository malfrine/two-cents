from pennies.model.factories.investment import InvestmentFactory
from pennies.model.factories.loan import LoanFactory
from pennies.model.financial_profile import FinancialProfile
from pennies.model.parameters import Parameters
from pennies.model.portfolio import Portfolio
from pennies.model.problem_input import ProblemInput
from pennies.model.request import PenniesRequest
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.utilities.finance import DiscountFactorCalculator


class ProblemInputFactory:
    @classmethod
    def from_request(cls, request: PenniesRequest) -> ProblemInput:
        print(request.json(indent=3))
        instruments = dict()
        for loan in request.loans:
            instruments[loan.id_] = loan
        for investment in request.investments:
            investment = InvestmentFactory.from_request_investment(investment)
            instruments[investment.id_] = investment
        portfolio = Portfolio(instruments=instruments)
        return ProblemInput(
            user_finances=UserPersonalFinances(
                financial_profile=request.financial_profile,
                portfolio=portfolio,
            ),
            strategies=request.strategies,
        )
