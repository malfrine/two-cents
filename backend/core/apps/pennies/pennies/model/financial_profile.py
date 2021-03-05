from pydantic.main import BaseModel

from pennies.model.constants import Province
from pennies.utilities.datetime import MONTHS_IN_YEAR


class FinancialProfile(BaseModel):
    monthly_allowance: float
    years_to_retirement: int  # TODO: get this as months_to_retirement (assume they retire on their birthday)
    risk_tolerance: float = 50
    annual_income: float = 100_000  # TODO: remove default
    province_of_residence: Province = Province.AB  # TODO: remove default
    years_to_death: int = 70  # TODO: remove default
    # monthly_retirement_spending: float = 900  # TODO: remove default

    @property
    def retirement_month(self):
        return self.years_to_retirement * MONTHS_IN_YEAR

    @property
    def death_month(self):
        return self.years_to_death * MONTHS_IN_YEAR

    @property
    def monthly_income(self):
        return self.annual_income / MONTHS_IN_YEAR

    @property
    def monthly_retirement_spending(self):
        return self.monthly_allowance
