"""Module responsible for calculating our approach for Multi-Agent precision and recall."""
import csv
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Tuple

from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import (
    Domain,
    MultiAgentObservation,
)
from pddl_plus_parser.multi_agent import MultiAgentTrajectoryExporter

from statistics import SemanticPerformanceCalculator, _calculate_precision_recall
from utilities import LearningAlgorithmType, NegativePreconditionPolicy

SEMANTIC_PRECISION_STATS = [
    "fold",
    "learning_algorithm",
    "policy",
    "action_name",
    "num_trajectories",
    "precondition_precision",
    "precondition_recall",
]


class MASamPerformanceCalculator(SemanticPerformanceCalculator):
    """Class responsible for calculating the Multi-Agent precision and recall of a model."""

    dataset_observations: List[MultiAgentObservation]

    def __init__(
        self,
        model_domain: Domain,
        model_domain_path: Path,
        observations: List[MultiAgentObservation],
        working_directory_path: Path,
        learning_algorithm: LearningAlgorithmType,
    ):
        super().__init__(model_domain, model_domain_path, observations, working_directory_path, learning_algorithm)

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
                for action in component.grounded_joint_action.actions:
                    if action.name not in learned_domain.actions:
                        continue

                    true_positive, false_positive, false_negative = self._calculate_action_applicability_rate(
                        action, learned_domain_path, component.previous_state, observation_objects,
                    )
                    num_true_positives[action.name] += true_positive
                    num_false_positives[action.name] += false_positive
                    num_false_negatives[action.name] += false_negative

        return _calculate_precision_recall(num_false_negatives, num_false_positives, num_true_positives)

    def _calculate_effects_difference_rate_for_multi_agent_experiments(
        self,
        observation: MultiAgentObservation,
        learned_domain: Domain,
        ma_trajectory_exporter: MultiAgentTrajectoryExporter,
        num_false_negatives: Dict[str, int],
        num_false_positives: Dict[str, int],
        num_true_positives: Dict[str, int],
    ) -> None:
        """Calculates the effects difference rate for each action.

        :param observation: the observation that is being tested.
        :param learned_domain: the domain that was learned using the action model learning algorithm.
        :param ma_trajectory_exporter: module able to create multi-agent trajectories.
        :param num_false_negatives: the dictionary mapping between the action name and the number of false negative
        :param num_false_positives: the dictionary mapping between the action name and the number of false positive
        :param num_true_positives: the dictionary mapping between the action name and the number of true positive
        """
        self.logger.info("Calculating effects difference rate for the observation.")
        for observation_triplet in observation.components:
            model_previous_state = observation_triplet.previous_state
            executed_joint_action = observation_triplet.grounded_joint_action
            model_next_state = observation_triplet.next_state
            if any([action.name not in learned_domain.actions for action in executed_joint_action.actions]):
                continue

            try:
                ma_triplet = ma_trajectory_exporter.create_multi_agent_triplet(
                    previous_state=model_previous_state,
                    action_call=str(executed_joint_action),
                    problem_objects=observation.grounded_objects,
                    allow_inapplicable_actions=False,
                )

                model_state_predicates = {
                    predicate.untyped_representation
                    for grounded_predicate in model_next_state.state_predicates.values()
                    for predicate in grounded_predicate
                }
                learned_state_predicates = {
                    predicate.untyped_representation
                    for grounded_predicate in ma_triplet.next_state.state_predicates.values()
                    for predicate in grounded_predicate
                }

                for action in observation_triplet.grounded_joint_action.actions:
                    num_true_positives[action.name] += len(model_state_predicates.intersection(learned_state_predicates))
                    num_false_positives[action.name] += len(learned_state_predicates.difference(model_state_predicates))
                    num_false_negatives[action.name] += len(model_state_predicates.difference(learned_state_predicates))

            except ValueError:
                self.logger.debug("The joint action is not applicable according to the learned model.")
                continue

    def calculate_effects_semantic_performance(self, learned_domain: Domain) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Calculates the precision recall values of the learned effects.

        :param learned_domain: the action model that was learned using the action model learning algorithm
        :return: the precision and recall dictionaries.
        """
        self.logger.info("Starting to calculate the semantic effects performance for the multi-agent model.")
        num_true_positives = defaultdict(int)
        num_false_negatives = defaultdict(int)
        num_false_positives = defaultdict(int)
        if len(self.model_domain.predicates) == 0:
            return (
                {action_name: 1 for action_name in self.model_domain.actions.keys()},
                {action_name: 1 for action_name in self.model_domain.actions.keys()},
            )

        multi_agent_trajectory_exporter = MultiAgentTrajectoryExporter(domain=learned_domain, allow_invalid_actions=False)
        for observation in self.dataset_observations:
            self._calculate_effects_difference_rate_for_multi_agent_experiments(
                observation, learned_domain, multi_agent_trajectory_exporter, num_false_negatives, num_false_positives, num_true_positives
            )

        return _calculate_precision_recall(num_false_negatives, num_false_positives, num_true_positives)

    def calculate_performance_for_ma_sam_experiments(
        self, learned_domain_path: Path, num_used_observations: int, policy: NegativePreconditionPolicy
    ) -> None:
        """Calculates the model's performance with both the precision and the recall values calculated.
        :param learned_domain_path: the path to the learned action model.
        :param num_used_observations: the number of observations used to learn the action model.
        :param policy: the negative precondition policy to use.
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

        self.logger.info(f"Finished calculating the learning performance for {self.learning_algorithm.name}.")

    def export_combined_semantic_performance(self) -> None:
        """Export the numeric learning statistics to a CSV report file."""
        statistics_path = self.results_dir_path / f"{self.learning_algorithm.name}_{self.model_domain.name}_combined_semantic_performance.csv"
        with open(statistics_path, "wt", newline="") as statistics_file:
            stats_writer = csv.DictWriter(statistics_file, fieldnames=SEMANTIC_PRECISION_STATS)
            stats_writer.writeheader()
            for data_line in self.combined_stats:
                stats_writer.writerow(data_line)
