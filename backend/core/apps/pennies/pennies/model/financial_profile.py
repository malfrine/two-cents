from pydantic.main import BaseModel

from pennies.model.constants import Province
from pennies.utilities.datetime import MONTHS_IN_YEAR


class FinancialProfile(BaseModel):
    monthly_allowance: float
    years_to_retirement: int  # TODO: get this as months_to_retirement (assume they retire on their birthday)
    risk_tolerance: float = 50
    annual_income: float = 100_000
    province_of_residence: Province = Province.AB

    @property
    def retirement_month(self):
        return self.years_to_retirement * MONTHS_IN_YEAR

    @property
    def monthly_income(self):
        return self.annual_income / MONTHS_IN_YEAR
