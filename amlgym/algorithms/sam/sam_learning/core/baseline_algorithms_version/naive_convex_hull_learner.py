"""This module contains the ConvexHullLearner class."""
import logging
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame, Series
from pddl_plus_parser.models import Precondition, PDDLFunction
from scipy.spatial import ConvexHull, convex_hull_plot_2d, QhullError

from sam_learning.core import NotSafeActionError
from sam_learning.core.learning_types import ConditionType, EquationSolutionType
from sam_learning.core.numeric_learning.numeric_utils import (
    construct_multiplication_strings,
    construct_linear_equation_string,
    prettify_coefficients,
    construct_numeric_conditions,
    filter_constant_features,
    detect_linear_dependent_features,
)

EPSILON = 1e-10


class NaiveConvexHullLearner:
    """Class that learns the convex hull of the preconditions of an action."""

    logger: logging.Logger
    action_name: str
    domain_functions: Dict[str, PDDLFunction]
    convex_hull_error_file_path: Path

    def __init__(self, action_name: str, domain_functions: Dict[str, PDDLFunction]):
        self.logger = logging.getLogger(__name__)
        self.convex_hull_error_file_path = Path(os.environ["CONVEX_HULL_ERROR_PATH"])
        self.action_name = action_name
        self.domain_functions = domain_functions

    def _execute_convex_hull(self, points: np.ndarray, display_mode: bool = True) -> Tuple[List[List[float]], List[float]]:
        """Runs the convex hull algorithm on the given input points.

        :param points: the points to run the convex hull algorithm on.
        :param display_mode: whether to display the convex hull.
        :return: the coefficients of the planes that represent the convex hull and the border point.
        """
        hull = ConvexHull(points)
        self._display_convex_hull(display_mode, hull, points.shape[1])

        A = hull.equations[:, : points.shape[1]]
        b = -hull.equations[:, points.shape[1]]
        coefficients = [prettify_coefficients(row) for row in A]
        border_point = prettify_coefficients(b)
        return coefficients, border_point

    def _create_convex_hull_linear_inequalities(
        self, points_df: DataFrame, display_mode: bool = True
    ) -> Tuple[List[List[float]], List[float], List[str], Optional[List[str]]]:
        """Create the convex hull and returns the matrix representing the inequalities.

        :param points_df: the dataframe containing the points that represent the values of the function in the states
            of the observations prior to the action's execution.
        :return: the matrix representing the inequalities of the planes created by the convex hull as well as the
            names of the features that are part of the convex hull.

        Note: the returned values represents the linear inequalities of the convex hull, i.e.,  Ax <= b.
        """
        self.logger.debug(f"Creating convex hull for action {self.action_name}.")
        extra_conditions = []
        columns_to_use = points_df.columns.tolist()
        if points_df.shape[1] == 1:
            points = points_df.to_numpy()
            self.logger.debug("The convex hull is single dimensional, creating min-max conditions on the new basis.")
            coefficients = [[-1], [1]]
            border_point = prettify_coefficients([-points.min(), points.max()])

        else:
            no_constant_columns_matrix, equality_strs, removed_fluents = filter_constant_features(points_df)
            filtered_previous_state_matrix, column_equality_strs, removed_fluents = detect_linear_dependent_features(no_constant_columns_matrix)
            coefficients, border_point = self._execute_convex_hull(filtered_previous_state_matrix.to_numpy(), display_mode)
            extra_conditions = [*equality_strs, *column_equality_strs]
            columns_to_use = filtered_previous_state_matrix.columns.tolist()

        return coefficients, border_point, columns_to_use, extra_conditions

    @staticmethod
    def _construct_pddl_inequality_scheme(
        coefficient_matrix: np.ndarray, border_points: np.ndarray, headers: List[str], sign_to_use: str = "<="
    ) -> List[str]:
        """Construct the inequality strings in the appropriate PDDL format.

        :param coefficient_matrix: the matrix containing the coefficient vectors for each inequality.
        :param border_points: the convex hull point which ensures that Ax <= b.
        :param headers: the headers of the columns in the coefficient matrix.
        :param sign_to_use: the sign to use in the inequalities (for cases when we want to use equalities).
        :return: the inequalities PDDL formatted strings.
        """
        inequalities = set()
        for inequality_coefficients, border_point in zip(coefficient_matrix, border_points):
            multiplication_functions = construct_multiplication_strings(inequality_coefficients, headers)
            constructed_left_side = construct_linear_equation_string(multiplication_functions)
            inequalities.add(f"({sign_to_use} {constructed_left_side} {border_point})")

        return list(inequalities)

    def _display_convex_hull(self, display_mode: bool, hull: ConvexHull, num_dimensions: int) -> None:
        """Displays the convex hull in as a plot.

        :param display_mode: whether to display the plot.
        :param hull: the convex hull to display.
        :param num_dimensions: the number of dimensions of the original data.
        """
        if not display_mode:
            return

        if num_dimensions == 2:
            _ = convex_hull_plot_2d(hull)
            plt.title(f"{self.action_name} - convex hull")
            plt.show()

        elif num_dimensions == 3:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            ax.plot_trisurf(hull.points[:, 0], hull.points[:, 1], hull.points[:, 2], triangles=hull.simplices)
            plt.title(f"{self.action_name} - convex hull")
            plt.show()

    def _construct_single_dimension_inequalities(self, single_column_df: Series, equality_strs: List[str] = []) -> Precondition:
        """Construct a single dimension precondition representation.

        :param single_column_df: the fluent only fluent that is relevant to the preconditions' creation.
        :param equality_strs: the equality conditions that are already present in the preconditions.
        :return: the preconditions string and the condition type.
        """
        min_value = single_column_df.min()
        max_value = single_column_df.max()
        relevant_fluent = single_column_df.name
        if min_value == max_value:
            conditions = [f"(= {relevant_fluent} {min_value})"]
        else:
            conditions = [f"(>= {relevant_fluent} {min_value})", f"(<= {relevant_fluent} {max_value})"]

        conditions.extend(equality_strs)
        return construct_numeric_conditions(conditions, condition_type=ConditionType.conjunctive, domain_functions=self.domain_functions)

    def construct_safe_linear_inequalities(self, state_storge: Dict[str, List[float]], relevant_fluents: Optional[List[str]] = []) -> Precondition:
        """Constructs the linear inequalities strings that will be used in the learned model later.

        :return: the inequality strings and the type of equations that were constructed (injunctive / disjunctive)
        """
        irrelevant_fluents = [fluent for fluent in state_storge.keys() if fluent not in relevant_fluents] if relevant_fluents is not None else []
        state_data = DataFrame(state_storge).drop_duplicates().drop(columns=irrelevant_fluents)
        if relevant_fluents is not None and len(relevant_fluents) == 1:
            self.logger.debug("Only one dimension is needed in the preconditions!")
            return self._construct_single_dimension_inequalities(state_data.loc[:, relevant_fluents[0]])

        try:
            A, b, column_names, additional_projection_conditions = self._create_convex_hull_linear_inequalities(state_data, display_mode=False)
            inequalities_strs = self._construct_pddl_inequality_scheme(A, b, column_names)
            if additional_projection_conditions is not None:
                inequalities_strs.extend(additional_projection_conditions)

            return construct_numeric_conditions(inequalities_strs, condition_type=ConditionType.conjunctive, domain_functions=self.domain_functions)

        except (QhullError, ValueError):
            self.logger.warning(
                "Convex hull failed to create a convex hull, using disjunctive preconditions "
                "(probably since the rank of the matrix is 2 and it cannot create a degraded "
                "convex hull)."
            )
            raise NotSafeActionError(
                name=self.action_name, reason="Convex hull failed to create a convex hull", solution_type=EquationSolutionType.convex_hull_not_found
            )
