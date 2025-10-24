"""This module contains the ConvexHullLearner class."""

from typing import Dict, List, Tuple, Optional, Union

import warnings
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from pddl_plus_parser.models import Precondition, PDDLFunction
from scipy.spatial import ConvexHull, QhullError

from sam_learning.core.exceptions import NotSafeActionError
from sam_learning.core.learning_types import ConditionType, EquationSolutionType
from sam_learning.core.numeric_learning.convex_hull_learner import ConvexHullLearner
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
    EPSILON,
    construct_pddl_inequality_scheme,
)

warnings.simplefilter(action="ignore", category=FutureWarning)


class IncrementalConvexHullLearner(ConvexHullLearner):
    """Class that learns the convex hull for the preconditions of an action - incrementally."""

    _convex_hull: Optional[ConvexHull]
    _gsp_base: Optional[List[List[float]]]
    _complementary_base: Optional[List[List[float]]]
    _spanning_standard_base: bool
    data: DataFrame
    relevant_fluents: Optional[List[str]]
    affine_independent_data: DataFrame
    additional_dependency_conditions: List[str]

    def __init__(
        self,
        action_name: str,
        domain_functions: Dict[str, PDDLFunction],
        polynom_degree: int = 0,
        epsilon: float = 0.0,
        qhull_options: str = "",
        relevant_fluents: Optional[List[str]] = None,
    ):
        super().__init__(
            action_name,
            {function.name: function for function in domain_functions.values()},
            polynom_degree=polynom_degree,
        )
        self._convex_hull = None
        self._gsp_base = None
        self._complementary_base = None
        self._spanning_standard_base = False
        self.polynom_degree = polynom_degree
        functions = list([function.untyped_representation for function in domain_functions.values()])
        self.monomials = create_monomials(functions, polynom_degree)
        self.data = DataFrame(columns=[create_polynomial_string(monomial) for monomial in self.monomials])
        self.relevant_fluents = relevant_fluents if relevant_fluents is not None else self.data.columns.tolist()
        self.affine_independent_data = None
        self.additional_dependency_conditions = []
        self._epsilon = epsilon
        self._qhull_options = qhull_options

    @staticmethod
    def _calculate_orthonormal_complementary_base(
        orthonormal_base: List[List[float]], num_dimensions: int
    ) -> List[List[float]]:
        """Calculates the orthonormal complementary base of the given orthonormal base.

        :param orthonormal_base: the orthonormal base spanning the points in the storage dataframe.
        :param num_dimensions: the number of dimensions of the original space.
        :return: the orthonormal complementary base of the given orthonormal base.
        """
        diagonal_eye = [list(vector) for vector in np.eye(num_dimensions)]
        return extended_gram_schmidt(diagonal_eye, orthonormal_base)

    @staticmethod
    def _calculate_orthonormal_base(points_df: DataFrame) -> List[List[float]]:
        """Calculates the orthonormal base of the given points.

        :param points_df: the points to calculate the orthonormal base from.
        :return: the orthonormal base of the given points.
        """
        points = points_df.to_numpy()
        shift_axis = points[0].tolist()  # selected the first vector to be the start of the axis.
        shifted_points = points - shift_axis
        return extended_gram_schmidt(shifted_points)

    def _shift_new_point(self, point: Union[Series, DataFrame]) -> np.ndarray:
        """Shifts the points based on the first sample in the dataframe.

        Note: if the points are spanning the original space, we do not need to shift the points.

        :return: the shifted point based on the first sample in the dataframe.
        """
        numpy_sample = point.to_numpy()
        if (isinstance(point, DataFrame) and point.shape[1]) == 1 or (
            isinstance(point, Series) and point.shape[0] == 1
        ):
            self.logger.debug("The point is a single dimensional.")
            return numpy_sample - self.affine_independent_data.iloc[0][0]

        shifted_sample = (
            numpy_sample - self.affine_independent_data.iloc[0] if not self._spanning_standard_base else numpy_sample
        )
        return shifted_sample

    def _is_spanned_in_base(self, point: Series) -> bool:
        """Checks if the new point is spanned by the base.

        :return: whether the new point is spanned by the base.
        """
        shifted_sample = self._shift_new_point(point)
        return len(extended_gram_schmidt([list(shifted_sample)], self._gsp_base)) == 0

    def _learn_new_bases(self) -> None:
        """Learns the new bases of the points in the storage dataframe.

        :return: the new bases of the points in the storage dataframe.
        """
        self.logger.debug("Learning the new normal and the complementary bases of the points in the storage dataframe.")
        self._gsp_base = self._calculate_orthonormal_base(self.affine_independent_data)
        self._complementary_base = self._calculate_orthonormal_complementary_base(
            self._gsp_base, self.affine_independent_data.shape[1]
        )
        self._complementary_base = divide_span_by_common_denominator(self._complementary_base)
        if (len(self._gsp_base) > 1) and (len(self._gsp_base) == self.affine_independent_data.shape[1]):
            self.logger.debug("The points are spanning the original space, no need to project the points.")
            self._gsp_base = [list(vector) for vector in np.eye(self.affine_independent_data.shape[1])]
            self._spanning_standard_base = True

    def _learn_new_convex_hull(self, incremental: bool = True) -> None:
        """Learns the convex hull of the points in the storage dataframe.

        :param incremental: whether to use the incremental convex hull algorithm.
        :return: the convex hull of the points in the storage dataframe.
        """
        if self._convex_hull is not None:
            self._convex_hull.close()
            self._convex_hull = None

        self.logger.debug("Creating the convex hull for the first time (or in case that the base had changed).")
        points = self.affine_independent_data.to_numpy()
        shift_axis = (
            points[0].tolist()
            if not self._spanning_standard_base
            else [0] * len(self.affine_independent_data.columns.tolist())
        )
        projected_points = np.dot(points - shift_axis, np.array(self._gsp_base).T)
        self._convex_hull = self._epsilon_approximate_hull(points=projected_points, incremental=incremental)

    def _calculate_basis_and_hull(self, from_reset: bool = False) -> None:
        """Calculates the basis and the convex hull of the points in the storage dataframe."""
        prev_conditions = self.additional_dependency_conditions
        # Avoid cases when some of the data points are NaN and thus removed.
        self.affine_independent_data, self.additional_dependency_conditions = remove_complex_linear_dependencies(
            self.data[[col for col in self.data.columns if col in self.relevant_fluents]]
        )
        if self.affine_independent_data.empty:
            self.logger.debug("There are no affine independent rows, no need for further processing.")
            return

        # If dependency conditions changed, retrain base and CH (if needed)
        if prev_conditions != self.additional_dependency_conditions or from_reset or self._gsp_base is None:
            self.logger.debug(
                "Either new point affects the dependency conditions or no base learned. Learning base and possibly CH."
            )
            self._learn_new_bases()
            if self._gsp_base is not None and len(self._gsp_base) >= 2 and len(self.data) >= 3:
                self._learn_new_convex_hull()

            return

        # Validate span and try to add to convex hull
        if not self._is_spanned_in_base(self.affine_independent_data.iloc[-1]):
            self.logger.debug("New point is not spanned by base. Relearning base and CH.")
            self._learn_new_bases()
            if len(self._gsp_base) <= 1:
                self.logger.debug("New base is 1D or empty. Cannot form a convex hull.")
                return

            self._learn_new_convex_hull()
            return

        if self._convex_hull is not None:
            # If reached here - the point is spanned by the base and the convex hull is not None
            projected_point = np.dot(
                self._shift_new_point(self.affine_independent_data.iloc[-1]), np.array(self._gsp_base).T
            )
            self._convex_hull.add_points([projected_point])

    def add_new_point(self, point: Dict[str, float]) -> None:
        """Adds a new point to the convex hull learner.

        Note:
            This method is supposed to improve the performance of the CH calculations by incrementally adding points.

        :param point: the point to add to the convex hull learner.
        """
        new_sample = pd.DataFrame({k: [v] for k, v in point.items()})
        # check if the new sample is already in the dataframe
        concat_data = pd.concat([self.data, new_sample], ignore_index=True).dropna(axis=1)
        if concat_data.duplicated().any():
            self.logger.debug("The new point is already in the storage, not adding it again.")
            return

        self.data = concat_data.dropna(axis=1)
        self._calculate_basis_and_hull()

    def _create_ch_coefficients_data(self, display_mode: bool = True) -> Tuple[List[List[float]], List[float]]:
        """Runs the convex hull algorithm on the given input points.

        :param display_mode: whether to display the convex hull.
        :return: the coefficients of the planes that represent the convex hull and the border point.
        """
        display_convex_hull(self.action_name, display_mode, self._convex_hull)
        equations = np.unique(self._convex_hull.equations, axis=0)
        A = equations[:, : self._convex_hull.points.shape[1]]
        b = -equations[:, self._convex_hull.points.shape[1]]
        coefficients = [prettify_coefficients(row) for row in A]
        border_point = prettify_coefficients(b)
        return coefficients, border_point

    def _incremental_create_ch_inequalities(
        self, display_mode: bool = False
    ) -> Tuple[List[List[float]], List[float], List[str], Optional[List[str]]]:
        """Create the convex hull and returns the matrix representing the inequalities.

        :return: the matrix representing the inequalities of the planes created by the convex hull as well as the
            names of the features that are part of the convex hull.

        Note: the returned values represents the linear inequalities of the convex hull, i.e.,  Ax <= b.
        """
        if self._gsp_base is None:
            self.logger.debug("The base is not yet learned since didn't receive enough points.")
            raise ValueError()

        points = self.affine_independent_data.to_numpy()
        shift_axis = points[0].tolist()  # selected the first vector to be the start of the axis.

        if (len(self._gsp_base) > 1) and (len(self._gsp_base) == self.affine_independent_data.shape[1]):
            self.logger.debug("The points are spanning the original space and the basis is full rank.")
            coefficients, border_point = self._create_ch_coefficients_data(display_mode)
            return coefficients, border_point, self.affine_independent_data.columns.tolist(), None

        projected_points = np.dot(points - shift_axis, np.array(self._gsp_base).T)

        if self._convex_hull is None:
            self.logger.debug("The projected points are 1D, creating min-max conditions on the new base.")
            coefficients = [[-1], [1]]
            border_point = prettify_coefficients([-projected_points.min(), projected_points.max()])

        else:
            coefficients, border_point = self._create_ch_coefficients_data(display_mode)

        transformed_vars = construct_projected_variable_strings(
            self.affine_independent_data.columns.tolist(), shift_axis, self._gsp_base
        )
        self.logger.debug("Constructing the conditions to verify that points are in the correct span.")
        transformed_orthonormal_vars = construct_projected_variable_strings(
            self.affine_independent_data.columns.tolist(),
            shift_axis,
            [list(vector) for vector in np.eye(points.shape[1])],
        )
        span_verification_conditions = construct_pddl_inequality_scheme(
            np.array(self._complementary_base),
            np.zeros(len(self._complementary_base)),
            transformed_orthonormal_vars,
            sign_to_use="=",
        )
        return coefficients, border_point, transformed_vars, span_verification_conditions

    def construct_safe_linear_inequalities(self, *args, **kwargs) -> Precondition:
        """Constructs the linear inequalities strings that will be used in the learned model later.

        :return: the inequality strings and the type of equations that were constructed (injunctive / disjunctive)
        """
        if len(self.data) == 0 or len(self.relevant_fluents) == 0:
            self.logger.debug(
                "No observations were given or the relevant fluents are empty - no conditions could be learned."
            )
            return Precondition("and")

        if len(self.data.columns.tolist()) == 1 or len(self.relevant_fluents) == 1:
            self.logger.debug("Only one dimension is needed in the preconditions!")
            return self._construct_single_dimension_inequalities(self.data.loc[:, self.data.columns.tolist()[0]])

        try:
            if len(self.affine_independent_data) == 0:
                self.logger.warning("The matrix is empty, no need to create a convex hull.")
                return construct_numeric_conditions(
                    self.additional_dependency_conditions,
                    condition_type=ConditionType.conjunctive,
                    domain_functions=self.domain_functions,
                )

            A, b, column_names, additional_projection_conditions = self._incremental_create_ch_inequalities()
            self.logger.debug(f"Constructing the PDDL inequality scheme for the action {self.action_name}.")
            inequalities_strs = construct_pddl_inequality_scheme(A, b, column_names)
            if additional_projection_conditions is not None:
                inequalities_strs.extend(additional_projection_conditions)

            self.logger.debug("Constructing the precondition object from the constructed strings.")
            return construct_numeric_conditions(
                [*inequalities_strs, *self.additional_dependency_conditions],
                condition_type=ConditionType.conjunctive,
                domain_functions=self.domain_functions,
            )

        except (QhullError, ValueError):
            self.logger.warning(
                "Convex hull failed to create a convex hull, using disjunctive preconditions "
                "(probably since the rank of the matrix is 2 and it cannot create a degraded "
                "convex hull)."
            )
            raise NotSafeActionError(
                name=self.action_name,
                reason="Convex hull failed to create a convex hull",
                solution_type=EquationSolutionType.convex_hull_not_found,
            )

    def is_point_in_convex_hull(self, point: Union[Series, DataFrame]) -> bool:
        """Checks if the given point is in the convex hull.

        :param point: the point to check.
        :return: whether the point is in the convex hull.
        """
        concat_data = (
            pd.concat([self.data, point], ignore_index=True)
            if isinstance(point, DataFrame)
            else pd.concat([self.data, point.to_frame().T], ignore_index=True)
        )
        if concat_data.duplicated().any():
            self.logger.debug("The new point is already in the storage, it is thus is the convex hull.")
            return True

        if self._gsp_base is None:
            self.logger.debug("The convex hull is not yet learned since didn't receive enough points.")
            return False

        new_entry = point[self.affine_independent_data.columns.tolist()]
        if not self._is_spanned_in_base(new_entry):
            self.logger.debug("The point is not spanned by the base.")
            return False

        shifted_new_entry = self._shift_new_point(new_entry)
        projected_entry = np.dot(shifted_new_entry, np.array(self._gsp_base).T)
        if (
            len(self._complementary_base) > 0
            and (np.absolute(np.dot(np.array(self._complementary_base), np.array(shifted_new_entry).T)) > EPSILON).any()
        ):
            self.logger.debug("The new points are not in the span of the input points.")
            return False

        if projected_entry.shape[0] > 1:
            self.logger.debug("Validating whether the new point conforms with the CH inequalities.")
            A = self._convex_hull.equations[:, :-1]
            b = self._convex_hull.equations[:, -1]
            return bool(np.all(A.dot(projected_entry) + b <= EPSILON))

        self.logger.debug("The new point is single dimensional... checking if it is within the legal interval.")
        projected_dataset = np.dot(
            self.affine_independent_data.to_numpy() - self.affine_independent_data.to_numpy()[0],
            np.array(self._gsp_base).T,
        )
        return projected_dataset.min() <= projected_entry <= projected_dataset.max()

    def reset(self, new_relevant_features: List[str]) -> None:
        """Resets changes the features used to create the convex hull and reset to start the learning from scratch.

        :param new_relevant_features: the new relevant features to use.
        """
        self.logger.debug("Resetting the convex hull learner.")
        self.relevant_fluents = new_relevant_features
        self._convex_hull.close()
        self._convex_hull = None
        self._calculate_basis_and_hull(from_reset=True)

    def copy(self, one_shot: bool = False) -> "IncrementalConvexHullLearner":
        """Creates a copy of the current object.

        :param one_shot: whether to create a one-shot copy of the covex hull.
        :return: a copy of the current object.
        """
        new_learner = IncrementalConvexHullLearner(
            action_name=self.action_name,
            domain_functions=self.domain_functions,
            polynom_degree=self.polynom_degree,
            epsilon=self._epsilon,
            qhull_options=self._qhull_options,
            relevant_fluents=self.relevant_fluents,
        )
        if self.data.empty:
            self.logger.debug("The data is empty, no need to copy the convex hull.")
            return new_learner

        new_learner.data = self.data.copy()
        new_learner.affine_independent_data = self.affine_independent_data.copy()
        new_learner.additional_dependency_conditions = self.additional_dependency_conditions.copy()
        new_learner._gsp_base = self._gsp_base.copy() if self._gsp_base is not None else None
        new_learner._complementary_base = (
            self._complementary_base.copy() if self._complementary_base is not None else None
        )
        new_learner._spanning_standard_base = self._spanning_standard_base
        if self._convex_hull is not None:
            new_learner._learn_new_convex_hull(incremental=not one_shot)

        return new_learner

    def close_convex_hull(self) -> None:
        """Closes the convex hull."""
        if self._convex_hull is not None:
            self._convex_hull.close()
            self._convex_hull = None

    def is_spanning_standard_base(self) -> bool:
        """Checks if the convex hull is spanning the standard base.

        :return: whether the convex hull is spanning the standard base.
        """
        return self._spanning_standard_base
