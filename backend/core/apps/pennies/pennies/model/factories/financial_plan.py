from typing import List, Dict, Optional

from pennies.model.parameters import Parameters
from pennies.model.portfolio import Portfolio
from pennies.model.portfolio_manager import PortfolioManager
from pennies.model.solution import MonthlyAllocation, MonthlySolution, FinancialPlan
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.utilities.finance import calculate_monthly_income_tax


class FinancialPlanFactory:

    @classmethod
    def create(
        cls,
        monthly_payments: List[Dict[str, float]],
        user_personal_finances: UserPersonalFinances,
        parameters: Parameters,
        monthly_withdrawals: Optional[List[Dict[str, float]]] = None,
    ) -> FinancialPlan:
        if monthly_withdrawals is None:
            monthly_withdrawals = [dict() for _ in range(len(monthly_payments))]

        monthly_solutions = []
        cur_portfolio = user_personal_finances.portfolio.copy(deep=True)
        income = user_personal_finances.financial_profile.monthly_income
        province = user_personal_finances.financial_profile.province_of_residence
        monthly_allowance = user_personal_finances.financial_profile.monthly_allowance
        for index, (mp, w) in enumerate(zip(monthly_payments, monthly_withdrawals)):
            taxes_paid = calculate_monthly_income_tax(income=income, province=province)
            month = index + parameters.starting_month
            monthly_solutions.append(
                MonthlySolution(
                    allocation=MonthlyAllocation(
                        payments=mp,
                        leftover=monthly_allowance - sum(m for m in mp.values()),
                    ),
                    portfolio=cur_portfolio,
                    month=month,
                    taxes_paid=taxes_paid,
                    withdrawals=w
                )
            )
            cur_portfolio = PortfolioManager.forward_on_month(
                portfolio=cur_portfolio, payments=mp, month=month, withdrawals=w
            )
        return FinancialPlan(monthly_solutions=monthly_solutions)
