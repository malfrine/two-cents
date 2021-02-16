from collections import defaultdict
from typing import Dict, Optional, Iterable, List
from uuid import UUID

from pennies.model.financial_profile import FinancialProfile
from pennies.model.investment import Investment
from pennies.model.loan import Loan
from pennies.model.parameters import Parameters
from pennies.model.payment_horizons import PaymentHorizonsFactory, PaymentHorizon
from pennies.model.portfolio import Portfolio
from pennies.model.portfolio_manager import PortfolioManager
from pennies.model.solution import FinancialPlan, MonthlySolution, MonthlyAllocation
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.allocation_strategy import AllocationStrategy
from pennies.strategies.milp.strategy import MILPStrategy
from pennies.utilities.finance import (
    calculate_loan_ending_payment,
    calculate_average_monthly_interest_rate,
    calculate_balance_after_fixed_monthly_payments,
)


def _pay_loan(
    loan_payments: Dict[str, float], loan: Loan, payment_amount: float
) -> None:
    loan.current_balance -= payment_amount
    loan_payments[loan.name] += payment_amount


def _pay_investment(
    investment_payments: Dict[str, float], investment: Investment, payment_amount: float
) -> None:
    investment_payments[investment.name] += payment_amount
    investment.current_balance += payment_amount


class GreedyAllocationStrategy(AllocationStrategy):
    def create_solution(
        self, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> FinancialPlan:
        cur_portfolio: Portfolio = user_finances.portfolio.copy(deep=True)
        monthly_solutions = list()
        payment_horizons = PaymentHorizonsFactory(
            max_months=parameters.max_months_in_payment_horizon,
        ).from_num_months(
            start_month=parameters.starting_month, final_month=user_finances.final_month
        )

        finish_with_milp = False
        start_month = user_finances.final_month
        for payment_horizon in payment_horizons.data:
            if not cur_portfolio.loans and cur_portfolio.investments():
                finish_with_milp = True
                start_month = payment_horizon.months[0]
                break
            allocations = self.create_allocation_for_payment_horizon(
                cur_portfolio,
                user_finances.financial_profile.monthly_allowance,
                payment_horizon=payment_horizon,
            )
            for month, allocation in zip(payment_horizon.months, allocations):
                monthly_solutions.append(
                    MonthlySolution(
                        portfolio=cur_portfolio, allocation=allocation, month=month
                    )
                )
                cur_portfolio = PortfolioManager.forward_on_month(
                    cur_portfolio, payments=allocation.payments, month=month
                )

        if finish_with_milp:
            milp_monthly_solutions = self.solve_with_milp(
                start_month,
                cur_portfolio,
                user_finances.financial_profile,
                parameters,
            )
            monthly_solutions.extend(milp_monthly_solutions)
        return FinancialPlan(monthly_solutions=monthly_solutions)

    def solve_with_milp(
        self,
        start_month: int,
        portfolio: Portfolio,
        financial_profile: FinancialProfile,
        parameters: Parameters,
    ) -> List[MonthlySolution]:
        milp_parameters = Parameters.parse_obj(
            dict(parameters.dict(), starting_month=start_month)
        )
        user_finances = UserPersonalFinances(
            portfolio=portfolio, financial_profile=financial_profile
        )
        financial_plan = MILPStrategy().create_solution(
            user_finances=user_finances, parameters=milp_parameters
        )
        return financial_plan.monthly_solutions

    def create_allocation_for_payment_horizon(
        self, portfolio: Portfolio, allowance: float, payment_horizon: PaymentHorizon
    ) -> List[MonthlyAllocation]:
        ...


class GreedyHeuristicStrategy(GreedyAllocationStrategy):
    def create_allocation_for_payment_horizon(
        self, portfolio: Portfolio, allowance: float, payment_horizon: PaymentHorizon
    ) -> List[MonthlyAllocation]:
        payments = defaultdict(float)
        min_payments = self.calculate_min_payments(portfolio, payment_horizon.months)
        for key, value in min_payments.items():
            payments[key] = value
        allowance -= sum(payment for payment in payments.values())
        remaining_loans = portfolio.loans
        while remaining_loans and allowance:
            worst_loan = self.get_worst_loan(remaining_loans, payment_horizon.months)
            max_additional_payment = self.calculate_max_possible_loan_payment(
                worst_loan, allowance, payment_horizon.months, payments[worst_loan.id_]
            )
            payments[worst_loan.id_] += max_additional_payment
            allowance -= max_additional_payment
            remaining_loans = list(
                loan for loan in remaining_loans if loan.id_ != worst_loan.id_
            )
        if allowance and portfolio.investments():
            best_investment = self.get_best_investment(
                portfolio.investments(), payment_horizon.months
            )
            payments[best_investment.id_] += allowance
            allowance = 0
        return self.make_monthly_allocations(
            dict(payments), portfolio, payment_horizon.months, allowance
        )

    @classmethod
    def calculate_min_payments(
        cls, portfolio: Portfolio, months: List[int]
    ) -> Dict[UUID, float]:
        min_payments = dict()
        for instrument in portfolio.instruments.values():
            avg_interest_rate = calculate_average_monthly_interest_rate(
                instrument, months
            )
            loan_ending_payment = calculate_loan_ending_payment(
                abs(instrument.current_balance), avg_interest_rate, len(months)
            )
            max_min_payment = max(
                instrument.get_minimum_monthly_payment(month)
                for month in months
            )
            min_payments[instrument.id_] = min(
                max_min_payment, loan_ending_payment
            )
        return min_payments

    @classmethod
    def calculate_max_possible_loan_payment(
        cls, loan: Loan, allowance: float, months: List[int], cur_payment: float
    ) -> float:
        interest_rate = calculate_average_monthly_interest_rate(loan, months)
        loan_ending_payment = (
            calculate_loan_ending_payment(
                abs(loan.current_balance), interest_rate, len(months)
            )
            - cur_payment
        )
        return min(loan_ending_payment, allowance)

    @classmethod
    def make_monthly_allocations(
        cls,
        payments: Dict[UUID, float],
        portfolio: Portfolio,
        months: List[int],
        leftover: float,
    ) -> List[MonthlyAllocation]:
        payments_by_name = {
            portfolio.instruments_by_id[key].name: value
            for key, value in payments.items()
        }
        return [
            MonthlyAllocation(payments=payments_by_name, leftover=leftover)
            for _ in months
        ]

    @classmethod
    def get_best_investment(
        cls, investments: Iterable[Investment], month
    ) -> Investment:
        best_investment: Optional[Investment] = None
        for investment in investments:
            if best_investment is None or investment.monthly_interest_rate(
                month
            ) < best_investment.monthly_interest_rate(month):
                best_investment = investment
        return best_investment

    @classmethod
    def get_worst_loan(cls, loans: Iterable[Loan], months: List[int]) -> Loan:
        ...


class SnowballStrategy(GreedyHeuristicStrategy):
    @classmethod
    def get_worst_loan(cls, loans: Iterable[Loan], months: List[int]) -> Loan:
        worst_loan: Optional[Loan] = None
        for loan in loans:
            if worst_loan is None or abs(loan.current_balance) < abs(
                worst_loan.current_balance
            ):
                worst_loan = loan
        return worst_loan


class AvalancheStrategy(GreedyHeuristicStrategy):
    @classmethod
    def get_worst_loan(self, loans: Iterable[Loan], months: List[int]) -> Loan:
        worst_loan: Optional[Loan] = None
        for loan in loans:
            if worst_loan is None or loan.monthly_interest_rate(
                months[0]
            ) > worst_loan.monthly_interest_rate(months[0]):
                worst_loan = loan
        return worst_loan


class AvalancheBallStrategy(GreedyHeuristicStrategy):
    @classmethod
    def get_worst_loan(self, loans: Iterable[Loan], months: List[int]) -> Loan:
        worst_loan: Optional[Loan] = None
        for loan in loans:
            if worst_loan is None or loan.current_balance * loan.monthly_interest_rate(
                months[0]
            ) < worst_loan.current_balance * worst_loan.monthly_interest_rate(
                months[0]
            ):
                worst_loan = loan
        return worst_loan
