from typing import List, Union, Any, Literal

from pydantic import BaseModel, root_validator, validator

from pennies.model.prime import PrimeInterestRateForecast
from pennies.utilities.datetime import MONTHS_IN_YEAR


class CompoundingRate(BaseModel):
    def get_monthly_interest_rate(self, month: int) -> float:
        raise NotImplementedError()

    def get_volatility(self):
        raise NotImplementedError()

    class Meta:
        underscore_attrs_are_private = True


class InterestRate(CompoundingRate):
    """for loans"""
    interest_type: Any


class ReturnRate(CompoundingRate):
    """for investments"""


class ZeroGrowthRate(ReturnRate):
    def get_monthly_interest_rate(self, month: int) -> float:
        return 0

    def get_volatility(self):
        return 0


class FixedLoanInterestRate(InterestRate):
    interest_type: Literal['Fixed'] = 'Fixed'
    apr: float
    volatility: float = 0

    def get_monthly_interest_rate(self, month: int) -> float:
        return self.apr / MONTHS_IN_YEAR / 100

    def get_volatility(self):
        return self.volatility


class VariableLoanInterestRate(InterestRate):
    interest_type: Literal['Variable'] = 'Variable'
    prime_modifier: float
    volatility: float = 0
    _prime_forecast: PrimeInterestRateForecast = PrimeInterestRateForecast()

    def get_monthly_interest_rate(self, month: int) -> float:
        return (
            (self._prime_forecast.get_prime(month) + self.prime_modifier)
            / MONTHS_IN_YEAR
            / 100
        )

    def get_volatility(self):
        return self.volatility


class FixedInvestmentInterestRate(ReturnRate):
    roi: float
    volatility: float = 0

    def get_monthly_interest_rate(self, month: int) -> float:
        return self.roi / MONTHS_IN_YEAR / 100

    def get_volatility(self):
        return self.volatility


class VariableInvestmentInterestRate(ReturnRate):
    prime_modifier: float
    volatility: float = 0
    _prime_forecast: PrimeInterestRateForecast = PrimeInterestRateForecast()

    def get_monthly_interest_rate(self, month: int) -> float:
        return (
            (self._prime_forecast.get_prime(month) + self.prime_modifier)
            / MONTHS_IN_YEAR
            / 100
        )

    def get_volatility(self):
        return self.volatility


class InvestmentReturnRate(ReturnRate):
    roi: float
    volatility: float

    def get_monthly_interest_rate(self, month: int) -> float:
        return self.roi / MONTHS_IN_YEAR / 100

    def get_volatility(self):
        return self.volatility


class GuaranteedInvestmentReturnRate(ReturnRate):
    interest_rate: ReturnRate
    final_month: int

    def get_monthly_interest_rate(self, month: int) -> float:
        if month <= self.final_month:
            return self.interest_rate.get_monthly_interest_rate(month)
        else:
            return 0

    def get_volatility(self):
        return self.interest_rate.get_volatility()

class MortgageInterestRate(InterestRate):

    interest_type: Literal['Mortgage Interest Rate'] = 'Mortgage Interest Rate'
    interest_rate: Union[FixedLoanInterestRate, VariableLoanInterestRate]
    current_term_end_month: int
    default_interest_rate: InterestRate = FixedLoanInterestRate(apr=2.5)

    def get_monthly_interest_rate(self, month: int) -> float:
        if month <= self.current_term_end_month:
            return self.interest_rate.get_monthly_interest_rate(month)
        else:
            return self.default_interest_rate.get_monthly_interest_rate(month)

AllLoanInterestTypes = Union[FixedLoanInterestRate, VariableLoanInterestRate, MortgageInterestRate]
