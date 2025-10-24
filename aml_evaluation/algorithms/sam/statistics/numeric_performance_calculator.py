"""Module responsible for calculating our approach for numeric precision and recall."""
import csv
import os
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Union, Optional

import sklearn
from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import Domain, Observation, MultiAgentObservation

from statistics.performance_calculation_utils import _ground_executed_action
from statistics.semantic_performance_calculator import SemanticPerformanceCalculator
from utilities import LearningAlgorithmType
from utilities.util_types import NUMERIC_PRECISION, NegativePreconditionPolicy

NUMERIC_PERFORMANCE_STATS = [
    "learning_algorithm",
    "policy",
    "action_name",
    "epsilon_precision",
    "num_trajectories",
    "precondition_precision",
    "precondition_recall",
    "effects_precision",
    "effects_recall",
    "effects_mse",
]

MAX_INT = 10 ** 6


class NumericPerformanceCalculator(SemanticPerformanceCalculator):
    """Class responsible for calculating the numeric precision and recall of a model."""

    def __init__(
        self,
        model_domain: Domain,
        model_domain_path: Path,
        observations: List[Union[Observation, MultiAgentObservation]],
        working_directory_path: Path,
        learning_algorithm: LearningAlgorithmType,
    ):
        super().__init__(model_domain, model_domain_path, observations, working_directory_path, learning_algorithm)
        self.epsilon_precision = 10 ** (-int(os.environ.get(NUMERIC_PRECISION, 4)))

    def calculate_effects_mse(self, learned_domain: Domain) -> Dict[str, float]:
        """Calculates the effects MSE value using the actual state fluents and the ones generated using the learned
            action.

        Note:
            The final value is averaged over the number of states per action.

        :param learned_domain: the domain that was learned by the action model learning algorithm.
        :return: a mapping between the action name and its MSE value.
        """
        squared_errors = defaultdict(list)
        mse_values = {action_name: 0 for action_name in learned_domain.actions.keys()}
        for observation in self.dataset_observations:
            for observation_component in observation.components:
                action_call = observation_component.grounded_action_call
                previous_state = observation_component.previous_state
                if action_call.name not in learned_domain.actions:
                    continue

                grounded_operator = _ground_executed_action(action_call, learned_domain, observation.grounded_objects)
                grounded_model_operator = _ground_executed_action(action_call, self.model_domain, observation.grounded_objects)
                try:
                    next_state = grounded_operator.apply(previous_state, allow_inapplicable_actions=False)
                    model_next_state = grounded_model_operator.apply(previous_state, allow_inapplicable_actions=False)

                except ValueError:
                    self.logger.debug("The action is not applicable in the state.")
                    next_state = previous_state.copy()
                    # since the learned action is not applicable in the state there is no point to compare
                    # with an action that is not applicable in the model domain.
                    model_next_state = previous_state.copy()

                except ZeroDivisionError:
                    # If the action performed division by zero the MSE is set to the maximum value.
                    squared_errors[action_call.name].append(MAX_INT)
                    continue

                values = [
                    (next_state.state_fluents[fluent].value, model_next_state.state_fluents[fluent].value)
                    for fluent in next_state.state_fluents.keys()
                ]
                actual_values, expected_values = zip(*values)
                state_mse = sklearn.metrics.mean_squared_error(expected_values, actual_values)
                squared_errors[action_call.name].append(state_mse)

        mse_values.update({action_name: sum(square_errors) / len(square_errors) for action_name, square_errors in squared_errors.items()})
        return mse_values

    def calculate_performance(self, learned_domain_path: Path, num_used_observations: int, policy: NegativePreconditionPolicy) -> None:
        """Calculates the model's performance with both the precision and the recall values calculated.

        :param learned_domain_path: the path to the learned action model.
        :param num_used_observations: the number of observations used to learn the action model.
        :param policy: the policy to use for the negative preconditions.
        """
        super().calculate_performance(learned_domain_path, num_used_observations, policy)
        learned_domain = DomainParser(domain_path=learned_domain_path, partial_parsing=False).parse_domain()
        effects_mse = self.calculate_effects_mse(learned_domain)
        for action in self.model_domain.actions:
            for action_stats in self.combined_stats:
                if action_stats["action_name"] == action and action_stats["num_trajectories"] == num_used_observations:
                    action_stats["effects_mse"] = effects_mse.get(action, 0)
                    action_stats["epsilon_precision"] = self.epsilon_precision
                    break

        self.logger.info(f"Finished calculating the numeric learning performance for {self.learning_algorithm.name}.")

    def export_semantic_performance(self, fold_num: int, iteration_num: Optional[int] = None) -> None:
        """Export the numeric learning statistics to a CSV report file.

        :param fold_num: the fold number of the current experiment.
        :param iteration_num: the iteration number of the current experiment.
        """
        iteration_suffix = f"_{iteration_num}" if iteration_num is not None else ""
        statistics_path = (
            self.results_dir_path / f"{self.learning_algorithm.name}_{self.model_domain.name}"
            f"_numeric_learning_performance_stats_fold_{fold_num}{iteration_suffix}.csv"
        )
        with open(statistics_path, "wt", newline="") as statistics_file:
            stats_writer = csv.DictWriter(statistics_file, fieldnames=NUMERIC_PERFORMANCE_STATS)
            stats_writer.writeheader()
            for data_line in self.combined_stats:
                stats_writer.writerow(data_line)

    def export_combined_semantic_performance(self) -> None:
        """Export the numeric learning statistics to a CSV report file."""
        statistics_path = self.results_dir_path / f"{self.learning_algorithm.name}_{self.model_domain.name}" "combined_numeric_performance.csv"
        with open(statistics_path, "wt", newline="") as statistics_file:
            stats_writer = csv.DictWriter(statistics_file, fieldnames=NUMERIC_PERFORMANCE_STATS)
            stats_writer.writeheader()
            for data_line in self.combined_stats:
                stats_writer.writerow(data_line)
