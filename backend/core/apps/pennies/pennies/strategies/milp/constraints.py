import itertools
from dataclasses import dataclass

import pyomo.environ as pe

from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables


@dataclass
class _ConstraintMaker:

    sets: MILPSets
    pars: MILPParameters
    vars: MILPVariables

    def make_define_loan_paid_off_indicator(self) -> pe.Constraint:
        def rule(_, l, t):
            return self.vars.get_balance(l, t) >= (
                self.pars.get_loan_upper_bound(l) * (self.vars.get_is_paid_off(l, t))
            )

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.months), rule=rule
        )

    def make_allocate_minimum_payments(self) -> pe.Constraint:
        def rule(_, l, t):
            if t >= self.pars.get_final_month(l):
                return pe.Constraint.Skip
            else:
                return self.pars.get_minimum_monthly_payment(l) <= (
                    self.vars.get_allocation(l, t)
                    + (
                        self.pars.get_monthly_allowance()
                        * (1 - self.vars.get_is_paid_off(l, t))
                    )
                )

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.months), rule=rule
        )

    def make_define_account_balance(self) -> pe.Constraint:
        def rule(_, i, t):
            if t == 0:
                return self.vars.get_balance(i, t) == self.pars.get_starting_balance(i)
            elif t >= self.pars.get_final_month(i):
                return self.vars.get_balance(i, t) == self.vars.get_balance(i, t - 1)
            else:
                return self.vars.get_balance(i, t) == (
                    (
                        self.vars.get_balance(i, t - 1)
                        * (1 + self.pars.get_monthly_interest_rate(i))
                    )
                    + self.vars.get_allocation(i, t - 1)
                )

        return pe.Constraint(
            itertools.product(self.sets.instruments, self.sets.months), rule=rule
        )

    def make_total_payments_limit(self) -> pe.Constraint:
        def rule(_, t):
            return (
                sum(self.vars.get_allocation(i, t) for i in self.sets.instruments)
                <= self.pars.get_monthly_allowance()
            )

        return pe.Constraint(self.sets.months, rule=rule)

    def make_loans_are_non_positive(self) -> pe.Constraint:
        def rule(_, l, t):
            return self.vars.get_balance(l, t) <= 0

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.months), rule=rule
        )

    def make_pay_off_loans_by_end_date(self) -> pe.Constraint:
        def rule(_, l, t):
            if t < self.pars.get_final_month(l) - 1:
                return pe.Constraint.Skip
            else:
                return self.vars.get_balance(l, t) == 0

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.months), rule=rule
        )


@dataclass
class MILPConstraints:

    define_loan_paid_off_indicator: pe.Constraint
    allocate_minimum_payments: pe.Constraint
    define_account_balance: pe.Constraint
    total_payments_limit: pe.Constraint
    loans_are_non_positive: pe.Constraint
    pay_off_loans_by_end_date: pe.Constraint

    @classmethod
    def create(
        cls, sets: MILPSets, pars: MILPParameters, vars_: MILPVariables
    ) -> "MILPConstraints":
        cm = _ConstraintMaker(sets=sets, pars=pars, vars=vars_)
        return MILPConstraints(
            define_loan_paid_off_indicator=cm.make_define_loan_paid_off_indicator(),
            allocate_minimum_payments=cm.make_allocate_minimum_payments(),
            define_account_balance=cm.make_define_account_balance(),
            total_payments_limit=cm.make_total_payments_limit(),
            loans_are_non_positive=cm.make_loans_are_non_positive(),
            pay_off_loans_by_end_date=cm.make_pay_off_loans_by_end_date(),
        )
