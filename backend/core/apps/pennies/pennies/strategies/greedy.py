from collections import defaultdict
from typing import Dict, Optional, Iterable, List, Tuple
from uuid import UUID

from pennies.model.decision_periods import (
    DecisionPeriodsManagerFactory,
    WorkingPeriod,
    DecisionPeriodsManager,
)
from pennies.model.factories.financial_plan import FinancialPlanFactory
from pennies.model.financial_profile import FinancialProfile
from pennies.model.goal import AllGoalTypes, BigPurchase, NestEgg
from pennies.model.instrument import Instrument
from pennies.model.investment import NonGuaranteedInvestment
from pennies.model.loan import Loan
from pennies.model.parameters import Parameters
from pennies.model.portfolio import Portfolio
from pennies.model.portfolio_manager import PortfolioManager
from pennies.model.solution import FinancialPlan, MonthlySolution, MonthlyAllocation
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.allocation_strategy import AllocationStrategy
from pennies.strategies.milp.strategy import MILPStrategy
from pennies.utilities.finance import (
    calculate_loan_ending_payment,
    calculate_average_monthly_interest_rate,
    calculate_monthly_income_tax,
)

DEFAULT_GOAL_SPEND_IN_DEBT = 0.6
MAX_MILP_SECONDS = 1


class GreedyAllocationStrategy(AllocationStrategy):
    def create_solution(
        self, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> FinancialPlan:
        cur_portfolio: Portfolio = user_finances.portfolio.copy(deep=True)
        monthly_payments = list()
        monthly_withdrawals = list()
        decision_periods = self._make_decision_periods(user_finances, parameters)
        start_month = user_finances.financial_profile.retirement_month
        total_goal_contributions = {goal_id: 0.0 for goal_id in user_finances.goals}
        for working_period in decision_periods.working_periods:
            if (
                not cur_portfolio.non_mortgage_loans
                and cur_portfolio.non_guaranteed_investments()
            ):
                start_month = working_period.months[0]
                break

            (
                allocations,
                goal_contributions,
                withdrawals,
            ) = self.create_allocation_for_working_period(
                cur_portfolio,
                user_finances.goals,
                total_goal_contributions,
                user_finances.financial_profile,
                working_period=working_period,
            )

            for month, allocation, withdrawal in zip(
                working_period.months, allocations, withdrawals
            ):
                monthly_payments.append(allocation.payments)
                monthly_withdrawals.append(withdrawal)
                cur_portfolio = cur_portfolio.copy(deep=True)
                PortfolioManager.forward_on_month(
                    cur_portfolio,
                    payments=allocation.payments,
                    month=month,
                    withdrawals=withdrawal,
                )
                for goal_id, contribution in goal_contributions.items():
                    total_goal_contributions[goal_id] += contribution
        monthly_solutions = FinancialPlanFactory.create(
            monthly_payments,
            user_finances,
            parameters,
            monthly_withdrawals=monthly_withdrawals,
        ).monthly_solutions
        milp_monthly_solutions = self.solve_with_milp(
            start_month,
            cur_portfolio,
            user_finances.financial_profile,
            parameters,
            user_finances.goals,
        )
        monthly_solutions.extend(milp_monthly_solutions)
        return FinancialPlan(monthly_solutions=monthly_solutions)

    @classmethod
    def _make_decision_periods(
        cls, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> DecisionPeriodsManager:
        return DecisionPeriodsManagerFactory(
            max_working_months=parameters.max_months_in_payment_horizon,
            max_retirement_months=parameters.max_months_in_retirement_period,
        ).from_user_finances(
            start_month=parameters.starting_month, user_finances=user_finances
        )

    def solve_with_milp(
        self,
        start_month: int,
        portfolio: Portfolio,
        financial_profile: FinancialProfile,
        parameters: Parameters,
        goals: Dict[UUID, AllGoalTypes],
    ) -> List[MonthlySolution]:
        milp_parameters = Parameters.parse_obj(
            dict(parameters.dict(), starting_month=start_month)
        )
        user_finances = UserPersonalFinances(
            portfolio=portfolio, financial_profile=financial_profile, goals=goals
        )
        financial_plan = MILPStrategy().create_solution(
            user_finances=user_finances, parameters=milp_parameters
        )
        return financial_plan.monthly_solutions

    def create_allocation_for_working_period(
        self,
        portfolio: Portfolio,
        goals: Dict[UUID, AllGoalTypes],
        total_goal_contributions: Dict[UUID, float],
        financial_profile: FinancialProfile,
        working_period: WorkingPeriod,
    ) -> Tuple[List[MonthlyAllocation], Dict, List]:
        ...


class GreedyHeuristicStrategy(GreedyAllocationStrategy):
    @classmethod
    def get_monthly_allowance(cls, financial_profile: FinancialProfile, month: int):
        # this only works if greedy algorithm doesn't make rrsp contributions
        savings_fraction = financial_profile.percent_salary_for_spending / 100
        gross_income = financial_profile.get_pre_tax_monthly_income(month)
        tax = calculate_monthly_income_tax(
            gross_income, financial_profile.province_of_residence
        )
        return (gross_income - tax) * savings_fraction

    @classmethod
    def get_average_monthly_allowance(
        cls, financial_profile: FinancialProfile, months: List[int]
    ):
        if len(months) == 0:
            return 0
        total_monthly_allowance = sum(
            cls.get_monthly_allowance(financial_profile, month) for month in months
        )
        return total_monthly_allowance / len(months)

    def create_allocation_for_working_period(
        self,
        portfolio: Portfolio,
        goals: Dict[UUID, AllGoalTypes],
        total_goal_contributions: Dict[UUID, float],
        financial_profile: FinancialProfile,
        working_period: WorkingPeriod,
    ) -> Tuple[List[MonthlyAllocation], Dict, Dict]:
        payments = defaultdict(float)
        allowance = self.get_average_monthly_allowance(
            financial_profile, working_period.months
        )

        # min loan and investment payments
        min_payments = self.calculate_min_payments(
            portfolio, working_period.months, allowance
        )
        for key, value in min_payments.items():
            payments[key] = value
        remaining_loans = portfolio.non_mortgage_loans

        goal_spend_fraction = DEFAULT_GOAL_SPEND_IN_DEBT if remaining_loans else 1
        total_min_payments = sum(payment for payment in payments.values())
        max_goal_spend = min(
            allowance * goal_spend_fraction, allowance - total_min_payments
        )
        allowance -= total_min_payments

        contributions_for_period = self.calculate_goal_contributions_for_period(
            goals=goals,
            total_goal_contributions=total_goal_contributions,
            allowance=max_goal_spend,
            current_month=working_period.months[0],
        )
        savings_for_goal = sum(contributions_for_period.values())
        payments[portfolio.cash_investment.id_] += savings_for_goal
        allowance -= savings_for_goal

        cash_withdrawals = self.make_big_purchase_cash_withdrawals(
            goals, working_period.months, portfolio.cash_investment.current_balance
        )

        while remaining_loans and allowance > 0:
            worst_loan = self.get_worst_loan(remaining_loans, working_period.months)
            max_additional_payment = self.calculate_max_possible_loan_payment(
                worst_loan, allowance, working_period.months, payments[worst_loan.id_]
            )  # payment in addition to the minimum payment made
            payments[worst_loan.id_] += max_additional_payment
            allowance -= max_additional_payment
            remaining_loans = list(
                loan for loan in remaining_loans if loan.id_ != worst_loan.id_
            )
        if allowance and portfolio.non_guaranteed_investments():
            best_investment = self.get_best_investment(
                portfolio.non_guaranteed_investments(), working_period.months
            )
            payments[best_investment.id_] += allowance
            allowance = 0

        monthly_allocations = self.make_monthly_allocations(
            dict(payments), portfolio, working_period.months, allowance
        )
        monthly_withdrawals = [
            {portfolio.cash_investment.id_: cash_withdrawals.get(month, 0)}
            for month in working_period.months
        ]
        return monthly_allocations, contributions_for_period, monthly_withdrawals

    @classmethod
    def calculate_min_payments(
        cls, portfolio: Portfolio, months: List[int], allowance: float
    ) -> Dict[UUID, float]:
        min_payments = defaultdict(int)

        while allowance > 0:
            # loan min payments
            for loan in portfolio.loans:
                avg_interest_rate = calculate_average_monthly_interest_rate(
                    loan, months
                )
                loan_ending_payment = calculate_loan_ending_payment(
                    abs(loan.current_balance), avg_interest_rate, len(months)
                )
                max_min_payment = max(
                    loan.get_minimum_monthly_payment(month) for month in months
                )
                payment = min(max_min_payment, loan_ending_payment, allowance)
                min_payments[loan.id_] += payment
                allowance -= payment

            # investment min payments
            for investment in portfolio.non_guaranteed_investments():
                investment_min_payment = max(
                    investment.get_minimum_monthly_payment(month) for month in months
                )
                min_payment = min(allowance, investment_min_payment)
                min_payments[investment.id_] += min_payment
                allowance -= min_payment

            break

        return min_payments

    @classmethod
    def calculate_goal_contributions_for_period(
        cls,
        goals: Dict[UUID, AllGoalTypes],
        total_goal_contributions: Dict[UUID, float],
        allowance: float,
        current_month: int,
    ) -> Dict[UUID, float]:
        contributions = {goal_id: 0.0 for goal_id in goals}
        for goal in goals.values():

            months_left_for_goal = goal.due_month - current_month
            amount_saved_up_so_far = total_goal_contributions.get(goal.id_, 0)
            if amount_saved_up_so_far >= goal.amount:
                continue
            if months_left_for_goal <= 0:
                if isinstance(goal, NestEgg):
                    goal_spend = goal.amount - amount_saved_up_so_far
                elif isinstance(goal, BigPurchase):
                    continue  # assume we have missed the deadline and there
                    # is no need to save up for it because it is a strict deadline
                else:
                    raise ValueError(f"Unknown goal type: {goal.type}")
            else:
                goal_spend = (
                    goal.amount - amount_saved_up_so_far
                ) / months_left_for_goal
            if goal_spend >= allowance:
                contributions[goal.id_] += allowance
                allowance = 0
                break
            else:
                contributions[goal.id_] += goal_spend
                allowance -= goal_spend
        return contributions

    @classmethod
    def make_big_purchase_cash_withdrawals(
        cls, goals: Dict[UUID, AllGoalTypes], months: List[int], cash_balance: float
    ) -> Dict[int, float]:
        cash_withdrawals = {m: 0 for m in months}
        for goal in goals.values():
            if isinstance(goal, BigPurchase) and goal.due_month in months:
                if goal.amount >= cash_balance:
                    cash_withdrawals[goal.due_month] = cash_balance
                    cash_balance = 0
                    break
                else:
                    cash_withdrawals[goal.due_month] = goal.amount
                    cash_balance -= goal.amount
        return cash_withdrawals

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
        return min(
            loan_ending_payment,
            allowance,
            cls.get_max_payment(loan, months) or allowance,
        )

    @classmethod
    def get_max_payment(cls, instrument: Instrument, months: List[int]):
        return min(
            (
                instrument.get_maximum_monthly_payment(month)
                for month in months
                if instrument.get_maximum_monthly_payment(month) is not None
            ),
            default=None,
        )

    @classmethod
    def make_monthly_allocations(
        cls,
        payments: Dict[UUID, float],
        portfolio: Portfolio,
        months: List[int],
        leftover: float,
    ) -> List[MonthlyAllocation]:
        payments_by_name = {
            portfolio.instruments[key].id_: value for key, value in payments.items()
        }
        return [
            MonthlyAllocation(payments=payments_by_name, leftover=leftover)
            for _ in months
        ]

    @classmethod
    def get_best_investment(
        cls, investments: Iterable[NonGuaranteedInvestment], month
    ) -> Optional[NonGuaranteedInvestment]:
        best_investment: Optional[NonGuaranteedInvestment] = None
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
