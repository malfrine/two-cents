import logging
from datetime import datetime, date
from enum import Enum
from typing import Optional, NewType, List

from pydantic import BaseModel

from pennies.model.goal import BigPurchase, NestEgg
from pennies.model.instrument import Instrument
from pennies.model.investment import Investment
from pennies.model.loan import Loan
from pennies.model.problem_input import ProblemInput
from pennies.model.solution import FinancialPlan, MonthlySolution
from pennies.plan_processing.utilities import (
    get_loan_pay_off_date,
    get_actual_big_purchase_amount_and_withdrawals,
    get_nest_egg_completion_month_or_none,
    get_nest_egg_cash_balance_requirements,
)
from pennies.utilities.datetime import get_first_date_of_next_month, get_date_plus_month

"""
Plan failure types:
    - not meeting min payments (for loans or investments)
    - not paying off loans on time
    - not meeting goals on time
"""

_ALMOST_ZERO = 1
_TOLERANCE = 0.01
_ALLOWED_LOAN_PAYMENT_FAILURES = 4


class PlanFailureType(Enum):
    MIN_PAYMENT = "Loan Minimum Payment Failure"
    PRE_AUTHORIZED_CONTRIBUTION = "Pre-authorized Investment Contribution Failure"
    LOAN_DEFAULT = "Loan Default Failure"
    UNSATISFIED_GOAL = "Incomplete Goal Failure"


class PlanFailure(BaseModel):
    failure_type: str
    header: str
    text: str
    instrument_id: Optional[int] = None
    instrument_type: Optional[str] = None

    @classmethod
    def make_loan_default(
        cls, loan: Loan, exected_pay_off_date: date, actual_pay_off_date: Optional[date]
    ) -> "PlanFailure":
        if actual_pay_off_date is None:
            text = (
                f"{loan.name} must be paid off by {exected_pay_off_date} "
                f"but it will never be paid off according to this plan"
            )
        else:
            text = (
                f"{loan.name} must be paid off by {exected_pay_off_date} "
                f"but it will only be paid off by {actual_pay_off_date}"
            )

        return PlanFailure(
            failure_type=PlanFailureType.LOAN_DEFAULT.value,
            header=f"Unable to pay off {loan.name} on time",
            text=text,
        )

    @classmethod
    def make_loan_min_payment_failure(cls, loan: Loan, dates: List[date]):
        min_date = min(dates)
        max_date = max(dates)
        num_missed_payments = len(dates)
        text = (
            f"You will miss {num_missed_payments} payments on {loan.name} "
            f"on dates ranging from {min_date} to {max_date}"
        )
        return PlanFailure(
            failure_type=PlanFailureType.MIN_PAYMENT.value,
            header=f"Missed some payments on {loan.name}",
            text=text,
        )

    @classmethod
    def make_pre_authorized_contribution_failure(
        cls, investment: Investment, dates: List[date]
    ):
        min_date = min(dates)
        max_date = max(dates)
        num_missed_payments = len(dates)
        text = (
            f"You will miss {num_missed_payments} payments on "
            f"{investment.name} on dates ranging from {min_date} to {max_date}"
        )
        return PlanFailure(
            failure_type=PlanFailureType.PRE_AUTHORIZED_CONTRIBUTION.value,
            header=f"Missed some payments on {investment.name}",
            text=text,
        )

    @classmethod
    def make_failed_nest_egg_goal(
        cls,
        goal: NestEgg,
        expected_completion_date: date,
        actual_completion_date: Optional[date],
    ):
        if actual_completion_date is None:
            text = "You will never be able to build up this nest egg"
        else:
            text = (
                f"You will be x months late in reaching your nest "
                f"egg goal and only complete goal on {actual_completion_date}"
            )
        return PlanFailure(
            failure_type=PlanFailureType.UNSATISFIED_GOA.value,
            header=f"Unable to build nest egg for {goal.name} by {expected_completion_date}",
            text=text,
        )

    @classmethod
    def make_failed_big_purchase_goal(cls, goal: BigPurchase, actual_amount: float):
        return PlanFailure(
            failure_type=PlanFailureType.UNSATISFIED_GOAL.value,
            header=f"Unable to purchase {goal.name} for ${goal.amount:,.0f}",
            text=f"Only able to save up ${actual_amount:,.0f}",
        )


PlanFailures = NewType("PlanMilestones", List[PlanFailure])


class PlanFailuresFactory:
    @classmethod
    def create(cls, plan: FinancialPlan, problem_input: ProblemInput):
        start_date = get_first_date_of_next_month(datetime.today()).date()
        failures = list()
        failures.extend(cls.get_loan_defaults(plan, problem_input, start_date))
        failures.extend(
            cls.get_loan_min_payment_failures(plan, problem_input, start_date)
        )
        failures.extend(
            cls.get_pre_authorized_contribution_failures(
                plan, problem_input, start_date
            )
        )
        failures.extend(cls.get_goal_failures(plan, problem_input, start_date))
        for failure in failures:
            print(failure.text)
        return failures

    @classmethod
    def get_loan_defaults(
        cls, plan: FinancialPlan, problem_input: ProblemInput, start_date: date
    ) -> List[PlanFailure]:
        failures = []
        for loan in problem_input.user_finances.portfolio.loans:
            final_month = (
                loan.final_month or problem_input.user_finances.portfolio.final_month
            )
            pay_off_date = get_loan_pay_off_date(loan, plan, start_date)
            final_date = get_date_plus_month(start_date, final_month)
            if pay_off_date is None or pay_off_date > final_date:
                # unable to pay off loan on time
                failures.append(
                    PlanFailure.make_loan_default(loan, final_date, pay_off_date)
                )
        return failures

    @classmethod
    def get_loan_min_payment_failures(
        cls, plan: FinancialPlan, problem_input: ProblemInput, start_date: date
    ) -> List[PlanFailure]:
        failures = []
        for loan in problem_input.user_finances.portfolio.loans:
            missed_payment_dates = cls.get_missed_payment_dates(
                loan, plan.monthly_solutions, start_date
            )
            num_missed_payments = len(missed_payment_dates)
            if num_missed_payments > _ALLOWED_LOAN_PAYMENT_FAILURES:
                failures.append(
                    PlanFailure.make_loan_min_payment_failure(
                        loan, missed_payment_dates
                    )
                )
        return failures

    @classmethod
    def get_missed_payment_dates(
        cls,
        instrument: Instrument,
        monthly_solutions: List[MonthlySolution],
        start_date: date,
    ):
        missed_payment_dates = list()
        for ms in monthly_solutions:
            instrument = ms.portfolio.get_instrument_or_none(instrument.id_)
            if instrument is None:
                break  # loan has been paid off
            if instrument.current_balance > -_ALMOST_ZERO:
                break  # loan has been paid off pretty much
            expected_loan_payment = instrument.get_minimum_monthly_payment(ms.month)
            if expected_loan_payment < 10:
                continue
            loan_payment = ms.get_loan_payment(instrument.id_)
            if expected_loan_payment - 2 <= loan_payment:
                continue  # met the minimum monthly payment
            missed_payment_date = get_date_plus_month(start_date, ms.month)
            missed_payment_dates.append(missed_payment_date)
        return missed_payment_dates

    @classmethod
    def get_pre_authorized_contribution_failures(
        cls, plan: FinancialPlan, problem_input: ProblemInput, start_date: date
    ) -> List[PlanFailure]:
        failures = []
        for investment in problem_input.user_finances.portfolio.investments():
            missed_payment_dates = cls.get_missed_payment_dates(
                investment, plan.monthly_solutions, start_date
            )
            if missed_payment_dates:
                failures.append(
                    PlanFailure.make_pre_authorized_contribution_failure(
                        investment, missed_payment_dates
                    )
                )
        return failures

    @classmethod
    def get_goal_failures(
        cls, plan: FinancialPlan, problem_input: ProblemInput, start_date: date
    ) -> List[PlanFailure]:
        failures = []
        goals = problem_input.user_finances.goals
        cash_balance_requirements = get_nest_egg_cash_balance_requirements(goals)
        cash_balance_dict = {
            goal.id_: amount_needed for goal, amount_needed in cash_balance_requirements
        }
        for goal in goals.values():
            if isinstance(goal, NestEgg):
                amount_needed = cash_balance_dict.get(goal.id_)
                if amount_needed is None:
                    continue
                completion_month = get_nest_egg_completion_month_or_none(
                    goal, plan, amount_needed
                )
                expected_date = get_date_plus_month(start_date, goal.due_month)
                if completion_month is None:
                    failure = PlanFailure.make_failed_nest_egg_goal(
                        goal, expected_date, None
                    )
                    failures.append(failure)
                elif completion_month > goal.due_month:
                    actual_date = get_date_plus_month(start_date, completion_month)
                    failure = PlanFailure.make_failed_nest_egg_goal(
                        goal, expected_date, actual_date
                    )
                    failures.append(failure)
            elif isinstance(goal, BigPurchase):
                amount, _ = get_actual_big_purchase_amount_and_withdrawals(goal, plan)
                if amount < goal.amount - _TOLERANCE:
                    failure = PlanFailure.make_failed_big_purchase_goal(goal, amount)
                    failures.append(failure)
            else:
                logging.warning(
                    f"Goal {goal.type} is not recognized - cannot assess if it has been passed"
                )
        return failures
