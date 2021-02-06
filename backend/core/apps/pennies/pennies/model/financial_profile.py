from pydantic.main import BaseModel

from pennies.utilities.datetime import MONTHS_IN_YEAR


class FinancialProfile(BaseModel):
    monthly_allowance: float
    years_to_retirement: int  # TODO: get this as months_to_retirement (assume they retire on their birthday)

    @property
    def retirement_month(self):
        return self.years_to_retirement * MONTHS_IN_YEAR
