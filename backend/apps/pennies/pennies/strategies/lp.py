from pathlib import Path
from typing import List, Dict

import pyomo.environ as pe
from pyomo.core import ConcreteModel

from pennies.errors.strategy_errors import StrategyFailureException
from pennies.model.loan import Loan
from pennies.model.portfolio import Portfolio
from pennies.model.portfolio_manager import PortfolioManager
from pennies.model.problem import Problem
from pennies.model.solution import FinancialPlan, MonthlySolution, MonthlyAllocation
from pennies.strategies.allocation_strategy import AllocationStrategy


def _make_solution(
        starting_portfolio: Portfolio,
        monthly_payments: List[Dict[str, float]],
        monthly_allowance: float
):
    monthly_solutions = []
    cur_portfolio = starting_portfolio.copy(deep=True)
    for mp in monthly_payments:
        monthly_solutions.append(
            MonthlySolution(
                allocation=MonthlyAllocation(
                    payments=mp,
                    leftover=monthly_allowance - sum(m for m in mp.values())
                ),
                portfolio=cur_portfolio.copy(deep=True),
            )
        )
        PortfolioManager.forward_on_month(portfolio=cur_portfolio,payments=mp)

    return FinancialPlan(
        monthly_solutions=monthly_solutions
    )


class LinearProgramStrategy(AllocationStrategy):

    def create_solution(self, problem_input: Problem) -> FinancialPlan:

        def money_balance(m, i, t):
            if t == 0:
                return m.v[i, t] == s[i]
            elif t >= end_date[i]:
                return m.v[i, t] == m.v[i, t - 1]
            else:
                return m.v[i, t] == m.v[i, t - 1] * (1 + r[i]) + m.x[i, t - 1]

        def payment_sum(m, t):
            return sum(m.x[i, t] for i in instrument_names) <= X

        def min_payments_loans(m, i, t):
            if t >= end_date[i]:
                return pe.Constraint.Skip
            else:
                return -m.x[i, t] <= -min[i] + X * (1 - m.b[i, t])

        m = ConcreteModel()
        instruments = list(problem_input.portfolio.instruments.values())
        end_date = {i.name: i.final_month for i in instruments}
        max_end_date = max(i.final_month for i in instruments)

        # Sets
        instrument_names = list(i.name for i in instruments)
        time_periods = list(t for t in range(max_end_date))
        loan_names = list(i.name for i in instruments if isinstance(i, Loan))
        instruments_and_times = list((i.name, t) for i in instruments for t in range(max_end_date))
        loans_and_times = list((i, t) for i in loan_names for t in range(max_end_date))


        # Params
        r = {i.name: i.monthly_interest_rate() for i in instruments}
        s = {i.name: i.current_balance for i in instruments}
        X = problem_input.monthly_allowance
        min = {i.name: i.minimum_monthly_payment for i in instruments}

        # Vars
        m.x = pe.Var(instruments_and_times, bounds=(0.0,X), initialize=X)
        m.v = pe.Var(instruments_and_times, initialize=0)
        m.b = pe.Var(loans_and_times, domain=pe.Binary, initialize=1)

        # Objective
        m.obj = pe.Objective(
            expr=sum(m.v[i,t] * r[i] for i, t in instruments_and_times),
            sense=pe.maximize
        )

        m.c1 = pe.Constraint(
            loans_and_times,
            rule=min_payments_loans
        )
        m.c2 = pe.Constraint(
            instruments_and_times,
            rule=money_balance
        )
        m.c3 = pe.Constraint(
            time_periods,
            rule=payment_sum
        )
        m.c4 = pe.Constraint(
            loans_and_times,
            rule=lambda m, i, t: m.v[i, t] <= 0
        )
        m.c5 = pe.Constraint(
            list((i, t) for i in loan_names for t in range(end_date[i] - 1, max_end_date)),
            rule=lambda m, i, t: m.v[i, t] == 0
        )
        m.c6 = pe.Constraint(
            loans_and_times,
            rule= lambda m, i, t: m.v[i, t] >= - 10000000000 * m.b[i, t]
        )
        # TODO: add min payments for investments

        results = pe.SolverFactory("cbc").solve(m)
        print(results)
        if not ((results.solver.status == pe.SolverStatus.ok)
            and (results.solver.termination_condition == pe.TerminationCondition.optimal)):
            raise StrategyFailureException("Linear program strategy could not solve")

        monthly_payments = [
            {i.name: pe.value(m.x[i.name, t]) for i in instruments}
            for t in range(max_end_date)
        ]

        return _make_solution(problem_input.portfolio, monthly_payments, problem_input.monthly_allowance)






