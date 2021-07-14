import logging
import math
from typing import Tuple, Dict

from pennies.model.decision_periods import DecisionPeriodsManagerFactory
from pennies.model.factories.financial_plan import FinancialPlanFactory
from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.instrument import Instrument
from pennies.model.parameters import Parameters
from pennies.model.request import PenniesRequest
from pennies.model.solution import FinancialPlan, MonthlySolution
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.milp.milp import MILP
from pennies.strategies.milp.milp_solution import MILPSolution
from pennies.strategies.milp.strategy import MILPStrategy
from pennies.utilities.examples import simple_request


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
    logging.debug(f"Actual Tax: {actual_tax}")
    logging.debug(f"Decision Period: {t}")
    withdrawals = sum(
        milp_ms.withdrawals[i]
        for i in milp_solution.sets.investments_and_guaranteed_investments
    )
    gross_salary = milp_solution.pars.get_before_tax_monthly_income(t)
    logging.debug(f"\tGross Salary: {gross_salary}")
    logging.debug(f"\tWithdrawals: {withdrawals}")
    # TODO: print tax exempt allocations and taxable income

    for e, b in milp_solution.sets.taxing_entities_and_brackets:
        logging.debug(f"\tEntity: {e}, Bracket: {b}")
        pars = milp_solution.pars
        bracket_cumulative_income = pars.get_bracket_cumulative_income(e, b)
        bracket_marginal_income = pars.get_bracket_marginal_income(e, b)
        bracket_marginal_tax_rate = pars.get_bracket_marginal_tax_rate(e, b)
        logging.debug(
            f"\t\tMarginal Tax Rate: {bracket_marginal_tax_rate}, Marginal Income: {bracket_marginal_income}, "
            f"Cumulative Income: {bracket_cumulative_income}"
        )

        rem = milp_solution.get_remaining_marginal_income_in_bracket(t, e, b)
        overflow = milp_solution.get_positive_overflow_in_bracket(t, e, b)
        taxable_income_in_bracket_lb = bracket_marginal_income - rem
        logging.debug(f"\t\tRemaining Marginal Income in Bracket: {rem}")
        logging.debug(f"\t\tLB of Taxable Income in Bracket: {taxable_income_in_bracket_lb}")
        logging.debug(f"{overflow} - {rem} = ")


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
        logging.debug(f"\tCurrent Balance: {balance}")
        logging.debug(f"\tAllocation: {allocation}")
        logging.debug(f"\tWithdrawal: {withdrawal}")

    logging.debug(f"Instrument Name: {instrument.name}")
    for actual_ms in actual_plan.monthly_solutions:
        logging.debug(f"Month: {actual_ms.month}")
        logging.debug(f"Actual:")
        print_cur_month(actual_ms)
        milp_ms = milp_monthly_solutions.get(actual_ms.month, None)
        if milp_ms is not None:
            logging.debug(f"MILP:")
            print_cur_month(milp_ms)


def test_simple_request():
    request = simple_request()
    milp_solution, actual_plan = _solve(request)
    milp_monthly_solutions = milp_solution.get_milp_monthly_solutions()
    for month, milp_ms in milp_monthly_solutions.items():
        actual_ms = actual_plan.monthly_solutions[month]
        decision_period_index = (
            milp_solution.sets.decision_periods.get_corresponding_period(month).index
        )
        logging.debug(f"month: {month}")
        logging.debug(f"milp:")
        logging.debug(f"\tmilp taxes paid: {milp_ms.taxes_paid}")
        logging.debug(f"\tactual taxes paid: {actual_ms.taxes_paid}")
        if not math.isclose(milp_ms.taxes_paid, actual_ms.taxes_paid, abs_tol=5):
            # get more info
            print_tax_vars(milp_solution, actual_ms, milp_ms, decision_period_index)
            assert False
        logging.debug(f"\tbalances:")
        for id_, instrument in milp_ms.portfolio.instruments.items():
            milp_balance = instrument.current_balance
            actual_instrument = actual_ms.portfolio.instruments.get(id_, None)
            if actual_instrument is None:
                actual_balance = 0
            else:
                actual_balance = actual_instrument.current_balance
            logging.debug(f"\t\tmilp: {instrument.name}: {milp_balance}")
            logging.debug(f"\t\tactual {instrument.name}: {actual_balance}")
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
