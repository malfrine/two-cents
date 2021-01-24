from pennies.model.processed.action_plan import ActionPlanFactory
from pennies.model.processed.milestones import PlanMilestonesFactory
from pennies.model.processed.net_worth_forecast import NetWorthForecastFactory
from pennies.model.processed.solution import ProcessedSolution
from pennies.model.processed.plan import ProcessedFinancialPlan
from pennies.model.processed.summaries import PlanSummariesFactory
from pennies.model.solution import Solution, FinancialPlan


class SolutionProcessor:
    @classmethod
    def process(cls, solution: Solution) -> ProcessedSolution:
        return ProcessedSolution(
            {
                strategy_name: cls._process_plan(plan)
                for strategy_name, plan in solution.plans.items()
            }
        )

    @classmethod
    def _process_plan(cls, plan: FinancialPlan) -> ProcessedFinancialPlan:
        return ProcessedFinancialPlan(
            net_worth=NetWorthForecastFactory.from_plan(plan),
            summaries=PlanSummariesFactory.from_plan(plan),
            milestones=PlanMilestonesFactory.from_plan(plan),
            action_plan=ActionPlanFactory.from_plan(plan),
        )
