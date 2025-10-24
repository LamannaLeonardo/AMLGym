"""Creates the trajectories that will be used in the trajectory"""
import logging
import random
import shutil
import sys
from pathlib import Path
from typing import Dict, Set, List, Tuple, Optional

from pddl_plus_parser.exporters import TrajectoryExporter, TrajectoryTriplet
from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser
from pddl_plus_parser.models import PDDLObject, Domain, ActionCall, Problem, State, Operator

from sam_learning.core import VocabularyCreator
from utilities import SolverType

MAX_NUM_STEPS_IN_TRAJECTORY = 200
inapplicable_action_probability = 0.25
random.seed(42)


class RandomWalkTrajectoriesCreator:
    """Class that creates trajectories from executing random walks in the domain."""

    domain_file_name: str
    working_directory_path: Path
    vocabulary_creator: VocabularyCreator
    logger: logging.Logger

    def __init__(self, domain_file_name: str, working_directory_path: Path):
        self.domain_file_name = domain_file_name
        self.working_directory_path = working_directory_path
        self.vocabulary_creator = VocabularyCreator()
        self.logger = logging.getLogger(__name__)

    def _select_inapplicable_action(
        self, domain: Domain, problem: Problem, current_state: State, ground_actions: Set[ActionCall]
    ) -> Tuple[Operator, State]:
        """Selects an inapplicable action for the current state (This is for performance evaluation purposes).

        :param domain: the domain to select the inapplicable action from.
        :param problem: the problem defining the objects and the initial state.
        :param current_state: the current state to select the inapplicable action for.
        :param ground_actions: the grounded actions to select the inapplicable action from.
        :return: the inapplicable action and the next state.
        """
        self.logger.debug("Selecting an inapplicable action.")
        action_queue = list(ground_actions)
        random.shuffle(action_queue)
        inapplicable_action = action_queue.pop()
        operator = Operator(
            action=domain.actions[inapplicable_action.name],
            domain=domain,
            grounded_action_call=inapplicable_action.parameters,
            problem_objects=problem.objects,
        )
        while operator.is_applicable(current_state) and len(action_queue) > 0:
            inapplicable_action = action_queue.pop()
            operator = Operator(
                action=domain.actions[inapplicable_action.name],
                domain=domain,
                grounded_action_call=inapplicable_action.parameters,
                problem_objects=problem.objects,
            )

        return operator, State(predicates=current_state.state_predicates, fluents=current_state.state_fluents, is_init=False)

    def _select_applicable_action(
        self, domain: Domain, problem: Problem, current_state: State, grounded_actions: Set[ActionCall]
    ) -> Tuple[Operator, State]:
        """Selects a random applicable action for the current state.

        :param domain: the domain to select the applicable action from.
        :param problem: the problem defining the objects and the initial state.
        :param current_state: the current state to select the applicable action for.
        :param grounded_actions: the grounded actions to select the applicable action from.
        :return: the applicable action and the next state.
        """
        self.logger.debug("Selecting an applicable action.")
        action_queue = list(grounded_actions)
        random.shuffle(action_queue)
        action = action_queue.pop()
        operator = Operator(
            action=domain.actions[action.name], domain=domain, grounded_action_call=action.parameters, problem_objects=problem.objects
        )
        while not operator.is_applicable(current_state) and len(action_queue) > 0:
            self.logger.debug(f"Action {action} is inapplicable.")
            action = action_queue.pop()
            operator = Operator(
                action=domain.actions[action.name], domain=domain, grounded_action_call=action.parameters, problem_objects=problem.objects
            )

        if len(action_queue) == 0 and not operator.is_applicable(current_state):
            raise ValueError("No applicable actions found.")

        next_state = operator.apply(current_state, skip_validation=True)
        return operator, next_state

    def create_random_plan(self, domain: Domain, problem: Problem, grounded_actions: Set[ActionCall]) -> Tuple[List[TrajectoryTriplet], List[str]]:
        """Creates a random trajectory from the input domain and problem by randomly executing actions.

        :param domain: The domain that contain the actions to execute.
        :param problem: the problem containing the initial state and the objects.
        :param grounded_actions: a list of all the possible grounded actions that match the problem.
        :return: a list of the triplets that represent the trajectory and the plan.
        """
        self.logger.info(f"Starting to create a random trajectory for the problem - {problem.name}")
        plan = []
        current_state = State(predicates=problem.initial_state_predicates, fluents=problem.initial_state_fluents, is_init=True)
        action_triplets = []
        for i in range(MAX_NUM_STEPS_IN_TRAJECTORY):
            self.logger.debug(f"Selecting an action for timestep {i}.")
            if random.random() < inapplicable_action_probability:
                self.logger.debug(f"Selecting an inapplicable action for timestep {i}.")
                action, next_state = self._select_inapplicable_action(domain, problem, current_state, grounded_actions)
                action_triplets.append(TrajectoryTriplet(previous_state=current_state, op=action, next_state=next_state))
                plan.append(str(action))
                current_state = next_state.copy()
                continue

            self.logger.debug(f"Selecting an applicable action for timestep {i}.")
            try:
                action, next_state = self._select_applicable_action(domain, problem, current_state, grounded_actions)
                action_triplets.append(TrajectoryTriplet(previous_state=current_state, op=action, next_state=next_state))
                plan.append(str(action))
                current_state = next_state.copy()

            except ValueError:
                self.logger.warning(f"No applicable actions found for timestep {i}.")
                break

        return action_triplets, plan

    def create_all_grounded_actions(
        self, observed_objects: Dict[str, PDDLObject], domain: Domain, initial_state_fluents: List[str]
    ) -> Set[ActionCall]:
        """Creates all the grounded actions for the domain given the current possible objects.

        :param observed_objects: the objects that the learner has observed so far.
        :param domain: the domain of which the actions were taken from.
        :param initial_state_fluents: the initial state fluents to validate that all random actions do not interact with illegal fluents.
        :return: a set of all the possible grounded actions.
        """
        self.logger.info("Creating all the grounded actions for the domain given the current possible objects.")
        grounded_action_calls = self.vocabulary_creator.create_grounded_actions_vocabulary(domain=domain, observed_objects=observed_objects)
        legal_actions = set()

        for action in grounded_action_calls:
            operator = Operator(
                action=domain.actions[action.name], domain=domain, grounded_action_call=action.parameters, problem_objects=observed_objects
            )
            operator.ground()
            # validating that the preconditions do not contain any numeric fluents that do not exist in the problem.
            grounded_effect_fluents = set()
            for effect in operator.grounded_effects:
                grounded_effect_fluents.update(effect.grounded_numeric_fluents)

            if not (
                operator.grounded_preconditions.grounded_numeric_fluents.issubset(set(initial_state_fluents))
                and grounded_effect_fluents.issubset(set(initial_state_fluents))
            ):
                continue

            legal_actions.add(action)

        return legal_actions

    def create_domain_trajectories(self, problems_prefix: str = "pfile", output_directory_path: Optional[Path] = None) -> None:
        """Creates the domain trajectory files.

        :param problems_prefix: the prefix of the problem files.
        :param output_directory_path: the path to the output directory.
        """
        domain_file_path = self.working_directory_path / self.domain_file_name
        output_dir = output_directory_path or self.working_directory_path
        domain = DomainParser(domain_file_path).parse_domain()
        trajectory_exporter = TrajectoryExporter(domain=domain, allow_invalid_actions=False)
        for problem_file_path in self.working_directory_path.glob(f"{problems_prefix}*.pddl"):
            self.logger.info(f"Creating the trajectory for the problem - {problem_file_path.stem}")
            output_trajectory_path = output_dir / f"{problem_file_path.stem}_random_walk.trajectory"
            if output_trajectory_path.exists():
                continue

            problem = ProblemParser(problem_path=problem_file_path, domain=domain).parse_problem()
            grounded_actions = self.create_all_grounded_actions(
                observed_objects=problem.objects, domain=domain, initial_state_fluents=list(problem.initial_state_fluents.keys())
            )
            random_walk_triplets, plan = self.create_random_plan(domain, problem, grounded_actions)
            self.logger.debug("Creating a copy of the problem file with the trajectory as well as a solution_file.")
            with open(output_dir / f"{problem_file_path.stem}_random_walk.solution", "wt") as plan_file:
                plan_file.write("\n".join(plan))

            shutil.copy(problem_file_path, output_dir / f"{problem_file_path.stem}_random_walk.pddl")
            trajectory_exporter.export_to_file(random_walk_triplets, output_dir / f"{problem_file_path.stem}_random_walk.trajectory")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    trajectory_creator = RandomWalkTrajectoriesCreator(domain_file_name=sys.argv[1], working_directory_path=Path(sys.argv[2]))
    selected_solver = SolverType.enhsp
    trajectory_creator.create_domain_trajectories()
