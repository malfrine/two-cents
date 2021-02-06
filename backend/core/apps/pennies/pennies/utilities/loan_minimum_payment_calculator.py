import math

from pennies.utilities.datetime import MONTHS_IN_YEAR


class LoanMinimumPaymentCalculator:
    @classmethod
    def calculate_for_instalment_loan(
        cls, principal: float, apr: float, num_months: int
    ):
        mir = cls.calculate_monthly_interest_rate(apr)
        top = mir * (1 + mir) ** num_months
        bottom = (1 + mir) ** num_months - 1
        discount_factor = top / bottom
        return math.floor(principal * discount_factor)

    @classmethod
    def calculate_for_revolving_loan(cls, principal: float, apr: float):
        return math.floor(principal * cls.calculate_monthly_interest_rate(apr))

    @classmethod
    def calculate_monthly_interest_rate(cls, apr):
        return apr / MONTHS_IN_YEAR / 100
