"""Module that stores amd learns an action's numeric state fluents."""
import logging
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set

import numpy as np
from pddl_plus_parser.models import PDDLFunction, Precondition, NumericalExpressionTree

from sam_learning.core import NotSafeActionError, EquationSolutionType
from sam_learning.core.baseline_algorithms_version.naive_convex_hull_learner import NaiveConvexHullLearner
from sam_learning.core.baseline_algorithms_version.naive_linear_regression_learner import NaiveLinearRegressionLearner

np.seterr(divide='ignore', invalid='ignore')


class NaiveNumericFluentStateStorage:
    """Stores and learned the numeric state fluents of a single action."""

    logger: logging.Logger
    previous_state_storage: Dict[str, List[float]]  # lifted function str -> numeric values.
    negative_samples_storage: Dict[str, List[float]]  # lifted function str -> numeric values.
    next_state_storage: Dict[str, List[float]]  # lifted function str -> numeric values.

    def __init__(self, action_name: str, domain_functions: Dict[str, PDDLFunction]):
        self.logger = logging.getLogger(__name__)
        self.previous_state_storage = defaultdict(list)
        self.next_state_storage = defaultdict(list)
        self.action_name = action_name
        self.convex_hull_learner = NaiveConvexHullLearner(action_name, domain_functions)
        self.linear_regression_learner = NaiveLinearRegressionLearner(action_name, domain_functions)

    def add_to_previous_state_storage(self, state_fluents: Dict[str, PDDLFunction]) -> None:
        """Adds the matched lifted state fluents to the previous state storage.

        :param state_fluents: the lifted state fluents that were matched for the action.
        """
        for state_fluent_lifted_str, state_fluent_data in state_fluents.items():
            self.previous_state_storage[state_fluent_lifted_str].append(state_fluent_data.value)

    def add_to_next_state_storage(self, state_fluents: Dict[str, PDDLFunction]) -> None:
        """Adds the matched lifted state fluents to the next state storage.

        :param state_fluents: the lifted state fluents that were matched for the action.
        """
        for state_fluent_lifted_str, state_fluent_data in state_fluents.items():
            self.next_state_storage[state_fluent_lifted_str].append(state_fluent_data.value)
            if len(self.previous_state_storage.get(state_fluent_lifted_str, [])) != \
                    len(self.next_state_storage[state_fluent_lifted_str]):
                self.logger.debug("This is a case where effects create new fluents - should adjust the previous state.")
                self.previous_state_storage[state_fluent_lifted_str].append(0)

    def filter_out_inconsistent_state_variables(self) -> None:
        """Filters out fluents that appear only in part of the states since they are not safe.

        :return: only the safe state variables that appear in *all* states.
        """
        max_function_len = max([len(values) for values in self.previous_state_storage.values()])
        self.previous_state_storage = {lifted_function: state_values for lifted_function, state_values in
                                       self.previous_state_storage.items() if len(state_values) == max_function_len}
        self.next_state_storage = {lifted_function: state_values for lifted_function, state_values in
                                   self.next_state_storage.items() if len(state_values) == max_function_len}

    def construct_safe_linear_inequalities(
            self, relevant_fluents: Optional[List[str]] = None) -> Precondition:
        """Constructs the linear inequalities strings that will be used in the learned model later.

        :return: The precondition that contains the linear inequalities.
        """
        return self.convex_hull_learner.construct_safe_linear_inequalities(
            self.previous_state_storage, relevant_fluents)

    def _validate_safe_solving(self) -> None:
        """Validates that it is safe to apply linear regression to solve the input equations."""
        for lifted_function in self.next_state_storage:
            num_variables = len(self.previous_state_storage)
            num_equations = len(self.next_state_storage[lifted_function])
            # validate that it is possible to solve linear equations at all.
            if num_equations < num_variables or num_equations == num_variables == 1:
                failure_reason = f"Cannot solve linear equations when too little input equations given."
                self.logger.warning(failure_reason)
                raise NotSafeActionError(
                    self.action_name, failure_reason, EquationSolutionType.not_enough_data)

    def construct_assignment_equations(
            self, allow_unsafe_learning: bool = False, relevant_fluents: Optional[List[str]] = None) -> Tuple[
        Set[NumericalExpressionTree], Optional[Precondition], bool]:
        """Constructs the assignment statements for the action according to the changed value functions.

        :param allow_unsafe_learning: whether to allow learning from unsafe data.
        :param relevant_fluents: the fluents that are part of the action's preconditions and effects.
        :return: the constructed assignment statements.
        """
        self._validate_safe_solving()
        return self.linear_regression_learner.construct_assignment_equations(
            self.previous_state_storage, self.next_state_storage, allow_unsafe_learning=allow_unsafe_learning, relevant_fluents=relevant_fluents)
