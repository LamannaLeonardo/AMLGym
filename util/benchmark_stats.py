import os
import sys
from collections import defaultdict
from typing import Dict, Tuple

import pandas as pd
from unified_planning.model import Problem

# Add current project to sys path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import logging
from unified_planning.io import PDDLReader
import pandas as pd


def get_object_stats(problem_file: str) -> Dict[Tuple[str, str], float]:
    # Parse the problem in unified-planning
    problem = reader.parse_problem(domain_file, problem_file)

    # Get number of objects grouped by type
    objects = defaultdict(int)
    objects['total_objects'] = len(problem.all_objects) # get total number of objecys
    for o in problem.all_objects:
        objects[o.type.name] += 1

    return objects


if __name__ == '__main__':

    TRAJ_LEN_MIN = 5
    TRAJ_LEN_MAX = 30
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    GEN_DIR = "pddl-generators"
    BENCHMARK_DIR = "benchmarks"
    DOMAINS_DIR = "domains"
    PROB_DIR = "problems"
    TRAJ_DIR = "trajectories"
    CFG_DIR = "configs"
    DOM_CFG = f"{BENCHMARK_DIR}/{CFG_DIR}/domains.yaml"
    STATS_DIR = "stats"

    os.makedirs(f"../{BENCHMARK_DIR}/{STATS_DIR}", exist_ok=True)

    # Instantiate a PDDL problem reader
    reader = PDDLReader()

    all_domains_stats = dict()

    for domain in [d for d in os.listdir(f"../{BENCHMARK_DIR}/{TRAJ_DIR}")]:

        domain_file = f'../{BENCHMARK_DIR}/{DOMAINS_DIR}/{domain}.pddl'
        domain_stats = []

        for traj in sorted(os.listdir(f"../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}"), key=lambda x: int(x.split("_")[0])):
            traj_stats = {'id': traj}

            traj_file = f"../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}/{traj}"
            problem_file = f"../{BENCHMARK_DIR}/{PROB_DIR}/{domain}/{traj.replace('_traj', '_prob.pddl')}"


            # Get number of states and actions
            with open(traj_file, 'r') as f:
                rows = f.readlines()
                traj_stats['actions'] = len([r for r in rows if r.startswith("(:action ")])
                traj_stats['states'] = len([r for r in rows if r.startswith("(:state ")])

            # Get objects stats
            traj_stats.update(get_object_stats(problem_file))

            # Store trajectory stats
            domain_stats.append(traj_stats)

        # Store domain stats
        stats = pd.DataFrame(domain_stats)
        stats.to_excel(f"../{BENCHMARK_DIR}/{STATS_DIR}/{domain}.xlsx", index=False, float_format="%.2f")
