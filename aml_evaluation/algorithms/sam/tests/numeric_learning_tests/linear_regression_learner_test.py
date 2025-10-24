import random

import numpy as np
import pytest
from pandas import DataFrame
from pddl_plus_parser.models import PDDLFunction, ObjectType

from sam_learning.core import NotSafeActionError
from sam_learning.core.numeric_learning.linear_regression_learner import LinearRegressionLearner
from sam_learning.core.numeric_learning.numeric_utils import create_monomials, create_polynomial_string

TEST_ACTION_NAME = "test_action"


@pytest.fixture
def linear_regression_learner() -> LinearRegressionLearner:
    domain_functions = {
        "x": PDDLFunction(name="x", signature={}),
        "y": PDDLFunction(name="y", signature={}),
        "z": PDDLFunction(name="z", signature={}),
        "w": PDDLFunction(name="w", signature={}),
    }
    return LinearRegressionLearner(TEST_ACTION_NAME, domain_functions)


@pytest.fixture
def polynomial_regression_learner() -> LinearRegressionLearner:
    domain_functions = {
        "(x )": PDDLFunction(name="x", signature={}),
        "(y )": PDDLFunction(name="y", signature={}),
        "(z )": PDDLFunction(name="z", signature={}),
        "(w )": PDDLFunction(name="w", signature={}),
    }
    return LinearRegressionLearner(TEST_ACTION_NAME, domain_functions, polynom_degree=1)


@pytest.fixture
def regression_learner_with_functions_with_the_same_name() -> LinearRegressionLearner:
    domain_functions = {
        "(x ?f2)": PDDLFunction(name="x", signature={"?f2": ObjectType}),
        "(x ?f1)": PDDLFunction(name="x", signature={"?f1": ObjectType}),
        "(cost )": PDDLFunction(name="cost", signature={}),
    }
    return LinearRegressionLearner(TEST_ACTION_NAME, domain_functions)


def test_add_new_observation_to_the_previous_state_data_adds_the_data_to_this_dataframe_only(linear_regression_learner: LinearRegressionLearner,):
    pre_state_data = {"(x )": 2.0, "(y )": 3.31, "(z )": -1.12, "(w )": 0.0}
    linear_regression_learner.add_new_observation(pre_state_data, store_in_prev_state=True)
    assert len(linear_regression_learner.previous_state_data) == 1
    assert len(linear_regression_learner.next_state_data) == 0


def test_add_new_observation_to_the_next_state_data_adds_the_data_to_this_dataframe_only(linear_regression_learner: LinearRegressionLearner,):
    next_state_data = {"(x )": 2.0, "(y )": 3.31, "(z )": -1.12, "(w )": 0.0}
    linear_regression_learner.add_new_observation(next_state_data, store_in_prev_state=False)
    assert len(linear_regression_learner.previous_state_data) == 0
    assert len(linear_regression_learner.next_state_data) == 1


def test_add_new_observation_with_missing_functions_in_the_data_removes_the_columns_from_the_dataframe(
    linear_regression_learner: LinearRegressionLearner,
):
    assert len(linear_regression_learner.next_state_data.columns.tolist()) == 4
    next_state_data = {"(x )": 2.0, "(y )": 3.31, "(z )": -1.12}
    linear_regression_learner.add_new_observation(next_state_data, store_in_prev_state=False)
    assert len(linear_regression_learner.previous_state_data.columns.tolist()) == 4
    assert len(linear_regression_learner.next_state_data.columns.tolist()) == 3


def test_add_new_observation_when_the_input_is_a_polynom_with_variable_multiplications_adds_all_permutations_to_previous_state_db_and_only_values_of_variable_to_post_state_db(
    linear_regression_learner: LinearRegressionLearner,
):
    pre_state_matrix = {
        "(x )": [2],
        "(y )": [0],
        "(z )": [1],
    }
    next_state_matrix = {
        "(x )": [2],
        "(y )": [2],
        "(z )": [0],
    }
    function_names = ["(x )", "(y )", "(z )"]
    linear_regression_learner.add_new_observation({name: pre_state_matrix[name][0] for name in function_names}, store_in_prev_state=True)
    linear_regression_learner.add_new_observation({name: next_state_matrix[name][0] for name in function_names}, store_in_prev_state=False)
    numeric_effects, preconditions, learned_correctly = linear_regression_learner.construct_assignment_equations()
    assert not learned_correctly
    assert preconditions is None
    assert len(numeric_effects) == 2
    for effect in numeric_effects:
        print(effect.to_pddl())


def test_extract_const_conditions_extract_preconditions_that_appear_in_all_samples_as_constant_a_single_time(
    linear_regression_learner: LinearRegressionLearner,
):
    precondition_statements = [
        ["(> (x) 0)", "(> (y) 0)", "(> (z) 0)"],
        ["(> (x) 0)", "(> (y) 1)", "(> (z) 2)"],
        ["(> (x) 0)", "(> (y) 2)", "(> (z) 4)"],
    ]
    const_conditions = linear_regression_learner._extract_const_conditions(precondition_statements)
    assert len(const_conditions) == 1
    assert const_conditions[0] == "(> (x) 0)"
    for precond in precondition_statements:
        assert len(precond) == 2


def test_validate_legal_equations_returns_true_when_the_number_of_equations_is_valid_and_the_matrix_has_one_solution(
    linear_regression_learner: LinearRegressionLearner,
):
    pre_state_data = {"x": [2, 1, 3, 0], "y": [3, -1, 2, 0], "z": [-1, 2, 4, 1]}
    dataframe = DataFrame(pre_state_data)
    assert linear_regression_learner._validate_legal_equations(dataframe)


def test_validate_legal_returns_false_when_there_are_not_enough_independent_equations(linear_regression_learner: LinearRegressionLearner,):
    pre_state_data = {"x": [0, 1, 2, 4], "y": [0, 2, 4, 8], "z": [0, 0, 18, 6]}
    dataframe = DataFrame(pre_state_data)
    assert not linear_regression_learner._validate_legal_equations(dataframe)


def test_validate_legal_equations_returns_false_when_the_number_of_equations_is_too_small(linear_regression_learner: LinearRegressionLearner,):
    pre_state_data = {"x": [2, 1, 3], "y": [3, -1, 2], "z": [-1, 2, 4]}
    dataframe = DataFrame(pre_state_data)
    assert not linear_regression_learner._validate_legal_equations(dataframe)


def test_solve_function_linear_equations_returns_correct_solution_for_a_solvable_matrix(linear_regression_learner: LinearRegressionLearner,):
    equation_matrix = {"x": [2, 1, 3, 0], "y": [3, -1, 2, 0], "z": [-1, 2, 4, 1], "label": [4, -1, 9, 15 / 35]}
    dataframe = DataFrame(equation_matrix)
    regression_array = np.array(dataframe.loc[:, dataframe.columns != "label"])
    function_post_values = np.array(dataframe["label"])
    try:
        coefficients, learning_score = linear_regression_learner._solve_regression_problem(regression_array, function_post_values)
        assert learning_score == 1
        assert len(coefficients) == 4

    except NotSafeActionError:
        pytest.fail()


def test_solve_function_linear_equations_raises_error_when_there_is_no_solution_with_the_correct_score_required(
    linear_regression_learner: LinearRegressionLearner,
):
    equation_matrix = {"x": [0, 1, 1, 0], "y": [0, 0, 0, 0], "z": [-1, 0, -1, 1], "label": [4, -1, 9, 15 / 35]}
    dataframe = DataFrame(equation_matrix)
    regression_array = np.array(dataframe.loc[:, dataframe.columns != "label"])
    function_post_values = np.array(dataframe["label"])
    with pytest.raises(NotSafeActionError) as e:
        linear_regression_learner._solve_regression_problem(regression_array, function_post_values, allow_unsafe_learning=False)


def test_compute_non_constant_change_returns_correct_pddl_equation_form_for_variable_with_assignment_sign(
    linear_regression_learner: LinearRegressionLearner,
):
    equation_matrix = {"x": [2, 1, 3, 0], "y": [3, -1, 2, 0], "z": [-1, 2, 4, 1], "label": [4, -1, 9, 15 / 35]}
    dataframe = DataFrame(equation_matrix)
    try:
        equation = linear_regression_learner._solve_linear_equations("w", dataframe)
        assert equation is not None
        assert equation.startswith("(assign")

    except NotSafeActionError:
        pytest.fail()


def test_compute_non_constant_change_returns_correct_pddl_equation_form_for_variable_with_circular_assignment_statement(
    linear_regression_learner: LinearRegressionLearner,
):
    equation_matrix = {"x": [2, 1, 3, 0], "y": [3, -1, 2, 0], "z": [-1, 2, 4, 1], "label": [4, -1, 9, 15 / 35]}
    dataframe = DataFrame(equation_matrix)
    try:
        equation = linear_regression_learner._solve_linear_equations("x", dataframe)
        assert equation is not None
        assert equation.startswith("(increase")

    except NotSafeActionError:
        pytest.fail()


def test_action_not_affects_fluent_returns_true_when_action_does_not_affect_fluent(linear_regression_learner: LinearRegressionLearner,):
    equation_matrix = {
        "(x)": [2, 3, 4, 5, 6, 7, 8, 9],
        "label": [2, 3, 4, 5, 6, 7, 8, 9],
    }
    dataframe = DataFrame(equation_matrix)
    result = linear_regression_learner._solve_linear_equations("(x)", dataframe)
    assert result is None


def test_action_not_affects_fluent_returns_false_when_action_does_affect_fluent(linear_regression_learner: LinearRegressionLearner,):
    equation_matrix = {
        "(x)": [2, 4, 6],
        "label": [4, 6, 8],
    }
    dataframe = DataFrame(equation_matrix)
    result = linear_regression_learner._solve_linear_equations("(x)", dataframe)
    assert result is not None
    assert result == "(increase (x) 2)"


def test_combine_states_data_creates_correct_dataframe_with_correct_values(linear_regression_learner: LinearRegressionLearner,):
    pre_state_matrix = {
        "(x )": [2, 1, 3, 0, 1],
        "(y )": [0, 3, 12, 43, 1],
        "(z )": [0, 2, 4, 1, 100],
    }
    next_state_matrix = {
        "(x )": [2, 6, 19, 44, 102],
        "(y )": [3, 6, 15, 46, 4],
        "(z )": [1, 1, 1, 1, 1],
    }
    function_names = ["(x )", "(y )", "(z )"]
    for i in range(5):
        linear_regression_learner.add_new_observation({name: pre_state_matrix[name][i] for name in function_names}, store_in_prev_state=True)
        linear_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    combined_state = linear_regression_learner._combine_states_data()
    assert len(combined_state.columns) == 6


def test_solve_safe_independent_equations_returns_correct_pddl_equation_form_for_variable_with_assignment_sign(
    linear_regression_learner: LinearRegressionLearner,
):
    equation_matrix = {"(x)": [2, 1, 3, 0], "(y)": [3, -1, 2, 0], "(z)": [-1, 2, 4, 1], "label": [21, 20, 22, 19]}
    dataframe = DataFrame(equation_matrix)
    constant_change = linear_regression_learner._solve_linear_equations("(x)", dataframe)
    assert constant_change is not None
    assert constant_change == "(increase (x) 19)"


def test_solve_safe_independent_equations_equation_form_when_linear_equations_are_solvable(linear_regression_learner: LinearRegressionLearner,):
    equation_matrix = {"(x)": [2, 1, 3, 0], "(y)": [3, -1, 2, 0], "(z)": [-1, 2, 4, 1], "label": [21, 23, 252, 129]}
    dataframe = DataFrame(equation_matrix)
    non_constant_change = linear_regression_learner._solve_linear_equations("(x)", dataframe)
    assert non_constant_change is not None


def test_construct_assignment_equations_returns_correct_equations_for_all_fluents(linear_regression_learner: LinearRegressionLearner,):
    pre_state_matrix = {
        "(x )": [2, 1, 3, 0, 1],
        "(y )": [0, 3, 12, 43, 1],
        "(z )": [0, 2, 4, 1, 100],
    }
    next_state_matrix = {"(x )": [2, 6, 19, 44, 102], "(y )": [3, 6, 15, 46, 4], "(z )": [1, 1, 1, 1, 1]}
    function_names = ["(x )", "(y )", "(z )"]
    for i in range(5):
        linear_regression_learner.add_new_observation({name: pre_state_matrix[name][i] for name in function_names}, store_in_prev_state=True)
        linear_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    numeric_effects, preconditions, learned_correctly = linear_regression_learner.construct_assignment_equations()
    assert learned_correctly
    assert len(numeric_effects) == 3
    assert preconditions is None
    for effect in numeric_effects:
        print(effect.to_pddl())


def test_construct_assignment_equations_returns_correct_equations_when_no_change_happens(linear_regression_learner: LinearRegressionLearner,):
    pre_state_matrix = {
        "(x )": [2, 1, 3, 0, 1],
        "(y )": [0, 3, 12, 43, 1],
        "(z )": [0, 2, 4, 1, 100],
    }
    next_state_matrix = {
        "(x )": [2, 1, 3, 0, 1],
        "(y )": [0, 3, 12, 43, 1],
        "(z )": [0, 2, 4, 1, 100],
    }
    function_names = ["(x )", "(y )", "(z )"]
    for i in range(5):
        linear_regression_learner.add_new_observation({name: pre_state_matrix[name][i] for name in function_names}, store_in_prev_state=True)
        linear_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    numeric_effects, preconditions, learned_correctly = linear_regression_learner.construct_assignment_equations()
    assert learned_correctly
    assert len(numeric_effects) == 0
    assert preconditions is None


def test_construct_assignment_equations_restrictive_preconditions_when_not_enough_data_is_given_and_the_values_are_equal_before_and_after_results_in_no_effect(
    linear_regression_learner: LinearRegressionLearner,
):
    pre_state_matrix = {
        "(x )": [2, 1],
        "(y )": [0, 3],
        "(z )": [0, 2],
    }
    next_state_matrix = {
        "(x )": [2, 1],
        "(y )": [0, 3],
        "(z )": [0, 2],
    }
    function_names = ["(x )", "(y )", "(z )"]
    for i in range(2):
        linear_regression_learner.add_new_observation({name: pre_state_matrix[name][i] for name in function_names}, store_in_prev_state=True)
        linear_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    numeric_effects, preconditions, learned_correctly = linear_regression_learner.construct_assignment_equations()
    assert not learned_correctly
    assert preconditions is None  # The preconditions will be learned in externally to maintain safety.
    assert len(numeric_effects) == 0
    for effect in numeric_effects:
        print(effect.to_pddl())


def test_construct_assignment_equations_restrictive_preconditions_when_not_enough_data_is_given_and_the_values_are_not_equal_before_and_after_results_in_effect(
    linear_regression_learner: LinearRegressionLearner,
):
    pre_state_matrix = {
        "(x )": [2, 1],
        "(y )": [0, 3],
        "(z )": [0, 2],
    }
    next_state_matrix = {
        "(x )": [12, 3],
        "(y )": [1, 3],
        "(z )": [9, 2],
    }
    function_names = ["(x )", "(y )", "(z )"]
    for i in range(2):
        linear_regression_learner.add_new_observation({name: pre_state_matrix[name][i] for name in function_names}, store_in_prev_state=True)
        linear_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    numeric_effects, preconditions, learned_correctly = linear_regression_learner.construct_assignment_equations()
    assert not learned_correctly
    assert preconditions is None  # The preconditions will be learned in externally to maintain safety.
    assert len(numeric_effects) == 3
    for effect in numeric_effects:
        print(effect.to_pddl())


def test_construct_assignment_equations_restrictive_preconditions_given_only_one_sample(polynomial_regression_learner: LinearRegressionLearner,):
    pre_state_matrix = {
        "(x )": [2],
        "(y )": [0],
        "(z )": [1],
    }
    next_state_matrix = {
        "(x )": [2],
        "(y )": [2],
        "(z )": [0],
    }
    function_names = ["(x )", "(y )", "(z )"]
    monomials = create_monomials(function_names, polynom_degree=1)
    polynomial_regression_learner.add_new_observation(
        {create_polynomial_string(monomial): np.prod([pre_state_matrix[name][0] for name in monomial]) for monomial in monomials},
        store_in_prev_state=True,
    )
    polynomial_regression_learner.add_new_observation({name: next_state_matrix[name][0] for name in function_names}, store_in_prev_state=False)
    assert len(polynomial_regression_learner.previous_state_data) == 1
    assert len(polynomial_regression_learner.next_state_data) == 1
    assert len(polynomial_regression_learner.previous_state_data.columns) == 6
    assert len(polynomial_regression_learner.next_state_data.columns) == 3


def test_construct_assignment_equations_with_polynomial_degree_one_returns_correct_equations_when_polynom_is_linear(
    polynomial_regression_learner: LinearRegressionLearner,
):
    numbers = list(range(101))
    x = random.choices(numbers, k=20)
    y = random.choices(numbers, k=20)
    z = random.choices(numbers, k=20)
    pre_state_matrix = {
        "(x )": x,
        "(y )": y,
        "(z )": z,
    }
    next_state_matrix = {
        "(x )": [2 * x1 + 3 * y1 + 4 * z1 + 5 for x1, y1, z1 in zip(x, y, z)],
        "(y )": y,
        "(z )": z,
    }
    function_names = ["(x )", "(y )", "(z )"]
    monomials = create_monomials(function_names, polynom_degree=1)
    for i in range(20):
        polynomial_regression_learner.add_new_observation(
            {create_polynomial_string(monomial): np.prod([pre_state_matrix[name][i] for name in monomial]) for monomial in monomials},
            store_in_prev_state=True,
        )
        polynomial_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    numeric_effects, preconditions, learned_correctly = polynomial_regression_learner.construct_assignment_equations()
    assert learned_correctly
    assert len(numeric_effects) == 1
    effect = numeric_effects.pop()
    assert effect.to_pddl() == "(increase (x ) (+ (x ) (+ (* (y ) 3) (+ (* (z ) 4) 5))))"


def test_construct_assignment_equations_with_polynomial_degree_one_returns_correct_equations_when_polynom_degree_is_also_one(
    polynomial_regression_learner: LinearRegressionLearner,
):
    k = 500
    numbers = list(range(1000))
    x = random.sample(numbers, k=k)
    y = random.sample(numbers, k=k)
    z = random.sample(numbers, k=k)
    pre_state_matrix = {
        "(x )": x,
        "(y )": y,
        "(z )": z,
    }
    next_state_matrix = {
        "(x )": [2 * x1 + 3 * y1 * x1 + 4 * z1 + 5 for x1, y1, z1 in zip(x, y, z)],
        "(y )": y,
        "(z )": z,
    }
    function_names = ["(x )", "(y )", "(z )"]
    monomials = create_monomials(function_names, polynom_degree=1)
    for i in range(k):
        polynomial_regression_learner.add_new_observation(
            {create_polynomial_string(monomial): np.prod([pre_state_matrix[name][i] for name in monomial]) for monomial in monomials},
            store_in_prev_state=True,
        )
        polynomial_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    numeric_effects, preconditions, learned_correctly = polynomial_regression_learner.construct_assignment_equations()
    assert learned_correctly
    assert len(numeric_effects) == 1
    effect = numeric_effects.pop()
    assert effect.to_pddl() == "(increase (x ) (+ (x ) (+ (* (z ) 4) (+ (* (* (x ) (y )) 3) 5))))"


def test_construct_assignment_equations_with_polynomial_degree_one_returns_correct_equations_when_polynom_degree_is_also_one_and_calculating_multiple_different_equations(
    polynomial_regression_learner: LinearRegressionLearner,
):
    k = 500
    numbers = list(range(1000))
    x = random.sample(numbers, k=k)
    y = random.sample(numbers, k=k)
    z = random.sample(numbers, k=k)
    pre_state_matrix = {
        "(x )": x,
        "(y )": y,
        "(z )": z,
    }
    next_state_matrix = {
        "(x )": [2 * x1 + 3 * y1 * x1 + 4 * z1 + 5 for x1, y1, z1 in zip(x, y, z)],
        "(y )": [y1 + y1 * x1 + 1 for x1, y1, in zip(x, y)],
        "(z )": [8 * x1 + 3 * y1 + 4 * z1 + 19 for x1, y1, z1 in zip(x, y, z)],
    }
    function_names = ["(x )", "(y )", "(z )"]
    monomials = create_monomials(function_names, polynom_degree=1)
    for i in range(k):
        polynomial_regression_learner.add_new_observation(
            {create_polynomial_string(monomial): np.prod([pre_state_matrix[name][i] for name in monomial]) for monomial in monomials},
            store_in_prev_state=True,
        )
        polynomial_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    numeric_effects, preconditions, learned_correctly = polynomial_regression_learner.construct_assignment_equations()
    assert learned_correctly
    assert len(numeric_effects) == 3
    expected_effects = {
        "(increase (x ) (+ (x ) (+ (* (z ) 4) (+ (* (* (x ) (y )) 3) 5))))",
        "(increase (z ) (+ (* (x ) 8) (+ (* (y ) 3) (+ (* (z ) 3) 19))))",
        "(increase (y ) (+ (* (x ) (y )) 1))",
    }
    for effect in numeric_effects:
        assert effect.to_pddl() in expected_effects


def test_construct_assignment_equations_with_polynomial_degree_one_returns_correct_equations_when_polynom_degree_is_also_one_and_there_is_and_assignment_equation(
    polynomial_regression_learner: LinearRegressionLearner,
):
    k = 500
    numbers = list(range(1000))
    x = random.sample(numbers, k=k)
    y = random.sample(numbers, k=k)
    z = random.sample(numbers, k=k)
    pre_state_matrix = {
        "(x )": x,
        "(y )": y,
        "(z )": z,
    }
    next_state_matrix = {
        "(x )": [2 * x1 + 3 * y1 * x1 + 4 * z1 + 5 for x1, y1, z1 in zip(x, y, z)],
        "(y )": [y1 + y1 * x1 + 1 for x1, y1, in zip(x, y)],
        "(z )": [1] * k,
    }
    function_names = ["(x )", "(y )", "(z )"]
    monomials = create_monomials(function_names, polynom_degree=1)
    for i in range(k):
        polynomial_regression_learner.add_new_observation(
            {create_polynomial_string(monomial): np.prod([pre_state_matrix[name][i] for name in monomial]) for monomial in monomials},
            store_in_prev_state=True,
        )
        polynomial_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    numeric_effects, preconditions, learned_correctly = polynomial_regression_learner.construct_assignment_equations()
    assert learned_correctly
    assert len(numeric_effects) == 3
    expected_effects = {
        "(increase (x ) (+ (x ) (+ (* (z ) 4) (+ (* (* (x ) (y )) 3) 5))))",
        "(assign (z ) 1)",
        "(increase (y ) (+ (* (x ) (y )) 1))",
    }
    for effect in numeric_effects:
        assert effect.to_pddl() in expected_effects


def test_construct_assignment_equations_with_polynomial_degree_one_and_relevant_fluents_does_not_fail_and_returns_correct_equations(
    polynomial_regression_learner: LinearRegressionLearner,
):
    k = 500
    numbers = list(range(1000))
    x = random.sample(numbers, k=k)
    y = random.sample(numbers, k=k)
    z = random.sample(numbers, k=k)
    w = random.sample(numbers, k=k)
    q = random.sample(numbers, k=k)
    pre_state_matrix = {
        "(x )": x,
        "(y )": y,
        "(z )": z,
        "(w )": w,
        "(q )": q,
    }
    next_state_matrix = {
        "(x )": [2 * x1 + 3 * y1 * x1 + 4 * z1 + 5 for x1, y1, z1 in zip(x, y, z)],
        "(y )": [y1 + y1 * x1 + 1 for x1, y1, in zip(x, y)],
        "(z )": [1] * k,
        "(w )": [7 * x1 + 82 * w1 + 1 * z1 + 5 for x1, w1, z1 in zip(x, w, z)],
        "(q )": [2 * w1 + 245 * y1 + 21 * q1 + 5 for w1, y1, q1 in zip(w, y, q)],
    }
    function_names = ["(x )", "(y )", "(z )", "(w )", "(q )"]
    monomials = create_monomials(function_names, polynom_degree=1)
    for i in range(k):
        polynomial_regression_learner.add_new_observation(
            {create_polynomial_string(monomial): np.prod([pre_state_matrix[name][i] for name in monomial]) for monomial in monomials},
            store_in_prev_state=True,
        )
        polynomial_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    numeric_effects, preconditions, learned_correctly = polynomial_regression_learner.construct_assignment_equations(
        relevant_fluents=["(x )", "(* (x ) (y ))", "(y )", "(z )"]
    )
    assert learned_correctly
    assert len(numeric_effects) == 3
    expected_effects = {
        "(increase (x ) (+ (x ) (+ (* (z ) 4) (+ (* (* (x ) (y )) 3) 5))))",
        "(assign (z ) 1)",
        "(increase (y ) (+ (* (x ) (y )) 1))",
    }
    for effect in numeric_effects:
        assert effect.to_pddl() in expected_effects


def test_construct_assignment_equations_with_polynomial_degree_one_with_change_that_increase_by_constant_and_a_variable_calculates_result_correctly(
    polynomial_regression_learner: LinearRegressionLearner,
):
    k = 50
    numbers = list(range(500))
    x = random.sample(numbers, k=k)
    y = random.sample(numbers, k=k)
    z = random.sample(numbers, k=k)
    pre_state_matrix = {
        "(x )": x,
        "(y )": y,
        "(z )": z,
    }
    next_state_matrix = {
        "(x )": [x1 + 1 for x1 in x],
        "(y )": [y1 + x1 + 1 for x1, y1, in zip(x, y)],
        "(z )": [1] * k,
    }
    function_names = ["(x )", "(y )", "(z )"]
    monomials = create_monomials(function_names, polynom_degree=1)
    for i in range(k):
        polynomial_regression_learner.add_new_observation(
            {create_polynomial_string(monomial): np.prod([pre_state_matrix[name][i] for name in monomial]) for monomial in monomials},
            store_in_prev_state=True,
        )
        polynomial_regression_learner.add_new_observation({name: next_state_matrix[name][i] for name in function_names}, store_in_prev_state=False)

    numeric_effects, preconditions, learned_correctly = polynomial_regression_learner.construct_assignment_equations()
    assert learned_correctly
    assert len(numeric_effects) == 3
    expected_effects = {
        "(increase (x ) 1)",
        "(assign (z ) 1)",
        "(increase (y ) (+ (x ) 1))",
    }
    for effect in numeric_effects:
        assert effect.to_pddl() in expected_effects


def test_construct_assignment_equations_when_two_functions_share_the_same_name_but_with_different_parameters_will_result_in_correct_assignment_of_the_equations_for_both_versions(
    regression_learner_with_functions_with_the_same_name: LinearRegressionLearner,
):
    k = 50
    numbers = list(range(500))
    x_f1 = random.sample(numbers, k=k)
    x_f2 = random.sample(numbers, k=k)
    cost = random.sample(numbers, k=k)
    pre_state_matrix = {
        "(x ?f1)": x_f1,
        "(x ?f2)": x_f2,
        "(cost )": cost,
    }
    next_state_matrix = {
        "(x ?f1)": [x1 - 4 for x1 in x_f1],
        "(x ?f2)": [x2 + 2 for x2 in x_f2],
        "(cost )": [c + 1 for c in cost],
    }
    for i in range(k):
        regression_learner_with_functions_with_the_same_name.add_new_observation(
            state_data={name: pre_state_matrix[name][i] for name in pre_state_matrix}, store_in_prev_state=True
        )
        regression_learner_with_functions_with_the_same_name.add_new_observation(
            {name: next_state_matrix[name][i] for name in next_state_matrix}, store_in_prev_state=False
        )

    numeric_effects, preconditions, learned_correctly = regression_learner_with_functions_with_the_same_name.construct_assignment_equations()
    assert learned_correctly
    assert len(numeric_effects) == 3
    expected_effects = {
        "(decrease (x ?f1) 4)",
        "(increase (x ?f2) 2)",
        "(increase (cost ) 1)",
    }
    for effect in numeric_effects:
        assert effect.to_pddl() in expected_effects


def test_construct_assignment_equations_when_two_functions_share_the_same_name_but_with_different_parameters_will_result_in_correct_assignment_of_the_equations_for_both_versions_when_observing_only_a_few_samples(
    regression_learner_with_functions_with_the_same_name: LinearRegressionLearner,
):
    k = 3
    numbers = list(range(500))
    x_f1 = random.sample(numbers, k=k)
    cost = random.sample(numbers, k=k)
    pre_state_matrix = {
        "(x ?f1)": x_f1,
        "(x ?f2)": [0] * 3,
        "(cost )": cost,
    }
    next_state_matrix = {
        "(x ?f1)": [x1 - 4 for x1 in x_f1],
        "(x ?f2)": [2] * 3,
        "(cost )": [c + 1 for c in cost],
    }
    for i in range(k):
        regression_learner_with_functions_with_the_same_name.add_new_observation(
            state_data={name: pre_state_matrix[name][i] for name in pre_state_matrix}, store_in_prev_state=True
        )
        regression_learner_with_functions_with_the_same_name.add_new_observation(
            {name: next_state_matrix[name][i] for name in next_state_matrix}, store_in_prev_state=False
        )

    numeric_effects, preconditions, learned_correctly = regression_learner_with_functions_with_the_same_name.construct_assignment_equations()
    assert learned_correctly
    assert len(numeric_effects) == 3
    expected_effects = {
        "(decrease (x ?f1) 4)",
        "(assign (x ?f2) 2)",
        "(increase (cost ) 1)",
    }
    for effect in numeric_effects:
        assert effect.to_pddl() in expected_effects


def test_construct_assignment_equations_when_two_functions_share_the_same_name_but_with_different_parameters_identifies_that_action_does_not_affect_function_even_with_small_number_of_samples(
    regression_learner_with_functions_with_the_same_name: LinearRegressionLearner,
):
    k = 2
    numbers = list(range(500))
    x_f1 = random.sample(numbers, k=k)
    cost = random.sample(numbers, k=k)
    pre_state_matrix = {
        "(x ?f1)": x_f1,
        "(x ?f2)": [0] * 3,
        "(cost )": cost,
    }
    next_state_matrix = {
        "(x ?f1)": [x1 - 4 for x1 in x_f1],
        "(x ?f2)": [0] * 3,
        "(cost )": [c + 1 for c in cost],
    }
    for i in range(k):
        regression_learner_with_functions_with_the_same_name.add_new_observation(
            state_data={name: pre_state_matrix[name][i] for name in pre_state_matrix}, store_in_prev_state=True
        )
        regression_learner_with_functions_with_the_same_name.add_new_observation(
            {name: next_state_matrix[name][i] for name in next_state_matrix}, store_in_prev_state=False
        )

    numeric_effects, preconditions, learned_correctly = regression_learner_with_functions_with_the_same_name.construct_assignment_equations()
    assert len(numeric_effects) == 2
