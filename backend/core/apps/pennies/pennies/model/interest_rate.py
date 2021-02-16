from pydantic import BaseModel

from pennies.model.prime import PrimeInterestRateForecast
from pennies.utilities.datetime import MONTHS_IN_YEAR


class InterestRate(BaseModel):
    def get_monthly_interest_rate(self, month: int) -> float:
        raise NotImplementedError()


class FixedInterestRate(InterestRate):

    apr: float

    def get_monthly_interest_rate(self, month: int) -> float:
        return self.apr / MONTHS_IN_YEAR / 100


class VariableInterestRate(InterestRate):

    prime_modifier: float
    _prime_forecast: PrimeInterestRateForecast = PrimeInterestRateForecast()

    def get_monthly_interest_rate(self, month: int) -> float:
        return (
            (self._prime_forecast.get_prime(month) + self.prime_modifier)
            / MONTHS_IN_YEAR
            / 100
        )
