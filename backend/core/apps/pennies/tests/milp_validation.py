import logging
import math
import sys
from typing import Tuple, Dict

import pyomo.environ as pe

from pennies.model.factories.financial_plan import FinancialPlanFactory
from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.instrument import Instrument
from pennies.model.request import PenniesRequest
from pennies.model.solution import FinancialPlan, MonthlySolution
from pennies.strategies.milp.milp import MILP
from pennies.strategies.milp.milp_solution import MILPSolution
from pennies.utilities.finance import calculate_instrument_balance

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def _solve(request: PenniesRequest) -> Tuple[MILPSolution, FinancialPlan]:
    model_input = ProblemInputFactory.from_request(request)
    user_finances = model_input.user_finances
    parameters = model_input.parameters
    milp = MILP.create(user_finances=user_finances, parameters=parameters).solve()
    solution = MILPSolution(milp=milp)
    plan = FinancialPlanFactory.create(
        solution.get_monthly_payments(),
        user_finances,
        parameters,
        solution.get_monthly_withdrawals(),
    )
    return solution, plan


def print_tax_vars(
    milp_solution: MILPSolution,
    actual_ms: MonthlySolution,
    milp_ms: MonthlySolution,
    t: int,
    month: int,
):
    actual_tax = actual_ms.taxes_paid
    print(f"Actual Tax: {actual_tax}")
    print(f"Decision Period: {t}")
    print(f"Actual Gross Income: {actual_ms.gross_income}")
    print(f"MILP Gross Income: {milp_ms.gross_income}")
    print(f"Actual Taxable Income: {actual_ms.taxable_income}")
    print(f"MILP Taxable Income: {milp_ms.taxable_income}")

    # TODO: print tax exempt allocations and taxable income

    print(f"\tmilp taxes paid: {milp_ms.taxes_paid}")
    print(f"\tactual taxes paid: {actual_ms.taxes_paid}")
    sets = milp_solution.sets
    pars = milp_solution.pars
    vars_ = milp_solution.vars

    for e, b in sets.taxing_entities_and_brackets:
        t = sets.decision_periods.get_corresponding_period(month).index

        # constants
        rate = pars.get_bracket_marginal_tax_rate(e, b)
        cumulative_income = pars.get_bracket_cumulative_income(e, b)
        marginal_income = pars.get_bracket_marginal_income(e, b)
        prev_cumulative_income = pars.get_previous_bracket_cumulative_income(e, b)

        # actual
        actual_taxable_income = actual_ms.taxable_income
        actual_income_overflow = actual_taxable_income - prev_cumulative_income
        actual_taxable_income_in_bracket = max(
            0, min(marginal_income, actual_income_overflow)
        )
        actual_accrued_tax = actual_taxable_income_in_bracket * rate
        actual_indicator = int(actual_income_overflow >= marginal_income)

        # model
        model_accrued_taxes = pe.value(vars_.get_taxes_accrued_in_bracket(t, e, b))
        model_indicator = pe.value(
            vars_.get_income_surplus_greater_than_bracket_band(t, e, b)
        )
        model_monthly_taxable_income = pe.value(vars_.get_taxable_monthly_income(t))
        model_income_overflow = model_monthly_taxable_income - prev_cumulative_income
        model_taxable_income_in_bracket = pe.value(
            vars_.get_taxable_income_in_bracket(t, e, b)
        )

        remaining_taxes_to_be_paid = actual_accrued_tax - model_accrued_taxes
        if not math.isclose(actual_accrued_tax, model_accrued_taxes, abs_tol=1):
            print("\tlogging details of error:")
            print(f"\t\t{month=}, {t=}, {e=}, {b}, {actual_taxable_income=} ")
            print(
                f"\t\t{prev_cumulative_income=}, {cumulative_income=}, {marginal_income=}, {rate=}"
            )
            print(
                f"\t\t{model_taxable_income_in_bracket=}, {model_monthly_taxable_income=}, "
                f"{model_income_overflow=}, {model_accrued_taxes=}, {model_indicator=}"
            )
            print(
                f"\t\t{actual_taxable_income_in_bracket=}, {actual_taxable_income=}, "
                f"{actual_income_overflow=}, {actual_accrued_tax=}, {actual_indicator=}"
            )
            print(f"\t\t{remaining_taxes_to_be_paid=}")


def print_balance_history_of_instrument(
    instrument: Instrument,
    milp_monthly_solutions: Dict[int, MonthlySolution],
    actual_plan: FinancialPlan,
):
    def print_cur_month(ms: MonthlySolution):
        i = ms.portfolio.instruments.get(instrument.id_, None)
        balance = i.current_balance if i is not None else 0
        allocation = ms.allocation.payments.get(instrument.id_, 0)
        withdrawal = ms.withdrawals.get(instrument.id_, 0)
        print(f"\tCurrent Balance: {balance}")
        print(f"\tAllocation: {allocation}")
        print(f"\tWithdrawal: {withdrawal}")

    print(f"Instrument Name: {instrument.name}")
    for actual_ms in actual_plan.monthly_solutions:
        print(f"Month: {actual_ms.month}")
        print("Actual:")
        print_cur_month(actual_ms)
        milp_ms = milp_monthly_solutions.get(actual_ms.month, None)
        if milp_ms is not None:
            print("MILP:")
            print_cur_month(milp_ms)
        instrument = actual_ms.portfolio.instruments.get(instrument.id_, None)
        balance = instrument.current_balance if instrument is not None else 0
        actual_allocation = actual_ms.allocation.payments.get(instrument.id_, 0)
        next_balance = calculate_instrument_balance(
            balance,
            1,
            instrument.monthly_interest_rate(actual_ms.month),
            0,
            actual_allocation,
        )
        print(f"\tnext balance: {next_balance}")


def assert_correct_milp_calculations(request: PenniesRequest):
    milp_solution, actual_plan = _solve(request)
    milp_monthly_solutions = milp_solution.get_milp_monthly_solutions()
    for month, milp_ms in milp_monthly_solutions.items():
        actual_ms = actual_plan.monthly_solutions[month]
        decision_period_index = milp_solution.sets.decision_periods.get_corresponding_period(
            month
        ).index
        print(f"month: {month}")
        print("milp:")
        print(f"\tmilp taxes paid: {milp_ms.taxes_paid}")
        print(f"\tactual taxes paid: {actual_ms.taxes_paid}")
        if not math.isclose(
            milp_ms.taxes_paid, actual_ms.taxes_paid, rel_tol=0.01, abs_tol=0.1
        ):
            # get more info
            print_tax_vars(
                milp_solution, actual_ms, milp_ms, decision_period_index, month
            )
            logging.warning("Taxes are not equal")
            # assert False
        print("\tbalances:")
        for id_, instrument in milp_ms.portfolio.instruments.items():
            milp_balance = instrument.current_balance
            actual_instrument = actual_ms.portfolio.instruments.get(id_, None)
            if actual_instrument is None:
                actual_balance = 0
            else:
                actual_balance = actual_instrument.current_balance
            print(f"\t\tmilp: {instrument.name}: {milp_balance}")
            print(f"\t\tactual {instrument.name}: {actual_balance}")
            is_close = math.isclose(
                actual_balance, milp_balance, rel_tol=0.01, abs_tol=0.1
            )
            if not is_close:
                print_balance_history_of_instrument(
                    instrument, milp_monthly_solutions, actual_plan
                )
                assert (
                    False
                ), f"balance of {instrument.name} has diverged {actual_balance} vs {milp_balance} at {month}"
