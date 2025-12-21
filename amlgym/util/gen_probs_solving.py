# Add current project to sys path
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from .gen_problems import *  # do not remove

from datetime import datetime
import yaml
import re
import contextlib
import logging
import random
import shutil
import numpy as np
import unified_planning
from alive_progress import alive_bar
from unified_planning.io import PDDLReader
from unified_planning.shortcuts import OneshotPlanner


if __name__ == '__main__':

    MAX_PLANNING_TIME = 60
    PLANS_MIN_LEN = 5
    DOWNWARD_SEARCH_CFG = 'let(hff,ff(),let(hcea,cea(),lazy_greedy([hff,hcea],preferred=[hff,hcea])))'
    PLANNER_CFG = {  # heuristic planning
        'name': 'fast-downward',
        'params': dict(
            fast_downward_search_config=DOWNWARD_SEARCH_CFG,
            fast_downward_search_time_limit=f"{MAX_PLANNING_TIME}s"
        )}
    logging.basicConfig(
        # filename='out.log',
        level=logging.DEBUG
    )
    GEN_DIR = "pddl-generators"
    BENCHMARK_DIR = "benchmarks"
    DOMAINS_DIR = "domains"
    PROB_DIR = "problems/solving"
    DOM_CFG = f"{BENCHMARK_DIR}/problems_solving.yaml"

    # Trace CPU time
    run_start = datetime.now()

    # Instantiate a PDDL problem reader
    reader = PDDLReader()

    # Disable printing of planning engine credits to avoid overloading stdout
    unified_planning.shortcuts.get_environment().credits_stream = None

    # Read domain configs
    with open(f"../{DOM_CFG}") as f:
        cfg = yaml.safe_load(f)
        seed = cfg['SEED']
        domains = cfg['domains']

    to_be_avoided = []
    domains = {k: v for k, v in domains.items() if k not in to_be_avoided}

    for domain in domains:

        # Set random seed for reproducibility
        np.random.seed(seed)
        random.seed(seed)

        # Trace CPU time
        domain_run_start = datetime.now()

        # Clean domain problems directory
        if os.path.exists(f"../{BENCHMARK_DIR}/{PROB_DIR}/{domain}"):
            shutil.rmtree(f"../{BENCHMARK_DIR}/{PROB_DIR}/{domain}")
        os.makedirs(os.path.join(f"../{BENCHMARK_DIR}/{PROB_DIR}/{domain}"))

        with alive_bar(len(domains[domain]),
                       title=f'Processing domain {domain}',
                       length=20,
                       bar='halloween') as bar:
            # For every domain problem kwargs
            for i, kwargs in enumerate(domains[domain]):

                plan = None

                while (plan is None) or len(plan.actions) < PLANS_MIN_LEN:
                    # Generate a problem
                    logging.debug(f"Generating a new problem")
                    kwargs['seed'] = np.random.randint(1, 1000)
                    generate_prob = getattr(sys.modules[__name__], f'problem_{domain}')
                    problem_str = generate_prob(**kwargs)
                    # Fix hyphens to avoid issues with unified-planning parsing
                    problem_str = re.sub(r'(?<=\w)-(?=\w)', '_', problem_str)

                    # Write the problem string to a file
                    problems_dir = f"../{BENCHMARK_DIR}/{PROB_DIR}/{domain}"
                    problem_file = f'{problems_dir}/{len(os.listdir(problems_dir))}_{domain}_prob.pddl'
                    with open(problem_file, 'w') as f:
                        f.write(problem_str.lower())

                    # Parse the problem in unified-planning
                    domain_file = f'../{BENCHMARK_DIR}/{DOMAINS_DIR}/{domain}.pddl'
                    problem = reader.parse_problem(domain_file, problem_file)

                    # Solve the problem
                    logging.debug("Computing a new plan...")
                    with contextlib.redirect_stdout(open(os.devnull, 'w')):
                        with OneshotPlanner(
                                problem_kind=problem.kind,
                                **PLANNER_CFG
                        ) as planner:
                            result = planner.solve(problem, timeout=MAX_PLANNING_TIME)
                            plan = result.plan

                    if (plan is None) or len(plan.actions) < PLANS_MIN_LEN:
                        if plan is None:
                            logging.debug(f"Failed to generate a plan. Retrying...")
                        elif len(plan.actions) < PLANS_MIN_LEN:
                            logging.debug(f"Plan is not sufficiently long. Plan length is {len(plan.actions)}"
                                          f", minimum length is {PLANS_MIN_LEN}. Retrying...")
                        else:
                            raise Exception('Something went wrong during plan generation.')
                        plan = None
                        os.remove(problem_file)

                bar()  # update progress bar

    logging.info(f'Total CPU time (s): {(datetime.now() - run_start).seconds}')
