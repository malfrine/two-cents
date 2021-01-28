from collections import defaultdict
from datetime import date, datetime
from typing import NewType, Dict, List, Optional

from pydantic import BaseModel

from pennies.model.solution import FinancialPlan
from pennies.utilities.datetime import get_first_date_of_next_month, get_date_plus_month

_MAX_LOOKAHEAD_IN_MONTHS = 12
_MAX_LOOKAHEAD_AS_FRACTION_OF_PLAN = 0.2


class _ImportantDate(BaseModel):
    name: str
    date: date


class PlanSummaries(BaseModel):
    net_worth: float
    priorities: List[str]
    important_dates: List[_ImportantDate]


class PlanSummariesFactory:
    @classmethod
    def from_plan(cls, plan: FinancialPlan) -> PlanSummaries:

        return PlanSummaries(
            net_worth=plan.retirement_net_worth,
            priorities=cls.get_instrument_priorities(plan),
            important_dates=cls.get_important_dates(plan),
        )

    @classmethod
    def get_instrument_priorities(cls, plan: FinancialPlan) -> List[str]:
        def get_final_lookahead_index(num_sols: int) -> int:
            """look at payments for the max(min(num_months, 12), 20% of payments)"""
            return max(
                min(num_sols, _MAX_LOOKAHEAD_IN_MONTHS),
                round(num_sols * _MAX_LOOKAHEAD_AS_FRACTION_OF_PLAN),
            )

        num_sols = len(plan.monthly_solutions)
        if num_sols == 0:
            return list()

        final_index = get_final_lookahead_index(num_sols)
        total_payments = defaultdict(int)
        for ms in plan.monthly_solutions[:final_index]:
            for instrument, payment in ms.allocation.payments.items():
                total_payments[instrument] += payment
        sorted_payments = sorted(
            dict(total_payments).items(), key=lambda x: x[1], reverse=True
        )
        # TODO: once allocation is keyed on UUID, get instruments from portfolio
        return list(instrument for instrument, _ in sorted_payments)

    @classmethod
    def get_important_dates(cls, plan: FinancialPlan) -> List[_ImportantDate]:

        important_dates = list()
        start_date = get_first_date_of_next_month(datetime.today()).date()

        def append_if_not_none(month: Optional[int], name: str):
            if month is None:
                return
            important_dates.append(
                _ImportantDate(name=name, date=get_date_plus_month(start_date, month)),
            )

        append_if_not_none(plan.first_positive_net_worth_month, "Positive Net Worth")
        append_if_not_none(plan.debt_free_month, "Debt Free")
        append_if_not_none(plan.retirement_month, "Retirement")

        return sorted(important_dates, key=lambda x: x.date)
