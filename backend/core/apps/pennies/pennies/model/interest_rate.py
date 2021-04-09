from typing import List, Union, Any, Literal

from pydantic import BaseModel

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


class InterestRateTerm(BaseModel):
    start_month: int
    final_month: int
    interest_rate: Union[FixedLoanInterestRate, VariableLoanInterestRate]

    def get_monthly_interest_rate(self, month: int) -> float:
        if self.start_month <= month <= self.final_month:
            return self.interest_rate.get_monthly_interest_rate(month)
        else:
            raise ValueError(f"Cannot get monthly interest rate for month {month}")

    def get_volatility(self):
        return self.interest_rate.get_volatility()


class CurrentTermSelector:

    CURRENT_MONTH = 0

    @classmethod
    def get_term(self, terms: List[InterestRateTerm]):
        for term in terms:
            if term.start_month <= self.CURRENT_MONTH <= term.final_month:
                return term
        return terms[0]


class InterestRateTerms(InterestRate):
    interest_type: Literal['Interest Rate Terms'] = 'Interest Rate Terms'
    terms: List[InterestRateTerm]
    _volatility = 0  # TODO: read from terms but it's a loan so it should all be 0
    _default_term_selector: CurrentTermSelector = CurrentTermSelector()
    default_term: InterestRate = None

    def _get_term(self, month: int):
        for term in self.terms:
            if term.start_month <= month <= term.final_month:
                return term
        if self.default_term is None:
            self.default_term = self._default_term_selector.get_term(self.terms).interest_rate
        return self.default_term

    def get_monthly_interest_rate(self, month: int) -> float:
        return self._get_term(month).get_monthly_interest_rate(month)

    def get_volatility(self):
        return self._volatility


AllLoanInterestTypes = Union[FixedLoanInterestRate, VariableLoanInterestRate, InterestRateTerms]
