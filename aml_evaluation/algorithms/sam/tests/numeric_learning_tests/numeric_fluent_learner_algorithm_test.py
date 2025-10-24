"""Module test for the numeric state storage."""
import random

from pandas import DataFrame
from pddl_plus_parser.models import NumericalExpressionTree
from pytest import fixture

from sam_learning.core import NumericFluentStateStorage, construct_non_circular_assignment
from sam_learning.core.numeric_learning.numeric_utils import detect_linear_dependent_features, filter_constant_features
from tests.consts import FUEL_COST_FUNCTION, LOAD_LIMIT_TRAJECTORY_FUNCTION, CURRENT_LOAD_TRAJECTORY_FUNCTION

LOAD_ACTION = "load"

TEST_DOMAIN_FUNCTIONS = {
    "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
    "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
    "(fuel-cost )": FUEL_COST_FUNCTION,
}

random.seed(0)


@fixture()
def load_action_state_fluent_storage() -> NumericFluentStateStorage:
    return NumericFluentStateStorage(action_name=LOAD_ACTION, domain_functions=TEST_DOMAIN_FUNCTIONS)


def test_add_to_previous_state_storage_can_add_single_item_to_the_storage(load_action_state_fluent_storage: NumericFluentStateStorage,):
    LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(411.0)
    CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(121.0)
    FUEL_COST_FUNCTION.set_value(34.0)
    simple_state_fluents = {
        "(fuel-cost )": FUEL_COST_FUNCTION,
        "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
        "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
    }
    load_action_state_fluent_storage.add_to_previous_state_storage(simple_state_fluents)
    assert len(load_action_state_fluent_storage.convex_hull_learner.data) == 1
    assert load_action_state_fluent_storage.convex_hull_learner.data.iloc[0]["(fuel-cost )"] == [34.0]
    assert load_action_state_fluent_storage.convex_hull_learner.data.iloc[0]["(load_limit ?z)"] == [411.0]
    assert load_action_state_fluent_storage.convex_hull_learner.data.iloc[0]["(current_load ?z)"] == [121.0]


def test_add_to_next_state_storage_can_add_single_item_to_the_storage(load_action_state_fluent_storage: NumericFluentStateStorage,):
    LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(411.0)
    CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(121.0)
    FUEL_COST_FUNCTION.set_value(34.0)
    simple_state_fluents = {
        "(fuel-cost )": FUEL_COST_FUNCTION,
        "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
        "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
    }
    load_action_state_fluent_storage.add_to_next_state_storage(simple_state_fluents)
    assert load_action_state_fluent_storage.linear_regression_learner.next_state_data.iloc[0]["(fuel-cost )"] == [34.0]
    assert load_action_state_fluent_storage.linear_regression_learner.next_state_data.iloc[0]["(load_limit ?z)"] == [411.0]
    assert load_action_state_fluent_storage.linear_regression_learner.next_state_data.iloc[0]["(current_load ?z)"] == [121.0]


def test_add_to_previous_state_storage_can_add_multiple_state_values_correctly(load_action_state_fluent_storage: NumericFluentStateStorage,):
    for i in range(10):
        FUEL_COST_FUNCTION.set_value(i)
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(i + 1)
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(i + 2)
        simple_state_fluents = {
            "(fuel-cost )": FUEL_COST_FUNCTION,
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_state_fluents)

    assert len(load_action_state_fluent_storage.convex_hull_learner.data) == 10


def test_add_to_next_state_storage_can_add_multiple_state_values_correctly(load_action_state_fluent_storage: NumericFluentStateStorage,):
    for i in range(10):
        FUEL_COST_FUNCTION.set_value(i)
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(i + 1)
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(i + 2)
        simple_state_fluents = {
            "(fuel-cost )": FUEL_COST_FUNCTION,
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_next_state_storage(simple_state_fluents)

    assert len(load_action_state_fluent_storage.linear_regression_learner.next_state_data) == 10
    assert len(load_action_state_fluent_storage.linear_regression_learner.next_state_data.columns.tolist()) == 3


def test_construct_non_circular_assignment_constructs_correct_equation_with_correct_coefficient_sign_on_increase(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    lifted_function = "(current_load ?z)"
    coefficient_map = {"(current_load ?z)": 1.0, "(weight ?y)": 1.0}
    previous_value = 0.0
    next_value = 1.0
    increase_statement = construct_non_circular_assignment(lifted_function, coefficient_map, previous_value, next_value)
    assert increase_statement == "(increase (current_load ?z) (weight ?y))"


def test_construct_non_circular_assignment_constructs_correct_equation_with_correct_coefficient_sign_on_decrease(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    lifted_function = "(current_load ?z)"
    coefficient_map = {"(current_load ?z)": 1.0, "(weight ?y)": -1.0, "(dummy)": 0.0}
    previous_value = 1.0
    next_value = 0.0
    increase_statement = construct_non_circular_assignment(lifted_function, coefficient_map, previous_value, next_value)
    assert increase_statement == "(decrease (current_load ?z) (weight ?y))"


def test_construct_assignment_equations_with_simple_2d_equations_when_no_change_in_variables_returns_empty_set(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    for i in range(4):
        random_prev_load_limit = random.randint(0, 100)
        random_prev_current_load = random.randint(0, 100)
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(random_prev_load_limit)
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(random_prev_current_load)
        simple_prev_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_prev_state_fluents)
        load_action_state_fluent_storage.add_to_next_state_storage(simple_prev_state_fluents)

    (effects, numeric_preconditions, learned_perfectly,) = load_action_state_fluent_storage.construct_assignment_equations()
    assert learned_perfectly
    assert isinstance(effects, set)
    assert len(effects) == 0
    assert numeric_preconditions is None


def test_construct_assignment_equations_when_change_is_caused_by_constant_returns_correct_value(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    # This test is meant to validate that cases such as (assign (battery-level ?r) 10) can be handled.
    for i in range(3):
        random_prev_load_limit = random.randint(0, 100)
        random_prev_current_load = random.randint(0, 100)
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(random_prev_load_limit)
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(random_prev_current_load)
        simple_prev_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_prev_state_fluents)
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(10)
        simple_next_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_next_state_storage(simple_next_state_fluents)

    (effects, numeric_preconditions, learned_perfectly,) = load_action_state_fluent_storage.construct_assignment_equations()
    assert learned_perfectly
    assert isinstance(effects, set)
    assert len(effects) == 1
    assert numeric_preconditions is None
    assert effects.pop().to_pddl() == "(assign (current_load ?z) 10)"


def test_construct_assignment_equations_with_simple_2d_equations_returns_correct_string_representation(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    previous_state_values = [(1, 7), (2, -1), (2, 14), (1, 0)]
    next_state_values = [9, 18, 18, 9]
    for prev_values, next_state_value in zip(previous_state_values, next_state_values):
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(prev_values[0])
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(prev_values[1])
        simple_prev_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_prev_state_fluents)
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(next_state_value)
        simple_next_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_next_state_storage(simple_next_state_fluents)

    (effects, numeric_preconditions, learned_perfectly,) = load_action_state_fluent_storage.construct_assignment_equations()
    assert learned_perfectly
    assert isinstance(effects, set)
    assert len(effects) == 1
    assert numeric_preconditions is None
    assert effects.pop().to_pddl() == "(assign (current_load ?z) (* (load_limit ?z) 9))"


def test_construct_assignment_equations_with_two_equations_result_in_multiple_changes(load_action_state_fluent_storage: NumericFluentStateStorage,):
    previous_state_values = [(1, 7), (2, -1), (2, 14), (1, 0)]
    next_state_values = [(7, 9), (-16, 18), (14, 18), (-7, 9)]
    for prev_values, next_state_values in zip(previous_state_values, next_state_values):
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(prev_values[0])
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(prev_values[1])
        simple_prev_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_prev_state_fluents)
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(next_state_values[0])
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(next_state_values[1])
        simple_next_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_next_state_storage(simple_next_state_fluents)

    (effects, numeric_preconditions, learned_perfectly,) = load_action_state_fluent_storage.construct_assignment_equations()
    assert learned_perfectly
    assert isinstance(effects, set)
    assert numeric_preconditions is None
    assignment_equations = {expression.to_pddl() for expression in effects}
    assert len(assignment_equations) == 2
    assert assignment_equations == {
        "(increase (load_limit ?z) (+ (* (load_limit ?z) -8) (* (current_load ?z) 2)))",
        "(assign (current_load ?z) (* (load_limit ?z) 9))",
    }


def test_construct_assignment_equations_with_an_increase_change_results_in_correct_values(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    previous_state_values = [(0, 7), (2, -1), (12, 32)]
    next_state_values = [(0, 8), (2, 0), (12, 33)]
    for prev_values, next_state_values in zip(previous_state_values, next_state_values):
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(prev_values[0])
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(prev_values[1])
        simple_prev_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_prev_state_fluents)
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(next_state_values[0])
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(next_state_values[1])
        simple_next_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_next_state_storage(simple_next_state_fluents)

    (effects, numeric_preconditions, learned_perfectly,) = load_action_state_fluent_storage.construct_assignment_equations()
    assert learned_perfectly
    assert isinstance(effects, set)
    assert numeric_preconditions is None
    assignment_equations = {expression.to_pddl() for expression in effects}
    print(assignment_equations)


def test_construct_assignment_equations_with_fewer_equations_than_needed_to_create_single_solution_should_numeric_effect_and_preconditions(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    # Note the function that we are trying to calculate is y[i+1] = y[i] + 10 * x[i]
    # In this setting we create an observation where x[i] = 2 constantly but y[i] = 1, 2, 3, 4
    LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(2)
    for i in range(1, 10):
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(i)
        simple_prev_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_prev_state_fluents)
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(i + 10 * 2)
        simple_next_state_fluents = {
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_next_state_storage(simple_next_state_fluents)

    (effects, numeric_preconditions, learned_perfectly,) = load_action_state_fluent_storage.construct_assignment_equations()
    assert learned_perfectly
    assert numeric_preconditions is not None
    assert effects is not None


def test_construct_safe_linear_inequalities_when_given_only_one_state_returns_degraded_conditions(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(411.0)
    CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(121.0)
    FUEL_COST_FUNCTION.set_value(34.0)
    simple_state_fluents = {
        "(fuel-cost )": FUEL_COST_FUNCTION,
        "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
        "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
    }
    load_action_state_fluent_storage.add_to_previous_state_storage(simple_state_fluents)
    output_conditions = load_action_state_fluent_storage.construct_safe_linear_inequalities(["(fuel-cost )", "(load_limit ?z)", "(current_load ?z)"])
    assert output_conditions.binary_operator == "and"
    assert len(output_conditions.operands) == 3
    numeric_operands = [operand for operand in output_conditions.operands if isinstance(operand, NumericalExpressionTree)]
    for op in numeric_operands:
        assert op.to_pddl() in ["(= (fuel-cost ) 34)", "(= (load_limit ?z) 411)", "(= (current_load ?z) 121)"]


def test_construct_safe_linear_inequalities_when_given_only_two_states_returns_smaller_convex_hull_and_const_condition(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(411.0)
    CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(121.0)
    FUEL_COST_FUNCTION.set_value(34.0)
    simple_state_fluents = {
        "(fuel-cost )": FUEL_COST_FUNCTION,
        "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
        "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
    }
    load_action_state_fluent_storage.add_to_previous_state_storage(simple_state_fluents)
    LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(413.0)
    CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(121.0)
    FUEL_COST_FUNCTION.set_value(35.0)
    another_simple_state_fluents = {
        "(fuel-cost )": FUEL_COST_FUNCTION,
        "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
        "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
    }
    load_action_state_fluent_storage.add_to_previous_state_storage(another_simple_state_fluents)
    output_conditions = load_action_state_fluent_storage.construct_safe_linear_inequalities(["(fuel-cost )", "(load_limit ?z)", "(current_load ?z)"])
    assert output_conditions.binary_operator == "and"
    assert len(output_conditions.operands) == 4
    numeric_conditions = [operand.to_pddl() for operand in output_conditions.operands if isinstance(operand, NumericalExpressionTree)]
    assert "(= (current_load ?z) 121)" in numeric_conditions  # the condition is shifted
    assert len([condition for condition in numeric_conditions if condition.startswith("(<=")]) == 2
    assert len([condition for condition in numeric_conditions if condition.startswith("(=")]) == 2
    print(str(output_conditions))


def test_construct_safe_linear_inequalities_will_create_correct_inequalities_when_given_three_points_for_two_variables(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    pre_state_input_values = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0)]
    for fuel_cost_val, current_limit_val in pre_state_input_values:
        FUEL_COST_FUNCTION.set_value(fuel_cost_val)
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(current_limit_val)
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(0.0)
        simple_state_fluents = {
            "(fuel-cost )": FUEL_COST_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_state_fluents)

    output_conditions = load_action_state_fluent_storage.construct_safe_linear_inequalities()

    expected_conditions = [
        "(<= (* (fuel-cost ) -1) 0)",
        "(<= (* (current_load ?z) -1) 0)",
        "(<= (+ (* (current_load ?z) 0.7071) (* (fuel-cost ) 0.7071)) 0.7071)",
        "(= (load_limit ?z) 0)",
    ]
    for _, precondition in output_conditions:
        assert precondition.to_pddl() in expected_conditions


def test_construct_safe_linear_inequalities_will_create_correct_inequalities_when_given_four_points_for_two_variables(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    pre_state_input_values = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    for fuel_cost_val, current_limit_val in pre_state_input_values:
        FUEL_COST_FUNCTION.set_value(fuel_cost_val)
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(current_limit_val)
        LOAD_LIMIT_TRAJECTORY_FUNCTION.set_value(0.0)
        simple_state_fluents = {
            "(fuel-cost )": FUEL_COST_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
            "(load_limit ?z)": LOAD_LIMIT_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_state_fluents)

    output_conditions = load_action_state_fluent_storage.construct_safe_linear_inequalities()
    expected_conditions = [
        "(<= (current_load ?z) 1)",
        "(<= (* (fuel-cost ) -1) 0)",
        "(<= (fuel-cost ) 1)",
        "(<= (* (current_load ?z) -1) 0)",
        "(= (load_limit ?z) 0)",
    ]

    for _, precondition in output_conditions:
        assert precondition.to_pddl() in expected_conditions


def test_construct_safe_linear_inequalities_with_one_dimension_variable_select_min_and_max_values(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):

    pre_state_input_values = [-19.0, 14.0, 28.0, -7.0]
    for fuel_cost_val in pre_state_input_values:
        FUEL_COST_FUNCTION.set_value(fuel_cost_val)
        simple_state_fluents = {
            "(fuel-cost )": FUEL_COST_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_state_fluents)

    output_conditions = load_action_state_fluent_storage.construct_safe_linear_inequalities()
    expected_conditions = [
        "(<= (fuel-cost ) 28)",
        "(>= (fuel-cost ) -19)",
    ]
    for _, precondition in output_conditions:
        assert precondition.to_pddl() in expected_conditions


def test_construct_safe_linear_inequalities_when_not_given_relevant_fluents_uses_all_variables_in_previous_state(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    pre_state_input_values = [(-19.0, 32.0), (14.0, 52.0), (28.0, 12.0), (-7.0, 13.0)]
    for fuel_cost_val, current_limit_val in pre_state_input_values:
        FUEL_COST_FUNCTION.set_value(fuel_cost_val)
        CURRENT_LOAD_TRAJECTORY_FUNCTION.set_value(current_limit_val)

        simple_state_fluents = {
            "(fuel-cost )": FUEL_COST_FUNCTION,
            "(current_load ?z)": CURRENT_LOAD_TRAJECTORY_FUNCTION,
        }
        load_action_state_fluent_storage.add_to_previous_state_storage(simple_state_fluents)

    output_conditions = load_action_state_fluent_storage.construct_safe_linear_inequalities()
    print(output_conditions)
    for _, precondition in output_conditions:
        assert "(fuel-cost )" in precondition.to_pddl()
        assert "(current_load ?z)" in precondition.to_pddl()


def test_detect_linear_dependent_features_when_given_only_one_sample_returns_that_no_column_is_dependent_since_there_are_not_enough_samples_to_guarantee_correctness():
    pre_state_data = {
        "(fuel-cost )": [1.0],
        "(current_load ?z)": [1.0],
    }
    linear_dependant_matrix = DataFrame(pre_state_data)
    output_matrix, linear_dependent_fluents, remained_fluents = detect_linear_dependent_features(linear_dependant_matrix)
    assert list(output_matrix.columns) == ["(fuel-cost )", "(current_load ?z)"]


def test_detect_linear_dependent_features_detects_that_two_equal_features_are_linear_dependant():
    pre_state_data = {
        "(fuel-cost )": [1.0, 2.0],
        "(current_load ?z)": [1.0, 2.0],
    }
    linear_dependant_matrix = DataFrame(pre_state_data)

    output_matrix, linear_dependent_fluent_strs, removed_fluents = detect_linear_dependent_features(linear_dependant_matrix)

    assert linear_dependent_fluent_strs == ["(= (current_load ?z) (* 1 (fuel-cost )))"]
    assert list(output_matrix.columns) == ["(fuel-cost )"]
    assert removed_fluents == {"(current_load ?z)": "(fuel-cost )"}


def test_detect_linear_dependent_features_detects_that_two_linear_dependent_features_are_linear_dependant(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    pre_state_data = {
        "(fuel-cost )": [1.0, 2.0],
        "(current_load ?z)": [2.0, 4.0],
    }
    linear_dependant_matrix = DataFrame(pre_state_data)
    output_matrix, linear_dependent_fluent_strs, removed_fluents = detect_linear_dependent_features(linear_dependant_matrix)

    assert linear_dependent_fluent_strs == ["(= (current_load ?z) (* 2 (fuel-cost )))"]
    assert removed_fluents == {"(current_load ?z)": "(fuel-cost )"}
    assert output_matrix.shape[1] == 1


def test_detect_linear_dependent_features_detects_when_variables_are_independent():
    pre_state_data = {
        "(fuel-cost )": [-19.0, 14.0, 28],
        "(current_load ?z)": [32.0, 54.0, 17.0],
    }
    linear_dependant_matrix = DataFrame(pre_state_data)
    relevant_fluents = ["(fuel-cost )", "(current_load ?z)"]
    output_matrix, linear_dependent_fluent_strs, removed_fluents_map = detect_linear_dependent_features(linear_dependant_matrix)

    assert linear_dependent_fluent_strs == []
    assert removed_fluents_map == {}
    assert output_matrix.shape[1] == 2


def test_detect_linear_dependent_features_when_one_feature_is_zero_constant_does_not_include_it_in_the_additional_conditions():
    pre_state_data = {
        "(fuel-cost )": [0.0, 0.0, 0.0],
        "(current_load ?z)": [32.0, 54.0, 17.0],
    }
    linear_dependant_matrix = DataFrame(pre_state_data)
    output_matrix, linear_dependent_fluent_strs, removed_fluents_map = detect_linear_dependent_features(linear_dependant_matrix)

    assert linear_dependent_fluent_strs == []
    assert removed_fluents_map == {}
    assert output_matrix.shape[1] == 2


def test_filter_constant_features_detects_features_that_equal_to_a_single_constant_value(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    pre_state_data = {
        "(fuel-cost )": [1.0, 32.0, 95.0],
        "(current_load ?z)": [15.0, 12.0, 17.0],
        "(load_limit ?z)": [33.0, 33.0, 33.0],
    }
    matrix_with_constant_column = DataFrame(pre_state_data)
    filtered_matrix, equal_fluent_strs, removed_fluents = filter_constant_features(matrix_with_constant_column)
    assert filtered_matrix.shape[1] == 2
    assert equal_fluent_strs == ["(= (load_limit ?z) 33.0)"]
    assert removed_fluents == ["(load_limit ?z)"]


def test_filter_constant_features_with_two_constant_detects_both_and_removes_them(load_action_state_fluent_storage: NumericFluentStateStorage,):
    pre_state_data = {
        "(fuel-cost )": [1.0, 32.0, 95.0],
        "(current_load ?z)": [15.0, 12.0, 17.0],
        "(load_limit ?z)": [33.0, 33.0, 33.0],
        "(weight ?z)": [5.0, 5.0, 5.0],
    }
    matrix_with_constant_column = DataFrame(pre_state_data)
    filtered_matrix, equal_fluent_strs, removed_fluents = filter_constant_features(matrix_with_constant_column)
    assert filtered_matrix.shape[1] == 2
    assert set(equal_fluent_strs) == {"(= (load_limit ?z) 33.0)", "(= (weight ?z) 5.0)"}
    assert set(removed_fluents) == {"(load_limit ?z)", "(weight ?z)"}


def test_filter_constant_features_with_all_features_being_constant_returns_correct_empty_df_and_correct_conditions(
    load_action_state_fluent_storage: NumericFluentStateStorage,
):
    pre_state_data = {
        "(fuel-cost )": [1.0, 1.0, 1.0],
        "(current_load ?z)": [15.0, 15.0, 15.0],
        "(load_limit ?z)": [33.0, 33.0, 33.0],
        "(weight ?z)": [5.0, 5.0, 5.0],
    }
    matrix_with_constant_column = DataFrame(pre_state_data)
    filtered_matrix, equal_fluent_strs, removed_fluents = filter_constant_features(matrix_with_constant_column)
    assert filtered_matrix.shape[1] == 0
    assert filtered_matrix.shape[0] == 0

    assert set(equal_fluent_strs) == {
        "(= (load_limit ?z) 33.0)",
        "(= (weight ?z) 5.0)",
        "(= (fuel-cost ) 1.0)",
        "(= (current_load ?z) 15.0)",
    }
    assert set(removed_fluents) == {"(load_limit ?z)", "(weight ?z)", "(fuel-cost )", "(current_load ?z)"}
