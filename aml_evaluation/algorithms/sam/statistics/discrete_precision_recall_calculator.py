from collections import defaultdict
from typing import Dict, Set, List

from pddl_plus_parser.models import Action, Predicate

from sam_learning.core import LearnerAction


def calculate_number_true_positives(learned_predicates: Set[str], expected_predicates: Set[str]) -> int:
    """Calculates the number of predicates that appear both in the model domain and in the learned domain.

    :param learned_predicates: the predicates that belong in the learned domain.
    :param expected_predicates: the predicates that belong to the model domain.
    :return: the number of predicates that match in both domains.
    """
    return len(learned_predicates.intersection(expected_predicates))


def calculate_number_false_positives(learned_predicates: Set[str], expected_predicates: Set[str]) -> int:
    """Calculates the number of predicates that appear in the learned domain but are not in the model domain.

    :param learned_predicates: the predicates that belong in the learned domain.
    :param expected_predicates: the predicates that belong to the model domain.
    :return: the number of predicates that belong to the learned domain and not the model domain.
    """
    return len(learned_predicates.difference(expected_predicates))


def calculate_number_false_negatives(learned_predicates: Set[str], expected_predicates: Set[str]) -> int:
    """Calculates the number of predicates that are missing in the learned domain from the model domain.

    :param learned_predicates: the predicates that belong in the learned domain.
    :param expected_predicates: the predicates that belong to the model domain.
    :return: the number of predicates missing in the learned domain.
    """
    return len(expected_predicates.difference(learned_predicates))


def calculate_syntactic_recall(learned_predicates: Set[str], actual_predicates: Set[str]) -> float:
    """Calculates the recall value of the input predicates.

    :param learned_predicates: the predicates learned using the learning algorithm.
    :param actual_predicates: the predicates belonging to the model domain.
    :return: the recall value.
    """
    if len(actual_predicates) == 0:
        return 1

    if len(learned_predicates) == 0:
        return 0

    true_positives = calculate_number_true_positives(learned_predicates, actual_predicates)
    false_negatives = calculate_number_false_negatives(learned_predicates, actual_predicates)
    return true_positives / (true_positives + false_negatives)


def calculate_syntactic_precision(learned_predicates: Set[str], actual_predicates: Set[str]) -> float:
    """Calculates the precision value of the input predicates.

    :param learned_predicates: the predicates learned using the learning algorithm.
    :param actual_predicates: the predicates belonging to the model domain.
    :return: the precision value.
    """
    if len(learned_predicates) == 0:
        if len(actual_predicates) == 0:
            return 1

        return 0

    true_positives = calculate_number_true_positives(learned_predicates, actual_predicates)
    false_positives = calculate_number_false_positives(learned_predicates, actual_predicates)
    return true_positives / (true_positives + false_positives)


class PrecisionRecallCalculator:
    """Class that manages the calculation of the precision and recall of the learned model."""

    preconditions: Dict[str, Set[str]]
    ground_truth_preconditions: Dict[str, Set[str]]
    discrete_effects: Dict[str, Set[str]]
    ground_discrete_effects: Dict[str, Set[str]]
    _learned_actions: List[str]

    def __init__(self):
        self.preconditions = defaultdict(set)
        self.ground_truth_preconditions = defaultdict(set)
        self.discrete_effects = defaultdict(set)
        self.ground_discrete_effects = defaultdict(set)
        self._compared_tuples = [(self.preconditions, self.ground_truth_preconditions), (self.discrete_effects, self.ground_discrete_effects)]
        self._learned_actions = []

    def add_action_data(self, learned_action: LearnerAction, model_action: Action) -> None:
        """Adds the discrete action's data to the class data to calculate the precision and recall values.

        :param learned_action: the action that was learned using the action model learning algorithm.
        :param model_action: the expected action of the original domain.
        """
        self._learned_actions.append(learned_action.name)
        self.preconditions[learned_action.name] = {p.untyped_representation for _, p in learned_action.preconditions if isinstance(p, Predicate)}

        self.ground_truth_preconditions[model_action.name] = {
            p.untyped_representation for _, p in model_action.preconditions if isinstance(p, Predicate)
        }

        self.discrete_effects[learned_action.name] = {p.untyped_representation for p in learned_action.discrete_effects}
        self.ground_discrete_effects[model_action.name] = {p.untyped_representation for p in model_action.discrete_effects}

    def calculate_action_precision(self, action_name: str) -> float:
        """calculates the precision value of a certain action.

        :param action_name: the name of the action that is being tested.
        :return: the action's precision.
        """
        true_positives = sum(calculate_number_true_positives(tup[0][action_name], tup[1][action_name]) for tup in self._compared_tuples)
        false_positives = sum(calculate_number_false_positives(tup[0][action_name], tup[1][action_name]) for tup in self._compared_tuples)
        if true_positives == 0 and false_positives == 0:
            return 1

        return true_positives / (true_positives + false_positives)

    def calculate_action_recall(self, action_name: str) -> float:
        """calculates the recall value of a certain action.

        :param action_name: the name of the action that is being tested.
        :return: the action's recall.
        """
        true_positives = sum(calculate_number_true_positives(tup[0][action_name], tup[1][action_name]) for tup in self._compared_tuples)
        false_negatives = sum(calculate_number_false_negatives(tup[0][action_name], tup[1][action_name]) for tup in self._compared_tuples)

        if true_positives == 0 and false_negatives == 0:
            return 1

        return true_positives / (true_positives + false_negatives)

    def calculate_syntactic_precision(self) -> float:
        """calculates the precision value of a learned domain.

        :return: the model's precision.
        """
        true_positives = sum(
            [
                sum(calculate_number_true_positives(tup[0][action_name], tup[1][action_name]) for tup in self._compared_tuples)
                for action_name in self._learned_actions
            ]
        )
        false_positives = sum(
            [
                sum(calculate_number_false_positives(tup[0][action_name], tup[1][action_name]) for tup in self._compared_tuples)
                for action_name in self._learned_actions
            ]
        )
        if true_positives == 0 and false_positives == 0:
            return 1

        return true_positives / (true_positives + false_positives)

    def calculate_syntactic_recall(self) -> float:
        """calculates the recall value of a learned domain.

        :return: the model's recall.
        """
        true_positives = sum(
            [
                sum(calculate_number_true_positives(tup[0][action_name], tup[1][action_name]) for tup in self._compared_tuples)
                for action_name in self._learned_actions
            ]
        )
        false_negatives = sum(
            [
                sum(calculate_number_false_negatives(tup[0][action_name], tup[1][action_name]) for tup in self._compared_tuples)
                for action_name in self._learned_actions
            ]
        )
        if true_positives == 0 and false_negatives == 0:
            return 1

        return true_positives / (true_positives + false_negatives)

    def export_action_syntactic_statistics(self, action_name: str) -> Dict[str, float]:
        """Export the statistics of an action that was observed during the learning process.

        :param action_name: the name of the action that was learned.
        :return: the dictionary containing the precision and recall statistics of the action.
        """
        action_precision = self.calculate_action_precision(action_name)
        action_recall = self.calculate_action_recall(action_name)
        action_f1_score = (
            0 if action_precision == 0 and action_recall == 0 else 2 * (action_precision * action_recall) / (action_precision + action_recall)
        )

        return {
            "preconditions_precision": calculate_syntactic_precision(self.preconditions[action_name], self.ground_truth_preconditions[action_name]),
            "effects_precision": calculate_syntactic_precision(self.discrete_effects[action_name], self.ground_discrete_effects[action_name]),
            "preconditions_recall": calculate_syntactic_recall(self.preconditions[action_name], self.ground_truth_preconditions[action_name]),
            "effects_recall": calculate_syntactic_recall(self.discrete_effects[action_name], self.ground_discrete_effects[action_name]),
            "action_precision": action_precision,
            "action_recall": action_recall,
            "f1_score": action_f1_score,
        }
