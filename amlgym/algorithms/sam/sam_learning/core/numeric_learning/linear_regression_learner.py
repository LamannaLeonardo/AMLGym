"""This module contains the LinearRegressionLearner class."""
import logging
from typing import Optional, List, Dict, Tuple, Set

import numpy as np
import pandas as pd
from pandas import DataFrame
from pddl_plus_parser.models import Precondition, NumericalExpressionTree, PDDLFunction
from sklearn.linear_model import LinearRegression

from sam_learning.core.exceptions import NotSafeActionError
from sam_learning.core.learning_types import EquationSolutionType, ConditionType
from sam_learning.core.numeric_learning.numeric_utils import (
    detect_linear_dependent_features,
    construct_linear_equation_string,
    construct_non_circular_assignment,
    construct_multiplication_strings,
    prettify_coefficients,
    construct_numeric_conditions,
    construct_numeric_effects,
    filter_constant_features,
    get_num_independent_equations,
    create_monomials,
    create_polynomial_string,
)

LABEL_COLUMN = "label"
NEXT_STATE_PREFIX = "next_state_"  # prefix for the next state variables.
SUBTRACTION_COLUMN = "subtraction"
POST_NEXT_STATE_PREFIX_INDEX = len(NEXT_STATE_PREFIX)

LEGAL_LEARNING_SCORE = 1.00


class LinearRegressionLearner:
    def __init__(self, action_name: str, domain_functions: Dict[str, PDDLFunction], polynom_degree: int = 0):
        self.logger = logging.getLogger(__name__)
        self.action_name = action_name
        self.domain_functions = {func.name: func for func in domain_functions.values()}
        functions = list([function.untyped_representation for function in domain_functions.values()])
        self._function_representation = functions
        monomials = create_monomials(functions, polynom_degree)
        self.previous_state_data = DataFrame(columns=[create_polynomial_string(monomial) for monomial in monomials])
        self.next_state_data = DataFrame(columns=functions)

    def _combine_states_data(self, relevant_fluents: Optional[List[str]] = None) -> DataFrame:
        """Combines the previous and next states data into a single dataframe.

        :return: the combined dataframe.
        """
        # assuming that if a function is an effect of the action it will always be present in the next state.
        if relevant_fluents is not None:
            self.previous_state_data = self.previous_state_data[
                [fluent for fluent in self.previous_state_data.columns.tolist() if fluent in relevant_fluents]
            ]
            self.next_state_data = self.next_state_data[[fluent for fluent in self.next_state_data.columns.tolist() if fluent in relevant_fluents]]

        next_state_df = self.next_state_data.add_prefix(NEXT_STATE_PREFIX)
        combined_data = pd.concat([self.previous_state_data, next_state_df], axis=1)
        # getting the columns that contain missing values in the previous state.
        combined_data.drop_duplicates(inplace=True)
        return combined_data

    def _validate_legal_equations(self, values_df: DataFrame) -> bool:
        """Validates that there are enough independent equations which enable for a single solution for the equation.

        :param values_df: the matrix constructed based on the observations.
        """
        if len(values_df) == 1:
            return False

        num_dimensions = len(values_df.columns.tolist()) + 1  # +1 for the bias.
        num_independent_rows = get_num_independent_equations(values_df)
        if num_independent_rows >= num_dimensions:
            return True

        failure_reason = (
            f"There are too few independent rows of data! " f"cannot create a linear equation from the current data for action - {self.action_name}!"
        )
        self.logger.warning(failure_reason)

        return False

    def _solve_regression_problem(
        self, values_matrix: np.ndarray, function_post_values: np.ndarray, allow_unsafe_learning: bool = True
    ) -> Tuple[List[float], float]:
        """Solves the polynomial equations using a matrix form.

        Note: the equation Ax=b is solved as: x = inverse(A)*b.

        :param values_matrix: the A matrix that contains the previous values of the function variables.
        :param function_post_values: the resulting values after the linear change.
        :param allow_unsafe_learning: whether to allow unsafe learning.
        :return: the vector representing the coefficients for the function variables and the learning score (R^2).
        """
        regressor = LinearRegression()
        regressor.fit(values_matrix, function_post_values)
        learning_score = regressor.score(values_matrix, function_post_values)
        if learning_score < LEGAL_LEARNING_SCORE:
            reason = (
                f"The learned effects are not safe since the R^2 is not high enough. "
                f"Got R^2 of {learning_score} and expected {LEGAL_LEARNING_SCORE}! "
                f"Action {self.action_name} is not safe!"
            )
            self.logger.warning(reason)
            if not allow_unsafe_learning:
                raise NotSafeActionError(self.action_name, reason, EquationSolutionType.no_solution_found)

        coefficients = list(regressor.coef_) + [regressor.intercept_]
        coefficients = prettify_coefficients(coefficients)
        self.logger.debug(f"Learned the coefficients for the numeric equations with r^2 score of {learning_score}")
        return coefficients, learning_score

    def _calculate_scale_factor(self, coefficient_vector: List[float], regression_df: DataFrame, lifted_function: str) -> Optional[float]:
        """Calculates the scale factor for the function.

        Note:
            The scale factor defines the number of times a variable increases or decreases in value.

        :param coefficient_vector: the vector of coefficients for the function variables.
        :param regression_df: the dataframe containing the regression features.
        :param lifted_function: the function to calculate the scale factor for.
        :return: the scale factor for the function.
        """
        if (
            lifted_function in regression_df.columns
            and coefficient_vector[list(regression_df.columns).index(lifted_function)] != 0
            and all(
                [
                    coefficient_vector[list(regression_df.columns).index(function)] == 0
                    for function in regression_df.columns
                    if function != lifted_function
                ]
            )
        ):
            self.logger.debug(f"The value of the {lifted_function} is being scaled by a constant factor!")
            return round(coefficient_vector[list(regression_df.columns).index(lifted_function)], 10)

        return None

    @staticmethod
    def _extract_non_zero_change(lifted_function: str, regression_df: DataFrame) -> Tuple[float, float]:
        """Extracts the non-zero change in the function.

         Note:
            The value is extracted  based on the difference between the previous and the next states.

        :param lifted_function: the name of the function to extract the change for.
        :param regression_df: the matrix containing the previous values of the function and the resulting values.
        :return: the first non-zero value of the function and the previous value.
        """
        previous_value = next_value = 0.0
        for i in range(len(regression_df)):
            previous_value = regression_df.iloc[i][lifted_function]
            next_value = regression_df.iloc[i][LABEL_COLUMN]
            if previous_value != next_value:
                break

        return next_value, previous_value

    def _solve_linear_equations(self, lifted_function: str, regression_df: DataFrame, allow_unsafe_learning: bool = False) -> Optional[str]:
        """Computes the change in the function value based on the previous values of the function.

        Note: We assume in this stage that the change results from a polynomial function of the previous values.

        :param lifted_function: the function to compute the change for.
        :param regression_df: the matrix containing the previous values of the function and the resulting values.
        :param allow_unsafe_learning: whether to allow unsafe learning.
        :return: the string representing the polynomial function change in PDDL+ format.
        """
        regression_array = np.array(regression_df.loc[:, regression_df.columns != LABEL_COLUMN])
        function_post_values = np.array(regression_df[LABEL_COLUMN])
        coefficient_vector, learning_score = self._solve_regression_problem(regression_array, function_post_values, allow_unsafe_learning)

        if all([coef == 0 for coef in coefficient_vector]) and len(regression_df[LABEL_COLUMN].unique()) == 1:
            self.logger.debug(
                "The algorithm designated a vector of zeros to the equation "
                "which means that there are no coefficients and the label is also constant value."
            )
            return f"(assign {lifted_function} {regression_df[LABEL_COLUMN].unique()[0]})"

        functions_and_dummy = list(regression_df.columns[:-1]) + ["(dummy)"]
        scale_factor = self._calculate_scale_factor(coefficient_vector, regression_df, lifted_function)
        if scale_factor is not None:
            if scale_factor == 1:
                self.logger.debug("The scale factor is 1, there is no change in the function value.")
                return None

            scale = "scale-up" if scale_factor > 1 else "scale-down"
            self.logger.debug("Currently supporting only scaling of the function by a constant value.")
            return f"({scale} {lifted_function} {scale_factor})"

        if lifted_function in regression_df.columns and coefficient_vector[list(regression_df.columns).index(lifted_function)] != 0:
            self.logger.debug("the function is a part of the equation, cannot use circular format!")
            coefficients_map = {lifted_func: coef for lifted_func, coef in zip(functions_and_dummy, coefficient_vector)}
            next_value, previous_value = self._extract_non_zero_change(lifted_function, regression_df)
            return construct_non_circular_assignment(lifted_function, coefficients_map, previous_value, next_value)

        multiplication_functions = construct_multiplication_strings(coefficient_vector, functions_and_dummy)
        if len(multiplication_functions) == 0:
            self.logger.debug(
                "The algorithm designated a vector of zeros to the equation " "which means that there are not coefficients. Continuing."
            )
            return None

        constructed_right_side = construct_linear_equation_string(multiplication_functions)
        return f"(assign {lifted_function} {constructed_right_side})"

    @staticmethod
    def _extract_const_conditions(precondition_statements: List[List[str]], additional_conditions: List[str] = None) -> List[str]:
        """Extract conditions that are constant for all the samples.

        Note:
            These preconditions that appear in all samples will be considered axioms and will be added the
            general preconditions to create a more compact version of the action's preconditions.

        :param precondition_statements: the precondition statements.
        :return: the extracted constant conditions.
        """
        const_preconditions = set(additional_conditions) if additional_conditions else set()
        for conjunction_statement in precondition_statements:
            for condition in conjunction_statement:
                if all([condition in other_conjunction for other_conjunction in precondition_statements]):
                    const_preconditions.add(condition)
                    continue

        for conjunction_statement in precondition_statements:
            for const_condition in const_preconditions:
                if const_condition in conjunction_statement:
                    conjunction_statement.remove(const_condition)

        return list(const_preconditions)

    def _construct_effect_from_single_sample(self) -> Set[NumericalExpressionTree]:
        """constructs the effect from a single sample.

        :return: the constructed numeric effect.
        """
        assignment_statements = []
        for fluent in self.next_state_data.columns.tolist():
            if (
                fluent in self.previous_state_data.columns.tolist()
                and self.previous_state_data.iloc[0][fluent] == self.next_state_data.iloc[0][fluent]
            ):
                self.logger.debug("The value of the fluent is the same before and after the application of the action.")
                continue

            if fluent not in self.previous_state_data.columns.tolist():
                self.logger.debug("Assuming that the fluent wasn't initialized and the next state is an assignment.")

            assignment_statements.append(f"(assign {fluent} {self.next_state_data.iloc[0][fluent]})")

        return construct_numeric_effects(assignment_statements, self.domain_functions)

    def add_new_observation(self, state_data: Dict[str, float], store_in_prev_state: bool = True) -> None:
        """Adds a new point to the convex hull learner.

        Note:
            This method is supposed to improve the performance of the CH calculations by incrementally adding points.

        :param state_data: the data of the state.
        :param store_in_prev_state: whether to store the data in the previous state or the next state.
        """
        state_sample = DataFrame.from_dict(data={k: [v] for k, v in state_data.items()}, orient="columns")
        data_to_update = self.previous_state_data if store_in_prev_state else self.next_state_data
        if not store_in_prev_state:
            state_sample = state_sample.drop([col for col in state_sample.columns if col not in self._function_representation], axis=1)

        attribute_name = "previous_state_data" if store_in_prev_state else "next_state_data"

        if data_to_update.empty:
            setattr(self, attribute_name, state_sample)
            return

        data_to_update = pd.concat([data_to_update, state_sample], ignore_index=True)
        data_to_update.dropna(axis="columns", inplace=True)
        setattr(self, attribute_name, data_to_update)

    def construct_assignment_equations(
        self, allow_unsafe: bool = False, relevant_fluents: Optional[List[str]] = None
    ) -> Tuple[Set[NumericalExpressionTree], Optional[Precondition], bool]:
        """Constructs the assignment statements for the action according to the changed value functions.

        :param allow_unsafe: whether to allow unsafe learning.
        :param relevant_fluents: the fluents that are part of the action's preconditions and effects.
        :return: the constructed effects with the possibly additional preconditions.
        """
        if relevant_fluents is not None and len(relevant_fluents) == 0:
            self.logger.debug(f"No numeric effects for the action {self.action_name}.")
            return set(), None, False

        if len(self.next_state_data) == 0:
            self.logger.debug(f"No observations for the action {self.action_name}.")
            return set(), None, False

        assignment_statements = []
        self.logger.info(f"Constructing the fluent assignment equations for action {self.action_name}.")
        combined_data = self._combine_states_data(relevant_fluents)
        if combined_data.shape[0] == 1:
            self.logger.info(f"The action {self.action_name} contains a single unique observation!")
            return self._construct_effect_from_single_sample(), None, False

        # The dataset contains more than one observation.
        self.logger.debug("Removing fluents that are constant...")
        tagged_next_state_fluents = [f"{NEXT_STATE_PREFIX}{fluent_name}" for fluent_name in self.next_state_data.columns.tolist()]
        filtered_df, const_features_conditions, const_features = filter_constant_features(combined_data, columns_to_ignore=tagged_next_state_fluents)

        features_df = filtered_df.copy()[[k for k in self.previous_state_data.columns.tolist() if k in filtered_df.columns]]
        regression_df, linear_dep_conditions, dependent_columns = detect_linear_dependent_features(features_df)
        combined_conditions = linear_dep_conditions + const_features_conditions

        is_safe_to_learn = self._validate_legal_equations(regression_df)
        for feature_fluent, tagged_fluent in zip(self.next_state_data.columns.tolist(), tagged_next_state_fluents):
            regression_df[LABEL_COLUMN] = combined_data[tagged_fluent]
            if self.previous_state_data[feature_fluent].equals(self.next_state_data[feature_fluent]):
                self.logger.debug(
                    f"The value of the {feature_fluent} is the same before and "
                    f"after the application of the action. The action does not change the value!"
                )
                continue

            polynomial_equation = self._solve_linear_equations(feature_fluent, regression_df, allow_unsafe_learning=allow_unsafe)

            if polynomial_equation is not None:
                assignment_statements.append(polynomial_equation)

        if not is_safe_to_learn:
            return construct_numeric_effects(assignment_statements, self.domain_functions), None, False

        return (
            construct_numeric_effects(assignment_statements, domain_functions=self.domain_functions),
            construct_numeric_conditions(combined_conditions, ConditionType.conjunctive, domain_functions=self.domain_functions,),
            True,
        )
