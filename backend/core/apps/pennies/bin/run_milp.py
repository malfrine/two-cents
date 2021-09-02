import logging
import math
from pathlib import Path

import pyomo.environ as pe

from pennies.dao.json_dao import JsonDao
from pennies.model.factories.financial_plan import FinancialPlanFactory
from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.strategies.milp.milp import MILP
from pennies.strategies.milp.milp_solution import MILPSolution
from pennies.utilities.visualization import visualize_solution

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def get_request():
    # request = simple_request()
    json_dao = JsonDao(data_dir=Path("tests", "data"))
    request = json_dao.read_request("fail12.json")
    return request


def main():
    request = get_request()
    model_input = ProblemInputFactory.from_request(request)
    user_finances = model_input.user_finances
    parameters = model_input.parameters
    milp = MILP.create(user_finances=user_finances, parameters=parameters).solve()
    if milp is None:
        assert False
    solution = MILPSolution(milp=milp)
    for dp in solution.sets.decision_periods.data:
        t = dp.index
        months = dp.months
        print(f"{t=}, {months=}")
        for i in solution.sets.instruments:
            balance = pe.value(solution.vars.get_balance(i, t))
            allocation = pe.value(solution.vars.get_allocation(i, t))
            if solution.pars.get_is_non_guaranteed_investment(i):
                withdrawal = pe.value(solution.vars.get_withdrawal(i, t))
            else:
                withdrawal = 0
            name = user_finances.portfolio.get_instrument(i).name
            print(f"\t{name=}, {allocation=}, {balance=}, {withdrawal=}")
        gross_monthly_income = pe.value(
            solution.attribute_utility.get_gross_monthly_income(t)
        )
        post_tax_monthly_income = pe.value(
            solution.attribute_utility.get_post_tax_monthly_income(t)
        )
        total_withdrawals = pe.value(solution.attribute_utility.get_all_withdrawals(t))
        total_taxes = pe.value(solution.attribute_utility.get_total_tax(t))
        print(
            f"\t{gross_monthly_income=}, {post_tax_monthly_income=}, {total_withdrawals=}, {total_taxes=}"
        )

        for e, b in solution.sets.taxing_entities_and_brackets:
            taxes_accrued = pe.value(
                solution.vars.get_taxes_accrued_in_bracket(t, e, b)
            )
            print(f"\t\t{taxes_accrued=}, {e=}, {b=}")

    for year in solution.sets.years:
        rrsp_limit = pe.value(solution.vars.get_rrsp_deduction_limit(year))
        tfsa_limit = pe.value(solution.vars.get_tfsa_contribution_limit(year))
        print(f"{year=}, {rrsp_limit=}, {tfsa_limit=}")

    plan = FinancialPlanFactory.create(
        solution.get_monthly_payments(),
        user_finances,
        parameters,
        solution.get_monthly_withdrawals(),
    )
    visualize_solution(plan, suffix="milp-test")
    vars_ = solution.vars
    sets = solution.sets
    pars = solution.pars
    for t in solution.milp.sets.retirement_periods_as_set:
        retirement_violation = pe.value(
            milp.variables.get_retirement_spending_violation(t)
        )
        if retirement_violation > 0:
            all_withdrawals = pe.value(
                sum(vars_.get_withdrawal(i, t) for i in sets.investments)
            )
            spending = pe.value(pars.get_minimum_monthly_withdrawals(t))
            violation = pe.value(vars_.get_retirement_spending_violation(t))
            logging.info(f"{retirement_violation} retirement violation at {t}")
            logging.info(f"\t{violation=}, {spending=} {all_withdrawals=}")
    for t in solution.milp.sets.working_periods_as_set:
        total_risk_violation = pe.value(milp.variables.get_total_risk_violation(t))
        investment_risk_violation = pe.value(
            milp.variables.get_investment_risk_violation(t)
        )
        if total_risk_violation >= 1:
            print(f"{total_risk_violation=} at {t}")

        if investment_risk_violation >= 1:
            print(f"{investment_risk_violation=} at {t}")
    for t in solution.milp.sets.all_decision_periods_as_set:
        for g in solution.milp.sets.goals:
            try:
                goal_violation = pe.value(
                    milp.variables.get_savings_goal_violation(g, t)
                )
            except KeyError:
                continue
            if goal_violation > 1:
                logging.info(f"{goal_violation=} at {t} for goal {g}")
    milp_monthly_solutions = solution.get_milp_monthly_solutions()
    for month, milp_ms in milp_monthly_solutions.items():
        actual_ms = plan.monthly_solutions[month]
        if not math.isclose(milp_ms.taxes_paid, actual_ms.taxes_paid, abs_tol=1):
            print(f"\tmilp taxes paid: {milp_ms.taxes_paid}")
            print(f"\tactual taxes paid: {actual_ms.taxes_paid}")
            for e, b in sets.taxing_entities_and_brackets:
                t = sets.decision_periods.get_corresponding_period(month).index

                # constants
                rate = pars.get_bracket_marginal_tax_rate(e, b)
                cumulative_income = pars.get_bracket_cumulative_income(e, b)
                marginal_income = pars.get_bracket_marginal_income(e, b)
                prev_cumulative_income = pars.get_previous_bracket_cumulative_income(
                    e, b
                )

                # actual
                actual_taxable_income = actual_ms.taxable_income
                actual_income_overflow = actual_taxable_income - prev_cumulative_income
                actual_taxable_income_in_bracket = max(
                    0, min(marginal_income, actual_income_overflow)
                )
                actual_accrued_tax = actual_taxable_income_in_bracket * rate
                actual_indicator = int(actual_income_overflow >= marginal_income)

                # model
                taxable_withdrawals = pe.value(
                    solution.attribute_utility.get_total_taxable_withdrawals(t)
                )
                rrsp_allocations = pe.value(
                    solution.attribute_utility.get_rrsp_allocations(t)
                )
                taxable_income = pe.value(solution.vars.get_taxable_monthly_income(t))
                before_tax_monthly_income = solution.pars.get_before_tax_monthly_income(
                    t
                )
                model_accrued_taxes = pe.value(
                    vars_.get_taxes_accrued_in_bracket(t, e, b)
                )

                model_indicator = pe.value(
                    vars_.get_income_surplus_greater_than_bracket_band(t, e, b)
                )
                model_monthly_taxable_income = pe.value(
                    vars_.get_taxable_monthly_income(t)
                )
                model_income_overflow = pe.value(
                    solution.attribute_utility.get_income_surplus_over_bracket(t, e, b)
                )
                model_taxable_income_in_bracket = pe.value(
                    vars_.get_taxable_income_in_bracket(t, e, b)
                )

                remaining_taxes_to_be_paid = actual_accrued_tax - model_accrued_taxes
                if not math.isclose(actual_accrued_tax, model_accrued_taxes, abs_tol=1):
                    print(
                        f"\t{taxable_withdrawals=}, {rrsp_allocations=}, {taxable_income=}, "
                        f"{before_tax_monthly_income=}"
                    )

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
    for g in sets.purchase_goals:
        investments = sets.get_allowed_investments_for_goal(g)
        m = pars.get_goal_due_month(g)
        t = sets.decision_periods.get_corresponding_period_or_closest(m).index
        model_withdrawal = pe.value(
            sum(vars_.get_withdrawal(i, t) for i in investments)
        )
        goal_violation = pe.value(vars_.get_purchase_goal_violation(g))
        expected_withdrawal = pars.get_goal_amount(g, t)
        goal_name = model_input.user_finances.goals.get(g).name
        if goal_violation > 0:
            print(f"\tfailed to meet purchase goal {goal_name=}, {t=}, {m=}")
            print(f"\t{model_withdrawal=}, {expected_withdrawal=}")
    for g, t in sets.savings_goals_and_decision_periods:
        investments = sets.get_allowed_investments_for_goal(g)
        model_current_balance = pe.value(
            sum(vars_.get_balance(i, t) for i in investments)
        )
        goal_violation = pe.value(vars_.get_savings_goal_violation(g, t))
        expected_balance = pars.get_goal_amount(g, t)
        goal_name = model_input.user_finances.goals.get(g).name

        if goal_violation > 0:
            print(f"\tfailed to meet savings goal {goal_name=}, {t=}")
            print(f"\t{model_current_balance=}, {expected_balance=}")

    solution.print_objective_components_breakdown()


if __name__ == "__main__":
    main()
