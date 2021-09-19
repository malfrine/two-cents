import logging
from dataclasses import dataclass
from typing import List, Dict, Optional

from pyomo import environ as pe
from pyomo.core import ConcreteModel

from pennies.model.parameters import Parameters
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.milp.constraints import MILPConstraints
from pennies.strategies.milp.objective import MILPObjective
from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables


@dataclass
class MILP:

    user_finances: UserPersonalFinances
    problem_parameters: Parameters
    pyomodel: ConcreteModel
    sets: MILPSets
    milp_parameters: MILPParameters
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
            parameters.max_months_in_retirement_period,
            parameters.starting_month,
        )

        milp_parameters = MILPParameters(user_finances, sets)

        variables = MILPVariables.create(user_finances, sets)
        m.balances = variables.balances
        m.allocations = variables.allocations
        m.goal_allocations = variables.goal_allocations
        m.paid_off_indicators = variables.not_paid_off_indicators
        m.investment_risk_violations = variables.investment_risk_violations
        m.total_risk_violations = variables.total_risk_violations
        m.loan_due_date_violations = variables.loan_due_date_violations
        m.taxable_monthly_incomes = variables.taxable_monthly_incomes
        m.taxes_accrued_in_brackets = variables.taxes_accrued_in_brackets
        m.withdrawals = variables.withdrawals
        m.retirement_spending_violations = variables.retirement_spending_violations
        m.taxable_monthly_incomes = variables.taxable_monthly_incomes
        m.rrsp_deduction_limits = variables.rrsp_deduction_limits
        m.tfsa_contribution_limits = variables.tfsa_contribution_limits
        m.savings_goal_violations = variables.savings_goal_violations
        m.purchase_goal_violations = variables.purchase_goal_violations
        m.min_payment_violations = variables.min_payment_violations
        m.taxable_incomes_in_brackets = variables.taxable_incomes_in_brackets
        m.taxable_incomes_indicator = variables.taxable_incomes_indicator

        constraints = MILPConstraints.create(sets, milp_parameters, variables)
        m.c1 = constraints.define_loan_paid_off_indicator
        m.c2 = constraints.allocate_minimum_payments
        m.c3 = constraints.define_account_balance
        m.c4 = constraints.total_payments_limit
        m.c5 = constraints.loans_are_non_positive
        m.c6 = constraints.pay_off_loans_by_end_date
        # m.c7 = constraints.limit_total_risk
        m.c9 = constraints.limit_investment_risk
        m.c12 = constraints.define_taxes_accrued_in_bracket
        m.c13 = constraints.satisfy_retirement_spending_requirement
        m.c14 = constraints.zero_allocations_for_guaranteed_investments
        m.c15 = constraints.define_taxable_monthly_income
        m.c16 = constraints.define_rrsp_deduction_limits
        m.c17 = constraints.set_minimum_rrif_withdrawals
        m.c18 = constraints.define_tfsa_deduction_limits
        m.c19 = constraints.set_withdrawal_limits
        m.c23 = constraints.same_mortgage_payments
        m.c24 = constraints.penalize_purchase_goal_violations
        m.c25 = constraints.penalize_savings_goal_violations
        m.c26 = constraints.bracket_taxable_income_upper_bound1
        m.c27 = constraints.bracket_taxable_income_upper_bound2
        m.c28 = constraints.bracket_taxable_income_lower_bound1
        m.c29 = constraints.bracket_taxable_income_lower_bound2
        m.c30 = constraints.income_surplus_upper_bound
        m.c31 = constraints.bracket_band_upper_bound
        # m.c32 = constraints.set_annual_rrsp_allocation_limit # TODO: some bug in rrsp limits

        objective = MILPObjective.create(sets, milp_parameters, variables,)
        m.obj = objective.obj

        return MILP(
            problem_parameters=parameters,
            user_finances=user_finances,
            pyomodel=m,
            sets=sets,
            milp_parameters=milp_parameters,
            variables=variables,
            constraints=constraints,
            objective=objective,
        )

    def _is_valid_solution(self, results) -> bool:
        status = results.solver.status
        termination_condition = results.solver.termination_condition

        is_aborted = status == pe.SolverStatus.aborted
        is_okay = status == pe.SolverStatus.ok
        is_optimal = termination_condition == pe.TerminationCondition.optimal

        return (is_optimal and is_okay) or is_aborted

    def _make_monthly_payments(self) -> List[Dict[str, float]]:
        def get_allocation(i_, t_):
            return pe.value(self.variables.get_allocation(i_, t_))

        return [
            {i: get_allocation(i, t) for i in self.sets.instruments}
            for t in list(sorted(self.sets.all_decision_periods_as_set))
            for _ in range(self.sets.get_num_months_in_decision_period(t))
        ]

    def solve(self) -> Optional["MILP"]:
        solver = pe.SolverFactory("cbc")
        solver.options["ratio"] = self.problem_parameters.optimality_gap
        solver.options["seconds"] = self.problem_parameters.max_milp_seconds
        solver.options["maxNodes"] = self.problem_parameters.max_milp_nodes
        is_log_milp = self.problem_parameters.is_log_milp
        results = solver.solve(self.pyomodel, tee=is_log_milp)
        if not self._is_valid_solution(results):
            logging.error(
                f"Did not get a valid solution; status: {results.solver.status};"
                f" termination condition: {results.solver.termination_condition}"
            )
            return self
        return self
