from datetime import date
from typing import Optional, Tuple, Dict, List
from uuid import UUID

from pennies.model.decision_periods import DecisionPeriodsManagerFactory
from pennies.model.goal import NestEgg, BigPurchase, AllGoalTypes
from pennies.model.investment import Cash
from pennies.model.loan import Loan
from pennies.model.solution import FinancialPlan
from pennies.utilities.datetime import get_date_plus_month

_ALMOST_ZERO_LOWER_BOUND = -1


def get_loan_pay_off_date(
    loan: Loan, plan: FinancialPlan, start_date: date
) -> Optional[date]:
    for month, ms in enumerate(plan.monthly_solutions):
        loan_at_month = ms.portfolio.loans_by_id.get(loan.id_, None)
        if loan_at_month is None:
            return get_date_plus_month(start_date, month + 1)
        elif loan_at_month.current_balance >= _ALMOST_ZERO_LOWER_BOUND:
            return get_date_plus_month(start_date, month + 1)
    return None


def get_nest_egg_completion_month_or_none(
    goal: NestEgg, plan: FinancialPlan, amount_needed: float
) -> Optional[int]:
    current_month = goal.due_month - 1
    final_month = plan.monthly_solutions[-1].portfolio.final_month
    current_cash_balance = 0
    while current_month <= final_month:
        current_month += 1
        monthly_solution = plan.monthly_solutions[current_month]
        current_cash_balance = sum(
            i.current_balance
            for i in monthly_solution.portfolio.investments()
            if isinstance(i, Cash)
        )
        if current_cash_balance >= amount_needed:
            return current_month
    if current_cash_balance >= amount_needed:
        return current_month
    else:
        return None


def get_nest_egg_cash_balance_requirements(
    goals: Dict[UUID, AllGoalTypes]
) -> List[Tuple[NestEgg, float]]:
    """get total cash balance needed for each goal's due month'"""
    nest_egg_goals = [goal for goal in goals.values() if isinstance(goal, NestEgg)]
    nest_egg_goals = sorted(nest_egg_goals, key=lambda x: x.due_month)
    nest_egg_requirements = list()
    for i in range(len(nest_egg_goals)):
        amount_needed = sum(goal.amount for goal in nest_egg_goals[:i])
        goal = nest_egg_goals[i]
        nest_egg_requirements.append((goal, amount_needed))
    return nest_egg_requirements


def get_actual_big_purchase_amount_and_withdrawals(
    goal: BigPurchase, plan: FinancialPlan
) -> Tuple[float, List[Tuple[str, float]]]:
    # TODO: how to handle multiple big purchases on the same day???
    monthly_withdrawal = plan.monthly_solutions[goal.due_month].withdrawals
    portfolio = plan.monthly_solutions[goal.due_month].portfolio
    withdrawal_list = [
        (
            portfolio.get_instrument(investment_id).name,
            amount * DecisionPeriodsManagerFactory.max_months,
        )
        # TODO: this is a quick fix to multiply by max_months
        for investment_id, amount in monthly_withdrawal.items()
        if amount > 0
    ]
    total_purchase = sum(amount for _, amount in withdrawal_list)
    return total_purchase, withdrawal_list
