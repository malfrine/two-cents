from pydantic.main import BaseModel

from pennies.model.constants import Province
from pennies.utilities.datetime import MONTHS_IN_YEAR


class FinancialProfile(BaseModel):
    monthly_allowance_before_retirement: float
    years_to_retirement: int
    risk_tolerance: float = 50
    annual_income_before_retirement: float = 100_000
    province_of_residence: Province = Province.AB
    years_to_death: int = 70
    starting_rrsp_contribution_limit: float = 50_000
    starting_tfsa_contribution_limit: float = 50_000
    current_age: int = 20

    @property
    def retirement_month(self):
        return self.years_to_retirement * MONTHS_IN_YEAR

    @property
    def death_month(self):
        return self.years_to_death * MONTHS_IN_YEAR

    def get_monthly_income(self, month: int):
        return (
            self.annual_income_before_retirement / MONTHS_IN_YEAR
            if month < self.retirement_month
            else 0
        )

    def get_monthly_allowance(self, month: int):
        return (
            self.monthly_allowance_before_retirement
            if month < self.retirement_month
            else 0
        )

    @property
    def monthly_retirement_spending(self):
        return self.monthly_allowance_before_retirement

    @property
    def retirement_age(self):
        return self.current_age + self.years_to_retirement

    @property
    def death_age(self):
        return self.current_age + self.years_to_death
