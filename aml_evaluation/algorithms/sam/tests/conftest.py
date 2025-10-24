import os
from typing import Dict

from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser, TrajectoryParser
from pddl_plus_parser.models import Domain, Problem, Observation, PDDLObject, MultiAgentObservation
from pytest import fixture

from sam_learning.learners import SAMLearner
from tests.consts import (
    ELEVATORS_DOMAIN_PATH,
    ELEVATORS_PROBLEM_PATH,
    ELEVATORS_TRAJECTORY_PATH,
    WOODWORKING_PROBLEM_PATH,
    WOODWORKING_TRAJECTORY_PATH,
    WOODWORKING_COMBINED_DOMAIN_PATH,
    WOODWORKING_COMBINED_PROBLEM_PATH,
    WOODWORKING_COMBINED_TRAJECTORY_PATH,
    ROVERS_COMBINED_DOMAIN_PATH,
    ROVERS_COMBINED_PROBLEM_PATH,
    ROVERS_COMBINED_TRAJECTORY_PATH,
    LOGISTICS_DOMAIN_PATH,
    SPIDER_DOMAIN_PATH,
    SPIDER_PROBLEM_PATH,
    SPIDER_TRAJECTORY_PATH,
    DEPOTS_NUMERIC_DOMAIN_PATH,
    DEPOTS_NUMERIC_PROBLEM_PATH,
    DEPOT_NUMERIC_TRAJECTORY_PATH,
    NURIKABE_DOMAIN_PATH,
    MINECRAFT_DOMAIN_PATH,
    MINECRAFT_PROBLEM_PATH,
    MINECRAFT_TRAJECTORY_PATH,
    SATELLITE_DOMAIN_PATH,
    SATELLITE_PROBLEM_PATH,
    SATELLITE_NUMERIC_TRAJECTORY_PATH,
    NURIKABE_PROBLEM_PATH,
    NURIKABE_TRAJECTORY_PATH,
    ADL_SATELLITE_DOMAIN_PATH,
    ADL_SATELLITE_PROBLEM_PATH,
    ADL_SATELLITE_TRAJECTORY_PATH,
    DEPOTS_DISCRETE_DOMAIN_PATH,
    DEPOTS_DISCRETE_PROBLEM_PATH,
    MINECRAFT_LARGE_DOMAIN_PATH,
    MINECRAFT_LARGE_PROBLEM_PATH,
    MINECRAFT_LARGE_TRAJECTORY_PATH,
    DRIVERLOG_COMBINED_DOMAIN_PATH,
    DRIVERLOG_COMBINED_PROBLEM_PATH,
    DRIVERLOG_COMBINED_TRAJECTORY_PATH,
    ROVERS_COMBINED_WITH_MACRO_DOMAIN_PATH,
    WOODWORKING_DOMAIN_PATH,
)
from utilities import NegativePreconditionPolicy

os.environ["CONVEX_HULL_ERROR_PATH"] = "tests\\convex_hull_error.txt"
DRIVERLOG_AGENT_NAMES = [f"driver{i}" for i in range(1, 9)]


@fixture()
def elevators_domain() -> Domain:
    domain_parser = DomainParser(ELEVATORS_DOMAIN_PATH, partial_parsing=True)
    return domain_parser.parse_domain()


@fixture()
def elevators_problem(elevators_domain: Domain) -> Problem:
    return ProblemParser(problem_path=ELEVATORS_PROBLEM_PATH, domain=elevators_domain).parse_problem()


@fixture()
def elevators_observation(elevators_domain: Domain, elevators_problem: Problem) -> Observation:
    return TrajectoryParser(elevators_domain, elevators_problem).parse_trajectory(ELEVATORS_TRAJECTORY_PATH)


@fixture()
def elevators_sam_learning(elevators_domain: Domain) -> SAMLearner:
    return SAMLearner(elevators_domain)


@fixture()
def elevators_sam_learning_soft_policy(elevators_domain: Domain) -> SAMLearner:
    return SAMLearner(elevators_domain, negative_preconditions_policy=NegativePreconditionPolicy.soft)


@fixture()
def elevators_sam_learning_hard_policy(elevators_domain: Domain) -> SAMLearner:
    return SAMLearner(elevators_domain, negative_preconditions_policy=NegativePreconditionPolicy.hard)


@fixture()
def elevators_objects(elevators_observation: Observation) -> Dict[str, PDDLObject]:
    return elevators_observation.grounded_objects


@fixture()
def logistics_domain() -> Domain:
    parser = DomainParser(LOGISTICS_DOMAIN_PATH, partial_parsing=True)
    return parser.parse_domain()


@fixture()
def rovers_domain() -> Domain:
    domain_parser = DomainParser(ROVERS_COMBINED_DOMAIN_PATH, partial_parsing=True)
    return domain_parser.parse_domain()


@fixture()
def woodworking_domain() -> Domain:
    return DomainParser(WOODWORKING_DOMAIN_PATH, partial_parsing=True).parse_domain()


@fixture()
def woodworking_problem(woodworking_domain: Domain) -> Problem:
    return ProblemParser(problem_path=WOODWORKING_PROBLEM_PATH, domain=woodworking_domain).parse_problem()


@fixture()
def woodworking_observation(woodworking_domain: Domain, woodworking_problem: Problem) -> Observation:
    return TrajectoryParser(woodworking_domain, woodworking_problem).parse_trajectory(WOODWORKING_TRAJECTORY_PATH)


@fixture()
def woodworking_ma_combined_domain() -> Domain:
    return DomainParser(WOODWORKING_COMBINED_DOMAIN_PATH, partial_parsing=True).parse_domain()


@fixture()
def woodworking_ma_combined_problem(woodworking_ma_combined_domain: Domain) -> Problem:
    return ProblemParser(problem_path=WOODWORKING_COMBINED_PROBLEM_PATH, domain=woodworking_ma_combined_domain).parse_problem()


@fixture()
def multi_agent_observation(woodworking_ma_combined_domain: Domain, woodworking_ma_combined_problem) -> MultiAgentObservation:
    return TrajectoryParser(woodworking_ma_combined_domain, woodworking_ma_combined_problem).parse_trajectory(
        WOODWORKING_COMBINED_TRAJECTORY_PATH, executing_agents=WOODWORKING_AGENT_NAMES
    )


@fixture()
def ma_rovers_domain() -> Domain:
    return DomainParser(ROVERS_COMBINED_DOMAIN_PATH, partial_parsing=True).parse_domain()


@fixture()
def ma_rovers_problem(ma_rovers_domain: Domain) -> Problem:
    return ProblemParser(problem_path=ROVERS_COMBINED_PROBLEM_PATH, domain=ma_rovers_domain).parse_problem()


@fixture()
def ma_rovers_observation(ma_rovers_domain: Domain, ma_rovers_problem: Problem) -> MultiAgentObservation:
    return TrajectoryParser(ma_rovers_domain, ma_rovers_problem).parse_trajectory(
        ROVERS_COMBINED_TRAJECTORY_PATH, executing_agents=ROVERS_AGENT_NAMES
    )


@fixture()
def spider_domain() -> Domain:
    return DomainParser(SPIDER_DOMAIN_PATH, partial_parsing=True).parse_domain()


@fixture()
def spider_problem(spider_domain: Domain) -> Problem:
    return ProblemParser(problem_path=SPIDER_PROBLEM_PATH, domain=spider_domain).parse_problem()


@fixture()
def spider_observation(spider_domain: Domain, spider_problem: Problem) -> Observation:
    return TrajectoryParser(spider_domain, spider_problem).parse_trajectory(SPIDER_TRAJECTORY_PATH)


@fixture()
def depot_domain() -> Domain:
    domain_parser = DomainParser(DEPOTS_NUMERIC_DOMAIN_PATH, partial_parsing=True)
    return domain_parser.parse_domain()


@fixture()
def depot_problem(depot_domain: Domain) -> Problem:
    return ProblemParser(problem_path=DEPOTS_NUMERIC_PROBLEM_PATH, domain=depot_domain).parse_problem()


@fixture()
def depot_discrete_domain() -> Domain:
    domain_parser = DomainParser(DEPOTS_DISCRETE_DOMAIN_PATH, partial_parsing=False)
    return domain_parser.parse_domain()


@fixture()
def depot_discrete_problem(depot_discrete_domain: Domain) -> Problem:
    return ProblemParser(problem_path=DEPOTS_DISCRETE_PROBLEM_PATH, domain=depot_discrete_domain).parse_problem()


@fixture()
def depot_observation(depot_domain: Domain, depot_problem: Problem) -> Observation:
    return TrajectoryParser(depot_domain, depot_problem).parse_trajectory(DEPOT_NUMERIC_TRAJECTORY_PATH)


@fixture()
def nurikabe_domain() -> Domain:
    return DomainParser(NURIKABE_DOMAIN_PATH, partial_parsing=True).parse_domain()


@fixture()
def nurikabe_problem(nurikabe_domain: Domain) -> Problem:
    return ProblemParser(problem_path=NURIKABE_PROBLEM_PATH, domain=nurikabe_domain).parse_problem()


@fixture()
def nurikabe_observation(nurikabe_domain: Domain, nurikabe_problem: Problem) -> Observation:
    return TrajectoryParser(nurikabe_domain, nurikabe_problem).parse_trajectory(NURIKABE_TRAJECTORY_PATH)


@fixture()
def satellite_adl_domain() -> Domain:
    return DomainParser(ADL_SATELLITE_DOMAIN_PATH, partial_parsing=True).parse_domain()


@fixture()
def satellite_adl_problem(satellite_adl_domain: Domain) -> Problem:
    return ProblemParser(problem_path=ADL_SATELLITE_PROBLEM_PATH, domain=satellite_adl_domain).parse_problem()


@fixture()
def satellite_adl_observation(satellite_adl_domain: Domain, satellite_adl_problem: Problem) -> Observation:
    return TrajectoryParser(satellite_adl_domain, satellite_adl_problem).parse_trajectory(ADL_SATELLITE_TRAJECTORY_PATH)


@fixture()
def minecraft_domain() -> Domain:
    domain_parser = DomainParser(MINECRAFT_DOMAIN_PATH, partial_parsing=True)
    return domain_parser.parse_domain()


@fixture()
def minecraft_full_domain() -> Domain:
    domain_parser = DomainParser(MINECRAFT_DOMAIN_PATH, partial_parsing=False)
    return domain_parser.parse_domain()


@fixture()
def minecraft_problem(minecraft_domain: Domain) -> Problem:
    return ProblemParser(problem_path=MINECRAFT_PROBLEM_PATH, domain=minecraft_domain).parse_problem()


@fixture()
def minecraft_observation(minecraft_domain: Domain, minecraft_problem: Problem) -> Observation:
    return TrajectoryParser(minecraft_domain, minecraft_problem).parse_trajectory(MINECRAFT_TRAJECTORY_PATH)


@fixture()
def satellite_numeric_domain() -> Domain:
    domain_parser = DomainParser(SATELLITE_DOMAIN_PATH, partial_parsing=True)
    return domain_parser.parse_domain()


@fixture()
def satellite_numeric_problem(satellite_numeric_domain: Domain) -> Problem:
    return ProblemParser(problem_path=SATELLITE_PROBLEM_PATH, domain=satellite_numeric_domain).parse_problem()


@fixture()
def satellite_numeric_observation(satellite_numeric_domain: Domain, satellite_numeric_problem: Problem) -> Observation:
    return TrajectoryParser(satellite_numeric_domain, satellite_numeric_problem).parse_trajectory(SATELLITE_NUMERIC_TRAJECTORY_PATH)


@fixture()
def minecraft_large_domain() -> Domain:
    domain_parser = DomainParser(MINECRAFT_LARGE_DOMAIN_PATH, partial_parsing=True)
    return domain_parser.parse_domain()


@fixture()
def minecraft_large_problem(minecraft_large_domain: Domain) -> Problem:
    return ProblemParser(problem_path=MINECRAFT_LARGE_PROBLEM_PATH, domain=minecraft_large_domain).parse_problem()


@fixture()
def minecraft_large_trajectory(minecraft_large_domain: Domain, minecraft_large_problem: Problem) -> Observation:
    return TrajectoryParser(minecraft_large_domain, minecraft_large_problem).parse_trajectory(MINECRAFT_LARGE_TRAJECTORY_PATH)
