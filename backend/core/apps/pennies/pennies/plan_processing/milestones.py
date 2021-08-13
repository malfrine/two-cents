from datetime import date, datetime
from enum import Enum
from typing import Dict, NewType, List, Optional, Tuple
from uuid import UUID

from pydantic import BaseModel

from pennies.model.goal import AllGoalTypes, NestEgg, BigPurchase
from pennies.model.loan import Loan
from pennies.model.problem_input import ProblemInput
from pennies.model.solution import FinancialPlan
from pennies.plan_processing.utilities import (
    get_loan_pay_off_date,
    get_nest_egg_completion_month_or_none,
    get_actual_big_purchase_amount_and_withdrawals,
    get_nest_egg_cash_balance_requirements,
)
from pennies.utilities.datetime import (
    get_first_date_of_next_month,
    get_months_difference,
    get_date_plus_month,
)

_ALMOST_ZERO_LOWER_BOUND = -1
_ALMOST_ZERO_UPPER_BOUND = 1


class MilestoneTypeEnum(Enum):
    DEBT_FREE = "DEBT FREE"
    LOAN_PAYOFF = "LOAN PAYOFF"
    GOAL_FAILURE = "GOAL FAILURE"
    GOAL_SUCCESS = "GOAL SUCCESS"


class Milestone(BaseModel):
    name: str
    date: date
    header: str
    text: str
    instrument_id: Optional[int] = None
    instrument_type: Optional[str] = None


PlanMilestones = NewType("PlanMilestones", Dict[str, Milestone])


class MilestoneFactory:
    @classmethod
    def make_loan_pay_off_milestone(
        cls, loan: Loan, payoff_date: date, interest_paid: float
    ):
        start_date = get_first_date_of_next_month(datetime.today())
        months = get_months_difference(payoff_date, start_date)

        interest_paid_str = "${:,.0f}".format(interest_paid)
        text = (
            f"You will pay off {loan.name} on {str(payoff_date)}. You will have paid {interest_paid_str} in interest "
            f"over {months} months"
        )
        return Milestone(
            name=f"Pay off {loan.name}",
            date=payoff_date,
            header=f"Pay off {loan.name}",
            text=text,
            instrument_id=loan.db_id,
            instrument_type="loan",
        )

    @classmethod
    def make_debt_free_milestone(cls, debt_free_date: date):
        return Milestone(
            name="Debt Free",
            date=debt_free_date,
            header="Debt Free",
            text=f"You will be debt free on {debt_free_date}!",
        )

    @classmethod
    def make_positive_net_worth_milestone(cls, milestone_date: date):
        return Milestone(
            name="Positive Net Worth",
            date=milestone_date,
            header="Positive Net Worth",
            text=f"Your net worth will be positive on {milestone_date}!",
        )

    @classmethod
    def make_retirement_milestone(cls, retirement_date: date, net_worth: float):
        net_worth_str = "${:,.0f}".format(net_worth)
        return Milestone(
            name="Retirement",
            date=retirement_date,
            header="You Finally Retire!",
            text=f"You will retire on {retirement_date}."
            f" Your net worth at retirement will be {net_worth_str}!",
        )

    @classmethod
    def make_nest_egg_completed_milestone(
        cls, completion_date: date, goal_due_date: date, goal: NestEgg
    ):
        is_on_time = completion_date <= goal_due_date
        if is_on_time:
            text = (
                f"Woo! You will be able to build your nest egg on time. "
                f"You will be able to save ${goal.amount:,.0f} by {completion_date}"
            )
        else:
            text = (
                f"Unfortunately, you will not be able to build your nest egg on time. "
                f"You will only be able to save ${goal.amount:,.0f} by {completion_date}"
            )

        return Milestone(
            name=f"Complete Goal: {goal.name}",
            date=completion_date,
            header=f"{goal.name} goal will be completed on {completion_date}",
            text=text,
        )

    @classmethod
    def make_big_purchase_milestone(
        cls,
        goal: BigPurchase,
        goal_due_date: date,
        actual_purchase_amount: float,
        withdrawals: List[Tuple[str, float]],
    ) -> Milestone:
        is_success = actual_purchase_amount >= goal.amount
        if not is_success:
            name = f"Unable to purchase {goal.name}"
            header = f"Only able to save ${actual_purchase_amount:,.0f} for {goal.name}"
        else:
            name = f"Successfully purchase {goal.name}"
            header = (
                f"Complete {goal.name} big purchase for ${actual_purchase_amount:,.0f}"
            )
        if actual_purchase_amount >= 0:
            withdrawal_text = ", ".join(
                (f"{name}: ${amount:,.0f}" for (name, amount) in withdrawals)
            )
            text = f"Your ${actual_purchase_amount:,.0f} can be withdrawn from the following: {withdrawal_text}"
        else:
            text = ""
        return Milestone(name=name, date=goal_due_date, header=header, text=text)


class PlanMilestonesFactory:
    @classmethod
    def create(cls, plan: FinancialPlan, problem_input: ProblemInput) -> PlanMilestones:
        start_date = get_first_date_of_next_month(datetime.today()).date()
        milestones = list()
        milestones.extend(cls.get_loan_payoff_milestones(plan, start_date))
        debt_free_milestone = cls.get_debt_free_milestone(plan, start_date)
        if debt_free_milestone is not None:
            milestones.append(debt_free_milestone)
        positive_net_worth_ms = cls.get_positive_net_worth_milestone(plan, start_date)
        if positive_net_worth_ms is not None:
            milestones.append(positive_net_worth_ms)
        retirement_month = (
            problem_input.user_finances.financial_profile.retirement_month
        )
        retirement_milestone = MilestoneFactory.make_retirement_milestone(
            retirement_date=get_date_plus_month(start_date, retirement_month),
            net_worth=plan.get_net_worth_at(retirement_month),
        )
        milestones.append(retirement_milestone)
        goal_milestones = cls.get_goal_milestones(
            plan, problem_input.user_finances.goals, start_date
        )
        milestones.extend(goal_milestones)

        milestones = sorted(milestones, key=lambda x: x.date)
        for milestone in milestones:
            print(milestone.text)

        return PlanMilestones({m.name: m for m in milestones})

    @classmethod
    def get_loan_payoff_milestones(
        cls, plan: FinancialPlan, start_date: date
    ) -> List[Milestone]:
        if len(plan.monthly_solutions) == 0:
            return list()
        all_loans = list(
            loan
            for loan in plan.monthly_solutions[0].portfolio.loans
            if loan.current_balance < 0
        )
        milestones = list()
        for loan in all_loans:
            payoff_date = get_loan_pay_off_date(loan, plan, start_date)
            if payoff_date is None:
                continue
            interest_paid = plan.get_interest_paid_on_loan(loan.id_)
            milestones.append(
                MilestoneFactory.make_loan_pay_off_milestone(
                    loan, payoff_date, interest_paid
                )
            )
        return milestones

    @classmethod
    def get_debt_free_milestone(
        cls, plan: FinancialPlan, start_date: date
    ) -> Optional[Milestone]:
        starting_portfolio = plan.monthly_solutions[0].portfolio
        if len(starting_portfolio.loans) == 0:
            return None  # if they don't have any loans they are already debt free
        month = plan.debt_free_month
        if month is None:
            return None
        debt_free_date = get_date_plus_month(start_date, month)
        return MilestoneFactory.make_debt_free_milestone(debt_free_date)

    @classmethod
    def get_positive_net_worth_milestone(
        cls, plan: FinancialPlan, start_date: date
    ) -> Optional[Milestone]:
        starting_portfolio = plan.monthly_solutions[0].portfolio
        if len(starting_portfolio.loans) == 0:
            return None  # if they don't have any loans they already have a positive net worth
        month = plan.first_positive_net_worth_month
        if month is None:
            return None
        milestone_date = get_date_plus_month(start_date, month)
        return MilestoneFactory.make_positive_net_worth_milestone(milestone_date)

    @classmethod
    def get_nest_egg_milestones(
        cls, goals: Dict[UUID, NestEgg], plan: FinancialPlan, start_date: date
    ) -> List[Milestone]:
        milestones = list()
        nest_egg_requirements = get_nest_egg_cash_balance_requirements(goals=goals)
        for goal, amount_needed in nest_egg_requirements:
            completion_month = get_nest_egg_completion_month_or_none(
                goal, plan, amount_needed
            )
            if completion_month is None:
                continue
            else:
                completion_date = get_date_plus_month(start_date, completion_month)
                milestone = MilestoneFactory.make_nest_egg_completed_milestone(
                    completion_date=completion_date,
                    goal_due_date=get_date_plus_month(start_date, goal.due_month),
                    goal=goal,
                )
                milestones.append(milestone)
        return milestones

    @classmethod
    def get_big_purchase_milestones(
        cls, goals: Dict[UUID, AllGoalTypes], plan: FinancialPlan, start_date: date
    ):
        milestones = list()
        big_purchase_goals = [
            goal for goal in goals.values() if isinstance(goal, BigPurchase)
        ]
        big_purchase_goals = sorted(big_purchase_goals, key=lambda x: x.due_month)
        for goal in big_purchase_goals:
            (
                actual_purchase,
                withdrawals,
            ) = get_actual_big_purchase_amount_and_withdrawals(goal, plan)
            milestone = MilestoneFactory.make_big_purchase_milestone(
                goal=goal,
                goal_due_date=get_date_plus_month(start_date, goal.due_month),
                actual_purchase_amount=actual_purchase,
                withdrawals=withdrawals,
            )
            milestones.append(milestone)
        return milestones

    @classmethod
    def get_goal_milestones(
        cls, plan: FinancialPlan, goals: Dict[UUID, AllGoalTypes], start_date: date
    ) -> List[Milestone]:
        milestones = list()
        milestones.extend(
            cls.get_nest_egg_milestones(goals=goals, plan=plan, start_date=start_date)
        )
        milestones.extend(
            cls.get_big_purchase_milestones(
                goals=goals, plan=plan, start_date=start_date
            )
        )
        return milestones
