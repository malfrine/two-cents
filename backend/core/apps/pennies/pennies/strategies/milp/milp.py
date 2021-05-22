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
            parameters.starting_month,
        )

        milp_parameters = MILPParameters(user_finances, sets)

        variables = MILPVariables.create(user_finances, sets)
        m.balances = variables.balances
        m.allocations = variables.allocations
        m.paid_off_indicators = variables.not_paid_off_indicators
        m.debt_free_indicators = variables.in_debt_indicators
        m.investment_risk_violations = variables.investment_risk_violations
        m.total_risk_violations = variables.total_risk_violations
        m.allocation_slacks = variables.allocation_slacks
        m.loan_due_date_violations = variables.loan_due_date_violations
        m.taxable_monthly_incomes = variables.taxable_monthly_incomes
        m.pos_overflow_in_brackets = variables.pos_overflow_in_brackets
        m.remaining_marginal_income_in_brackets = (
            variables.remaining_marginal_income_in_brackets
        )
        m.taxes_accrued_in_brackets = variables.taxes_accrued_in_brackets
        m.withdrawals = variables.withdrawals
        m.retirement_spending_violations = variables.retirement_spending_violations
        m.taxable_monthly_incomes = variables.taxable_monthly_incomes
        m.rrsp_deduction_limits = variables.rrsp_deduction_limits
        m.tfsa_contribution_limits = variables.tfsa_contribution_limits
        m.pos_withdrawal_differences = variables.pos_withdrawal_differences
        m.neg_withdrawal_differences = variables.neg_withdrawal_differences
        m.withdrawal_fluctuation_violation = variables.withdrawal_fluctuation_violation
        m.max_monthly_payment_violations = variables.max_monthly_payment_violations
        m.savings_goal_violations = variables.savings_goal_violations
        m.purchase_goal_violations = variables.purchase_goal_violations

        cls._fix_final_allocation_to_zero(sets, variables)

        constraints = MILPConstraints.create(sets, milp_parameters, variables)
        m.c1 = constraints.define_loan_paid_off_indicator
        m.c2 = constraints.allocate_minimum_payments
        m.c3 = constraints.define_account_balance
        m.c4 = constraints.total_payments_limit
        m.c5 = constraints.loans_are_non_positive
        m.c6 = constraints.pay_off_loans_by_end_date
        m.c7 = constraints.limit_total_risk
        m.c8 = constraints.define_in_debt_indicator
        m.c9 = constraints.limit_investment_risk
        m.c10 = constraints.define_taxable_income_in_bracket
        m.c11 = constraints.limit_remaining_marginal_income_in_bracket
        m.c12 = constraints.define_taxes_accrued_in_bracket
        m.c13 = constraints.satisfy_retirement_spending_requirement
        m.c14 = constraints.zero_allocations_for_guaranteed_investments
        m.c15 = constraints.define_taxable_monthly_income
        m.c16 = constraints.define_rrsp_deduction_limits
        m.c17 = constraints.set_minimum_rrif_withdrawals
        m.c18 = constraints.define_tfsa_deduction_limits
        m.c19 = constraints.set_withdrawal_limits
        # m.c20 = constraints.define_surplus_withdrawal_differences
        # m.c21 = constraints.limit_surplus_withdrawal_fluctuations
        m.c22 = constraints.limit_monthly_payment
        m.c23 = constraints.same_mortgage_payments
        m.c24 = constraints.penalize_purchase_goal_violations
        m.c25 = constraints.penalize_savings_goal_violations

        objective = MILPObjective.create(sets, milp_parameters, variables, discount_factor=parameters.discount_factor)
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

    #
    @classmethod
    def _fix_final_allocation_to_zero(cls, sets: MILPSets, variables: MILPVariables):
        final_decision_period_index = max(sets.all_decision_periods_as_set)
        for i in sets.instruments:
            variables.get_allocation(i, final_decision_period_index).fix(0)
        for i in sets.investments_and_guaranteed_investments:
            variables.get_withdrawal(i, final_decision_period_index).fix(0)

    def _is_valid_solution(self, results) -> bool:
        return (results.solver.status == pe.SolverStatus.ok) and (
            results.solver.termination_condition == pe.TerminationCondition.optimal
        )

    def _make_monthly_payments(self) -> List[Dict[str, float]]:
        def get_allocation(i_, t_):
            return pe.value(self.variables.get_allocation(i_, t_))

        return [
            {i: get_allocation(i, t) for i in self.sets.instruments}
            for t in list(sorted(self.sets.all_decision_periods_as_set))
            for _ in range(self.sets.get_num_months_in_decision_period(t))
        ]

    def _make_monthly_withdrawals(self) -> List[Dict[str, float]]:
        def get_withdrawal(i_, t_):
            if t_ < min(self.sets.retirement_periods_as_set):
                return 0
            return pe.value(self.variables.get_withdrawal(i_, t_))

        return [
            {
                i: get_withdrawal(i, t)
                for i in self.sets.investments_and_guaranteed_investments
            }
            for t in list(sorted(self.sets.all_decision_periods_as_set))
            for _ in range(self.sets.get_num_months_in_decision_period(t))
        ]

    def solve(self) -> Optional["MILP"]:
        results = pe.SolverFactory("cbc").solve(self.pyomodel)
        if not self._is_valid_solution(results):
            print("It is not a valid solution")
            print(results.solver.status)
            print(results.solver.termination_condition)
            return None
        return self
