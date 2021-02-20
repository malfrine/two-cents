from pennies.model.interest_rate import (
    FixedLoanInterestRate,
    InvestmentReturnRate,
    VariableLoanInterestRate,
    ZeroGrowthRate,
    FixedInvestmentInterestRate,
    VariableInvestmentInterestRate,
)
from pennies.model.investment import (
    Investment,
    MutualFund,
    ETF,
    Stock,
    Cash,
    GIC,
    TermDeposit,
)
from pennies.model.request import RequestInvestment, RequestInvestmentType, InterestType


class InvestmentFactory:

    _INVESTMENT_MAP = {
        RequestInvestmentType.MUTUAL_FUND: MutualFund,
        RequestInvestmentType.ETF: ETF,
        RequestInvestmentType.STOCK: Stock,
        RequestInvestmentType.CASH: Cash,
        RequestInvestmentType.GIC: GIC,
        RequestInvestmentType.TERM_DEPOSIT: TermDeposit,
    }

    _INTEREST_RATE_MAP = {
        InterestType.FIXED: FixedInvestmentInterestRate,
        InterestType.VARIABLE: VariableInvestmentInterestRate,
    }

    @classmethod
    def from_request_investment(
        cls, request_investment: RequestInvestment
    ) -> Investment:
        if request_investment.interest_type is None:
            if request_investment.investment_type == RequestInvestmentType.CASH:
                interest_rate = ZeroGrowthRate()
            else:
                interest_rate = InvestmentReturnRate(
                    roi=request_investment.roi, volatility=request_investment.volatility
                )
        else:
            interest_rate = cls._INTEREST_RATE_MAP[
                request_investment.interest_type
            ].parse_obj(request_investment.dict())
        return cls._INVESTMENT_MAP[request_investment.investment_type].parse_obj(
            dict(request_investment.dict(), interest_rate=interest_rate)
        )
