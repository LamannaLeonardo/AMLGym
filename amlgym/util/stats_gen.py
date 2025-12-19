import os
import sys

import numpy as np
from alive_progress import alive_bar

# Add current project to sys path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import logging
from unified_planning.io import PDDLReader
from collections import defaultdict
from typing import Dict, Tuple
import pandas as pd
import re
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def get_object_stats(domain_file: str,
                     problem_file: str) -> Dict[Tuple[str, str], float]:

    # Parse the problem in unified-planning
    reader = PDDLReader()
    problem = reader.parse_problem(domain_file, problem_file)

    # Get number of objects grouped by type
    objects = defaultdict(int)
    objects['objects'] = len(problem.all_objects)  # get total number of objects
    for o in problem.all_objects:
        objects[o.type.name] += 1

    return objects


def write_trajectory_stats(file_name):
    all_domains_stats = dict()
    domains = sorted([d for d in os.listdir(f"../{BENCHMARK_DIR}/{TRAJ_DIR}")
                      if d not in ['.DS_Store']])

    min_objs = np.inf
    max_objs = -1
    min_states = np.inf
    max_states = -1
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

            # Update overall stats
            min_objs = min(min_objs, all_domains_stats[domain]['objects'].min())
            max_objs = max(max_objs, all_domains_stats[domain]['objects'].max())
            min_states = min(min_states, all_domains_stats[domain]['states'].min())
            max_states = max(max_states, all_domains_stats[domain]['states'].max())

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

    # print overall stats
    print(f'Minimum number of objects: {min_objs}\n'
          f'Maximum number of objects: {max_objs}\n'
          f'Minimum number of states: {min_states}\n'
          f'Maximum number of states: {max_states}')


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
                'domain': domain,
                'operators': len(upl_domain.actions),
                'min operators arity': min([len(a.parameters) for a in upl_domain.actions]),
                'max operators arity': max([len(a.parameters) for a in upl_domain.actions]),
                'predicates': len(upl_domain.fluents),
                'min predicates arity': min(f.arity for f in upl_domain.fluents),
                'max predicates arity': max(f.arity for f in upl_domain.fluents),
                'types': len(upl_domain.user_types),
                'constants': 'no' if domain not in ['childsnack'] else 'yes',
                'negative preconditions': 'no',
                'injective assumption': 'no' if np.any([len([p.type.name for p in a.parameters])
                                                    > len({p.type.name for p in a.parameters})
                                                    for a in upl_domain.actions]) else 'yes'

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


def plot_avg_attr(df_file_path: str,
                     attribute: str,
                     img_file_path: str) -> None:

    # Load all sheets into a dictionary of DataFrames
    all_sheets = pd.read_excel(df_file_path, sheet_name=None)

    # Collect all data in one list
    all_data = []

    for sheet_name, df in all_sheets.items():
        df = df.copy()

        # extract the trajectory number from 'id' (e.g. '0_blocksworld_traj' -> '0')
        df['x'] = df['id'].apply(lambda s: re.match(r'^(\d+)_', s).group(1) if re.match(r'^(\d+)_', s) else None)

        # Keep only necessary columns
        all_data.append(df[['x', attribute]])

    # Combine all domains into one DataFrame
    combined = pd.concat(all_data)

    # Group by 'x' and average total_objects
    grouped = combined.groupby('x')[attribute].mean().sort_index()

    # Plot
    plt.figure(figsize=(10, 6))
    grouped.plot(kind='bar', color='skyblue', edgecolor='none')
    # plt.title('Average number of objects')
    plt.xlabel('Trajectory', size=18)
    plt.ylabel(f'#{attribute.capitalize()}', size=18)
    plt.xticks(rotation=0, size=13)
    plt.yticks(rotation=0, size=13)
    plt.tight_layout()
    plt.savefig(img_file_path)


def print_domain_stats(domain_df):
    df = pd.read_excel(f"../{BENCHMARK_DIR}/domains.xlsx")
    print(f"Max operators: {df['operators'].max()}")
    print(f"min operators: {df['operators'].min()}")
    print(f"Max predicates: {df['predicates'].max()}")
    print(f"min predicates: {df['predicates'].min()}")
    print(f"Max types: {df['types'].max()}")
    print(f"min types: {df['types'].min()}")


def print_traj_table(traj_df):
    # Load Excel file with multiple sheets
    xls = pd.read_excel(traj_df, sheet_name=None)  # sheet_name=None loads all sheets

    # Identify common columns
    common_cols = set.intersection(*(set(df.columns) for df in xls.values()))

    # Compute averages for common columns per sheet
    averages = {
        sheet_name: df[list(common_cols)].mean(numeric_only=True)
        for sheet_name, df in xls.items()
    }

    # Convert to DataFrame for LaTeX export
    average_df = pd.DataFrame(averages).T  # Transpose to have sheet names as rows

    # Optionally round for presentation
    average_df = average_df.round(2)

    # Export to LaTeX
    latex_table = average_df.to_latex(index=True,
                                      caption="Stastistics of the trajectories.",
                                      label="tab:traj-stats",
                                      float_format="%.2f")

    print(latex_table)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    BENCHMARK_DIR = "benchmarks"
    DOMAINS_DIR = "domains"
    PROB_DIR = "problems/learning"
    TRAJ_DIR = "trajectories/learning"

    # # Generate xlsx file of trajectory statistics
    # write_trajectory_stats(f"../{BENCHMARK_DIR}/trajectories.xlsx")
    # print_traj_table(f"../{BENCHMARK_DIR}/trajectories.xlsx")
    #
    # # Generate xlsx file of domain statistics
    # write_domain_stats(f"../{BENCHMARK_DIR}/domains.xlsx")
    #
    # # # Print domain statistics into a markdown table
    # domain_table_columns = ['domain', 'operators', 'predicates', 'types', 'constants',
    #                         'min operators arity', 'max operators arity',
    #                         'min predicates arity', 'max predicates arity', 'negative preconditions',
    #                         'injective assumption']
    # print(pd.read_excel(f"../{BENCHMARK_DIR}/domains.xlsx")[domain_table_columns].to_markdown(index=False))
    #
    # # Print domain statistics into an html table
    # print(pd.read_excel(f"../{BENCHMARK_DIR}/domains.xlsx")[domain_table_columns].to_html(index=False))
    #
    # # Print domain statistics into latex table
    # print(pd.read_excel(f"../{BENCHMARK_DIR}/domains.xlsx")[domain_table_columns].to_latex(index=False))

    # # Print domain statistics
    # print_domain_stats(pd.read_excel(f"../{BENCHMARK_DIR}/domains.xlsx"))

    # # Plot number of objects for every trace averaged over all domains
    # plot_avg_attr(f"../{BENCHMARK_DIR}/trajectories_hard.xlsx",
    #               'objects',
    #               f"../{BENCHMARK_DIR}/objects.png")
    #
    # # Plot number of states for every trace averaged over all domains
    # plot_avg_attr(f"../{BENCHMARK_DIR}/trajectories_hard.xlsx",
    #               'states',
    #               f"../{BENCHMARK_DIR}/states.png")
