"""Module tests for the numeric function matcher."""
from pddl_plus_parser.models import Domain, PDDLFunction, ActionCall, Observation
from pytest import fixture

from sam_learning.core import NumericFunctionMatcher
from tests.consts import (
    TRUCK_TYPE,
    FUEL_COST_FUNCTION,
    CURRENT_LOAD_GROUNDED_TRAJECTORY_FUNCTION,
    LOAD_LIMIT_GROUNDED_TRAJECTORY_FUNCTION,
)

TEST_NUMERIC_LOAD_LIMIT_FUNCTION = PDDLFunction(name="load_limit", signature={"?t": TRUCK_TYPE})

TEST_GROUNDED_NUMERIC_LOAD_LIMIT_FUNCTION = PDDLFunction(name="load_limit", signature={"tru1": TRUCK_TYPE})

CURRENT_LIMIT_TRAJECTORY_FUNCTION = PDDLFunction(name="current_load", signature={"truck1": TRUCK_TYPE})


@fixture()
def numeric_function_matcher(depot_domain: Domain) -> NumericFunctionMatcher:
    return NumericFunctionMatcher(domain=depot_domain)


@fixture()
def minecraft_function_matcher(minecraft_domain: Domain) -> NumericFunctionMatcher:
    return NumericFunctionMatcher(domain=minecraft_domain)


def test_create_possible_function_signatures_with_simple_action_creates_all_possible_signature_permutations(
    numeric_function_matcher: NumericFunctionMatcher,
):
    test_action_call_params = ActionCall(name="load", grounded_parameters=["hoist1", "crate1", "tru1", "loc1"])
    possible_signatures = numeric_function_matcher.create_possible_function_signatures(
        action_parameters=test_action_call_params.parameters, numeric_function=TEST_NUMERIC_LOAD_LIMIT_FUNCTION
    )

    assert len(possible_signatures) == 4
    assert possible_signatures == [
        "(load_limit hoist1)",
        "(load_limit crate1)",
        "(load_limit tru1)",
        "(load_limit loc1)",
    ]


def test_create_possible_function_signatures_when_action_is_called_with_a_constant_returns_all_possible_combinations_of_grounded_functions(
    minecraft_function_matcher: NumericFunctionMatcher, minecraft_domain: Domain
):
    test_action_call_params = ActionCall(name="tp_to", grounded_parameters=["crafting_table", "cell767"])
    tp_to_functions = PDDLFunction(name="cell_type", signature={"crafting_table": minecraft_domain.types["cell"]})
    possible_signatures = minecraft_function_matcher.create_possible_function_signatures(
        action_parameters=test_action_call_params.parameters, numeric_function=tp_to_functions
    )
    assert len(possible_signatures) == 2


def test_lift_matched_parameters_when_given_function_with_constant_that_can_match_multiple_options_returns_all_options(
    minecraft_function_matcher: NumericFunctionMatcher, minecraft_domain: Domain
):
    tp_to_function = PDDLFunction(name="cell_type", signature={"crafting_table": minecraft_domain.types["cell"]})
    grounded_execution = ["crafting_table"]
    lifted_functions = minecraft_function_matcher.lift_matched_parameters(
        executed_action=minecraft_domain.actions["tp_to"],
        grounded_call_parameters=grounded_execution,
        grounded_function=tp_to_function,
    )
    assert len(lifted_functions) == 2


def test_lift_matched_parameters_creates_lifted_version_of_function(
    numeric_function_matcher: NumericFunctionMatcher, depot_domain: Domain
):
    TEST_GROUNDED_NUMERIC_LOAD_LIMIT_FUNCTION.set_value(132.87)
    test_lifted_action = depot_domain.actions["load"]
    test_action_call_params = ActionCall(name="load", grounded_parameters=["hoist1", "crate1", "tru1", "loc1"])
    lifted_function = numeric_function_matcher.lift_matched_parameters(
        executed_action=test_lifted_action,
        grounded_call_parameters=test_action_call_params.parameters,
        grounded_function=TEST_GROUNDED_NUMERIC_LOAD_LIMIT_FUNCTION,
    )[0]

    assert lifted_function.untyped_representation == "(load_limit ?z)"
    assert lifted_function.value == 132.87


def test_match_state_functions_with_single_parameterized_grounded_function_finds_all_possible_matches(
    numeric_function_matcher: NumericFunctionMatcher,
):
    LOAD_LIMIT_GROUNDED_TRAJECTORY_FUNCTION.set_value(411.0)
    FUEL_COST_FUNCTION.set_value(34.0)
    simple_state_fluents = {
        "(fuel-cost )": FUEL_COST_FUNCTION,
        "(load_limit truck1)": LOAD_LIMIT_GROUNDED_TRAJECTORY_FUNCTION,
    }
    test_action_call = ActionCall(name="load", grounded_parameters=["hoist2", "crate1", "truck1", "distributor1"])
    matches = numeric_function_matcher.match_state_functions(
        action_call=test_action_call, grounded_state_fluents=simple_state_fluents
    )
    assert len(matches) == 2
    assert list(matches.keys()) == ["(load_limit ?z)", "(fuel-cost )"]
    assert matches["(fuel-cost )"].value == 34.0
    assert matches["(load_limit ?z)"].value == 411.0


def test_match_state_functions_with_small_number_of_grounded_functions_finds_all_possible_matches(
    numeric_function_matcher: NumericFunctionMatcher,
):
    LOAD_LIMIT_GROUNDED_TRAJECTORY_FUNCTION.set_value(411.0)
    CURRENT_LOAD_GROUNDED_TRAJECTORY_FUNCTION.set_value(121.0)
    FUEL_COST_FUNCTION.set_value(34.0)

    simple_state_fluents = {
        "(fuel-cost )": FUEL_COST_FUNCTION,
        "(load_limit truck1)": LOAD_LIMIT_GROUNDED_TRAJECTORY_FUNCTION,
        "(current_load truck1)": CURRENT_LOAD_GROUNDED_TRAJECTORY_FUNCTION,
    }
    test_action_call = ActionCall(name="load", grounded_parameters=["hoist2", "crate1", "truck1", "distributor1"])
    matches = numeric_function_matcher.match_state_functions(
        action_call=test_action_call, grounded_state_fluents=simple_state_fluents
    )
    assert len(matches) == 3
    assert list(matches.keys()) == ["(load_limit ?z)", "(current_load ?z)", "(fuel-cost )"]
    assert matches["(fuel-cost )"].value == 34.0
    assert matches["(load_limit ?z)"].value == 411.0
    assert matches["(current_load ?z)"].value == 121.0


def test_match_state_functions_matches_from_actual_trajectory_state(
    numeric_function_matcher: NumericFunctionMatcher, depot_observation: Observation
):
    observation_component = depot_observation.components[0]
    test_action_call = observation_component.grounded_action_call
    test_previous_state_fluents = observation_component.previous_state.state_fluents
    possible_matches = numeric_function_matcher.match_state_functions(
        action_call=test_action_call, grounded_state_fluents=test_previous_state_fluents
    )

    for matched_lifted_function in possible_matches.values():
        for parameter in matched_lifted_function.signature:
            assert parameter in ["?x", "?y", "?z"]
