# Add current project to sys path
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from typing import List

import yaml
import re
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
                   seed: int = 123) -> str:
    """
    See `util/pddl-generators/depots/README.txt`.
    :param e: number of depots
    :param i: number of distributors
    :param t: number of trucks
    :param p: number of pallets
    :param h: number of hoists
    :param c: number of crates
    :param seed: random seed
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/depots -e {e} -i {i} -t {t} -p {p} -h {h} -c {c} -s {seed}".split(),
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


def problem_ferry(seed: int = 123,
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
    result = subprocess.run(f"./{GEN_DIR}/{domain}/ferry -l {l} -c {c} -s {seed}".split(),
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


def problem_goldminer(seed: int = 123,
                      r: int = 2,
                      c: int = 2) -> str:
    """
    See `util/pddl-generators/goldminer/README`.
    :param seed: random seed
    :param r: number of rows
    :param c: number of columns
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/gold-miner-generator -r {r} -c {c} -s {seed}".split(),
                            capture_output=True, text=True)
    problem = f"{result.stdout}\n)"

    return problem


def problem_grid(seed: int = 123,
                 x: int = 1,
                 y: int = 1,
                 t: int = 1,
                 p: List[int] = np.array([100]),
                 k: List[int] = np.array([1]),
                 l: List[int] = np.array([1])) -> str:
    """
    See `util/pddl-generators/grid/README`.
    :param seed: random seed
    :param x: horizontal extension of grid
    :param y: vertical extension of grid
    :param t: number of different key and lock types
    :param p: probability, for any key, to be mentioned in the goal
    :param k: number of keys vector (one 0 ... 9 entry for each type)
    :param l: number of locks vector (one 0 ... 9 entry for each type)
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/grid  -x {x} -y {y} -t {t} "
                            f"-k {str(k)[1:-1].replace(',', '').replace(' ', '')} "
                            f"-l {str(l)[1:-1].replace(',', '').replace(' ', '')} "
                            f"-s {seed}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    # Add object types
    refactored_problem = []
    rows = problem.split('\n')
    for i in range(len(rows)):
        if ' f0-' in rows[i] and rows[i+1].strip().startswith('shape0'):
            refactored_problem.append(f"{rows[i]} - place")
        elif ' shape' in rows[i] and rows[i+1].strip().startswith('key0-'):
            refactored_problem.append(f"{rows[i]} - shape")
        elif rows[i].strip().startswith('key') and rows[i+1] == ')':
            refactored_problem.append(f"{rows[i]} - key")
        elif '(key ' not in rows[i] and "(place " not in rows[i] and "(shape " not in rows[i]:
            refactored_problem.append(rows[i])
    problem = '\n'.join(refactored_problem)
    return problem


def problem_grippers(seed: int = 123,
                     n: int = 1,
                     r: int = 1,
                     o: int = 1) -> str:
    """
    See `util/pddl-generators/grippers/README.txt`.
    :param seed: random seed
    :param n: number of robots
    :param r: number of rooms
    :param o: number of balls
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/grippers  -n {n} -r {r} -o {o} -s {seed}".split(),
                            capture_output=True, text=True)
    problem = result.stdout
    problem = problem.replace(' object', ' ball')  # unified-planning does not support type `object`
    return problem


def problem_hanoi(seed: int = 123,
                  n: int = 1) -> str:
    """
    See `util/pddl-generators/hanoi/README.txt`.
    :param seed: random seed (not used since the problems generator is not randomized)
    :param n: number of discs
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/hanoi  -n {n}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    # Add object types
    refactored_problem = []
    rows = problem.split('\n')
    for i in range(len(rows)):
        if rows[i].startswith('(:objects'):
            platforms = [w for w in rows[i].split()[1:-1] if w.startswith('peg')]
            discs = [w for w in rows[i].split()[1:-1] if w.startswith('d')]
            refactored_problem.append(f"(:objects \n{' '.join(platforms)} - platform\n {' '.join(discs)} - disc\n)")
        else:
            refactored_problem.append(rows[i])
    problem = '\n'.join(refactored_problem)
    return problem


def problem_matchingbw(seed: int = 123,
                       n: int = 1) -> str:
    """
    See `util/pddl-generators/hanoi/README.txt`.
    :param seed: random seed (not used since the problems generator is not randomized)
    :param n: number of blocks
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/matching-bw-generator.sh tmp {n} {seed}".split(),
                            capture_output=True, text=True)
    with open(f"{GEN_DIR}/{domain}/tmp-typed.pddl", 'r') as f:
        problem = f.read()
    os.remove(f"{GEN_DIR}/{domain}/tmp-typed.pddl")
    os.remove(f"{GEN_DIR}/{domain}/tmp-untyped.pddl")

    return problem


def problem_miconic(seed: int = 123,
                       f: int = 1,
                       p: int = 1) -> str:
    """
    See `util/pddl-generators/miconic/README.txt`.
    :param seed: random seed
    :param f: number of floors
    :param p: number of passengers
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/miconic -f {f} -p {p} -r {seed}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    return problem


def problem_npuzzle(seed: int = 123,
                    n: int = 1) -> str:
    """
    See `util/pddl-generators/npuzzle/README.txt`.
    :param seed: random seed
    :param n: number of rows/columns
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/n-puzzle-generator -n {n} -s {seed}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    return problem


def problem_nomystery(seed: int = 123,
                      l: int = 1,
                      p: int = 1,
                      n: int = 1,
                      m: int = 1,
                      c: int = 1) -> str:
    """
    See `util/pddl-generators/nomystery/README.txt`.
    :param seed: random seed
    :param l: number of locations
    :param p: number of packages
    :param n: edges ratio in location graph (i.e. total edges = n * l)
    :param m: maximum edges weight
    :param c: constrainedness (initial fuel supply = c * optimal_cost)
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/nomystery -l {l} -p {p} -n {n} -m {m} -c {c} -s {seed} -e 0".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    # Remove total cost a cost minimization
    problem = problem.replace('(= (total-cost) 0)', '')
    problem = problem.replace('(:metric minimize (total-cost))', '')

    return problem


def problem_parking(seed: int = 123,
                    curbs: int = 1,
                    cars: int = 1) -> str:
    """
    See `util/pddl-generators/parking/README.txt`.
    :param seed: random seed
    :param curbs: number of curbs
    :param cars: number of cars
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"perl ./{GEN_DIR}/{domain}/parking-generator.pl _ {curbs} {cars} seq {seed}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    # Remove PDDL comments
    problem = '\n'.join([r for r in problem.split('\n') if not r.strip().startswith(';')])

    return problem


def problem_rovers(seed: int = 123,
                   r: int = 1,
                   w: int = 1,
                   o: int = 1,
                   c: int = 1,
                   g: int = 1) -> str:
    """
    See `util/pddl-generators/rovers/README`.
    :param seed: random seed
    :param r: number of rovers
    :param w: number of waypoints
    :param o: number of objectives
    :param c: number of cameras
    :param g: number of goals
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/rovgen {seed} {r} {w} {o} {c} {g}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    return problem


def problem_satellite(seed: int = 123,
                      s: int = 1,
                      i: int = 1,
                      m: int = 1,
                      t: int = 1,
                      o: int = 1) -> str:
    """
    See `util/pddl-generators/satellite/README`.
    :param seed: random seed
    :param s: number of satellites
    :param i: maximum number of instruments
    :param m: number of modes
    :param t: number of targets
    :param o: number of observations
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/satgen {seed} {s} {i} {m} {t} {o}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    return problem


def problem_sokoban(seed: int = 123,
                    n: int = 1,
                    b: int = 1,
                    w: int = 1) -> str:
    """
    See `util/pddl-generators/sokoban/README.txt`.
    :param seed: random seed
    :param n: grid size
    :param b: number of boxes
    :param w: number of walls
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/random/sokoban-generator-typed -n {n} -b {b} -w {w} -s {seed}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    return problem


def problem_spanner(seed: int = 123,
                    spanners: int = 1,
                    nuts: int = 1,
                    locations: int = 3) -> str:
    """
    See `util/pddl-generators/spanner/README.txt`.
    :param seed: random seed
    :param spanners: number of spanners
    :param nuts: number of nuts
    :param locations: number of locations
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"python ./{GEN_DIR}/{domain}/spanner-generator.py --seed {seed}"
                            f" {spanners} {nuts} {locations}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    return problem


def problem_tpp(seed: int = 123,
                p: int = 1,
                m: int = 1,
                t: int = 3,
                d: int = 3,
                l: int = 3) -> str:
    """
    See `util/pddl-generators/tpp/README`.
    :param seed: random seed
    :param p: number of products
    :param m: number of markets
    :param t: number of trucks
    :param d: number of depots
    :param l: maximum goods level
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/tpp -s {seed} -p {p} -m {m} -t {t} -d {d} -l {l} tmp.pddl".split(),
                            capture_output=True, text=True)

    with open(f"tmp.pddl", 'r') as f:
        problem = f.read()
    os.remove(f"tmp.pddl")

    return problem


def problem_transport(seed: int = 123,
                      generator: str = 'city',
                      n: int = 1,
                      size: int = 10,
                      degree: int = 3,
                      mindistance: int = 10,
                      trucks: int = 3,
                      packages: int = 3) -> str:
    """

    See `util/pddl-generators/transport/README.txt`.
    :param seed: random seed
    :param generator: transport generator type in [city, two-cities, three-cities]
    :param n: number of nodes
    :param size: size for computing `connect_distance` = math.sqrt((degree * size * size) / (nodes * math.pi * 0.694))
    :param degree: degree for computing `connect_distance` = math.sqrt((degree * size * size) / (nodes * math.pi * 0.694))
    :param mindistance: minimum distance between two nodes
    :param trucks: number of trucks
    :param packages: number of packages
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"python ./{GEN_DIR}/{domain}/{generator}-generator.py"
                            f" {n} {size} {degree} {mindistance} {trucks} {packages} {seed}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    # Remove total cost a cost minimization
    problem = problem.replace('(= (total-cost) 0)', '')
    problem = problem.replace('(:metric minimize (total-cost))', '')

    # Remove road lengths and comments
    problem = '\n'.join([r for r in problem.split('\n')
                         if not r.strip().startswith('(= ') and not r.strip().startswith(';')])

    return problem


def problem_zenotravel(seed: int = 123,
                       cities: int = 1,
                       planes: int = 1,
                       people: int = 3,
                       distance: int = 1) -> str:
    """
    See `util/pddl-generators/zenotravel/README`.
    :param seed: random seed
    :param cities: number of cities
    :param planes: number of planes
    :param people: number of people
    :param distance: numerical distance between cities
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"./{GEN_DIR}/{domain}/ztravel {seed} {cities} {planes} {people}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    return problem


def problem_childsnack(seed: int = 123,
                       children: int = 1,
                       trays: int = 1,
                       gluten_factor: int = 3,
                       const_ratio: int = 1.3) -> str:
    """
    See `util/pddl-generators/childsnack/README.txt`.
    :param seed: random seed
    :param children: number of children
    :param trays: number of trays
    :param gluten_factor: gluten ratio among children
    :param const_ratio: proportion of needed symbols that are declared in advance in the problem file.
    The min ratio should be 1.0 to guarantee solvability.
    :return: problem string
    """

    # Generate a problem
    result = subprocess.run(f"python ./{GEN_DIR}/{domain}/child-snack-generator.py pool "
                            f"{seed} {children} {trays} {gluten_factor} {const_ratio}".split(),
                            capture_output=True, text=True)
    problem = result.stdout

    return problem


def problem_elevators(seed: int = 123,
                      floors: int = 2,
                      area_size: int = 2,
                      fast_elevators: int = 1,
                      slow_elevators: int = 1,
                      fast_capacity: int = 1,
                      slow_capacity: int = 3,
                      passengers: int = 2) -> str:
    """
    See `util/pddl-generators/elevators/README.txt`.
    :param seed: random seed
    :param floors: number of floors
    :param area_size: area size (must be a factor of floors, otherwise passengers can start in out of bounds floors)
    :param fast_elevators: number of fast elevators
    :param slow_elevators: number of slow elevators
    :param fast_capacity: passengers capacity of every fast elevators
    :param slow_capacity: passengers capacity of every slow elevators
    :param passengers: number of passengers
    :return: problem string
    """

    def generate_executable(c_file_path: str, **kwargs):
        # Path to your C source file
        # c_file ==
        # executable = "./elevator_problem"  # Linux/macOS, use "elevator_problem.exe" for Windows

        c_file = 'my_generate_data.c'
        my_c_file = f"{os.path.join(*c_file_path.split('/')[:-1])}/{c_file}"
        shutil.copy(c_file_path, my_c_file)

        # Constants that can be changed
        constants = {"FLOORS", "AREA_SIZE", "FAST_ELEVATORS", "SLOW_ELEVATORS", "FAST_CAPACITY", "SLOW_CAPACITY"}
        assert set(kwargs.keys()).issubset({c.lower() for c in constants})

        # modify constants in the C file
        with open(my_c_file, "r") as f:
            c_code = f.read()
        for const, new_value in kwargs.items():
            pattern = rf"#define\s+{const.upper()}\s+\d+"
            replacement = f"#define {const.upper()} {new_value}"
            c_code = re.sub(pattern, replacement, c_code)

        # make generation reproducible by allowing for a random seed as input argument
        c_code = c_code.replace('MinPassengers=atoi(argv[1]);', 'srand((unsigned int)atoi(argv[1]));\nMinPassengers=atoi(argv[2]);')
        c_code = c_code.replace('MaxPassengers=atoi(argv[2]);', 'MaxPassengers=atoi(argv[3]);')
        c_code = c_code.replace('Step=atoi(argv[3]);', 'Step=atoi(argv[4]);')
        c_code = c_code.replace('MinID=atoi(argv[4]);', 'MinID=atoi(argv[5]);')
        c_code = c_code.replace(f'MaxID=atoi(argv[5]);', f'MaxID=atoi(argv[6]);')
        c_code = c_code.replace("if (argc!=6) {", "if (argc!=7) {")
        c_code = c_code.replace('printf("MinPassengers, MaxPassenegrs, Step, MinID, MaxID\n\nwhere:\n\n");',
                       'printf("Seed, MinPassengers, MaxPassenegrs, Step, MinID, MaxID\n\nwhere:\n\n");'
                       '\nprintf("Seed : random seed\n");')
        c_code = c_code.replace("srand( (unsigned)time( NULL ) );", "")

        # save the updated C file
        with open(my_c_file, "w") as file:
            file.write(c_code)

        # compile the C file
        executable_file_path = my_c_file.replace(".c", "")
        compile_cmd = ["gcc", my_c_file, "-o", executable_file_path]
        result = subprocess.run(compile_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("Compilation failed:\n", result.stderr)
            exit(1)
        return executable_file_path

    # Generate a problem
    executable_path = generate_executable(f"./{GEN_DIR}/{domain}/generate_data.c",
        **dict(floors=floors, area_size=area_size, fast_elevators=fast_elevators, slow_elevators=slow_elevators,
             fast_capacity=fast_capacity, slow_capacity=slow_capacity))
    # Generate problem in txt
    result = subprocess.run(f"{executable_path} {seed} {passengers} {passengers} 1 1 1".split(),
                            capture_output=True, text=True)
    # Parse problem in pddl
    result = subprocess.run(f"./{GEN_DIR}/{domain}/generate_pddl {floors} {floors} 1 {passengers} {passengers} 1 1 1".split(),
                            capture_output=True, text=True)

    prob_file = [f for f in os.listdir(f"./") if f.endswith('.pddl') and f.startswith('p')][0]
    with open(prob_file, 'r') as f:
        problem = f.read()
    os.remove(prob_file)
    os.remove(prob_file.replace('.pddl', '.txt'))

    # Remove cost functions
    problem = '\n'.join([r for r in problem.split('\n')
                         if ':metric' not in r and not r.startswith('(=')])

    return problem


#./"$GEN_DIR"/generate_data_p4-1 3 3 1 1 1
#./"$GEN_DIR"/generate_pddl 4 4 1 3 3 1 1 1

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
                elif result.status.name == 'UNSOLVABLE_INCOMPLETELY':
                    logging.debug(f"Planning unsolvable.")
                    break
                else:
                    raise Exception(f"Planning exited with status: {result.status.name}")

            for action_instance in plan.actions:

                # Possibly execute a random action and replan
                if random.random() < randomness:
                    action, params = random.choices(list(simulator.get_applicable_actions(current_state)))[0]
                    action_instance = ActionInstance(action, params)

                    # Check random action does not make the problem unfeasible
                    max_trials = 5
                    trial = 0
                    while not check_feasibility(problem, current_state, action_instance):
                        trial += 1
                        logging.debug(f"Random action {action_instance} makes the problem unsolvable."
                                      f" Newly sampling a random action.")
                        action, params = random.choices(list(simulator.get_applicable_actions(current_state)))[0]
                        action_instance = ActionInstance(action, params)
                        if trial > max_trials:
                            break

                    if trial > max_trials:
                        logging.debug(f"Maximum number of random action trials reached."
                                      f" Avoiding random action execution.")
                        # Trigger replanning
                        plan = None
                        break

                    logging.debug(f"Simulating random action {action_instance}.")
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

                logging.debug(f"Simulating action {action_instance}.")
                current_state = simulator.apply(current_state, action_instance)
                actions.append(action_instance)

                if current_state is None:
                    raise Exception(f"Error in applying: {action_instance}")

                states.append(current_state)

    # Randomly sample trajectory length
    done = (len(states) - TRAJ_LEN_MIN >= 0)  # check a sufficiently long trajectory can be generated from the plan
    traj_len = np.random.choice(range(TRAJ_LEN_MIN, min(TRAJ_LEN_MAX, len(states) + 1))) if done else 0

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

    to_be_avoided = [
        'floortile',    # problems are too hard to solve
        'npuzzle',      # problems are too hard to solve
        'sokoban',      # problems are too hard to solve
    ]
    # domains = {k: v for k, v in domains.items() if k not in to_be_avoided}
    domains = {k: v for k, v in domains.items() if k in to_be_avoided}


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

                trajectory = Trajectory([], [])

                while len(trajectory.states) < TRAJ_LEN_MIN:
                    # Generate a problem
                    logging.debug(f"Generating a new problem")
                    kwargs['seed'] = np.random.randint(1, 1000)
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
                    if len(trajectory.states) < TRAJ_LEN_MIN:
                        logging.debug(f"Failed to generate a sufficiently long trace. Retrying...")
                        os.remove(problem_file)
                        # trajectory = generate_traj(problem)

                trace_file = f'../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}/{len(os.listdir(f"../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}"))}_{domain}_traj'
                trajectory.write(trace_file)
                bar()  # update progress bar


