import logging
import math
import sys
from typing import Tuple, Dict

from pennies.model.factories.financial_plan import FinancialPlanFactory
from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.instrument import Instrument
from pennies.model.request import PenniesRequest
from pennies.model.solution import FinancialPlan, MonthlySolution
from pennies.strategies.milp.milp import MILP
from pennies.strategies.milp.milp_solution import MILPSolution
from pennies.utilities.examples import simple_request

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def _solve(request: PenniesRequest) -> Tuple[MILPSolution, FinancialPlan]:
    model_input = ProblemInputFactory.from_request(request)
    user_finances = model_input.user_finances
    parameters = model_input.parameters
    milp = MILP.create(user_finances=user_finances, parameters=parameters).solve()
    if milp is None:
        assert False
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
):
    actual_tax = actual_ms.taxes_paid
    print(f"Actual Tax: {actual_tax}")
    print(f"Decision Period: {t}")
    print(f"Actual Gross Income: {actual_ms.gross_income}")
    print(f"MILP Gross Income: {milp_ms.gross_income}")
    print(f"Actual Taxable Income: {actual_ms.taxable_income}")
    print(f"MILP Taxable Income: {milp_ms.taxable_income}")

    # TODO: print tax exempt allocations and taxable income

    for e, b in milp_solution.sets.taxing_entities_and_brackets:
        print(f"\tEntity: {e}, Bracket: {b}")
        pars = milp_solution.pars
        bracket_cumulative_income = pars.get_bracket_cumulative_income(e, b)
        bracket_marginal_income = pars.get_bracket_marginal_income(e, b)
        bracket_marginal_tax_rate = pars.get_bracket_marginal_tax_rate(e, b)
        print(
            f"\t\tMarginal Tax Rate: {bracket_marginal_tax_rate}, "
            f"Marginal Income: {bracket_marginal_income}, "
            f"Cumulative Income: {bracket_cumulative_income}"
        )

        rem = milp_solution.get_remaining_marginal_income_in_bracket(t, e, b)
        overflow = milp_solution.get_positive_overflow_in_bracket(t, e, b)
        taxable_income_in_bracket_lb = bracket_marginal_income - rem
        print(f"\t\tRemaining Marginal Income in Bracket: {rem}")
        print(f"\t\tLB of Taxable Income in Bracket: {taxable_income_in_bracket_lb}")
        print(f"\t\t{overflow} - {rem} = {overflow - rem}")
        print(
            f"\t\tmilp taxes accrued in bracket: {milp_solution.get_taxes_accrued_in_bracket(t, e, b)}"
        )
        prev_cumulative_income = (
            pars.get_bracket_cumulative_income(e, b) if b > 0 else 0
        )
        actual_taxable_income_in_bracket = max(
            0, actual_ms.taxable_income - prev_cumulative_income
        )
        print(
            "\t\tactual taxes accrued in bracket:"
            f" {actual_taxable_income_in_bracket} * {bracket_marginal_tax_rate}"
            f" = {actual_taxable_income_in_bracket * bracket_marginal_tax_rate}"
        )


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


def test_simple_request():
    request = simple_request()
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
        if not math.isclose(milp_ms.taxes_paid, actual_ms.taxes_paid, abs_tol=5):
            # get more info
            print_tax_vars(milp_solution, actual_ms, milp_ms, decision_period_index)
            assert False
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
            if not math.isclose(actual_balance, milp_balance, abs_tol=5):
                print_balance_history_of_instrument(
                    instrument, milp_monthly_solutions, actual_plan
                )
                assert math.isclose(actual_balance, milp_balance, abs_tol=5)
    assert math.isclose(
        milp_solution.get_total_taxes_paid(),
        actual_plan.get_total_income_taxes_paid(),
        abs_tol=5,
    )
