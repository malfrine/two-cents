from pennies.model.interest_rate import (
    FixedLoanInterestRate,
    InvestmentReturnRate,
    VariableLoanInterestRate,
    ZeroGrowthRate,
    FixedInvestmentInterestRate,
    VariableInvestmentInterestRate,
    GuaranteedInvestmentReturnRate,
)
from pennies.model.investment import (
    Investment,
    MutualFund,
    ETF,
    Stock,
    Cash,
    GIC,
    TermDeposit, InvestmentAccountType,
)
from pennies.model.request import RequestInvestment, RequestInvestmentType, InterestType, RequestInvestmentAccountType


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

    _ACCOUNT_TYPE_MAP = {
        RequestInvestmentAccountType.NON_REGISTERED: InvestmentAccountType.NON_REGISTERED,
        RequestInvestmentAccountType.RRSP: InvestmentAccountType.RRSP,
        RequestInvestmentAccountType.TFSA: InvestmentAccountType.TFSA,
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
            internal_interest_rate = cls._INTEREST_RATE_MAP[
                request_investment.interest_type
            ].parse_obj(request_investment.dict())
            interest_rate = GuaranteedInvestmentReturnRate(
                interest_rate=internal_interest_rate,
                final_month=request_investment.final_month,
            )
        account_type = cls._ACCOUNT_TYPE_MAP[request_investment.account_type]
        return cls._INVESTMENT_MAP[request_investment.investment_type].parse_obj(
            dict(request_investment.dict(), interest_rate=interest_rate, account_type=account_type)
        )
