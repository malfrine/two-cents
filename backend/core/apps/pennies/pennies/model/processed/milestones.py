from datetime import date, datetime, timedelta
from enum import Enum
from typing import Dict, NewType, List, Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel

from pennies.model.loan import Loan
from pennies.model.solution import FinancialPlan
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

        interest_paid_str = "${:,.2f}".format(interest_paid)
        text = (
            f"You will payoff {loan.name} on {str(payoff_date)}. You will have paid {interest_paid_str} in interest "
            f"over {months} months"
        )
        return Milestone(
            name=f"Pay off {loan.name}",
            date=payoff_date,
            header=f"Pay off {loan.name}",
            text=text,
            instrument_id=loan.db_id,
            instrument_type='loan'
        )

    @classmethod
    def make_debt_free_milestone(cls, debt_free_date: date):
        return Milestone(
            name=f"Debt Free",
            date=debt_free_date,
            header=f"Debt Free",
            text=f"You will be debt free on {debt_free_date}!",
        )

    @classmethod
    def make_positive_net_worth_milestone(cls, milestone_date: date):
        return Milestone(
            name=f"Positive Net Worth",
            date=milestone_date,
            header=f"Positive Net Worth",
            text=f"Your net worth will be positive on {milestone_date}!",
        )

    @classmethod
    def make_retirement_milestone(cls, retirement_date: date, net_worth: float):
        net_worth_str = "${:,.2f}".format(net_worth)
        return Milestone(
            name="Retirement",
            date=retirement_date,
            header="You Finally Retire!",
            text=f"You will retire on {retirement_date}. Your net worth at retirement will be {net_worth_str}!",
        )


class PlanMilestonesFactory:
    @classmethod
    def from_plan(cls, plan: FinancialPlan) -> PlanMilestones:
        start_date = get_first_date_of_next_month(datetime.today()).date()
        milestones = list()
        milestones.extend(cls.get_loan_payoff_milestones(plan, start_date))
        debt_free_milestone = cls.get_debt_free_milestone(plan, start_date)
        if debt_free_milestone is not None:
            milestones.append(debt_free_milestone)
        positive_net_worth_ms = cls.get_positive_net_worth_milestone(plan, start_date)
        if positive_net_worth_ms is not None:
            milestones.append(positive_net_worth_ms)
        milestones = sorted(milestones, key=lambda x: x.date)
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
            payoff_date = cls.get_loan_payoff_date(loan, plan, start_date)
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
    def get_loan_payoff_date(
        cls, loan: Loan, plan: FinancialPlan, start_date: date
    ) -> Optional[date]:
        for month, ms in enumerate(plan.monthly_solutions):
            loan_at_month = ms.portfolio.loans_by_id.get(loan.id_, None)
            if loan_at_month is None:
                return get_date_plus_month(start_date, month + 1)
            elif loan_at_month.current_balance >= _ALMOST_ZERO_LOWER_BOUND:
                return get_date_plus_month(start_date, month + 1)
        return None

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
