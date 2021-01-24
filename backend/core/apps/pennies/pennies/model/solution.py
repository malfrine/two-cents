from typing import List, Dict, Optional

from pydantic import BaseModel

from pennies.model.portfolio import Portfolio
from pennies.utilities.dict import get_value_from_dict

_ALMOST_ZERO_LOWER_BOUND = -1
_ALMOST_ZERO_UPPER_BOUND = 1


class MonthlyAllocation(BaseModel):
    payments: Dict[str, float]  # TODO: key payments on UUID
    leftover: float = 0.0

    def __getitem__(self, item):
        return self.payments[item]


class MonthlySolution(BaseModel):
    portfolio: Portfolio
    allocation: MonthlyAllocation

    def get_loan_payment(self, loan_name: str) -> float:
        return get_value_from_dict(loan_name, self.allocation.payments)

    def get_investment_payment(self, investment_name: str) -> float:
        return get_value_from_dict(investment_name, self.allocation.payments)

    def get_total_payments(self):
        return sum(payment for payment in self.allocation.payments.values())

    def get_value(self):
        return sum(i.current_balance for i in self.portfolio.instruments.values())

    def get_current_loans_value(self):
        return sum(loan.current_balance for loan in self.portfolio.loans)

    def get_total_loan_payments(self):
        return sum(self.get_loan_payment(loan.name) for loan in self.portfolio.loans)

    def get_total_loans_interest(self):
        return sum(
            loan.current_balance * loan.monthly_interest_rate
            for loan in self.portfolio.loans
        )

    def get_total_investments_interest(self):
        return sum(
            investment.current_balance * investment.monthly_interest_rate
            for investment in self.portfolio.investments()
        )

    def get_total_interest(self):
        return sum(
            instrument.current_balance * instrument.monthly_interest_rate
            for instrument in self.portfolio.instruments.values()
        )

    def get_current_investments_value(self):
        return sum(i.current_balance for i in self.portfolio.investments())

    def get_total_investment_payments(self):
        return sum(
            self.get_investment_payment(i.name) for i in self.portfolio.investments()
        )


class FinancialPlan(BaseModel):
    monthly_solutions: List[MonthlySolution]

    def get_total_payments(self):
        return sum(ms.get_total_payments() for ms in self.monthly_solutions)

    def get_net_worth(self):
        return self.monthly_solutions[-1].get_value()

    def get_total_interest_paid_on_loans(self):
        return sum(ms.get_total_loans_interest() for ms in self.monthly_solutions)

    def get_total_interest_earned_on_investments(self):
        return sum(ms.get_total_investments_interest() for ms in self.monthly_solutions)

    def get_total_interest(self):
        return sum(ms.get_total_interest() for ms in self.monthly_solutions)

    @property
    def retirement_net_worth(self) -> float:
        if len(self.monthly_solutions) == 0:
            return 0
        return round(self.monthly_solutions[-1].portfolio.net_worth)

    @property
    def retirement_month(self) -> int:
        if len(self.monthly_solutions) == 0:
            return 0
        return len(self.monthly_solutions)

    @property
    def first_positive_net_worth_month(self) -> Optional[int]:
        for month, ms in enumerate(self.monthly_solutions):
            net_worth = ms.portfolio.net_worth
            if net_worth <= _ALMOST_ZERO_LOWER_BOUND:
                continue
            return month + 1
        return None

    @property
    def debt_free_month(self) -> Optional[int]:
        for month, ms in enumerate(self.monthly_solutions):
            debt = ms.portfolio.get_debt()
            if debt >= _ALMOST_ZERO_UPPER_BOUND:
                continue
            return month + 1
        return None



class Solution(BaseModel):
    plans: Dict[str, FinancialPlan]

    def __getitem__(self, item) -> FinancialPlan:
        return self.plans[item]
