from typing import List, Dict
from uuid import UUID

from pydantic import BaseModel, root_validator

from pennies.model.financial_profile import FinancialProfile
from pennies.model.goal import AllGoalTypes
from pennies.model.portfolio import Portfolio


class UserPersonalFinances(BaseModel):
    name: str = "portfolio"
    portfolio: Portfolio
    financial_profile: FinancialProfile = None
    goals: Dict[UUID, AllGoalTypes]

    def __str__(self):
        return "name: {:s}, monthly_allowance ${:,.2f} \n".format(
            self.name, self.financial_profile.monthly_allowance_before_retirement
        ) + "portfolio: \n\t{}".format(str(self.portfolio))

    @property
    def final_month(self):
        """The final month that calculations need to be run for"""
        return max(self.portfolio.final_month, self.financial_profile.retirement_month)

    @root_validator
    def enough_funds_to_solve(cls, values):
        fp: FinancialProfile = values["financial_profile"]
        p: Portfolio = values["portfolio"]
        total_min_payments = sum(
            instrument.get_minimum_monthly_payment(0)
            for instrument in p.instruments.values()
        )
        assert total_min_payments <= fp.monthly_allowance_before_retirement
        return values
