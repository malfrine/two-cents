import logging
from dataclasses import dataclass

from pyomo import environ as pe
from pyomo.core import ConcreteModel

from pennies.model.parameters import Parameters
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.milp.components import MILPComponents
from pennies.strategies.milp.constraints import MILPConstraints
from pennies.strategies.milp.objective import MILPObjective
from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.utilities import ConcreteModelBuilder
from pennies.strategies.milp.variables import MILPVariables


@dataclass
class MILP:

    user_finances: UserPersonalFinances
    problem_parameters: Parameters
    pyomodel: ConcreteModel
    components: MILPComponents

    @property
    def sets(self) -> MILPSets:
        return self.components.sets

    @property
    def milp_parameters(self) -> MILPParameters:
        return self.components.parameters

    @property
    def variables(self) -> MILPVariables:
        return self.components.variables

    @property
    def constraints(self) -> MILPConstraints:
        return self.components.constraints

    @property
    def objective(self) -> MILPObjective:
        return self.components.objective

    @classmethod
    def create(
        cls, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> "MILP":
        milp_components = MILPComponents.create(
            user_finances=user_finances, parameters=parameters
        )
        builder = ConcreteModelBuilder()
        m = builder.build(
            constraints=milp_components.constraints.as_list,
            variables=milp_components.variables.as_list,
            objective=milp_components.objective.obj,
        )
        return MILP(
            problem_parameters=parameters,
            user_finances=user_finances,
            pyomodel=m,
            components=milp_components,
        )

    def _is_valid_solution(self, results) -> bool:
        status = results.solver.status
        termination_condition = results.solver.termination_condition

        is_aborted = status == pe.SolverStatus.aborted
        is_okay = status == pe.SolverStatus.ok
        is_optimal = termination_condition == pe.TerminationCondition.optimal

        return (is_optimal and is_okay) or is_aborted

    def create_solver(self):
        solver = pe.SolverFactory("cbc")
        solver.options["ratio"] = self.problem_parameters.optimality_gap
        solver.options["seconds"] = self.problem_parameters.max_milp_seconds
        solver.options["maxNodes"] = self.problem_parameters.max_milp_nodes
        return solver

    def solve(self) -> bool:
        solver = self.create_solver()
        is_log_milp = self.problem_parameters.is_log_milp
        results = solver.solve(self.pyomodel, tee=is_log_milp)
        if not self._is_valid_solution(results):
            logging.error(
                f"Did not get a valid solution; status: {results.solver.status};"
                f" termination condition: {results.solver.termination_condition}"
            )
            return False
        return True
