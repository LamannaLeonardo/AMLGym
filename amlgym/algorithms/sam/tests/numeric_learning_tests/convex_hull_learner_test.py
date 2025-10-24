import random
from unittest.mock import patch

import numpy as np
import pytest
from pandas import DataFrame
from pddl_plus_parser.models import PDDLFunction, Precondition, NumericalExpressionTree
from scipy.spatial import ConvexHull

from sam_learning.core.numeric_learning.convex_hull_learner import ConvexHullLearner
from sam_learning.core.numeric_learning.numeric_utils import remove_complex_linear_dependencies, construct_pddl_inequality_scheme

TEST_ACTION_NAME = "test_action"

random.seed(42)


@pytest.fixture
def convex_hull_learner() -> ConvexHullLearner:
    domain_functions = {
        "x": PDDLFunction(name="x", signature={}),
        "y": PDDLFunction(name="y", signature={}),
        "z": PDDLFunction(name="z", signature={}),
        "w": PDDLFunction(name="w", signature={}),
    }
    return ConvexHullLearner(TEST_ACTION_NAME, domain_functions)


def test_construct_pddl_inequality_scheme_with_simple_2d_four_equations_returns_correct_representation(convex_hull_learner: ConvexHullLearner,):
    np.random.seed(42)
    left_side_coefficients = np.random.randint(10, size=(4, 2))
    right_side_points = np.random.randint(10, size=4)

    inequalities = construct_pddl_inequality_scheme(left_side_coefficients, right_side_points, ["(x)", "(y)"])
    assert len(inequalities) == 4
    for ineq in inequalities:
        assert ineq.startswith("(<=")


def test_create_disjunctive_preconditions_with_input_dataframe_of_size_one_returns_a_single_precondition_with_and_condition(
    convex_hull_learner: ConvexHullLearner,
):
    pre_state_data = {"(x)": [2], "(y)": [3], "(z)": [-1]}
    dataframe = DataFrame(pre_state_data)
    equality_condition = convex_hull_learner._create_disjunctive_preconditions(dataframe, equality_conditions=[])
    assert len(equality_condition.operands) == 3
    assert equality_condition.binary_operator == "and"
    for operand in equality_condition.operands:
        assert operand.to_pddl().startswith("(=")


def test_create_disjunctive_preconditions_with_input_dataframe_of_size_two_returns_a_single_precondition_with_or_condition(
    convex_hull_learner: ConvexHullLearner,
):
    pre_state_data = {"(x)": [2, 18], "(y)": [3, 32], "(z)": [-1, 17]}
    dataframe = DataFrame(pre_state_data)
    equality_condition = convex_hull_learner._create_disjunctive_preconditions(dataframe, equality_conditions=[])
    assert len(equality_condition.operands) == 2
    assert equality_condition.binary_operator == "or"
    for operand in equality_condition.operands:
        assert isinstance(operand, Precondition)
        assert operand.binary_operator == "and"
        assert len(operand.operands) == 3
        for sub_operand in operand.operands:
            assert sub_operand.to_pddl().startswith("(=")


def test_create_disjunctive_preconditions_with_input_dataframe_of_size_one_and_equality_condition_creates_combined_condition_correctly(
    convex_hull_learner: ConvexHullLearner,
):
    pre_state_data = {"(x)": [20], "(y)": [39], "(z)": [-12]}
    test_equality_conditions = ["(= (x ) 2)", "(= (y ) 3)", "(= (z ) -1)"]
    dataframe = DataFrame(pre_state_data)
    equality_condition = convex_hull_learner._create_disjunctive_preconditions(dataframe, equality_conditions=test_equality_conditions)
    assert len(equality_condition.operands) == 2 * len(test_equality_conditions)
    assert equality_condition.binary_operator == "and"
    for operand in equality_condition.operands:
        assert operand.to_pddl().startswith("(=")


def test_create_disjunctive_preconditions_with_input_dataframe_of_size_two_and_equality_condition_creates_combined_condition_correctly(
    convex_hull_learner: ConvexHullLearner,
):
    pre_state_data = {"(x)": [2, 18], "(y)": [3, 32], "(z)": [-1, 17]}
    dataframe = DataFrame(pre_state_data)
    test_equality_conditions = ["(= (x ) 97)", "(= (y ) 21)"]
    result_condition = convex_hull_learner._create_disjunctive_preconditions(dataframe, equality_conditions=test_equality_conditions)
    assert len(result_condition.operands) == 3
    assert len([op for op in result_condition.operands if isinstance(op, NumericalExpressionTree)]) == 2
    assert len([op for op in result_condition.operands if isinstance(op, Precondition)]) == 1


def test_construct_single_dimension_inequalities_with_input_dataframe_of_size_one_returns_correct_inequalities(
    convex_hull_learner: ConvexHullLearner,
):
    pre_state_data = {"(x)": [2, 18], "(y)": [3, 32], "(z)": [-1, 17]}
    dataframe = DataFrame(pre_state_data)
    inequality_precondition = convex_hull_learner._construct_single_dimension_inequalities(dataframe["(x)"])
    assert inequality_precondition.binary_operator == "and"
    assert len(inequality_precondition.operands) == 2
    inequalities = [op.to_pddl() for op in inequality_precondition.operands]
    assert "(>= (x ) 2)" in inequalities
    assert "(<= (x ) 18)" in inequalities


def test_construct_single_dimension_inequalities_with_input_lower_bound_equal_to_upper_bound_returns_correct_condition(
    convex_hull_learner: ConvexHullLearner,
):
    pre_state_data = {"(x)": [2, 2], "(y)": [3, 32], "(z)": [-1, 17]}
    dataframe = DataFrame(pre_state_data)
    inequality_precondition = convex_hull_learner._construct_single_dimension_inequalities(dataframe["(x)"])
    assert inequality_precondition.binary_operator == "and"
    assert len(inequality_precondition.operands) == 1
    equality = inequality_precondition.operands.pop()
    assert "(= (x ) 2)" == equality.to_pddl()


def test_construct_safe_linear_inequalities_when_the_number_of_samples_is_one_creates_a_single_condition(convex_hull_learner: ConvexHullLearner,):
    convex_hull_learner.add_new_point(
        {"(x )": 2, "(y )": 3, "(z )": -1,}
    )
    inequality_precondition = convex_hull_learner.construct_safe_linear_inequalities(None)
    assert inequality_precondition.binary_operator == "and"
    assert len(inequality_precondition.operands) == 3
    assert {op.to_pddl() for op in inequality_precondition.operands} == {
        "(= (x ) 2)",
        "(= (y ) 3)",
        "(= (z ) -1)",
    }


def test_construct_safe_linear_inequalities_when_the_number_of_samples_is_two_creates_a_two_conditions_in_or_statement(
    convex_hull_learner: ConvexHullLearner,
):
    pre_state_data = {"(x )": [2, 3], "(y )": [3, 5], "(z )": [-1, 7]}
    for i in range(2):
        convex_hull_learner.add_new_point(
            {"(x )": pre_state_data["(x )"][i], "(y )": pre_state_data["(y )"][i], "(z )": pre_state_data["(z )"][i],}
        )
    inequality_precondition = convex_hull_learner.construct_safe_linear_inequalities(None)
    print(str(inequality_precondition))
    assert inequality_precondition.binary_operator == "and"
    assert len(inequality_precondition.operands) == 2 + 2  # 2 for the CH and 2 for complementing the base
    assert all([isinstance(op, NumericalExpressionTree) for op in inequality_precondition.operands])
    assert len([cond.to_pddl() for cond in inequality_precondition.operands if cond.to_pddl().startswith("(=")]) == 2
    assert len([cond.to_pddl() for cond in inequality_precondition.operands if cond.to_pddl().startswith("(<=")]) == 2


def test_construct_safe_linear_inequalities_when_the_number_of_is_smaller_than_needed_dimensions_but_larger_than_two_creates_a_convex_hull_from_the_samples(
    convex_hull_learner: ConvexHullLearner,
):

    for i in range(3):
        convex_hull_learner.add_new_point(
            {"(x )": random.randint(0, 100), "(y )": random.randint(0, 100), "(z )": random.randint(0, 100),}
        )
    inequality_precondition = convex_hull_learner.construct_safe_linear_inequalities(None)
    assert inequality_precondition.binary_operator == "and"
    assert len(inequality_precondition.operands) == 3 + 1  # 3 for the CH and 1 for complementing the base
    assert all([isinstance(op, NumericalExpressionTree) for op in inequality_precondition.operands])
    print(str(inequality_precondition))


def test_create_convex_hull_linear_inequalities_returns_correct_conditions_when_constant_is_observed(convex_hull_learner: ConvexHullLearner,):
    pre_state_data = {"(x)": [1, 0, 0], "(y)": [0, 1, 0], "(z)": [0, 0, 0]}
    pre_state_df = DataFrame(pre_state_data)
    (coefficients, border_point, transformed_vars, span_verification_conditions,) = convex_hull_learner._create_convex_hull_linear_inequalities(
        pre_state_df, display_mode=False
    )
    assert span_verification_conditions == ["(= (z) 0.0)"]
    print(span_verification_conditions)


def test_create_convex_hull_linear_inequalities_returns_correct_conditions_when_constant_is_observed_and_there_is_enough_data_to_create_convex_hull(
    convex_hull_learner: ConvexHullLearner,
):
    pre_state_data = {"(x)": [1, 0, 0, 1], "(y)": [0, 1, 0, 1], "(z)": [0, 0, 1, 1]}
    pre_state_df = DataFrame(pre_state_data)
    (coefficients, border_point, transformed_vars, span_verification_conditions,) = convex_hull_learner._create_convex_hull_linear_inequalities(
        pre_state_df, display_mode=False
    )
    assert span_verification_conditions == []


def test_create_convex_hull_linear_inequalities_returns_correct_conditions_when_when_remaining_only_one_dimension_returns_correct_values(
    convex_hull_learner: ConvexHullLearner,
):
    pre_state_data = {
        "(x)": [2, 1, 3, 4],
        "(y)": [1, 1, 1, 1],
    }
    pre_state_df = DataFrame(pre_state_data)
    (coefficients, border_point, transformed_vars, span_verification_conditions,) = convex_hull_learner._create_convex_hull_linear_inequalities(
        pre_state_df, display_mode=False
    )
    assert span_verification_conditions == ["(= (- (y) 1) 0.0)"]
    assert coefficients == [[-1], [1]]
    assert transformed_vars == ["(* (- (x) 2) -1)"]
    assert border_point == [2, 1]


def test_create_convex_hull_linear_inequalities_when_for_some_reason_the_gs_returns_a_base_with_larger_dimension_than_original_points_just_uses_original_points(
    convex_hull_learner: ConvexHullLearner,
):
    with patch("sam_learning.core.numeric_learning.numeric_utils.extended_gram_schmidt") as mock_gs:
        mock_gs.return_value = [[1, 0], [0, 1], [0, 0], [0, 23]]

        pre_state_data = {
            "(x)": [0, -1, 0],
            "(y)": [0, 0, -1],
        }
        pre_state_df = DataFrame(pre_state_data)
        (coefficients, border_point, transformed_vars, span_verification_conditions,) = convex_hull_learner._create_convex_hull_linear_inequalities(
            pre_state_df, display_mode=False
        )
        assert len(coefficients) == 3
        assert len(span_verification_conditions) == 0
        assert len(transformed_vars) == 2


def test_create_convex_hull_linear_inequalities_returns_correct_conditions_with_paper_example(convex_hull_learner: ConvexHullLearner,):
    pre_state_data = {
        "(x)": [1, 0, 0],
        "(y)": [0, 1, 0],
        "(z)": [0, 0, 1],
    }
    pre_state_df = DataFrame(pre_state_data)
    (coefficients, border_point, transformed_vars, span_verification_conditions,) = convex_hull_learner._create_convex_hull_linear_inequalities(
        pre_state_df, display_mode=False
    )
    print(span_verification_conditions)
    assert len(span_verification_conditions) == 1  # One dimension was reduced.
    assert len(coefficients) == 3
    assert len(transformed_vars) == 2


def test_create_convex_hull_linear_creates_convex_hull_with_no_duplicate_equations_due_to_numeric_precision_restriction(
    convex_hull_learner: ConvexHullLearner,
):
    pre_state_data = {
        "(x)": [0, 0, 0, 7, 7, 1.2300056, 1.2300057],
        "(y)": [0, 1, 0, 0, 7, 2.5600057, 2.5600058],
        "(z)": [0, 0, 1, 0, 7, 3.8900058, 3.8900059],
    }
    pre_state_df = DataFrame(pre_state_data)
    (coefficients, border_point, transformed_vars, span_verification_conditions,) = convex_hull_learner._create_convex_hull_linear_inequalities(
        pre_state_df, display_mode=False
    )
    assert len(span_verification_conditions) == 0
    assert len([str(c) for c in coefficients]) == len(set([str(c) for c in coefficients]))


def test_create_convex_hull_with_and_without_linear_dependency_removal_should_create_the_same_number_of_inequalities_when_there_are_constants_and_linear_dependent_features(
    convex_hull_learner: ConvexHullLearner,
):
    # we have data with 4 features, one feature is constant with the value of 1, and the other two are linearly dependent on one another and the last one is independent.
    # we create 10 samples of this data, and then we create the convex hull with and without removing the linear dependency.
    # The number of inequalities should be the same.
    NUM_SAMPLES = 10
    pre_state_data = {
        "(x )": [1] * NUM_SAMPLES,
        "(y )": [i for i in range(NUM_SAMPLES)],
        "(z )": [2 * i for i in range(NUM_SAMPLES)],
        "(w )": [random.randint(0, 100) for _ in range(NUM_SAMPLES)],
    }
    pre_state_df = DataFrame(pre_state_data)
    filtered_df, linear_deps = remove_complex_linear_dependencies(pre_state_df)
    assert len(filtered_df.columns.tolist()) < len(pre_state_df.columns.tolist())
    (coefficients, border_point, transformed_vars, span_verification_conditions,) = convex_hull_learner._create_convex_hull_linear_inequalities(
        pre_state_df, display_mode=False
    )
    (
        coefficients_filtered,
        border_point_filtered,
        transformed_vars_filtered,
        span_verification_conditions_filtered,
    ) = convex_hull_learner._create_convex_hull_linear_inequalities(filtered_df, display_mode=False)
    assert len(coefficients_filtered) == len(coefficients)


def test_construct_safe_linear_inequalities_with_relevant_fluents_ignores_all_variables_that_are_not_in_the_relevant_fluents(
    convex_hull_learner: ConvexHullLearner,
):
    for i in range(10):
        convex_hull_learner.add_new_point(
            {"(x )": random.randint(0, 100), "(y )": random.randint(0, 100), "(z )": random.randint(0, 100),}
        )
    inequality_precondition = convex_hull_learner.construct_safe_linear_inequalities(["(x )"])
    print(str(inequality_precondition))
    assert inequality_precondition.binary_operator == "and"
    assert len(inequality_precondition.operands) == 2  # One for upper bound and one for lower bound.
    for operand in inequality_precondition.operands:
        assert "(x )" in operand.to_pddl()
        assert "(y )" not in operand.to_pddl()
        assert "(z )" not in operand.to_pddl()


def test_epsilon_approximate_hull_when_given_epsilon_zero_and_no_parameters_returns_original_convex_hull(convex_hull_learner: ConvexHullLearner,):
    # create a three-dimensional np.array with 10 samples of random numbers.
    data = np.random.randint(0, 100, (10, 3))
    convex_hull_learner._epsilon = 0
    convex_hull_learner._qhull_options = ""
    non_approximated_hull = convex_hull_learner._epsilon_approximate_hull(data)
    expected_convex_hull = ConvexHull(data)
    assert np.equal(non_approximated_hull.points, expected_convex_hull.points).all()
    assert np.equal(non_approximated_hull.equations, expected_convex_hull.equations).all()


def test_construct_safe_linear_inequalities_with_example_from_the_new_paper_returns_correct_values(convex_hull_learner: ConvexHullLearner,):
    pre_state_data = {
        "(x)": [2, 1, 11],
        "(y)": [0, 0, 0],
        "(z)": [1, 1, 0],
    }
    pre_state_df = DataFrame(pre_state_data)
    (coefficients, border_point, transformed_vars, span_verification_conditions,) = convex_hull_learner._create_convex_hull_linear_inequalities(
        pre_state_df, display_mode=False
    )
    print(coefficients)
