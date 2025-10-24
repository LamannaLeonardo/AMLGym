"""Module to manage the action model learning statistics."""
import csv
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import Domain, Observation, MultiAgentObservation, MultiAgentComponent, Predicate

from sam_learning.core import LearnerDomain, VocabularyCreator
from statistics.discrete_precision_recall_calculator import PrecisionRecallCalculator
from utilities import LearningAlgorithmType, NegativePreconditionPolicy

LEARNED_ACTIONS_STATS_COLUMNS = [
    "learning_algorithm",
    "policy",
    "domain_name",
    "num_trajectories",
    "learning_time",
    "num_trajectory_triplets",
    "total_number_of_actions",
    "learned_action_name",
    "num_triplets_action_appeared",
    "num_pb_literals",
    "num_pb_functions",
    "learned_discrete_preconditions",
    "num_learned_positive_preconditions",
    "num_learned_negative_preconditions",
    "num_learned_add_effects",
    "num_learned_delete_effects",
    "num_ground_truth_positive_preconditions",
    "num_ground_truth_negative_preconditions",
    "num_ground_truth_add_effects",
    "num_ground_truth_delete_effects",
    "learned_discrete_effects",
    "num_discrete_effects",
    "ground_truth_preconditions",
    "ground_truth_effects",
    "preconditions_precision",
    "effects_precision",
    "preconditions_recall",
    "effects_recall",
    "action_precision",
    "action_recall",
    "f1_score",
]
UNSAFE_LEARNING_ALGORITHMS = [
    LearningAlgorithmType.plan_miner,
]


class LearningStatisticsManager:
    """Class that manages the statistics about the action's learning properties gathered from the learning process."""

    model_domain: Domain
    learning_algorithm: LearningAlgorithmType
    working_directory_path: Path
    results_dir_path: Path
    action_learning_stats: List[Dict[str, Any]]
    numeric_learning_stats: List[Dict[str, Any]]
    merged_numeric_stats: List[Dict[str, Any]]
    merged_action_stats: List[Dict[str, Any]]

    def __init__(self, working_directory_path: Path, domain_path: Path, learning_algorithm: LearningAlgorithmType):
        self.working_directory_path = working_directory_path
        self.model_domain = DomainParser(domain_path=domain_path, partial_parsing=False).parse_domain()
        self.learning_algorithm = learning_algorithm
        self.action_learning_stats = []
        self.numeric_learning_stats = []
        self.merged_action_stats = []
        self.merged_numeric_stats = []
        self.results_dir_path = self.working_directory_path / "results_directory"
        self.vocabulary_creator = VocabularyCreator()

    @staticmethod
    def _update_action_appearances(used_observations: List[Union[Observation, MultiAgentObservation]]) -> Counter:
        """Updates the number of times each action appeared in the input trajectories.

        :param used_observations: the observations used to learn the actions.
        :return: Counter object mapping the action name to the number of appearances.
        """
        action_appearance_counter = Counter()
        for observation in used_observations:
            for component in observation.components:
                if isinstance(component, MultiAgentComponent):
                    for action in component.grounded_joint_action.actions:
                        action_appearance_counter[action.name] += 1
                else:
                    action_appearance_counter[component.grounded_action_call.name] += 1
        return action_appearance_counter

    def _extract_all_preconditions(self, action_name, learned_domain):
        learned_preconditions = [p.untyped_representation for _, p in learned_domain.actions[action_name].preconditions if isinstance(p, Predicate)]
        ground_truth_preconditions = [
            p.untyped_representation for _, p in self.model_domain.actions[action_name].preconditions if isinstance(p, Predicate)
        ]
        return ground_truth_preconditions, learned_preconditions

    def create_results_directory(self) -> None:
        """Creates the results' directory that contains the learning results."""
        self.results_dir_path.mkdir(exist_ok=True)

    def _add_default_statistic_fields(
        self,
        action_name: str,
        learning_report: Optional[Dict[str, str]],
        policy: NegativePreconditionPolicy,
        used_observations: List[Union[Observation, MultiAgentObservation]],
    ) -> Dict[str, Any]:
        """Adds the default fields to the action statistics (those not inferred from the learning process).

        :param action_name: the name of the action.
        :param learning_report: the report on the status of the learned actions, whether they were safe to learn or not.
        :param policy: the policy used to remove the negative preconditions from the action.
        :param used_observations: the observations that were used to learn the action.
        :return: the dictionary containing the default fields.
        """
        learning_time = float(learning_report["learning_time"])
        action_appearance_counter = self._update_action_appearances(used_observations)
        num_triplets = sum([len(observation.components) for observation in used_observations])
        ground_truth_preconditions = [p for _, p in self.model_domain.actions[action_name].preconditions if isinstance(p, Predicate)]
        ground_truth_effects = [p for p in self.model_domain.actions[action_name].discrete_effects]
        action_pbls_vocabulary = self.vocabulary_creator.create_lifted_vocabulary(
            domain=self.model_domain, possible_parameters=self.model_domain.actions[action_name].signature
        )
        action_pb_function_vocabulary = self.vocabulary_creator.create_lifted_functions_vocabulary(
            domain=self.model_domain, possible_parameters=self.model_domain.actions[action_name].signature
        )
        return {
            "learning_algorithm": self.learning_algorithm.name,
            "policy": policy.name,
            "domain_name": self.model_domain.name,
            "num_trajectories": len(used_observations),
            "learning_time": learning_time,
            "num_trajectory_triplets": num_triplets,
            "total_number_of_actions": len(self.model_domain.actions),
            "learned_action_name": action_name,
            "num_triplets_action_appeared": action_appearance_counter[action_name],
            "num_pb_literals": len(action_pbls_vocabulary),
            "num_pb_functions": len(action_pb_function_vocabulary),
            "num_ground_truth_positive_preconditions": len([p for p in ground_truth_preconditions if p.is_positive]),
            "num_ground_truth_negative_preconditions": len([p for p in ground_truth_preconditions if not p.is_positive]),
            "num_ground_truth_add_effects": len([p for p in ground_truth_effects if p.is_positive]),
            "num_ground_truth_delete_effects": len([p for p in ground_truth_effects if not p.is_positive]),
            "ground_truth_preconditions": [p.untyped_representation for p in ground_truth_preconditions],
            "ground_truth_effects": [p.untyped_representation for p in ground_truth_effects],
        }

    def add_to_action_stats(
        self,
        used_observations: List[Union[Observation, MultiAgentObservation]],
        learned_domain: LearnerDomain,
        learning_report: Optional[Dict[str, str]] = None,
        policy: NegativePreconditionPolicy = NegativePreconditionPolicy.no_remove,
    ) -> None:
        """Add the action data to the statistics.

        :param used_observations: the observations that were used to learn the action.
        :param learned_domain: the domain that was learned from the action model learning algorithm.
        :param learning_report: the report on the status of the learned actions, whether they were safe to learn or not.
        :param policy: the policy used to remove the negative preconditions from the action.
        """
        precision_recall_calculator = PrecisionRecallCalculator()
        for action_name, action_data in self.model_domain.actions.items():
            if action_name not in learned_domain.actions:
                action_stats = {
                    **self._add_default_statistic_fields(action_name, learning_report, policy, used_observations),
                    "learned_discrete_preconditions": [],
                    "learned_discrete_effects": [],
                    "num_learned_positive_preconditions": 0,
                    "num_learned_negative_preconditions": 0,
                    "num_learned_add_effects": 0,
                    "num_learned_delete_effects": 0,
                    "preconditions_precision": 0,
                    "effects_precision": 1,
                    "preconditions_recall": 1,
                    "effects_recall": 0,
                    "action_precision": 0,
                    "action_recall": 1,
                    "f1_score": 0,
                }
                self.action_learning_stats.append(action_stats)
                continue

            ground_truth_preconditions, learned_preconditions = self._extract_all_preconditions(action_name, learned_domain)
            precision_recall_calculator.add_action_data(learned_domain.actions[action_name], self.model_domain.actions[action_name])
            discrete_preconditions = [p for _, p in learned_domain.actions[action_name].preconditions if isinstance(p, Predicate)]
            learned_discrete_effects = [p.untyped_representation for p in learned_domain.actions[action_name].discrete_effects]
            action_stats = {
                **self._add_default_statistic_fields(action_name, learning_report, policy, used_observations),
                "learned_discrete_preconditions": learned_preconditions,
                "learned_discrete_effects": learned_discrete_effects,
                "num_learned_positive_preconditions": len([p for p in discrete_preconditions if p.is_positive]),
                "num_learned_negative_preconditions": len([p for p in discrete_preconditions if not p.is_positive]),
                "num_learned_add_effects": len([p for p in learned_domain.actions[action_name].discrete_effects if p.is_positive]),
                "num_learned_delete_effects": len([p for p in learned_domain.actions[action_name].discrete_effects if not p.is_positive]),
                **precision_recall_calculator.export_action_syntactic_statistics(action_name),
            }
            self.action_learning_stats.append(action_stats)

    def _export_statistics_data(
        self,
        fold_number: int,
        iteration_num: Optional[int] = None,
        columns: List[str] = [],
        action_data_to_export: List[Dict[str, Any]] = {},
        stats_data_file_name: str = "",
    ) -> None:
        """Exports statistics to a report CSV file.

        :param fold_number: the number of the currently running fold.
        :param iteration_num: the number of the current iteration.
        :param columns: the column names in the CSV report file.
        :param action_data_to_export: the data to export to the report.
        :param stats_data_file_name: the name of the statistics to publish in the report file.
        """
        iterations_suffix = f"_{iteration_num}" if iteration_num is not None else ""
        statistics_path = (
            self.results_dir_path / f"{self.learning_algorithm.name}_{self.model_domain.name}"
            f"_{stats_data_file_name}_{fold_number}{iterations_suffix}.csv"
        )
        with open(statistics_path, "wt", newline="") as statistics_file:
            stats_writer = csv.DictWriter(statistics_file, fieldnames=columns)
            stats_writer.writeheader()
            for data_line in action_data_to_export:
                stats_writer.writerow(data_line)

    def export_action_learning_statistics(self, fold_number: int, iteration_num: Optional[int] = None) -> None:
        """Export the statistics collected about the actions.

        :param fold_number: the number of the currently running fold.
        :param iteration_num: the number of the current iteration.
        """
        self._export_statistics_data(fold_number, iteration_num, LEARNED_ACTIONS_STATS_COLUMNS, self.action_learning_stats, "action_stats_fold")

    def export_all_folds_action_stats(self) -> None:
        """Export the statistics collected about the actions."""
        output_path = self.results_dir_path / f"all_folds_action_learning_stats.csv"
        with open(output_path, "wt", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=LEARNED_ACTIONS_STATS_COLUMNS)
            writer.writeheader()
            writer.writerows(self.merged_action_stats)

    def clear_statistics(self) -> None:
        """Clears the statistics so that each fold will have no relation to its predecessors."""
        self.merged_numeric_stats.extend(self.numeric_learning_stats)
        self.merged_action_stats.extend(self.action_learning_stats)
        self.numeric_learning_stats.clear()
        self.action_learning_stats.clear()

    def write_complete_joint_statistics(self) -> None:
        """Writes a statistics file containing all the folds combined data."""
        output_path = self.results_dir_path / f"{self.learning_algorithm.name}_all_folds_numeric_learning_stats.csv"
        with open(output_path, "wt", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=LEARNED_ACTIONS_STATS_COLUMNS)
            writer.writeheader()
            writer.writerows(self.merged_numeric_stats)
