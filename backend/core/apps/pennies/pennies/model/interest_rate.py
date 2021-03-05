from pydantic import BaseModel

from pennies.model.prime import PrimeInterestRateForecast
from pennies.utilities.datetime import MONTHS_IN_YEAR


class InterestRate(BaseModel):
    def get_monthly_interest_rate(self, month: int) -> float:
        raise NotImplementedError()

    def get_volatility(self):
        raise NotImplementedError()


class ZeroGrowthRate(InterestRate):
    def get_monthly_interest_rate(self, month: int) -> float:
        return 0

    def get_volatility(self):
        return 0


class FixedLoanInterestRate(InterestRate):

    apr: float
    volatility: float = 0

    def get_monthly_interest_rate(self, month: int) -> float:
        return self.apr / MONTHS_IN_YEAR / 100

    def get_volatility(self):
        return self.volatility


class VariableLoanInterestRate(InterestRate):

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


class FixedInvestmentInterestRate(InterestRate):

    roi: float
    volatility: float = 0

    def get_monthly_interest_rate(self, month: int) -> float:
        return self.roi / MONTHS_IN_YEAR / 100

    def get_volatility(self):
        return self.volatility


class VariableInvestmentInterestRate(InterestRate):

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


class InvestmentReturnRate(InterestRate):
    roi: float
    volatility: float

    def get_monthly_interest_rate(self, month: int) -> float:
        return self.roi / MONTHS_IN_YEAR / 100

    def get_volatility(self):
        return self.volatility


class GuaranteedInvestmentReturnRate(InterestRate):
    interest_rate: InterestRate
    final_month: int

    def get_monthly_interest_rate(self, month: int) -> float:
        if month <= self.final_month:
            return self.interest_rate.get_monthly_interest_rate(month)
        else:
            return 0

    def get_volatility(self):
        return self.interest_rate.get_volatility()
