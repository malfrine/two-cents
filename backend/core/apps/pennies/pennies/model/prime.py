from pydantic import BaseModel

from pennies.utilities.datetime import MONTHS_IN_YEAR

CURRENT_PRIME = 2.5
FUTURE_PRIME_START_YEAR = 3
FUTURE_EXPECTED_PRIME = 3


class PrimeInterestRateForecast(BaseModel):
    def get_prime(self, month: int):
        if month <= FUTURE_PRIME_START_YEAR * MONTHS_IN_YEAR:
            return CURRENT_PRIME
        else:
            return FUTURE_EXPECTED_PRIME
