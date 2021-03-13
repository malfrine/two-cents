from typing import Dict, List

from pydantic import BaseModel

from pennies.model.solution import FinancialPlan, MonthlyAllocation, MonthlySolution


class Payment(BaseModel):
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
        return [
            Payment(
                instrument=monthly_solution.portfolio.get_instrument(
                    instrument_id
                ).name,
                payment=payment_amount,
            )
            for instrument_id, payment_amount in monthly_solution.allocation.payments.items()
        ]
