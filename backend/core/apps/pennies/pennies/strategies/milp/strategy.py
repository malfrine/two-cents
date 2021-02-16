import itertools
from dataclasses import dataclass
from typing import List, Dict

import pyomo.environ as pe
import pyutilib
from pyomo.core import ConcreteModel

from pennies.model.parameters import Parameters
from pennies.model.portfolio import Portfolio
from pennies.model.portfolio_manager import PortfolioManager
from pennies.model.solution import FinancialPlan, MonthlySolution, MonthlyAllocation
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.allocation_strategy import AllocationStrategy
from pennies.strategies.milp.constraints import MILPConstraints
from pennies.strategies.milp.objective import MILPObjective
from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables

pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False


def _make_solution(
    starting_portfolio: Portfolio,
    monthly_payments: List[Dict[str, float]],
    monthly_allowance: float,
):
    monthly_solutions = []
    cur_portfolio = starting_portfolio.copy(deep=True)
    for index, mp in enumerate(monthly_payments):
        monthly_solutions.append(
            MonthlySolution(
                allocation=MonthlyAllocation(
                    payments=mp,
                    leftover=monthly_allowance - sum(m for m in mp.values()),
                ),
                portfolio=cur_portfolio,
                month=index,
            )
        )
        cur_portfolio = PortfolioManager.forward_on_month(
            portfolio=cur_portfolio, payments=mp, month=index
        )

    return FinancialPlan(monthly_solutions=monthly_solutions)


@dataclass
class MILP:

    user_finances: UserPersonalFinances
    pyomodel: ConcreteModel
    sets: MILPSets
    parameters: MILPParameters
    variables: MILPVariables
    constraints: MILPConstraints
    objective: MILPObjective

    @classmethod
    def create(
        cls, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> "MILP":
        m = ConcreteModel()

        sets = MILPSets.create(
            user_finances,
            parameters.max_months_in_payment_horizon,
            parameters.starting_month,
        )
        m.instruments = sets.instruments
        m.months = sets.payment_horizons_as_set
        m.loans = sets.loans
        m.investments = sets.investments

        parameters = MILPParameters(user_finances, sets)

        variables = MILPVariables.create(user_finances, sets)
        m.balances = variables.balances
        m.allocations = variables.allocations
        m.paid_off_indicators = variables.not_paid_off_indicators
        m.debt_free_indicators = variables.in_debt_indicators

        constraints = MILPConstraints.create(sets, parameters, variables)
        m.c1 = constraints.define_loan_paid_off_indicator
        m.c2 = constraints.allocate_minimum_payments
        m.c3 = constraints.define_account_balance
        m.c4 = constraints.total_payments_limit
        m.c5 = constraints.loans_are_non_positive
        m.c6 = constraints.pay_off_loans_by_end_date
        m.c7 = constraints.limit_total_risk
        m.c8 = constraints.define_in_debt_indicator
        m.c9 = constraints.limit_investment_risk

        objective = MILPObjective.create(sets, parameters, variables)
        m.obj = objective.obj

        return MILP(
            user_finances=user_finances,
            pyomodel=m,
            sets=sets,
            parameters=parameters,
            variables=variables,
            constraints=constraints,
            objective=objective,
        )

    def _is_valid_solution(self, results) -> bool:
        return (results.solver.status == pe.SolverStatus.ok) and (
            results.solver.termination_condition == pe.TerminationCondition.optimal
        )

    def _make_monthly_payments(self) -> List[Dict[str, float]]:
        # for t in sorted(self.sets.payment_horizons_as_set):
        #     print(t)
        #     print(pe.value(self.variables.get_allocation("LOC 2", t)))
        #     print(pe.value(self.variables.get_balance("LOC 2", t)))

        return [
            {
                i.name: pe.value(self.variables.get_allocation(i.name, t))
                for i in self.user_finances.portfolio.instruments.values()
            }
            for t in sorted(self.sets.payment_horizons_as_set)
            for _ in range(self.sets.get_num_months_in_horizon(t))
        ]

    def solve(self):
        results = pe.SolverFactory("cbc").solve(self.pyomodel, tee=True)
        if not self._is_valid_solution(results):
            print("It is not a valid solution")
            print(results.solver.status)
            print(results.solver.termination_condition)
            return None
        monthly_payments = self._make_monthly_payments()

        return _make_solution(
            self.user_finances.portfolio,
            monthly_payments,
            self.user_finances.financial_profile.monthly_allowance,
        )


class MILPStrategy(AllocationStrategy):
    def create_solution(
        self, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> FinancialPlan:
        milp = MILP.create(user_finances=user_finances, parameters=parameters)
        new_solution = milp.solve()
        return new_solution
