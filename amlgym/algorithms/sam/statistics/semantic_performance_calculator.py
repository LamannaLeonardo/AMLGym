"""Module responsible for calculating our approach for numeric precision and recall."""
import csv
import logging
import uuid
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Tuple, Any, Union, Optional

from pddl_plus_parser.exporters import ProblemExporter
from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import (
    Domain,
    Observation,
    ActionCall,
    State,
    MultiAgentObservation,
    Operator,
    PDDLObject,
    Problem,
)

from sam_learning.core import VocabularyCreator
from utilities import LearningAlgorithmType, NegativePreconditionPolicy
from validators import run_validate_script, VALID_PLAN

SEMANTIC_PRECISION_STATS = [
    "action_name",
    "policy",
    "learning_algorithm",
    "num_trajectories",
    "precondition_precision",
    "precondition_recall",
    "effects_precision",
    "effects_recall",
]


def _calculate_precision_recall(
    num_false_negatives: Dict[str, int], num_false_positives: Dict[str, int], num_true_positives: Dict[str, int]
) -> Tuple[Dict[str, float], Dict[str, float]]:
    """Calculates the precision and recall values for each action.

    :param num_false_negatives: the number of false negatives for each action.
    :param num_false_positives: the number of false positives for each action.
    :param num_true_positives: the number of true positives for each action.
    :return: a tuple of two dictionaries, one for the precision values and one for the recall values.
    """
    precision_dict = defaultdict(float)
    recall_dict = defaultdict(float)
    for action_name, tp_rate in num_true_positives.items():
        if tp_rate == 0:
            precision_dict[action_name] = 1 if num_false_positives[action_name] == 0 else 0
            recall_dict[action_name] = 0
            continue

        precision_dict[action_name] = tp_rate / (tp_rate + num_false_positives[action_name])
        recall_dict[action_name] = tp_rate / (tp_rate + num_false_negatives[action_name])

    return precision_dict, recall_dict


class SemanticPerformanceCalculator:
    """Class responsible for calculating the semantic precision and recall of a model."""

    model_domain: Domain
    dataset_observations: List[Union[Observation, MultiAgentObservation]]
    learning_algorithm: LearningAlgorithmType
    combined_stats: List[Dict[str, Any]]
    logger: logging.Logger
    results_dir_path: Path
    _random_actions: List[List[ActionCall]]

    def __init__(
        self,
        model_domain: Domain,
        model_domain_path: Path,
        observations: List[Union[Observation, MultiAgentObservation]],
        working_directory_path: Path,
        learning_algorithm: LearningAlgorithmType,
    ):
        self.logger = logging.getLogger(__name__)
        self.model_domain = model_domain
        self.model_domain_path = model_domain_path
        self.dataset_observations = observations
        self.learning_algorithm = learning_algorithm
        self.combined_stats = []
        self.results_dir_path = working_directory_path / "results_directory"
        self.temp_dir_path = working_directory_path / "temp"
        self.temp_dir_path.mkdir(exist_ok=True)
        self.vocabulary_creator = VocabularyCreator()
        self._random_actions = []

    def _calculate_action_applicability_rate(
        self, action_call: ActionCall, learned_domain_path: Path, observed_state: State, problem_objects: Dict[str, PDDLObject],
    ) -> Tuple[int, int, int]:
        """Test whether an action is applicable in both the model domain and the generated domain.

        :param action_call: the action call that is tested for applicability.
        :param learned_domain_path: the domain that was learned using the action model learning algorithm.
        :param observed_state: the state that was observed in the trajectory data.
        :param problem_objects: the objects that were used in the problem definition.
        :return: a tuple containing the number of true positives, false positives and false negatives.
        """
        self.logger.debug(f"Calculating the applicability rate for the action - {action_call.name}")
        applicability_validation_problem = Problem(domain=self.model_domain)
        applicability_validation_problem.name = f"instance_{uuid.uuid4()}"
        applicability_validation_problem.objects = problem_objects
        applicability_validation_problem.initial_state_predicates = observed_state.state_predicates
        applicability_validation_problem.initial_state_fluents = observed_state.state_fluents
        self.logger.debug(
            f"Exporting a problem with the initial state as in {str(observed_state)} and no goals to validate whether the action is applicable."
        )
        current_problem_file_path = self.temp_dir_path / f"applicability_validation_problem_{uuid.uuid4()}.pddl"
        current_solution_file_path = self.temp_dir_path / f"applicability_validation_solution_{uuid.uuid4()}.solution"
        with open(current_solution_file_path, "wt") as solution_file:
            solution_file.write(str(action_call))

        ProblemExporter().export_problem(problem=applicability_validation_problem, export_path=current_problem_file_path)

        self.logger.debug(f"Exported the problem to {current_problem_file_path}, now validating the action's applicability.")
        applicable_in_model = self._calculate_applicability_in_state(current_problem_file_path, current_solution_file_path, self.model_domain_path)
        applicable_in_learned = self._calculate_applicability_in_state(current_problem_file_path, current_solution_file_path, learned_domain_path)

        current_problem_file_path.unlink()
        current_solution_file_path.unlink()
        return (
            int(applicable_in_learned == applicable_in_model and applicable_in_learned),
            int(applicable_in_learned and not applicable_in_model),
            int(not applicable_in_learned and applicable_in_model),
        )

    @staticmethod
    def _calculate_applicability_in_state(problem_file_path: Path, solution_file_path: Path, domain_file_path: Path) -> bool:
        """Calculate whether the action is applicable in the state.

        :param problem_file_path: the path to the problem file.
        :param solution_file_path: the path to the solution file.
        :param domain_file_path: the path to the domain file.
        :return: whether the action is applicable in the state.
        """
        validation_file_path = run_validate_script(
            domain_file_path=domain_file_path, problem_file_path=problem_file_path, solution_file_path=solution_file_path
        )
        with open(validation_file_path, "r", encoding="utf-8") as validation_file:
            validation_file_content = validation_file.read()

        validation_file_path.unlink()
        return VALID_PLAN in validation_file_content

    def _calculate_effects_difference_rate(
        self,
        observation: Observation,
        learned_domain: Domain,
        num_false_negatives: Dict[str, int],
        num_false_positives: Dict[str, int],
        num_true_positives: Dict[str, int],
    ) -> None:
        """Calculates the effects difference rate for each action.

        :param observation: the observation that is being tested.
        :param learned_domain: the domain that was learned using the action model learning algorithm.
        :param num_false_negatives: the dictionary mapping between the action name and the number of false negative
        :param num_false_positives: the dictionary mapping between the action name and the number of false positive
        :param num_true_positives: the dictionary mapping between the action name and the number of true positive
        """
        self.logger.info("Calculating effects difference rate for the observation.")
        for observation_triplet in observation.components:
            model_previous_state = observation_triplet.previous_state
            executed_action = observation_triplet.grounded_action_call
            model_next_state = observation_triplet.next_state
            if executed_action.name not in learned_domain.actions:
                continue

            try:
                learned_operator = Operator(
                    action=learned_domain.actions[executed_action.name],
                    domain=learned_domain,
                    grounded_action_call=executed_action.parameters,
                    problem_objects=observation.grounded_objects,
                )
                # cannot apply when the action is inapplicable since the linear regression is fitted on applicable numeric points.
                try:
                    learned_next_state = learned_operator.apply(model_previous_state)

                except ValueError:
                    self.logger.debug("The action is not applicable in the state.")
                    learned_next_state = model_previous_state.copy()
                    model_next_state = model_previous_state.copy()

                except ZeroDivisionError:
                    self.logger.debug("Tried to perform a division by zero!")
                    learned_next_state = model_previous_state.copy()
                    model_next_state = model_previous_state.copy()

                self.logger.debug("Validating if there are any false negatives.")
                model_state_predicates = {
                    predicate.untyped_representation
                    for grounded_predicate in model_next_state.state_predicates.values()
                    for predicate in grounded_predicate
                }
                learned_state_predicates = {
                    predicate.untyped_representation
                    for grounded_predicate in learned_next_state.state_predicates.values()
                    for predicate in grounded_predicate
                }
                if len(model_state_predicates) == 0 and len(learned_state_predicates) == 0:
                    num_true_positives[executed_action.name] += 1
                    continue

                num_true_positives[executed_action.name] += len(model_state_predicates.intersection(learned_state_predicates))
                num_false_positives[executed_action.name] += len(learned_state_predicates.difference(model_state_predicates))
                num_false_negatives[executed_action.name] += len(model_state_predicates.difference(learned_state_predicates))

            except ValueError:
                self.logger.debug("The action is not applicable in the state.")
                continue

    def calculate_preconditions_semantic_performance(
        self, learned_domain: Domain, learned_domain_path: Path
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Calculates the precision recall values of the learned preconditions.

        :param learned_domain: the action model that was learned using the action model learning algorithm
        :param learned_domain_path: the path to the learned domain.
        :return: the precision and recall dictionaries.
        """
        num_true_positives = defaultdict(int)
        num_false_negatives = defaultdict(int)
        num_false_positives = defaultdict(int)
        self.logger.debug("Starting to calculate the semantic preconditions performance")
        for index, observation in enumerate(self.dataset_observations):
            observation_objects = observation.grounded_objects
            for component in observation.components:
                action = component.grounded_action_call
                if action.name not in learned_domain.actions:
                    continue

                true_positive, false_positive, false_negative = self._calculate_action_applicability_rate(
                    action, learned_domain_path, component.previous_state, observation_objects,
                )
                num_true_positives[action.name] += true_positive
                num_false_positives[action.name] += false_positive
                num_false_negatives[action.name] += false_negative

        return _calculate_precision_recall(num_false_negatives, num_false_positives, num_true_positives)

    def calculate_effects_semantic_performance(self, learned_domain: Domain) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Calculates the precision recall values of the learned effects.

        :param learned_domain: the action model that was learned using the action model learning algorithm
        :return: the precision and recall dictionaries.
        """
        self.logger.info("Starting to calculate the semantic effects performance")
        num_true_positives = defaultdict(int)
        num_false_negatives = defaultdict(int)
        num_false_positives = defaultdict(int)
        if len(self.model_domain.predicates) == 0:
            return (
                {action_name: 1 for action_name in self.model_domain.actions.keys()},
                {action_name: 1 for action_name in self.model_domain.actions.keys()},
            )

        for observation in self.dataset_observations:
            self._calculate_effects_difference_rate(observation, learned_domain, num_false_negatives, num_false_positives, num_true_positives)

        return _calculate_precision_recall(num_false_negatives, num_false_positives, num_true_positives)

    def calculate_performance(self, learned_domain_path: Path, num_used_observations: int, policy: NegativePreconditionPolicy) -> None:
        """Calculate the semantic precision and recall of the learned domain.

        :param learned_domain_path: the path to the learned domain.
        :param num_used_observations: the number of observations used to learn the domain.
        :param policy: the policy to use for the negative preconditions.
        """
        learned_domain = DomainParser(domain_path=learned_domain_path, partial_parsing=False).parse_domain()
        self.logger.info("Starting to calculate the semantic preconditions performance of the learned domain.")
        preconditions_precision, preconditions_recall = self.calculate_preconditions_semantic_performance(learned_domain, learned_domain_path)
        self.logger.info("Starting to calculate the semantic effects performance of the learned domain.")
        effects_precision, effects_recall = self.calculate_effects_semantic_performance(learned_domain)
        for action_name in self.model_domain.actions:
            action_stats = {
                "learning_algorithm": self.learning_algorithm.name,
                "policy": policy.name,
                "action_name": action_name,
                "num_trajectories": num_used_observations,
                "precondition_precision": preconditions_precision.get(action_name, 1),
                "precondition_recall": preconditions_recall.get(action_name, 0),
                "effects_precision": effects_precision.get(action_name, 1),
                "effects_recall": effects_recall.get(action_name, 1),
            }
            self.combined_stats.append(action_stats)

    def export_semantic_performance(self, fold_num: int, iteration_num: Optional[int] = None) -> None:
        """Exports the precision values of the learned preconditions to a CSV file.

        :param fold_num: the fold number.
        :param iteration_num: the iteration number.
        """
        iterations_suffix = f"{iteration_num}" if iteration_num is not None else ""
        statistics_path = (
            self.results_dir_path / f"{self.learning_algorithm.name}_{self.model_domain.name}_{fold_num}_{iterations_suffix}_semantic_performance.csv"
        )
        with open(statistics_path, "wt", newline="") as statistics_file:
            stats_writer = csv.DictWriter(statistics_file, fieldnames=SEMANTIC_PRECISION_STATS)
            stats_writer.writeheader()
            for data_line in self.combined_stats:
                stats_writer.writerow(data_line)

    def export_combined_semantic_performance(self) -> None:
        """Export the numeric learning statistics to a CSV report file."""
        statistics_path = self.results_dir_path / f"{self.learning_algorithm.name}_{self.model_domain.name}_combined_semantic_performance.csv"
        with open(statistics_path, "wt", newline="") as statistics_file:
            stats_writer = csv.DictWriter(statistics_file, fieldnames=SEMANTIC_PRECISION_STATS)
            stats_writer.writeheader()
            for data_line in self.combined_stats:
                stats_writer.writerow(data_line)
