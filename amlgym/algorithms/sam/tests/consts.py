"""Constants for the tests."""

from pathlib import Path
from typing import Dict, List

from pddl_plus_parser.exporters.numeric_trajectory_exporter import parse_action_call
from pddl_plus_parser.models import (
    PDDLType,
    Predicate,
    PDDLFunction,
    ObservedComponent,
    PDDLObject,
    MultiAgentComponent,
    ActionCall,
    CompoundPrecondition,
)

from sam_learning.learners import SAMLearner

EXAMPLES_DIR_PATH = Path(__file__).parent / "examples"
LOGISTICS_DOMAIN_PATH = EXAMPLES_DIR_PATH / "domain-logistics.pddl"
WOODWORKING_DOMAIN_PATH = EXAMPLES_DIR_PATH / "woodworking-domain.pddl"
WOODWORKING_PROBLEM_PATH = EXAMPLES_DIR_PATH / "woodworking_problem.pddl"
WOODWORKING_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "woodworking_trajectory.trajectory"

DEPOTS_NUMERIC_DOMAIN_PATH = EXAMPLES_DIR_PATH / "depot_numeric.pddl"
DEPOTS_NUMERIC_PROBLEM_PATH = EXAMPLES_DIR_PATH / "pfile2.pddl"

DEPOTS_DISCRETE_DOMAIN_PATH = EXAMPLES_DIR_PATH / "depot_discrete.pddl"
DEPOTS_DISCRETE_PROBLEM_PATH = EXAMPLES_DIR_PATH / "depot_discrete_problem.pddl"

ELEVATORS_DOMAIN_PATH = EXAMPLES_DIR_PATH / "elevators_domain.pddl"
ELEVATORS_PROBLEM_PATH = EXAMPLES_DIR_PATH / "elevators_p03.pddl"
ELEVATORS_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "test_trajectory"
DEPOT_NUMERIC_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "test_numeric_trajectory"
DEPOT_FLUENTS_MAP_PATH = EXAMPLES_DIR_PATH / "depot_fluents_map.json"

SATELLITE_DOMAIN_PATH = EXAMPLES_DIR_PATH / "metricSat.pddl"
SATELLITE_PROBLEM_PATH = EXAMPLES_DIR_PATH / "pfile3.pddl"
SATELLITE_NUMERIC_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "pfile3.trajectory"

SATELLITE_PROBLEMATIC_PROBLEM_PATH = EXAMPLES_DIR_PATH / "pfile1_sat.pddl"
SATELLITE_PROBLEMATIC_NUMERIC_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "pfile1_sat.trajectory"

SATELLITE_FLUENTS_MAP_PATH = EXAMPLES_DIR_PATH / "satellite_fluents_map.json"

SAILING_EXPECTED_DOMAIN_PATH = EXAMPLES_DIR_PATH / "sailing_expected_domain.pddl"
SAILING_LEARNED_DOMAIN_PATH = EXAMPLES_DIR_PATH / "sailing_domain.pddl"
SAILING_PROBLEM_PATH = EXAMPLES_DIR_PATH / "prob_sailing.pddl"
SAILING_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "sailing_observation.trajectory"

WOODWORKING_COMBINED_DOMAIN_PATH = EXAMPLES_DIR_PATH / "woodworking_combined_domain.pddl"
WOODWORKING_COMBINED_PROBLEM_PATH = EXAMPLES_DIR_PATH / "woodworking_combined_problem.pddl"
WOODWORKING_COMBINED_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "ma_woodworking_trajectory.trajectory"

ROVERS_COMBINED_DOMAIN_PATH = EXAMPLES_DIR_PATH / "rover_combined_domain.pddl"
ROVERS_ESAM_DOMAIN_PATH = EXAMPLES_DIR_PATH / "rovers_esam_domain.pddl"
ROVERS_COMBINED_PROBLEM_PATH = EXAMPLES_DIR_PATH / "rovers_conflicing_actions_problem.pddl"
ROVERS_COMBINED_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "rovers_conflicting_actions_trajectory.trajectory"
ROVERS_COMBINED_ESAM_PROBLEM_PATH = EXAMPLES_DIR_PATH / "rovers_esam_problem.pddl"
ROVERS_COMBINED_ESAM_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "rovers_esam_problem.trajectory"

SPIDER_DOMAIN_PATH = EXAMPLES_DIR_PATH / "spider_domain.pddl"
SPIDER_PROBLEM_PATH = EXAMPLES_DIR_PATH / "spider_problem.pddl"
SPIDER_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "spider_trajectory.trajectory"

NURIKABE_DOMAIN_PATH = EXAMPLES_DIR_PATH / "nurikabe_domain.pddl"
NURIKABE_PROBLEM_PATH = EXAMPLES_DIR_PATH / "nurikabe_pfile_random-9x9-107.pddl"
NURIKABE_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "nurikabe_pfile_random-9x9-107.trajectory"

ADL_SATELLITE_DOMAIN_PATH = EXAMPLES_DIR_PATH / "adlSat.pddl"
ADL_SATELLITE_PROBLEM_PATH = EXAMPLES_DIR_PATH / "adlSat_problem.pddl"
ADL_SATELLITE_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "adlSat_trajectory.trajectory"

MINECRAFT_DOMAIN_PATH = EXAMPLES_DIR_PATH / "minecraft_domain.pddl"
MINECRAFT_PROBLEM_PATH = EXAMPLES_DIR_PATH / "minecraft_pfile0.pddl"
MINECRAFT_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "minecraft_pfile0.trajectory"
MINECRAFT_FLUENTS_MAP_PATH = EXAMPLES_DIR_PATH / "minecraft_fluents_map.json"

STAR_CRAFT_DOMAIN_PATH = EXAMPLES_DIR_PATH / "starcraft_domain.pddl"
STAR_CRAFT_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "starcraft_trajectory.trajectory"
STAR_CRAFT_FLUENTS_MAP_PATH = EXAMPLES_DIR_PATH / "starcraft_fluents_map.json"

MINECRAFT_MEDIUM_DOMAIN_PATH = EXAMPLES_DIR_PATH / "domain_minecraft_medium.pddl"
MINECRAFT_MEDIUM_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "trajectory_minecraft_medium.trajectory"
MINECRAFT_MEDIUM_FLUENTS_MAP_PATH = EXAMPLES_DIR_PATH / "fluents_map_minecraft_medium.json"

MINECRAFT_SMALL_DOMAIN_PATH = EXAMPLES_DIR_PATH / "minecraft_domain_small.pddl"
MINECRAFT_SMALL_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "minecraft_problem_small.trajectory"

MINECRAFT_LARGE_DOMAIN_PATH = EXAMPLES_DIR_PATH / "advanced_minecraft_domain.pddl"
MINECRAFT_LARGE_PROBLEM_PATH = EXAMPLES_DIR_PATH / "advanced_map_instance_0.pddl"
MINECRAFT_LARGE_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "advanced_map_instance_0.trajectory"

DRIVERLOG_POLY_DOMAIN_PATH = EXAMPLES_DIR_PATH / "driverlogHardNumeric.pddl"
DRIVERLOG_POLY_PROBLEM_PATH = EXAMPLES_DIR_PATH / "driverlog_poly_problem.pddl"
DRIVERLOG_POLY_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "driverlog_poly_problem.trajectory"

FARMLAND_DOMAIN_PATH = EXAMPLES_DIR_PATH / "farmland.pddl"
FARMLAND_TRAJECTORIES_DIRECTORY = EXAMPLES_DIR_PATH / "large_data_examples" / "farmland"
SAILING_TRAJECTORIES_DIRECTORY = EXAMPLES_DIR_PATH / "large_data_examples" / "sailing"

COUNTERS_POLYNOMIAL_DOMAIN_PATH = EXAMPLES_DIR_PATH / "counters_poly.pddl"
COUNTERS_POLYNOMIAL_PROBLEMS_PATH = [path for path in EXAMPLES_DIR_PATH.glob("pfile_counters_poly*.pddl")]
COUNTERS_POLYNOMIAL_TRAJECTORIES_PATH = [path for path in EXAMPLES_DIR_PATH.glob("pfile_counters_poly*.trajectory")]

BLOCKS_PROPOSITIONAL_DOMAIN_PATH = EXAMPLES_DIR_PATH / "blocksworld_propositional_domain.pddl"
BLOCKS_PROPOSITIONAL_PROBLEM_PATH = EXAMPLES_DIR_PATH / "blocks_propositional_prob00.pddl"
BLOCKS_PROPOSITIONAL_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "blocks_propositional.trajectory"

TEST_PPO_OBSERVATIONS_DIRECTORY = EXAMPLES_DIR_PATH / "ppo_observations"
TEST_PPO_MINECRAFT_DOMAIN = EXAMPLES_DIR_PATH / "ppo_minecraft_domain.pddl"

BARMAN_CLASSICAL_DOMAIN_PATH = EXAMPLES_DIR_PATH / "barman_domain.pddl"
BARMAN_CLASSICAL_PROBLEM_PATH = EXAMPLES_DIR_PATH / "barman_pfile3.pddl"
BARMAN_CLASSICAL_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "barman_pfile3.trajectory"

FARMLAND_EXAMPLES_PATH = EXAMPLES_DIR_PATH / "convex_state_data.csv"
FARMLAND_PAPER_EXAMPLES_PATH = EXAMPLES_DIR_PATH / "convex_state_data_for_paper.csv"
FARMLAND_SPAN_EXAMPLES_PATH = EXAMPLES_DIR_PATH / "span_convex_state_data.csv"

DEPOT_ONLINE_LEARNING_PROBLEM = EXAMPLES_DIR_PATH / "depot_numeric_problem_online_learning.pddl"
DEPOT_ONLINE_LEARNING_PROBLEM_WITH_NUMERIC_GOAL = (
        EXAMPLES_DIR_PATH / "depot_numeric_problem_online_learning_with_numeric_goals.pddl"
)
DEPOT_ONLINE_LEARNING_PLAN = EXAMPLES_DIR_PATH / "depot_numeric_problem_online_learning.solution"

OBJECT_TYPE = PDDLType(name="object")
AGENT_TYPE = PDDLType(name="agent")
CITY_TYPE = PDDLType(name="city", parent=OBJECT_TYPE)
WOODOBJ_TYPE = PDDLType(name="woodobj", parent=OBJECT_TYPE)
SURFACE_TYPE = PDDLType(name="surface", parent=OBJECT_TYPE)
TREATMENT_STATUS_TYPE = PDDLType(name="treatmentstatus", parent=OBJECT_TYPE)
COLOR_TYPE = PDDLType(name="acolour", parent=OBJECT_TYPE)
PART_TYPE = PDDLType(name="part", parent=WOODOBJ_TYPE)
TAXI_TYPE = PDDLType(name="taxi", parent=AGENT_TYPE)
TRUCK_TYPE = PDDLType(name="truck", parent=AGENT_TYPE)
CRATE_TYPE = PDDLType(name="crate", parent=OBJECT_TYPE)
AIRPLANE_TYPE = PDDLType(name="airplane", parent=AGENT_TYPE)
LOCATION_TYPE = PDDLType(name="location", parent=OBJECT_TYPE)
COUNT_TYPE = PDDLType(name="count", parent=OBJECT_TYPE)

AT_TRUCK_PREDICATE = Predicate(name="at", signature={"?a": AGENT_TYPE, "?loc": LOCATION_TYPE})

FUEL_COST_FUNCTION = PDDLFunction(name="fuel-cost", signature={})
LOAD_LIMIT_TRAJECTORY_FUNCTION = PDDLFunction(name="load_limit", signature={"?z": TRUCK_TYPE})
LOAD_LIMIT_GROUNDED_TRAJECTORY_FUNCTION = PDDLFunction(name="load_limit", signature={"truck1": TRUCK_TYPE})
CURRENT_LOAD_TRAJECTORY_FUNCTION = PDDLFunction(name="current_load", signature={"?z": TRUCK_TYPE})
CURRENT_LOAD_GROUNDED_TRAJECTORY_FUNCTION = PDDLFunction(name="current_load", signature={"truck1": TRUCK_TYPE})
WEIGHT_FUNCTION = PDDLFunction(name="weight", signature={"?c": CRATE_TYPE})

DRIVERLOG_COMBINED_DOMAIN_PATH = EXAMPLES_DIR_PATH / "driverlog_combined_domain.pddl"
DRIVERLOG_COMBINED_PROBLEM_PATH = EXAMPLES_DIR_PATH / "driverlog_conflicting_problem.pddl"
DRIVERLOG_COMBINED_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "driverlog_ma_sam_pfile2.trajectory"
ROVERS_COMBINED_WITH_MACRO_DOMAIN_PATH = EXAMPLES_DIR_PATH / "rovers_ma_plus_domain.pddl"

TWO_SIDES_OF_BOX_PATH = EXAMPLES_DIR_PATH / "negative_from_two_sides.csv"
CLOSE_TO_BOX_PATH = EXAMPLES_DIR_PATH / "negative_close_to_box.csv"
CLOSE_TO_LINEAR_CONDITION_PATH = EXAMPLES_DIR_PATH / "negative_close_to_linear_condition.csv"

COUNTERS_ONLINE_LEARNING_DOMAIN_PATH = EXAMPLES_DIR_PATH / "counters_domain_online_learning.pddl"
COUNTERS_ONLINE_LEARNING_PROBLEM_PATH = EXAMPLES_DIR_PATH / "pfile10_0_counters_online.pddl"

DEPOT_ERROR_IN_INCREMENTAL_HULL_CSV = EXAMPLES_DIR_PATH / "depot_numeric_unload_action_error_case.csv"

BARMAN_ERROR_IN_PRODUCTION_DOMAIN_PATH = EXAMPLES_DIR_PATH / "barman_bug_in_prod.pddl"
BARMAN_ERROR_IN_PRODUCTION_PROBLEM_PATH = EXAMPLES_DIR_PATH / "0_barman_prob.pddl"
BARMAN_ERROR_IN_PRODUCTION_TRAJECTORY_PATH = EXAMPLES_DIR_PATH / "0_barman_traj.trajectory"


def sync_snapshot(
        sam_learning: SAMLearner,
        component: ObservedComponent,
        trajectory_objects: Dict[str, PDDLObject],
        should_include_all_objects: bool = False,
) -> None:
    previous_state = component.previous_state
    next_state = component.next_state
    test_action_call = component.grounded_action_call
    sam_learning.current_trajectory_objects = trajectory_objects
    if should_include_all_objects:
        all_types = [pddl_type for pddl_type in sam_learning.partial_domain.types if pddl_type != "object"]
    else:
        all_types = []

    sam_learning.triplet_snapshot.create_triplet_snapshot(
        previous_state=previous_state,
        next_state=next_state,
        current_action=test_action_call,
        observation_objects=trajectory_objects,
        specific_types=all_types,
    )


def extract_preconditions_predicates(compound_preconditions: CompoundPrecondition) -> List[Predicate]:
    predicates = []
    for _, precond in compound_preconditions:
        if isinstance(precond, Predicate):
            predicates.append(precond)

    return predicates


def create_plan_actions(plan_path: Path) -> List[ActionCall]:
    """Creates a list of action calls from a plan file.

    :param plan_path:
    :return:
    """
    with open(plan_path, "rt") as plan_file:
        plan_lines = plan_file.readlines()

    plan_actions = []
    for line in plan_lines:
        plan_actions.append(parse_action_call(line))

    return plan_actions
