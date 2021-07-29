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
        cur_portfolio: Portfolio = user_personal_finances.portfolio.copy(deep=True)
        province = user_personal_finances.financial_profile.province_of_residence
        for index, (mp, withdrawals) in enumerate(
            zip(monthly_payments, monthly_withdrawals)
        ):
            month = index + parameters.starting_month

            total_withdrawals = sum(
                withdrawals.get(i.id_, 0) for i in cur_portfolio.investments()
            )
            pre_tax_monthly_income = user_personal_finances.financial_profile.get_pre_tax_monthly_income(
                month
            )
            gross_income_in_month = pre_tax_monthly_income + total_withdrawals

            non_tfsa_withdrawals = sum(
                withdrawals.get(i.id_, 0)
                for i in cur_portfolio.non_tfsa_investments_and_guaranteed_investments
            )
            rrsp_contributions = sum(
                mp.get(i.id_, 0)
                for i in cur_portfolio.rrsp_investments_and_guaranteed_investments
            )
            taxable_income_in_month = (
                pre_tax_monthly_income + non_tfsa_withdrawals - rrsp_contributions
            )
            taxes_paid = calculate_monthly_income_tax(
                income=taxable_income_in_month, province=province
            )

            savings_fraction = (
                user_personal_finances.financial_profile.percent_salary_for_spending
                / 100
            )
            monthly_allowance = (gross_income_in_month - taxes_paid) * savings_fraction
            monthly_solutions.append(
                MonthlySolution(
                    allocation=MonthlyAllocation(
                        payments=mp,
                        leftover=monthly_allowance - sum(m for m in mp.values()),
                    ),
                    portfolio=cur_portfolio,
                    month=month,
                    taxes_paid=taxes_paid,
                    withdrawals=withdrawals,
                    gross_income=gross_income_in_month,
                    taxable_income=taxable_income_in_month,
                )
            )
            cur_portfolio = cur_portfolio.copy(deep=True)
            PortfolioManager.forward_on_month(
                portfolio=cur_portfolio,
                payments=mp,
                month=month,
                withdrawals=withdrawals,
            )
        return FinancialPlan(monthly_solutions=monthly_solutions)
