from pydantic import BaseModel

from pennies.model.financial_profile import FinancialProfile
from pennies.model.portfolio import Portfolio


class UserPersonalFinances(BaseModel):
    name: str = "portfolio"
    portfolio: Portfolio
    financial_profile: FinancialProfile = None

    def __str__(self):
        return "name: {:s}, monthly_allowance ${:,.2f} \n".format(
            self.name, self.financial_profile.monthly_allowance
        ) + "portfolio: \n\t{}".format(str(self.portfolio))

    @property
    def final_month(self):
        """The final month that calculations need to be run for"""
        return max(self.portfolio.final_month, self.financial_profile.retirement_month)
