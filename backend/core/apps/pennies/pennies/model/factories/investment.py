from pennies.model.interest_rate import FixedInterestRate
from pennies.model.investment import Investment
from pennies.model.request import RequestInvestment


class InvestmentFactory:
    @classmethod
    def from_request_investment(
        cls, request_investment: RequestInvestment
    ) -> Investment:
        interest_rate = FixedInterestRate(apr=request_investment.apr)
        return Investment.parse_obj(
            dict(request_investment.dict(), interest_rate=interest_rate)
        )
