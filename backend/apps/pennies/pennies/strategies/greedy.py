from typing import Dict, Optional, Iterable, List

from pennies.model.investment import Investment
from pennies.model.loan import Loan
from pennies.model.portfolio import Portfolio
from pennies.model.portfolio_manager import PortfolioManager
from pennies.model.problem import Problem
from pennies.model.solution import FinancialPlan, MonthlySolution, MonthlyAllocation
from pennies.strategies.allocation_strategy import AllocationStrategy


def _pay_loan(loan_payments: Dict[str, float], loan: Loan, payment_amount: float) -> None:
    loan.current_balance -= payment_amount
    loan_payments[loan.name] += payment_amount

def _pay_investment(investment_payments: Dict[str, float], investment: Investment, payment_amount: float) -> None:
    investment_payments[investment.name] += payment_amount
    investment.current_balance += payment_amount


class GreedyAllocationStrategy(AllocationStrategy):

    def create_solution(self, problem_input: Problem) -> FinancialPlan:
        minimum_payment = sum(loan.minimum_monthly_payment for loan in problem_input.portfolio.loans) + \
                          sum(investment.minimum_monthly_payment for investment in problem_input.portfolio.investments())
        if problem_input.monthly_allowance < minimum_payment:
            raise ValueError("Cannot pay minimum payment with given monthly spend")
        cur_portfolio: Portfolio = problem_input.portfolio.copy(deep=True)
        monthly_solutions = list()
        for _ in range(problem_input.portfolio.get_final_month()):
            ms = self.create_monthly_solution(cur_portfolio, problem_input.monthly_allowance)
            # print(ms.allocation.payments)
            monthly_solutions.append(ms)
            PortfolioManager.forward_on_month(cur_portfolio, ms.allocation.payments)
            # print({name: instrument.current_balance for name, instrument in cur_portfolio.instruments.items()})
        return FinancialPlan(monthly_solutions=monthly_solutions)

    def create_monthly_solution(self, portfolio: Portfolio, allowance: float) -> MonthlySolution:
        ...


class GreedyHeuristicStrategy(GreedyAllocationStrategy):

    def create_monthly_solution(self, portfolio: Portfolio, allowance: float) -> MonthlySolution:
        payments_manager = PaymentsManager(portfolio, allowance)
        payments_manager.pay_minimum_amounts()
        while payments_manager.has_allowance():
            if payments_manager.has_loans():
                worst_loan = self.get_worst_loan(payments_manager.get_loans())
                if worst_loan is not None:
                    payment_amount = min(payments_manager.get_allowance(), abs(worst_loan.current_balance))
                    payments_manager.pay_loan(worst_loan.name, payment_amount)
            elif payments_manager.has_investments():
                best_investment = self.get_best_investment(payments_manager.get_investments())
                if best_investment is not None:
                    payments_manager.pay_investment(best_investment.name, payments_manager.get_allowance())
            else:
                return payments_manager.make_monthly_solution()
        return payments_manager.make_monthly_solution()

    @classmethod
    def get_best_investment(cls, investments: Iterable[Investment]) -> Investment:
        best_investment: Optional[Investment] = None
        for investment in investments:
            if best_investment is None or investment.annual_interest_rate < best_investment.annual_interest_rate:
                best_investment = investment
        return best_investment

    @classmethod
    def get_worst_loan(cls, loans: Iterable[Loan]) -> Loan:
        ...

class SnowballStrategy(GreedyHeuristicStrategy):

    @classmethod
    def get_worst_loan(cls, loans: Iterable[Loan]) -> Loan:
        worst_loan: Optional[Loan] = None
        for loan in loans:
            if worst_loan is None or loan.current_balance < worst_loan.current_balance:
                worst_loan = loan
        return worst_loan


class AvalancheStrategy(GreedyHeuristicStrategy):

    @classmethod
    def get_worst_loan(self, loans: Iterable[Loan]) -> Loan:
        worst_loan: Optional[Loan] = None
        for loan in loans:
            if worst_loan is None or loan.annual_interest_rate > worst_loan.annual_interest_rate:
                worst_loan = loan
        return worst_loan


class AvalancheBallStrategy(GreedyHeuristicStrategy):

    @classmethod
    def get_worst_loan(self, loans: Iterable[Loan]) -> Loan:
        worst_loan: Optional[Loan] = None
        for loan in loans:
            if (worst_loan is None
                    or loan.current_balance * loan.monthly_interest_rate()
                    < worst_loan.current_balance * worst_loan.monthly_interest_rate()):
                worst_loan = loan
        return worst_loan


class PaymentsManager:
    """Utility class to assist with calculating payments for greedy strategies"""
    _payments: Dict[str, float]
    _cur_portfolio: Portfolio
    _allowance: float

    def __init__(self, portfolio: Portfolio, allowance: float):
        self._cur_portfolio = portfolio.copy(deep=True)
        self._allowance = allowance
        self._payments = {i: 0 for i in self._cur_portfolio.instruments.keys()}

    def _update_on_payment(self, instrument_name: str, payment_amount: float):
        self._payments[instrument_name] += payment_amount
        self._allowance -= payment_amount

    def pay_loan(self, loan_name: str, max_payment_amount: float) -> None:
        actual_payment = self._cur_portfolio.get_loan(loan_name).receive_payment(max_payment_amount)
        self._update_on_payment(loan_name, actual_payment)
        if self._cur_portfolio.get_loan(loan_name).is_paid_off():
            self._cur_portfolio.remove_instrument(loan_name)

    def pay_investment(self, investment_name: str, max_payment_amount: float) -> None:
        actual_payment = self._cur_portfolio.get_investment(investment_name).receive_payment(max_payment_amount)
        self._update_on_payment(investment_name, actual_payment)

    def pay_minimum_amounts(self):
        for loan in self.get_loans():
            self.pay_loan(loan.name, min(abs(loan.current_balance), loan.minimum_monthly_payment))
        for investment in self.get_investments():
            self.pay_investment(investment.name, investment.minimum_monthly_payment)

    def has_allowance(self) -> bool:
        return self._allowance > 0

    def has_loans(self) -> bool:
        return bool(self.get_loans())

    def get_loans(self) -> List[Loan]:
        return list(self._cur_portfolio.loans)

    def has_investments(self) -> bool:
        return bool(self.get_investments())

    def get_investments(self) -> List[Investment]:
        return list(self._cur_portfolio.investments())

    def get_allowance(self) -> float:
        return self._allowance

    def remove_loan(self, loan_name: str) -> None:
        self._cur_portfolio.remove_instrument(loan_name)

    def make_monthly_solution(self) -> MonthlySolution:
        return MonthlySolution(
            allocation=MonthlyAllocation(
                payments=self._payments,
                leftover=self.get_allowance()
            ),
            portfolio=self._cur_portfolio.copy(deep=True),
        )
