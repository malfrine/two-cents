from pydantic import validator
from pydantic.main import BaseModel

from pennies.model.constants import Province
from pennies.utilities.datetime import MONTHS_IN_YEAR


class FinancialProfile(BaseModel):
    # monthly_allowance_before_retirement: float
    risk_tolerance: float

    monthly_salary_before_tax: float
    percent_salary_for_spending: float
    years_to_retirement: int

    province_of_residence: Province
    starting_rrsp_contribution_limit: float
    starting_tfsa_contribution_limit: float

    current_age: int
    years_to_death: int

    @property
    def retirement_month(self):
        return self.years_to_retirement * MONTHS_IN_YEAR

    @property
    def death_month(self):
        return self.years_to_death * MONTHS_IN_YEAR

    def get_monthly_income(self, month: int):
        return (
            self.monthly_salary_before_tax
            if month < self.retirement_month
            else 0
        )

    def get_monthly_allowance(self, month: int):
        return self.get_monthly_income(month) * self.percent_salary_for_spending / 100

    @property
    def monthly_retirement_spending(self):
        return self.monthly_allowance_before_retirement

    @property
    def monthly_allowance_before_retirement(self):
        return self.monthly_salary_before_tax * self.percent_salary_for_spending / 100

    @property
    def retirement_age(self):
        return self.current_age + self.years_to_retirement

    @property
    def death_age(self):
        return self.current_age + self.years_to_death

    @property
    def annual_income_before_retirement(self):
        return self.monthly_salary_before_tax * MONTHS_IN_YEAR

    @validator("province_of_residence", pre=True)
    def parse_province(cls, v):
        if not isinstance(v, Province):
            return Province[str(v)]
        else:
            return v
