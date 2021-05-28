from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from pennies.model.loan import Loan
from pennies.model.solution import FinancialPlan, MonthlyAllocation, MonthlySolution


class Payment(BaseModel):
    id: int
    instrument_type: str
    instrument: str
    payment: float


class ActionPlan(BaseModel):
    monthly_allowance: float
    payments: List[Payment]


class ActionPlanFactory:
    @classmethod
    def from_plan(cls, plan: FinancialPlan) -> ActionPlan:
        if len(plan.monthly_solutions) == 0:
            raise ValueError("Cannot process plan with now monthly allocations")
        return ActionPlan(
            monthly_allowance=cls.get_monthly_allowance(plan.monthly_solutions[0]),
            payments=cls.get_payments(plan.monthly_solutions[0]),
        )

    @classmethod
    def get_monthly_allowance(cls, monthly_solution: MonthlySolution) -> float:
        return (
            sum(monthly_solution.allocation.payments.values())
            + monthly_solution.allocation.leftover
        )

    @classmethod
    def get_payments(cls, monthly_solution: MonthlySolution) -> List[Payment]:

        def make_payment(instrument_id, payment_amount):
            instrument = monthly_solution.portfolio.get_instrument(
                    instrument_id
            )
            return Payment(
                id=instrument.db_id,
                instrument=instrument.name,
                payment=payment_amount,
                instrument_type='loan' if isinstance(instrument, Loan) else 'investment',
            )

        return [
            make_payment(instrument_id, payment_amount)
            for instrument_id, payment_amount in monthly_solution.allocation.payments.items()
        ]
