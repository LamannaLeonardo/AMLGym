import os
import sys
from collections import defaultdict
from itertools import cycle

import seaborn
from alive_progress import alive_bar

# Add current project to sys path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import logging
import pandas as pd
import re
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def plot_metric(metric: str,
                img_file_path: str) -> None:
    # get metrics for each algorithm and run
    alg_stats = defaultdict(list)
    for alg in os.listdir(RES_DIR):
        for run in [d for d in os.listdir(os.path.join(RES_DIR, alg)) if '.DS_' not in d]:
            alg_stats[alg].append(pd.read_excel(f"{RES_DIR}/{alg}/{run}/metrics.xlsx"))

    assert all(len(alg_stats[k]) == len(alg_stats[list(alg_stats.keys())[0]]) for k in alg_stats)

    # plot each algorithm metric
    domain_df = pd.read_excel(f"../{BENCHMARK_DIR}/domains.xlsx")
    for alg in alg_stats:
        # extract numeric columns
        numeric_cols = alg_stats[alg][0].select_dtypes(include='number').columns

        # average only numeric parts
        avg_numeric_df = pd.concat([df[numeric_cols] for df in alg_stats[alg]]).groupby(level=0).mean()

        # merge non-numeric (i.e. 'domain') from the original dataframe
        non_numeric_cols = alg_stats[alg][0].drop(columns=numeric_cols)
        avg_metric = pd.concat([non_numeric_cols, avg_numeric_df], axis=1)

        # sort by domain dataframe column `operators`
        merged_df = avg_metric.merge(domain_df[['domain', 'operators']], on='domain')
        avg_metric = merged_df.sort_values(by='operators')

        plt.plot(avg_metric['domain'], avg_metric[metric], marker='o', label=alg,
                 alpha=.8, color=color_map[next(colors)])

    plt.legend()

    # plt.title('Average number of objects')
    plt.ylabel(f'Avg #{metric}', size=18)
    plt.xticks(rotation=70, size=13)
    plt.yticks(rotation=0, size=13)
    plt.tight_layout()
    plt.savefig(img_file_path)


def barplot_metric(metric: str,
                   img_file_path: str) -> None:

    # get metrics for each algorithm and run
    algs = [a for a in os.listdir(RES_DIR) if '.' not in a]

    alg_stats = defaultdict(list)
    for alg in algs:
        for run in [d for d in os.listdir(os.path.join(RES_DIR, alg)) if '.DS_' not in d]:
            alg_stats[alg].append(pd.read_excel(f"{RES_DIR}/{alg}/{run}/metrics.xlsx"))

    assert all(len(alg_stats[k]) == len(alg_stats[list(alg_stats.keys())[0]]) for k in alg_stats)

    # plot each algorithm metric
    domain_df = pd.read_excel(f"../{BENCHMARK_DIR}/domains.xlsx")
    avg_alg_stats = defaultdict()
    for alg in alg_stats:
        # extract numeric columns
        numeric_cols = alg_stats[alg][0].select_dtypes(include='number').columns

        # average only numeric parts
        avg_numeric_df = pd.concat([df[numeric_cols] for df in alg_stats[alg]]).groupby(level=0).mean()

        # merge non-numeric (i.e. 'domain') from the original dataframe
        non_numeric_cols = alg_stats[alg][0].drop(columns=numeric_cols)
        avg_metric = pd.concat([non_numeric_cols, avg_numeric_df], axis=1)

        # sort by domain dataframe column `operators`
        merged_df = avg_metric.merge(domain_df[['domain', 'operators']], on='domain')
        merged_df = merged_df.sort_values(by='operators')

        metric_series = merged_df.set_index('domain')[metric]
        metric_series.name = alg  # gives the column a name

        avg_alg_stats[alg] = metric_series

    barplot_df = pd.concat(avg_alg_stats.values(), axis=1)
    barplot_df.columns = avg_alg_stats.keys()

    # ensure consistent order <-- this remove sorting by number of domain operators
    # barplot_df = barplot_df.loc[avg_metric['domain']]

    # plot grouped bar chart
    barplot_df.plot(
        # kind='barh',
        # figsize=(6, 6),
        kind='bar',
        figsize=(12, 6),
        alpha=.8,
        color=[color_map[next(colors)] for _ in range(len(avg_alg_stats))])

    plt.legend(prop={'size': 13}, loc='lower left')

    # plt.title('Average number of objects')
    plt.xlabel('')
    plt.ylabel(f'{metric.replace("_", " ").capitalize()}', size=18)
    plt.ylabel('')
    # plt.ylabel(f'Avg applicability precision', size=18)
    plt.xticks(
        # [i * 0.1 for i in range(11)],
        rotation=70, size=13)
    plt.yticks(rotation=0, size=13)
    plt.tight_layout()
    plt.savefig(img_file_path)


def print_best_table():

    # get metrics for each algorithm and run
    run = 'run0'

    sam = pd.read_excel(f"{RES_DIR}/SAM/{run}/metrics.xlsx")
    offlam = pd.read_excel(f"{RES_DIR}/OffLAM/{run}/metrics.xlsx")
    nolam = pd.read_excel(f"{RES_DIR}/NOLAM/{run}/metrics.xlsx")

    # Label the dataframes
    labeled_dfs = {'1': sam, '2': offlam, '3': nolam}

    # Stack dataframes into a single multi-indexed dataframe
    combined = pd.concat(labeled_dfs, names=['Algorithm'])

    # Unstack so each column becomes a 3D array: (index, column, algorithm)
    stacked = combined.stack().unstack('Algorithm')

    # Compute the best value (e.g., max) for each cell
    best_values = stacked.max(axis=1)  # or min(axis=1) for minimization

    # Find labels that achieved the best value
    best_labels = stacked.eq(best_values, axis=0)

    # For each cell, get the list of algorithm names that matched the best value
    # labels_per_cell = best_labels.apply(lambda row: f"$^{{{','.join(row.index[row].tolist())}}}$", axis=1)
    labels_per_cell = best_labels.apply(lambda row: ','.join(row.index[row].tolist()), axis=1)

    # Combine best value and labels in a readable format
    result = best_values.astype(str) + ' $^{' + labels_per_cell + '}$'

    # Reshape back to original dataframe shape
    final_result = result.unstack()

    # # Write best results into xlsx
    # writer = pd.ExcelWriter('bests.xlsx', engine='xlsxwriter')
    # final_result.to_excel(writer, index=False, float_format="%.2f")
    # writer.close()

    final_result.to_latex(f'{RES_DIR}/res_bests.tex', index=False, float_format="%.2f")


if __name__ == '__main__':

    BENCHMARK_DIR = "benchmarks"
    RES_DIR = "../res"

    logging.basicConfig(level=logging.INFO)

    colors = cycle(['blue', 'green', 'orange'])
    palette = seaborn.color_palette("Paired")
    color_map = {
        "blue": palette[1],  # Default "blue" color in the pastel palette
        "orange": palette[7],  # Default "orange" color
        "green": palette[3],
        "purple": palette[9],
        "brown": palette[11],
    }

    # Plot metric for every domain
    # plot_metric('syn precision', "../benchmarks/syn_precision.png")

    # barplot_metric('syn precision', f"{RES_DIR}/syn_precision.png")
    # barplot_metric('syn recall', f"{RES_DIR}/syn_recall.png")
    # barplot_metric('app precision', f"{RES_DIR}/app_precision.png")
    # barplot_metric('app recall', f"{RES_DIR}/app_recall.png")
    # barplot_metric('predicted_effects precision', f"{RES_DIR}/predeffs_precision.png")
    # barplot_metric('predicted_effects recall', f"{RES_DIR}/predeffs_recall.png")
    # barplot_metric('solving_ratio', f"{RES_DIR}/solving.png")
    # barplot_metric('false_plans_ratio', f"{RES_DIR}/false_plans.png")

    # print_best_table()
