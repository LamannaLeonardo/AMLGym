import os
import sys

from alive_progress import alive_bar

# Add current project to sys path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import logging
from unified_planning.io import PDDLReader
import pandas as pd
from collections import defaultdict
from typing import Dict, Tuple


def get_object_stats(domain_file: str,
                     problem_file: str) -> Dict[Tuple[str, str], float]:

    # Parse the problem in unified-planning
    reader = PDDLReader()
    problem = reader.parse_problem(domain_file, problem_file)

    # Get number of objects grouped by type
    objects = defaultdict(int)
    objects['total_objects'] = len(problem.all_objects)  # get total number of objects
    for o in problem.all_objects:
        objects[o.type.name] += 1

    return objects


def write_trajectory_stats(file_name):
    all_domains_stats = dict()
    domains = sorted([d for d in os.listdir(f"../{BENCHMARK_DIR}/{TRAJ_DIR}")
                      if d not in ['.DS_Store']])
    with alive_bar(len(domains),
                   title=f'Producing trajectory statistics',
                   length=20,
                   bar='notes') as bar:

        for domain in domains:

            domain_file = f'../{BENCHMARK_DIR}/{DOMAINS_DIR}/{domain}.pddl'
            all_traj_stats = []

            for traj in sorted(os.listdir(f"../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}"),
                               key=lambda x: int(x.split("_")[0])):
                traj_stats = {'id': traj}

                traj_file = f"../{BENCHMARK_DIR}/{TRAJ_DIR}/{domain}/{traj}"
                problem_file = f"../{BENCHMARK_DIR}/{PROB_DIR}/{domain}/{traj.replace('_traj', '_prob.pddl')}"

                # Get number of states and actions
                with open(traj_file, 'r') as f:
                    rows = f.readlines()
                    traj_stats['actions'] = len([r for r in rows if r.startswith("(:action ")])
                    traj_stats['states'] = len([r for r in rows if r.startswith("(:state ")])

                # Get objects stats
                traj_stats.update(get_object_stats(domain_file, problem_file))

                # Store trajectory stats
                all_traj_stats.append(traj_stats)

            # Store domain stats
            stats = pd.DataFrame(all_traj_stats)
            all_domains_stats[domain] = stats

            bar()  # update progress bar

    # Write all domains statistics into xlsx
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    # Define a header format
    header_format = writer.book.add_format(
        {
            "bold": True,
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#D7E4BC",
            "border": 1,
        }
    )

    # Write one sheet for each domain
    for name, stats in all_domains_stats.items():
        stats.to_excel(writer, sheet_name=name, index=False, float_format="%.2f")
        # Access the worksheet

        # Auto-adjust the column width to make headers fully readable
        worksheet = writer.sheets[name]
        for col_num, value in enumerate(stats.columns.values):
            worksheet.write(0, col_num, value, header_format)
            max_len = max(
                stats[value].astype(str).map(len).max(),
                len(value)
            ) + 2  # offset
            worksheet.set_column(col_num, col_num, max_len)
    writer.close()


def write_domain_stats(file_name):

    all_domains_stats = list()
    domains = sorted([d for d in os.listdir(f"../{BENCHMARK_DIR}/{TRAJ_DIR}")
                          if d not in ['.DS_Store']])
    with alive_bar(len(domains),
                   title=f'Producing domain statistics',
                   length=20,
                   bar='bubbles') as bar:

        for domain in domains:

            # Parse the domain in unified-planning
            reader = PDDLReader()
            domain_file = f'../{BENCHMARK_DIR}/{DOMAINS_DIR}/{domain}.pddl'
            upl_domain = reader.parse_problem(domain_file)

            domain_stats = {
                'id': domain,
                'operators': len(upl_domain.actions),
                'min operators arity': min([len(a.parameters) for a in upl_domain.actions]),
                'max operators arity': max([len(a.parameters) for a in upl_domain.actions]),
                'predicates': len(upl_domain.fluents),
                'min predicates arity': min(f.arity for f in upl_domain.fluents),
                'max predicates arity': max(f.arity for f in upl_domain.fluents),
                'types': len(upl_domain.user_types),
            }

            # Store domain stats
            all_domains_stats.append(domain_stats)

            bar()  # update progress bar

    # Write all domains statistics into xlsx
    stats = pd.DataFrame(all_domains_stats)
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    # Define a header format
    header_format = writer.book.add_format(
        {
            "bold": True,
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#D7E4BC",
            "border": 1,
        }
    )

    # Write one sheet for each domain
    stats.to_excel(writer, sheet_name='domains', index=False, float_format="%.2f")
    # Access the worksheet

    # Auto-adjust the column width to make headers fully readable
    worksheet = writer.sheets['domains']
    for col_num, value in enumerate(stats.columns.values):
        worksheet.write(0, col_num, value, header_format)
        max_len = max(
            stats[value].astype(str).map(len).max(),
            len(value)
        ) + 2  # offset
        worksheet.set_column(col_num, col_num, max_len)
    writer.close()


if __name__ == '__main__':

    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    BENCHMARK_DIR = "benchmarks"
    DOMAINS_DIR = "domains"
    PROB_DIR = "problems"
    TRAJ_DIR = "trajectories"

    write_trajectory_stats(f"../{BENCHMARK_DIR}/trajectories.xlsx")
    write_domain_stats(f"../{BENCHMARK_DIR}/domains.xlsx")
