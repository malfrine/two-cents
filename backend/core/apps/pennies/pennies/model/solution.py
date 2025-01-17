from typing import List, Dict, Optional, NewType
from uuid import UUID

from pydantic import BaseModel

from pennies.model.portfolio import Portfolio
from pennies.model.problem_input import ProblemInput
from pennies.utilities.dict import get_value_from_dict

_ALMOST_ZERO_LOWER_BOUND = -1
_ALMOST_ZERO_UPPER_BOUND = 1


class MonthlyAllocation(BaseModel):
    payments: Dict[UUID, float]  # TODO: key payments on UUID
    leftover: float = 0.0

    def __getitem__(self, item):
        return self.payments[item]


MonthlyWithdrawal = NewType("MonthlyWithdrawal", Dict[UUID, float])


class MonthlySolution(BaseModel):
    month: int
    portfolio: Portfolio
    allocation: MonthlyAllocation
    taxes_paid: float
    gross_income: float
    taxable_income: float
    withdrawals: MonthlyWithdrawal

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
        return sum(self.get_loan_payment(loan.id_) for loan in self.portfolio.loans)

    def get_total_loans_interest(self, month: int):
        return sum(
            loan.current_balance * loan.monthly_interest_rate(month=month)
            for loan in self.portfolio.loans
        )

    def get_loan_interest_incurred(self, id_):
        # TODO: determine if this is the best way? should we just keep paid of loans on the portfolio?
        loan = self.portfolio.loans_by_id.get(id_, None)
        if loan is None:
            return 0
        else:
            return loan.current_balance * loan.monthly_interest_rate(self.month)

    def get_total_investments_interest(self, month):
        return sum(
            investment.current_balance * investment.monthly_interest_rate(month=month)
            for investment in self.portfolio.non_guaranteed_investments()
        )

    def get_total_interest(self, month: int):
        return sum(
            instrument.current_balance * instrument.monthly_interest_rate(month)
            for instrument in self.portfolio.instruments.values()
        )

    def get_current_investments_value(self):
        return sum(
            i.current_balance for i in self.portfolio.non_guaranteed_investments()
        )

    def get_total_investment_payments(self):
        return sum(
            self.get_investment_payment(i.id_)
            for i in self.portfolio.non_guaranteed_investments()
        )

    def get_total_withdrawals(self):
        return sum(w for w in self.withdrawals.values())


class FinancialPlan(BaseModel):
    monthly_solutions: List[MonthlySolution]

    def get_total_payments(self):
        return sum(ms.get_total_payments() for ms in self.monthly_solutions)

    def get_net_worth(self):
        if len(self.monthly_solutions) == 0:
            return 0
        return self.monthly_solutions[-1].get_value()

    def get_net_worth_at(self, month: int):
        return self.monthly_solutions[month - 1].get_value()

    def get_total_interest_paid_on_loans(self):
        return sum(
            ms.get_total_loans_interest(ms.month) for ms in self.monthly_solutions
        )

    def get_total_interest_earned_on_investments(self):
        return sum(
            ms.get_total_investments_interest(ms.month) for ms in self.monthly_solutions
        )

    def get_total_interest(self):
        return sum(ms.get_total_interest(ms.month) for ms in self.monthly_solutions)

    def get_interest_paid_on_loan(self, id_: UUID):
        return sum(
            abs(ms.get_loan_interest_incurred(id_)) for ms in self.monthly_solutions
        )

    @property
    def retirement_month(self) -> int:
        if len(self.monthly_solutions) == 0:
            return 0
        return len(self.monthly_solutions)  # TODO: this is wrong!

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

    def get_total_income_taxes_paid(self):
        return sum(ms.taxes_paid for ms in self.monthly_solutions)

    def get_total_withdrawals(self):
        return sum(ms.get_total_withdrawals() for ms in self.monthly_solutions)


class Solution(BaseModel):
    plans: Dict[str, FinancialPlan]
    problem_input: ProblemInput

    def __getitem__(self, item) -> FinancialPlan:
        return self.plans[item]
