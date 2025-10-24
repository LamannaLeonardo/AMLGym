"""This module contains the ConvexHullLearner class."""
import logging
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from pddl_plus_parser.models import Precondition, PDDLFunction
from scipy.spatial import ConvexHull, QhullError

from sam_learning.core.exceptions import NotSafeActionError
from sam_learning.core.learning_types import ConditionType, EquationSolutionType
from sam_learning.core.numeric_learning.numeric_utils import (
    prettify_coefficients,
    construct_numeric_conditions,
    construct_projected_variable_strings,
    extended_gram_schmidt,
    display_convex_hull,
    create_monomials,
    create_polynomial_string,
    divide_span_by_common_denominator,
    remove_complex_linear_dependencies,
    construct_pddl_inequality_scheme,
)

np.set_printoptions(precision=2)


class ConvexHullLearner:
    """Class that learns the convex hull of the preconditions of an action."""

    logger: logging.Logger
    action_name: str
    domain_functions: Dict[str, PDDLFunction]
    convex_hull_error_file_path: Path
    data: DataFrame

    def __init__(
        self, action_name: str, domain_functions: Dict[str, PDDLFunction], polynom_degree: int = 0, epsilon: float = 0.0, qhull_options: str = ""
    ):
        self.logger = logging.getLogger(__name__)
        self.convex_hull_error_file_path = Path(os.environ["CONVEX_HULL_ERROR_PATH"])
        functions = list([function.untyped_representation for function in domain_functions.values()])
        monomials = create_monomials(functions, polynom_degree)
        self.data = DataFrame(columns=[create_polynomial_string(monomial) for monomial in monomials])
        self.action_name = action_name
        self.domain_functions = {function.name: function for function in domain_functions.values()}
        self._epsilon = epsilon
        self._qhull_options = qhull_options

    def add_new_point(self, point: Dict[str, float]) -> None:
        """Adds a new point to the convex hull learner.

        Note:
            This method is supposed to improve the performance of the CH calculations by incrementally adding points.

        :param point: the point to add to the convex hull learner.
        """
        new_sample = DataFrame.from_dict(data={key: [value] for key, value in point.items()}, orient="columns")
        # assuming that if a feature is relevant to the preconditions it should always appear in the dataframe.
        if len(self.data) == 0:
            self.data = new_sample  # This is to avoid observing warnings when adding the first sample.
            self.logger.debug("Added the first sample to the points dataframe.")
            return

        concat_data = pd.concat([self.data, new_sample], ignore_index=True).dropna(axis=1)
        if concat_data.drop_duplicates().shape[0] == self.data.shape[0]:
            self.logger.debug("The new point is already in the storage, not adding it again.")
            return

        self.data = concat_data

    def _epsilon_approximate_hull(self, points: np.ndarray, incremental: bool = False) -> ConvexHull:
        """Approximates the convex hull of the given points with a margin of epsilon and a set of options for the qhull algorithm..

        :param points: The points comprising the convex hull.
        :param incremental: whether to use the incremental version of the qhull algorithm.
        :return: the approximated convex hull.
        """
        self.logger.debug(f"Approximating the convex hull with epsilon {self._epsilon}.")
        # Step 1: Compute the original convex hull
        hull = ConvexHull(points, incremental=incremental)
        if self._epsilon == 0.0 and self._qhull_options == "":
            return hull

        # Step 2: Find the centroid of the original hull (for expanding outward)
        centroid = np.mean(points[hull.vertices], axis=0)

        # Step 3: Calculate new points on expanded facets to include epsilon margin
        expanded_points = []
        for simplex in hull.simplices:
            # Get the points of the simplex (facet)
            facet_points = points[simplex]
            # Calculate the direction vectors from the centroid to each facet point
            directions = facet_points - centroid
            # Normalize directions and expand each point by (1 + epsilon)
            expanded_facet = centroid + (1 + self._epsilon) * directions
            expanded_points.extend(expanded_facet)

        # Combine original points with expanded points
        all_points = np.vstack([points, expanded_points])

        # Step 4: Compute the approximated convex hull on the expanded point set
        approx_hull = ConvexHull(all_points, qhull_options=self._qhull_options, incremental=incremental)
        return approx_hull

    def _execute_convex_hull(self, points: np.ndarray, display_mode: bool = True) -> Tuple[List[List[float]], List[float]]:
        """Runs the convex hull algorithm on the given input points.

        :param points: the points to run the convex hull algorithm on.
        :param display_mode: whether to display the convex hull.
        :return: the coefficients of the planes that represent the convex hull and the border point.
        """
        hull = self._epsilon_approximate_hull(points)
        display_convex_hull(self.action_name, display_mode, hull)
        equations = np.unique(hull.equations, axis=0)

        A = equations[:, : points.shape[1]]
        b = -equations[:, points.shape[1]]
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
        points = points_df.to_numpy()
        shift_axis = points[0].tolist()  # selected the first vector to be the start of the axis.
        shifted_points = points - shift_axis
        self.logger.debug("Finding the basis vectors for the projected CH using the extended Gram-Schmidt method.")
        projection_basis = extended_gram_schmidt(shifted_points)
        if len(shifted_points) > len(points_df.columns.tolist()) and len(projection_basis) >= len(points_df.columns.tolist()):
            self.logger.debug("The points are spanning the original space and the basis is full rank, " "no need to project the points.")
            coefficients, border_point = self._execute_convex_hull(points, display_mode)
            return coefficients, border_point, points_df.columns.tolist(), []

        projected_points = np.dot(shifted_points, np.array(projection_basis).T)
        if projected_points.shape[1] == 1:
            border_point, coefficients = self._construct_single_dimension_convex_hull(projected_points)

        else:
            coefficients, border_point = self._execute_convex_hull(projected_points, display_mode)

        transformed_vars = construct_projected_variable_strings(points_df.columns.tolist(), shift_axis, projection_basis)

        self.logger.debug("Constructing the conditions to verify that points are in the correct span.")
        diagonal_eye = [list(vector) for vector in np.eye(points.shape[1])]
        orthnormal_span = divide_span_by_common_denominator(extended_gram_schmidt(diagonal_eye, projection_basis))
        transformed_orthonormal_vars = construct_projected_variable_strings(points_df.columns.tolist(), shift_axis, diagonal_eye)
        span_verification_conditions = construct_pddl_inequality_scheme(
            np.array(orthnormal_span), np.zeros(len(orthnormal_span)), transformed_orthonormal_vars, sign_to_use="="
        )
        return coefficients, border_point, transformed_vars, span_verification_conditions

    def _construct_single_dimension_convex_hull(self, projected_points: np.array) -> Tuple[List[float], List[float]]:
        """Construct the convex hull for a single dimension.

        :param projected_points: the projected points on the single dimension.
        :return: the border point and the coefficients of the planes that represent the convex hull.
        """
        self.logger.debug("The convex hull is single dimensional, creating min-max conditions on the new basis.")
        coefficients = [[-1], [1]]
        border_point = prettify_coefficients([-projected_points.min(), projected_points.max()])
        return border_point, coefficients

    def _create_disjunctive_preconditions(self, previous_state_matrix: DataFrame, equality_conditions: List[str] = []) -> Precondition:
        """Create the disjunctive representation of the preconditions.

        :param previous_state_matrix: the matrix containing the previous state values.
        :return: a disjunctive representation for the precondition in case a convex hull cannot be created.
        """
        if previous_state_matrix.shape[0] == 1:
            extended_conditions = [*equality_conditions]
            extended_conditions.extend([f"(= {column} {previous_state_matrix[column].iloc[0]})" for column in previous_state_matrix.columns])
            return construct_numeric_conditions(extended_conditions, condition_type=ConditionType.conjunctive, domain_functions=self.domain_functions)

        disjunctive_precondition = Precondition("or")
        for _, row in previous_state_matrix.iterrows():
            conjunctive_conditions = []
            for column in previous_state_matrix.columns:
                conjunctive_conditions.append(f"(= {column} {row[column]})")

            disjunctive_precondition.add_condition(
                construct_numeric_conditions(
                    conjunctive_conditions, condition_type=ConditionType.conjunctive, domain_functions=self.domain_functions,
                )
            )

        if len(equality_conditions) > 0:
            combined_condition = construct_numeric_conditions(
                equality_conditions, condition_type=ConditionType.conjunctive, domain_functions=self.domain_functions
            )
            combined_condition.add_condition(disjunctive_precondition)
            return combined_condition

        return disjunctive_precondition

    def _construct_single_dimension_inequalities(self, single_column_df: Series) -> Precondition:
        """Construct a single dimension precondition representation.

        :param single_column_df: the fluent only fluent that is relevant to the preconditions' creation.
        :return: the preconditions string and the condition type.
        """
        min_value = single_column_df.min()
        max_value = single_column_df.max()
        relevant_fluent = single_column_df.name
        if min_value == max_value:
            conditions = [f"(= {relevant_fluent} {min_value})"]
        else:
            conditions = [f"(>= {relevant_fluent} {min_value})", f"(<= {relevant_fluent} {max_value})"]

        return construct_numeric_conditions(conditions, condition_type=ConditionType.conjunctive, domain_functions=self.domain_functions)

    def construct_safe_linear_inequalities(self, relevant_fluents: Optional[List[str]] = None) -> Precondition:
        """Constructs the linear inequalities strings that will be used in the learned model later.

        :param relevant_fluents: the relevant fluents that are used to create the convex hull.
        :return: the inequality strings and the type of equations that were constructed (injunctive / disjunctive)
        """
        irrelevant_fluents = (
            [fluent for fluent in self.data.columns.tolist() if fluent not in relevant_fluents] if relevant_fluents is not None else []
        )
        state_data = self.data.drop(columns=irrelevant_fluents)
        if (relevant_fluents is not None and len(relevant_fluents) == 1) or state_data.shape[1] == 1:
            self.logger.debug("Only one dimension is needed in the preconditions!")
            relevant_fluents = state_data.columns.tolist() if relevant_fluents is None else relevant_fluents
            return self._construct_single_dimension_inequalities(state_data.loc[:, relevant_fluents[0]])

        try:
            filtered_dataframe, extra_conditions = remove_complex_linear_dependencies(state_data)
            if filtered_dataframe.shape[0] == 0:
                self.logger.warning("The matrix is empty, no need to create a convex hull.")
                return construct_numeric_conditions(
                    extra_conditions, condition_type=ConditionType.conjunctive, domain_functions=self.domain_functions
                )

            if filtered_dataframe.shape[1] == 1:
                self.logger.debug("After filtering the linear dependencies remained with a single feature!")
                b, A = self._construct_single_dimension_convex_hull(filtered_dataframe.to_numpy())
                inequalities_strs = construct_pddl_inequality_scheme(A, b, filtered_dataframe.columns.tolist())
                return construct_numeric_conditions(
                    [*inequalities_strs, *extra_conditions], condition_type=ConditionType.conjunctive, domain_functions=self.domain_functions
                )

            A, b, column_names, additional_projection_conditions = self._create_convex_hull_linear_inequalities(
                filtered_dataframe, display_mode=False
            )
            inequalities_strs = construct_pddl_inequality_scheme(A, b, column_names)
            if additional_projection_conditions is not None:
                inequalities_strs.extend([*extra_conditions, *additional_projection_conditions])

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
