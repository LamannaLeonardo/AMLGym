import os
import sys

import yaml

# Add current project to sys path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import contextlib
import logging
import random
import shutil
import subprocess

import numpy as np
import unified_planning
from alive_progress import alive_bar
from unified_planning.io import PDDLReader
from unified_planning.model import Problem, UPState
from unified_planning.plans import ActionInstance
from unified_planning.shortcuts import OneshotPlanner, SequentialSimulator

from modeling.trajectory import Trajectory


def problem_blocksworld(seed: int = 123 ,
                        ops: int = 4,
                        num: int = 3) -> str:
    """
    See `util/pddl-generators/blocksworld/README`.
    :param seed: random seed
    :param ops: number of operators
    :param num: number of blocks
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/blocksworld {ops} {num} {seed}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    # Add `block` object type
    problem = "\n".join(
        [r if not r.startswith('(:objects') else r.strip()[:-1] + "- block)" for r in problem.split('\n')])

    # Rename `arm-empty` to `handempty`
    problem = problem.replace('arm-empty', 'handempty')

    # Rename `on-table` to `ontable`
    problem = problem.replace('on-table', 'ontable')

    return problem


def problem_depots(e: int = 1,
                   i: int = 1,
                   t: int = 2,
                   p: int = 2,
                   h: int = 2,
                   c: int = 2,
                   s: int = 123) -> str:
    """
    See `util/pddl-generators/depots/README.txt`.
    :param e: number of depots
    :param i: number of distributors
    :param t: number of trucks
    :param p: number of pallets
    :param h: number of hoists
    :param c: number of crates
    :param s: random seed
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/depots -e {e} -i {i} -t {t} -p {p} -h {h} -c {c} -s {s}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    return problem


def problem_driverlog(seed: int = 123,
                      road_junctions: int = 1,
                      drivers: int = 1,
                      packages: int = 1,
                      trucks: int = 1) -> str:
    """
    See `util/pddl-generators/driverlog/README.txt`.
    :param seed: random seed
    :param road_junctions: total number of connections between all location pairs
    :param drivers: number of drivers
    :param packages: number of packages
    :param trucks: number of trucks
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/dlgen -t {seed} {road_junctions} {drivers} {packages} {trucks}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    # Remove cost metric
    problem = problem.replace("(:metric minimize (total-time))", "")

    return problem


def problem_barman(seed: int = 123,
                   num_cocktails: int = 2,
                   num_ingredients: int = 3,
                   num_shots: int = 3) -> str:
    """
    See `util/pddl-generators/barman/README.txt`.
    :param seed: random seed
    :param num_cocktails: number of cocktails
    :param num_ingredients: number of ingredients
    :param num_shots: number of shots
    :return: problem string
    """
    # Generate a problem
    result = subprocess.run(f"python {GEN_DIR}/{domain}/barman-generator.py {num_cocktails} {num_ingredients} {num_shots} {seed}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    return problem


def problem_ferry(s: int = 123,
                  l: int = 2,
                  c: int = 1) -> str:
    """
    See `util/pddl-generators/ferry/README.txt`.
    :param seed: random seed
    :param l: number of locations
    :param c: number of cars
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/ferry -l {l} -c {c} -s {s}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    # Add location and car types
    refactored_problem = []
    rows = problem.split('\n')
    for i in range(len(rows)):
        r = rows[i]
        if 'objects' in r:
            refactored_problem.append(f"{r} - location")
        elif 'objects' in rows[i-1]:
            refactored_problem.append(f"{r} - car")
        else:
            if not r.startswith('(location ') and not r.startswith('(car '):
                refactored_problem.append(r)
    problem = "\n".join(refactored_problem)

    return problem


def problem_floortile(seed: int = 123,
                      num_rows: int = 2,
                      num_columns: int = 2,
                      num_robots: int = 2,
                      mode_flag: str = 'seq') -> str:
    """
    See `util/pddl-generators/floortile/README.txt`.
    :param seed: random seed
    :param num_rows: number of rows
    :param num_columns: number of columns
    :param num_robots: number of robots
    :param mode_flag: either `seq` or `time`
    :return: problem string
    """

    # Generate a problem
    problem_name = f"floortile-r{num_rows}-c{num_columns}-robot{num_robots}-s{seed}"
    result = subprocess.run(f"./{GEN_DIR}/{domain}/floortile-generator.py {problem_name} {num_rows} {num_columns} {num_robots} {mode_flag} {seed}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    # Remove total cost a cost minimization
    problem = problem.replace('(= (total-cost) 0)', '')
    problem = problem.replace('(:metric minimize (total-cost))', '')

    return problem


def check_feasibility(problem: Problem,
                      current_state: UPState,
                      action_instance: ActionInstance) -> bool:
    """
    Check action execution does not make the problem unsolvable
    :param problem: solvable problem
    :param action: action to be executed
    :return: problem is solvable
    """
    # Update the problem initial state
    problem = problem.clone()
    for fluent in problem.initial_values:
        value = current_state.get_value(fluent)
        problem.set_initial_value(fluent, value)

    # Simulate action execution
    with SequentialSimulator(problem=problem) as simulator:
        current_state = simulator.apply(current_state, action_instance)

    # Update the problem state
    problem = problem.clone()
    for fluent in problem.initial_values:
        value = current_state.get_value(fluent)
        problem.set_initial_value(fluent, value)

    # Check a plan still exists
    logging.debug("Computing a new plan...")
    with contextlib.redirect_stdout(open(os.devnull, 'w')):
        with OneshotPlanner(name='fast-downward', problem_kind=problem.kind) as planner:
            result = planner.solve(problem, timeout=MAX_PLANNING_TIME)
            plan = result.plan

    return plan is not None


def generate_traj(
        problem: Problem,
        randomness: float = 0.2) -> Trajectory:

    with SequentialSimulator(problem=problem) as simulator:

        current_state = simulator.get_initial_state()
        states = [current_state]  # init trajectory states
        actions = []  # init trajectory actions
        plan = None
        while plan is None and len(states) < TRAJ_LEN_MAX:

            logging.debug("Computing a new plan...")
            with contextlib.redirect_stdout(open(os.devnull, 'w')):
                with OneshotPlanner(name='fast-downward', problem_kind=problem.kind) as planner:
                    result = planner.solve(problem, timeout=MAX_PLANNING_TIME)
                    plan = result.plan

            # Problem unsolvable
            if plan is None:
                if result.status.name == 'TIMEOUT':
                    logging.debug(f"Planning timout reached ({MAX_PLANNING_TIME}s).")
                    break
                else:
                    raise Exception(f"Planning exited with status: {result.status.name}")

            for action_instance in plan.actions:

                # Possibly execute a random action and replan
                if random.random() < randomness:
                    action, params = random.choices(list(simulator.get_applicable_actions(current_state)))[0]
                    action_instance = ActionInstance(action, params)

                    # Check random action does not make the problem unfeasible
                    while not check_feasibility(problem, current_state, action_instance):
                        logging.debug(f"[Debug] Random action {action_instance} makes the problem unsolvable."
                                      f" Newly sampling a random action.")
                        action, params = random.choices(list(simulator.get_applicable_actions(current_state)))[0]
                        action_instance = ActionInstance(action, params)

                    logging.debug(f"[Debug] Simulating random action {action_instance}.")
                    current_state = simulator.apply(current_state, action_instance)
                    states.append(current_state)
                    actions.append(action_instance)

                    # Update the problem initial state
                    problem = problem.clone()
                    for fluent in problem.initial_values:
                        value = current_state.get_value(fluent)
                        problem.set_initial_value(fluent, value)

                    # Trigger replanning
                    plan = None
                    break

                logging.debug(f"[Debug] Simulating action {action_instance}.")
                current_state = simulator.apply(current_state, action_instance)
                actions.append(action_instance)

                if current_state is None:
                    raise Exception(f"Error in applying: {action_instance}")

                states.append(current_state)

    # Randomly sample trajectory length
    done = (len(states) - TRAJ_LEN_MIN >= 0)  # check a sufficiently long trajectory can be generated from the plan
    traj_len = np.random.choice(range(TRAJ_LEN_MIN, len(states) + 1)) if done else 0

    # Randomly select a subset of states
    start_idx = np.random.choice(range(len(states) - traj_len + 1))
    states = states[start_idx:start_idx + traj_len]
    actions = actions[start_idx:start_idx + traj_len - 1]

    return Trajectory(states, actions)


if __name__ == '__main__':

    TRAJ_LEN_MIN = 5
    TRAJ_LEN_MAX = 30
    MAX_PLANNING_TIME = 300
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    GEN_DIR = "pddl-generators"
    BENCHMARK_DIR = "benchmarks"
    DOMAINS_DIR = "domains"
    PROB_DIR = "problems"
    TRAJ_DIR = "trajectories"
    CFG_DIR = "configs"
    DOM_CFG = f"{BENCHMARK_DIR}/{CFG_DIR}/domains.yaml"

    # Instantiate a PDDL problem reader
    reader = PDDLReader()

    # Disable printing of planning engine credits to avoid overloading stdout
    unified_planning.shortcuts.get_environment().credits_stream = None

    # Read domain configs
    with open(f"../{DOM_CFG}") as f:
        cfg = yaml.safe_load(f)
        seed = cfg['SEED']
        domains = cfg['domains']

    to_be_avoided = ['elevators', 'floortile']
    domains = {'floortile': domains['floortile']}

    for domain in domains:

        # Set random seed for reproducibility
        np.random.seed(seed)
        random.seed(seed)

        # Clean domain problems directory
        if os.path.exists(f"../{BENCHMARK_DIR}/{PROB_DIR}/{domain}"):
            shutil.rmtree(f"../{BENCHMARK_DIR}/{PROB_DIR}/{domain}")
        os.makedirs(os.path.join(f"../{BENCHMARK_DIR}/{PROB_DIR}/{domain}"))

        # Clean domain trajectories directory
        if os.path.exists(f"../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}"):
            shutil.rmtree(f"../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}")
        os.makedirs(os.path.join(f"../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}"))

        with alive_bar(len(domains[domain]),
                       title=f'Processing domain {domain}',
                       length=20,
                       bar='halloween') as bar:
            # For every domain problem kwargs
            for kwargs in domains[domain]:

                # Generate a problem
                generate_prob = getattr(sys.modules[__name__], f'problem_{domain}')
                problem_str = generate_prob(**kwargs)

                # Write the problem string to a file
                problem_file = f'../{BENCHMARK_DIR}/{PROB_DIR}/{domain}/{len(os.listdir(f"../{BENCHMARK_DIR}/{PROB_DIR}/{domain}"))}_{domain}_prob.pddl'
                with open(problem_file, 'w') as f:
                    f.write(problem_str.lower())

                # Parse the problem in unified-planning
                domain_file = f'../{BENCHMARK_DIR}/{DOMAINS_DIR}/{domain}.pddl'
                problem = reader.parse_problem(domain_file, problem_file)

                # Generate a trace by solving the problem
                trajectory = generate_traj(problem)
                while len(trajectory.states) < TRAJ_LEN_MIN:
                    logging.debug(f"[Debug] Failed to generate a sufficiently long trace. Retrying...")
                    trajectory = generate_traj(problem)

                trace_file = f'../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}/{len(os.listdir(f"../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}"))}_{domain}_traj'
                trajectory.write(trace_file)
                bar()  # update progress bar


