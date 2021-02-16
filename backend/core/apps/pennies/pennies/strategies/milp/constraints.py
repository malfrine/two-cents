import itertools
from dataclasses import dataclass
from typing import Optional

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
            return (self.vars.get_balance(l, t)) >= (
                (self.pars.get_loan_upper_bound(l)) * (self.vars.get_is_unpaid(l, t))
            )

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.payment_horizons_as_set),
            rule=rule,
        )

    def make_allocate_minimum_payments(self) -> pe.Constraint:
        def rule(_, l, t):
            final_payment_order = self.pars.get_last_payment_horizon_order()
            allocation_slack = (
                self.pars.get_monthly_allowance()
                * (1 - self.vars.get_is_unpaid(l, min(t + 1, final_payment_order)))
            )
            loan_allocation = self.vars.get_allocation(l, t)
            if self.pars.get_is_revolving_loan(l):
                # mmp = -self.vars.get_balance(l, t) * self.pars.get_average_interest_rate(l, t) # TODO: make faster
                mmp = -self.pars.get_starting_balance(l) * self.pars.get_average_interest_rate(l, t)
                return mmp <= loan_allocation + allocation_slack
            else:
                return self.pars.get_minimum_monthly_payment(l, t) <= loan_allocation + allocation_slack

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.payment_horizons_as_set),
            rule=rule,
        )

    def make_define_account_balance(self) -> pe.Constraint:
        def rule(_, i, t):
            if t == 0:
                return self.vars.get_balance(i, t) == self.pars.get_starting_balance(i)
            elif t >= self.pars.get_instrument_final_payment_horizon(i).order:
                return self.vars.get_balance(i, t) == self.vars.get_balance(i, t - 1)
            else:
                r = 1 + self.pars.get_average_interest_rate(i, t - 1)
                n = self.sets.get_num_months_in_horizon(t)
                return self.vars.get_balance(i, t) == (
                    (self.vars.get_balance(i, t - 1) * r ** n)
                    + self.vars.get_allocation(i, t - 1)
                    * (r ** n - 1)
                    / self.pars.get_average_interest_rate(i, t - 1)
                )

        return pe.Constraint(
            itertools.product(self.sets.instruments, self.sets.payment_horizons_as_set),
            rule=rule,
        )

    def make_total_payments_limit(self) -> pe.Constraint:
        def rule(_, t):
            return (
                sum(self.vars.get_allocation(i, t) for i in self.sets.instruments)
                <= self.pars.get_monthly_allowance()
            )

        return pe.Constraint(self.sets.payment_horizons_as_set, rule=rule)

    def make_loans_are_non_positive(self) -> pe.Constraint:
        def rule(_, l, t):
            return self.vars.get_balance(l, t) <= 0

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.payment_horizons_as_set),
            rule=rule,
        )

    def make_pay_off_loans_by_end_date(self) -> pe.Constraint:
        def rule(_, l, t):
            if t < self.pars.get_instrument_final_payment_horizon(l).order - 1:
                return pe.Constraint.Skip
            else:
                return self.vars.get_balance(l, t) == 0

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.payment_horizons_as_set),
            rule=rule,
        )

    def make_define_in_debt_indicator(self) -> pe.Constraint:
        def rule(_, t):
            count_of_unpaid_loans = sum(
                self.vars.get_is_unpaid(l, t) for l in self.sets.loans
            )
            total_loans = len(self.sets.loans)
            return self.vars.get_is_in_debt(t) >= count_of_unpaid_loans / total_loans

        if not self.pars.has_loans():
            return pe.Constraint.NoConstraint
        else:
            return pe.Constraint(
                itertools.product(self.sets.payment_horizons_as_set), rule=rule
            )

    def _get_allocation_volatility(self, t):
        return sum(
            self.vars.get_allocation(i, t) * self.pars.get_volatility(i)
            for i in self.sets.investments
        )

    def make_limit_total_risk(self) -> pe.Constraint:
        def rule(_, t):

            final_payment_order = self.pars.get_last_payment_horizon_order()

            if self.pars.has_loans():
                min_volatility = self.pars.get_min_volatility() * (
                    1 - self.vars.get_is_in_debt(min(t + 1, final_payment_order))
                )
            else:
                min_volatility = self.pars.get_min_volatility()

            volatility_limit = min_volatility + self.pars.get_user_risk_profile_as_fraction() * (
                self.pars.get_max_volatility() - min_volatility
            )
            normalized_allocation_volatility = self._get_allocation_volatility(t)
            return (
                normalized_allocation_volatility
                <= volatility_limit * self.pars.get_monthly_allowance()
            )

        if self.pars.has_investments() and self.pars.has_loans():
            return pe.Constraint(
                itertools.product(self.sets.payment_horizons_as_set), rule=rule
            )
        else:
            return pe.Constraint.NoConstraint

    def make_limit_investment_risk(self) -> pe.Constraint:
        def rule(_, t):
            volatility_limit = (
                self.pars.get_min_volatility()
                + self.pars.get_user_risk_profile_as_fraction()
                * (self.pars.get_max_volatility() - self.pars.get_min_volatility())
            )

            total_investment_allocations = sum(
                self.vars.get_allocation(i, t) for i in self.sets.investments
            )

            allocation_volatility = sum(
                self.vars.get_allocation(i, t) * self.pars.get_volatility(i)
                for i in self.sets.investments
            )
            return (
                allocation_volatility <= volatility_limit * total_investment_allocations
            )

        if self.pars.has_investments():
            return pe.Constraint(
                itertools.product(self.sets.payment_horizons_as_set), rule=rule
            )
        else:
            return pe.Constraint.NoConstraint


@dataclass
class MILPConstraints:

    define_loan_paid_off_indicator: pe.Constraint
    allocate_minimum_payments: pe.Constraint
    define_account_balance: pe.Constraint
    total_payments_limit: pe.Constraint
    loans_are_non_positive: pe.Constraint
    pay_off_loans_by_end_date: pe.Constraint
    define_in_debt_indicator: pe.Constraint
    limit_total_risk: pe.Constraint
    limit_investment_risk: pe.Constraint

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
            define_in_debt_indicator=cm.make_define_in_debt_indicator(),
            limit_total_risk=cm.make_limit_total_risk(),
            limit_investment_risk=cm.make_limit_investment_risk(),
        )
