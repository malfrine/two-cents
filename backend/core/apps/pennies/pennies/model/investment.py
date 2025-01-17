import logging
from abc import ABC
from typing import Union, Literal

from pydantic import validator, root_validator

from pennies.errors.validation_errors import BadDomainException
from pennies.model.constants import InvestmentAccountType
from pennies.model.instrument import Instrument
from pennies.model.interest_rate import (
    ZeroGrowthRate,
    GuaranteedInvestmentReturnRate,
    AllInvestmentInterestTypes,
)


class BaseInvestment(Instrument, ABC):
    account_type: InvestmentAccountType = InvestmentAccountType.NON_REGISTERED
    interest_rate: AllInvestmentInterestTypes

    def get_minimum_monthly_payment(self, month: int):
        raise NotImplementedError()

    def get_type(self) -> str:
        return "investment"


class GuaranteedInvestment(BaseInvestment, ABC):
    principal_investment_amount: float
    start_month: int  # can be negative (current month is 0)
    final_month: int
    interest_rate: GuaranteedInvestmentReturnRate

    def get_minimum_monthly_payment(self, month: int):
        return 0

    @root_validator(skip_on_failure=True)
    def set_current_balance(cls, values):
        v: int = values["current_balance"]
        n: int = abs(values["start_month"])
        r: GuaranteedInvestmentReturnRate = values["interest_rate"]
        p: float = values["principal_investment_amount"]
        expected_current_balance = p * (1 + r.get_monthly_interest_rate(0)) ** n
        if v is None or v != expected_current_balance:
            logging.info(
                "Incorrect current balance for guaranteed return investment - overwriting"
            )
            values["current_balance"] = expected_current_balance
        return values


class GIC(GuaranteedInvestment):
    investment_type: Literal["GIC"] = "GIC"
    ...


class TermDeposit(GuaranteedInvestment):
    investment_type: Literal["Term Deposit"] = "Term Deposit"
    ...


class NonGuaranteedInvestment(BaseInvestment):
    pre_authorized_monthly_contribution: float

    @validator("current_balance")
    def validate_positive_balance(cls, v):
        if v < 0:
            raise BadDomainException("Investment balance must be positive")
        return v

    def get_minimum_monthly_payment(self, month: int):
        return self.pre_authorized_monthly_contribution


class MutualFund(NonGuaranteedInvestment):
    investment_type: Literal["Mutual Fund"] = "Mutual Fund"
    ...


class Portfolio(NonGuaranteedInvestment):
    investment_type: Literal["Portfolio"] = "Portfolio"
    ...


class ETF(NonGuaranteedInvestment):
    investment_type: Literal["ETF"] = "ETF"
    ...


class Stock(NonGuaranteedInvestment):
    investment_type: Literal["Stock"] = "Stock"
    ...


class Cash(NonGuaranteedInvestment):
    investment_type: Literal["Cash"] = "Cash"

    # add validator to make sure no growth rate
    @validator("interest_rate")
    def validate_zero_interest_rate(cls, v):
        assert isinstance(v, ZeroGrowthRate)
        return v


ALL_NON_GUARANTEED_INVESTMENTS = [MutualFund, ETF, Stock, Cash]
ALL_GUARANTEED_INVESTMENTS = [TermDeposit, GIC]
AllInvestmentTypes = Union[GIC, TermDeposit, MutualFund, Portfolio, ETF, Stock, Cash]
