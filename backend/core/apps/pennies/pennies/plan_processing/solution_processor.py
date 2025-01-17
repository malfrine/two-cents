from pennies.model.problem_input import ProblemInput
from pennies.plan_processing.action_plan import ActionPlanFactory
from pennies.plan_processing.failures import PlanFailuresFactory
from pennies.plan_processing.milestones import PlanMilestonesFactory
from pennies.plan_processing.net_worth_forecast import NetWorthForecastFactory
from pennies.plan_processing.plan import ProcessedFinancialPlan
from pennies.plan_processing.solution import ProcessedSolution
from pennies.plan_processing.summaries import PlanSummariesFactory
from pennies.model.solution import Solution, FinancialPlan


class SolutionProcessor:
    @classmethod
    def process_solution(cls, solution: Solution) -> ProcessedSolution:
        return ProcessedSolution(
            {
                strategy_name: cls.process_plan(plan, solution.problem_input)
                for strategy_name, plan in solution.plans.items()
            }
        )

    @classmethod
    def process_plan(
        cls, plan: FinancialPlan, problem_input: ProblemInput
    ) -> ProcessedFinancialPlan:
        return ProcessedFinancialPlan(
            net_worth=NetWorthForecastFactory.from_plan(plan),
            summaries=PlanSummariesFactory.from_plan(plan, problem_input),
            milestones=PlanMilestonesFactory.create(plan, problem_input),
            action_plan=ActionPlanFactory.from_plan(plan),
            failures=PlanFailuresFactory.create(plan, problem_input),
        )
