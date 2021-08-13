from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.problem_input import ProblemInput
from pennies.plan_processing.plan import ProcessedFinancialPlan
from pennies.plan_processing.solution_processor import SolutionProcessor
from pennies.solver import solve
from pennies.strategies import StrategyName
from pennies.utilities.examples import simple_request
from pennies.utilities.visualization import visualize_solution


def main():
    import cProfile

    pr = cProfile.Profile()
    pr.enable()
    # json_dao = JsonDao(data_dir=Path("data"))
    # request = json_dao.read_request("fail.json")
    request = simple_request()
    sp = ProblemInputFactory.from_request(request).user_finances
    mi = ProblemInput(
        user_finances=sp,
        strategies=[
            StrategyName.snowball.value,
            # StrategyName.avalanche.value,
            # StrategyName.avalanche_ball.value,
            StrategyName.lp.value,
        ],
    )
    solution = solve(mi)
    processed_solution = SolutionProcessor.process(solution)
    for strategy, plan in processed_solution.items():
        plan: ProcessedFinancialPlan
        print(f"Strategy: {strategy}")
        for milestone in plan.milestones.values():
            print(f"\t{milestone.text}")
    print(str(mi.user_finances))
    for strategy_name, plan in solution.plans.items():
        print(f"solution strategy: {strategy_name}")
        print(f"\t net worth: {plan.get_net_worth()}")
        print(f"\t interest paid on loans: {plan.get_total_interest_paid_on_loans()}")
        print(
            f"\t interest earned on investments: {plan.get_total_interest_earned_on_investments()}"
        )
        print(f"\t total withdrawals: {plan.get_total_withdrawals()}")
    pr.disable()
    # pr.print_stats(sort="cumulative")
    for strategy_name, plan in solution.plans.items():
        visualize_solution(plan, suffix=strategy_name)


if __name__ == "__main__":
    main()
