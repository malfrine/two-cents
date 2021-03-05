from collections import defaultdict
from typing import Dict, Optional, Iterable, List
from uuid import UUID

from pennies.model.factories.financial_plan import FinancialPlanFactory
from pennies.model.financial_profile import FinancialProfile
from pennies.model.investment import Investment
from pennies.model.loan import Loan
from pennies.model.parameters import Parameters
from pennies.model.decision_periods import DecisionPeriodsFactory, DecisionPeriod, WorkingPeriod, DecisionPeriods
from pennies.model.portfolio import Portfolio
from pennies.model.portfolio_manager import PortfolioManager
from pennies.model.solution import FinancialPlan, MonthlySolution, MonthlyAllocation
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.allocation_strategy import AllocationStrategy
from pennies.strategies.milp.strategy import MILPStrategy
from pennies.utilities.finance import (
    calculate_loan_ending_payment,
    calculate_average_monthly_interest_rate,
    calculate_balance_after_fixed_monthly_payments, calculate_monthly_income_tax,
)


class GreedyAllocationStrategy(AllocationStrategy):
    def create_solution(
        self, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> FinancialPlan:
        cur_portfolio: Portfolio = user_finances.portfolio.copy(deep=True)
        monthly_payments = list()
        decision_periods = self._make_decision_periods(user_finances, parameters)
        start_month = user_finances.financial_profile.retirement_month
        for working_period in decision_periods.working_periods:
            if not cur_portfolio.loans and cur_portfolio.investments():
                start_month = working_period.months[0]
                break
            allocations = self.create_allocation_for_working_period(
                cur_portfolio,
                user_finances.financial_profile.monthly_allowance,
                working_period=working_period,
            )
            for month, allocation in zip(working_period.months, allocations):
                monthly_payments.append(allocation.payments)
                cur_portfolio = PortfolioManager.forward_on_month(
                    cur_portfolio, payments=allocation.payments, month=month
                )
        monthly_solutions = FinancialPlanFactory.create(monthly_payments, user_finances, parameters).monthly_solutions
        milp_monthly_solutions = self.solve_with_milp(
            start_month,
            cur_portfolio,
            user_finances.financial_profile,
            parameters,
        )
        monthly_solutions.extend(milp_monthly_solutions)
        return FinancialPlan(monthly_solutions=monthly_solutions)

    @classmethod
    def _make_decision_periods(cls, user_finances: UserPersonalFinances, parameters: Parameters) -> DecisionPeriods:
        return DecisionPeriodsFactory(
            max_months=parameters.max_months_in_payment_horizon,
        ).from_num_months(
            start_month=parameters.starting_month,
            retirement_month=user_finances.financial_profile.retirement_month,
            final_month=user_finances.financial_profile.death_month
        )


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

    def create_allocation_for_working_period(
        self, portfolio: Portfolio, allowance: float, working_period: WorkingPeriod
    ) -> List[MonthlyAllocation]:
        ...


class GreedyHeuristicStrategy(GreedyAllocationStrategy):
    def create_allocation_for_working_period(
        self, portfolio: Portfolio, allowance: float, working_period: WorkingPeriod
    ) -> List[MonthlyAllocation]:
        payments = defaultdict(float)
        min_payments = self.calculate_min_payments(portfolio, working_period.months)
        for key, value in min_payments.items():
            payments[key] = value
        allowance -= sum(payment for payment in payments.values())
        remaining_loans = portfolio.loans
        while remaining_loans and allowance:
            worst_loan = self.get_worst_loan(remaining_loans, working_period.months)
            max_additional_payment = self.calculate_max_possible_loan_payment(
                worst_loan, allowance, working_period.months, payments[worst_loan.id_]
            ) # payment in addition to the minimum payment made
            payments[worst_loan.id_] += max_additional_payment
            allowance -= max_additional_payment
            remaining_loans = list(
                loan for loan in remaining_loans if loan.id_ != worst_loan.id_
            )
        if allowance and portfolio.investments():
            best_investment = self.get_best_investment(
                portfolio.investments(), working_period.months
            )
            payments[best_investment.id_] += allowance
            allowance = 0
        return self.make_monthly_allocations(
            dict(payments), portfolio, working_period.months, allowance
        )

    @classmethod
    def calculate_min_payments(
        cls, portfolio: Portfolio, months: List[int]
    ) -> Dict[UUID, float]:
        min_payments = dict()
        for loan in portfolio.loans:
            avg_interest_rate = calculate_average_monthly_interest_rate(loan, months)
            loan_ending_payment = calculate_loan_ending_payment(
                abs(loan.current_balance), avg_interest_rate, len(months)
            )
            max_min_payment = max(
                loan.get_minimum_monthly_payment(month) for month in months
            )
            min_payments[loan.id_] = min(max_min_payment, loan_ending_payment)
        for investment in portfolio.investments():
            min_payments[investment.id_] = max(
                investment.get_minimum_monthly_payment(month) for month in months
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
    ) -> Optional[Investment]:
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
