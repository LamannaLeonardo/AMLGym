"""Converts regular trajectories to the type of trajectories that PlanMiner algorithm accepts."""
import logging
import sys
from pathlib import Path
from typing import Set, Dict

from pddl_plus_parser.exporters import DomainExporter
from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser, TrajectoryParser
from pddl_plus_parser.models import Operator, GroundedPredicate, PDDLFunction, Domain

from sam_learning.core.environment_snapshot import EnvironmentSnapshot


class PlanMinerTrajectoriesCreator:
    """Class that transforms our trajectory file data into the type of trajectories that plan miner accepts.

    Note:
        This assumes that there are regular trajectories to be converted to the correct format.
    """

    domain_file_name: str
    working_directory_path: Path
    logger: logging.Logger

    def __init__(self, domain_file_name: str, working_directory_path: Path):
        self.domain_file_name = domain_file_name
        self.working_directory_path = working_directory_path
        self.logger = logging.getLogger(__name__)

    def convert_domain_to_plan_miner_form(self, domain: Domain) -> None:
        """Converts the domain to the format that PlanMiner later outputs.

        Note:
            This is a helper function for the experiments where the comparison between the learned domain and the
            original domain is needed.
        """
        export_path = self.working_directory_path / f"{self.domain_file_name.split('.')[0]}_plan_miner.pddl"
        # change the names of the parameters in the predicates to be in the form of ?param_<index>
        for predicate in domain.predicates.values():
            old_to_new_parameter_names = {param_name: f"?param_{index}" for index, param_name in enumerate(predicate.signature.keys())}
            predicate.change_signature(old_to_new_parameter_names)

        # change the names of the parameters in the numeric functions to be in the form of ?param_<index>
        for function in domain.functions.values():
            old_to_new_parameter_names = {param_name: f"?param_{index}" for index, param_name in enumerate(function.signature.keys())}
            function.change_signature(old_to_new_parameter_names)

        # change the names of the parameters in the actions to be in the form of ?param_<index>
        for action in domain.actions.values():
            old_to_new_parameter_names = {param_name: f"?param_{index}" for index, param_name in enumerate(action.signature.keys())}
            action.change_signature(old_to_new_parameter_names)

        # export the new domain to a file
        domain_exporter = DomainExporter()
        domain_exporter.export_domain(domain=domain, export_path=export_path)

    @staticmethod
    def create_complete_state(state_predicates: Set[GroundedPredicate], state_functions: Dict[str, PDDLFunction]) -> str:
        """Creates the complete state string from the state predicates and functions in the format that PlanMiner requires.

        :param state_predicates: the positive and negative state predicates.
        :param state_functions: the numeric functions in the state.
        :return: the complete state string in the PlanMiner format.
        """
        positive_state_predicates = [str(predicate).upper() for predicate in state_predicates if predicate.is_positive]
        negative_state_predicates = []
        for predicate in state_predicates:
            if not predicate.is_positive:
                negated_predicate = GroundedPredicate(
                    name=predicate.name, signature=predicate.signature, object_mapping=predicate.object_mapping, is_positive=True
                )
                negative_state_predicates.append(f"(not {str(negated_predicate).upper()})")

        functions = [function.state_typed_representation.upper() for function in state_functions.values()]
        return f"({' '.join(positive_state_predicates)} {' '.join(functions)} {' '.join(negative_state_predicates)})"

    def create_plan_miner_trajectories(self) -> None:
        """Creates the trajectories in the format file that PlanMiner requires.."""
        domain_file_path = self.working_directory_path / self.domain_file_name
        domain = DomainParser(domain_file_path).parse_domain()
        self.convert_domain_to_plan_miner_form(domain)
        triplet_snapshot = EnvironmentSnapshot(domain)
        plan_miner_trajectory_file_path = self.working_directory_path / "plan_miner_trajectories.pts"
        if plan_miner_trajectory_file_path.exists():
            return

        trajectories = []
        for trajectory_file_path in self.working_directory_path.glob("*.trajectory"):
            self.logger.info(f"Processing trajectory file: {trajectory_file_path}")
            problem_file_path = self.working_directory_path / f"{trajectory_file_path.stem}.pddl"
            problem = ProblemParser(problem_file_path, domain).parse_problem()
            observation = TrajectoryParser(domain, problem).parse_trajectory(trajectory_file_path)
            plan_sequence = ["##Tasks##"]
            state_sequence = ["##States##"]
            for index, action_triplet in enumerate(observation.components):
                action = action_triplet.grounded_action_call
                prev_state = action_triplet.previous_state
                next_state = action_triplet.next_state
                previous_state_predicates = triplet_snapshot._create_state_discrete_snapshot(prev_state, observation.grounded_objects)
                next_state_predicates = triplet_snapshot._create_state_discrete_snapshot(next_state, observation.grounded_objects)
                op = Operator(
                    action=domain.actions[action.name], domain=domain, grounded_action_call=action.parameters, problem_objects=problem.objects
                )
                plan_sequence.append(f"[{index}, {index + 1}]: {op.typed_action_call.upper()}")
                if index == 0:
                    state_str = self.create_complete_state(state_predicates=previous_state_predicates, state_functions=prev_state.state_fluents)
                    state_sequence.append(f"[{index}]: {state_str}")

                state_str = self.create_complete_state(state_predicates=next_state_predicates, state_functions=next_state.state_fluents)
                state_sequence.append(f"[{index + 1}]: {state_str}")

            action_trace = "\n".join(plan_sequence)
            state_trace = "\n\n".join(state_sequence)
            plan_miner_trajectory = f"New plan!!!\n\n" f"{action_trace}\n\n\n" f"{state_trace}"
            trajectories.append(plan_miner_trajectory)

        with open(plan_miner_trajectory_file_path, "wt") as plan_miner_trajectory_file:
            plan_miner_trajectory_file.write("\n\n".join(trajectories))


if __name__ == "__main__":
    trajectory_creator = PlanMinerTrajectoriesCreator(sys.argv[1], Path(sys.argv[2]))
    trajectory_creator.create_plan_miner_trajectories()
