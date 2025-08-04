import json
import os
import sys
from collections import defaultdict
from functools import reduce
from itertools import cycle
from typing import List

import seaborn

# Add current project to sys path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import logging
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def plot_metric(metric: List[str],
                img_file_path: str) -> None:

    # get metrics for each algorithm and run
    algs = [a for a in os.listdir(RES_DIR) if '.' not in a]

    alg_stats = defaultdict(list)
    for alg in algs:
        for run in [d for d in os.listdir(os.path.join(RES_DIR, alg)) if '.DS_' not in d]:
            with open(f"{RES_DIR}/{alg}/{run}/metrics.json", 'r') as f:
                # alg_stats[alg].append(pd.json_normalize(json.load(f)))

                df = pd.DataFrame.from_dict(
                    {
                        domain: {
                            metric[-1]: reduce(lambda d, key: d.get(key) if d else None, metric, values),
                            # 'applicability': values.get('applicability').get('avg_recall'),
                        }
                        for domain, values in json.load(f).items()
                    },
                    orient='index'
                ).reset_index().rename(columns={'index': 'domain'})
                alg_stats[alg].append(df)

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

        metric_series = merged_df.set_index('domain')[metric[-1]].astype(float)
        metric_series.name = alg  # gives the column a name

        avg_alg_stats[alg] = metric_series

    lineplot_df = pd.concat(avg_alg_stats.values(), axis=1)
    lineplot_df.columns = avg_alg_stats.keys()

    # Sort domains by average value across all algorithms
    domain_means = lineplot_df.mean(axis=1)
    lineplot_df = lineplot_df.loc[domain_means.sort_values().index]

    fig, ax = plt.subplots(figsize=(12, 6))

    for k, alg in enumerate(lineplot_df.columns):
        ax.plot(
            lineplot_df.index,
            lineplot_df[alg],
            label=alg,
            marker=next(markers),
            color=color_map[next(colors)],
            # alpha=.8,
            # linewidth=2,
            markersize=5 + (len(lineplot_df.columns) - k)*1.5
        )

    plt.legend(prop={'size': 13}, loc='lower right')

    # plt.title('Average number of objects')
    plt.xlabel('')
    plt.ylabel(f'{metric[-1].replace("_", " ").capitalize()}', size=18)
    plt.ylabel('')
    plt.title(' '.join(metric).replace('_', ' ').capitalize(), size=18)
    plt.xticks(rotation=70, size=13)
    plt.yticks(rotation=0, size=13)
    plt.tight_layout()
    plt.savefig(img_file_path)


def save_results_dataframe(res_file_path: str) -> None:
    # get metrics for each algorithm and run
    algs = [a for a in os.listdir(RES_DIR) if '.' not in a]

    alg_stats = defaultdict(list)
    for alg in algs:
        for run in [d for d in os.listdir(os.path.join(RES_DIR, alg)) if '.DS_' not in d]:
            alg_stats[alg].append(pd.read_excel(f"{RES_DIR}/{alg}/{run}/metrics.xlsx"))

    # Add a column to each
    all_dfs = []
    for alg, stats in alg_stats.items():
        alg_stats[alg][0]['algorithm'] = alg  # TODO: automatically average multiple runs
        all_dfs.append(alg_stats[alg][0])

    # Concatenate them
    df_all = pd.concat(all_dfs, ignore_index=True)

    # Sort by domain
    df_all = df_all.sort_values(by='domain')

    # Move "algorithm" column at the beginning
    df_all = df_all[[df_all.columns[-1]] + list(df_all.columns[:-1])]

    # Apply color gradient
    df_all = df_all.style.background_gradient(axis=0)

    # Save the dataframe to excel
    assert res_file_path.endswith('.xlsx'), f".xlsx file format must be used, current file name is {res_file_path}"
    df_all.to_excel(f"{RES_DIR}/{res_file_path}", index=False)


def lineplot_metric(metric: str,
                    img_file_path: str) -> None:
    # get metrics for each algorithm and run
    algs = [a for a in os.listdir(RES_DIR) if '.' not in a]

    alg_stats = defaultdict(list)
    for alg in algs:
        for run in [d for d in os.listdir(os.path.join(RES_DIR, alg)) if '.DS_' not in d]:
            alg_stats[alg].append(pd.read_excel(f"{RES_DIR}/{alg}/{run}/metrics.xlsx"))

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

    lineplot_df = pd.concat(avg_alg_stats.values(), axis=1)
    lineplot_df.columns = avg_alg_stats.keys()

    # Sort domains by average value across all algorithms
    domain_means = lineplot_df.mean(axis=1)
    lineplot_df = lineplot_df.loc[domain_means.sort_values().index]

    fig, ax = plt.subplots(figsize=(12, 6))

    for k, alg in enumerate(lineplot_df.columns):
        ax.plot(
            lineplot_df.index,
            lineplot_df[alg],
            label=alg,
            marker=next(markers),
            color=color_map[next(colors)],
            # alpha=.8,
            linewidth=2,
            markersize=5 + (len(lineplot_df.columns) - k)*1.5
        )

    plt.legend(prop={'size': 15}, loc='lower right')

    # plt.title('Average number of objects')
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=70, size=15)
    plt.yticks(rotation=0, size=15)
    plt.yticks([i * 0.1 for i in range(2, 11)],
               rotation=0, size=15)
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

    # # Sort domains by average value across all algorithms
    domain_means = barplot_df.mean(axis=1)
    barplot_df = barplot_df.loc[domain_means.sort_values().index]

    # plot grouped bar chart
    barplot_df.plot(
        # kind='barh',
        kind='bar',
        figsize=(12, 6),
        alpha=.8,
        color=[color_map[next(colors)] for _ in range(len(avg_alg_stats))]
    )

    plt.legend(prop={'size': 15}, loc='lower right')

    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=70, size=15)
    plt.yticks(rotation=0, size=15)
    plt.tight_layout()
    plt.savefig(img_file_path)


def print_metrics_table(metrics: List[str], run_dir: str = 'run0') -> None:
    # List algorithms
    algs = list(filter(os.path.isdir, [f"{RES_DIR}/{d}" for d in os.listdir(RES_DIR)]))

    # MultiIndex for columns
    columns = [('', 'Domain')] + [(metric, alg.split('/')[-1]) for metric in metrics for alg in algs]
    df = pd.DataFrame(columns=pd.MultiIndex.from_tuples(columns))

    # Load domains from the first algorithm
    with open(f'{algs[0]}/{run_dir}/metrics.json', 'r') as f:
        domains = json.load(f).keys()

    for d in domains:
        eval_row = {('', 'Domain'): d}
        metric_values = {metric: {} for metric in metrics}

        # Collect all values for later comparison
        for alg in algs:
            alg_name = alg.split('/')[-1]
            all_run_dfs = []
            for run_dir in os.listdir(f"{RES_DIR}/{alg}"):
                run_df = pd.read_excel(f"{RES_DIR}/{alg}/{run_dir}/metrics.xlsx")
                all_run_dfs.append(run_df)

            assert len(all_run_dfs) > 0, f'There is no run directory (e.g. "run0") in {RES_DIR}/{alg}.'

            # extract numeric columns
            numeric_cols = run_df.select_dtypes(include='number').columns

            # average only numeric parts
            avg_numeric_df = pd.concat([df[numeric_cols] for df in all_run_dfs]).groupby(level=0).mean()

            # merge non-numeric (i.e. 'domain') from the original dataframe
            non_numeric_cols = run_df.drop(columns=numeric_cols)
            alg_df = pd.concat([non_numeric_cols, avg_numeric_df], axis=1)

            alg_dom_df = alg_df[alg_df["domain"] == d]

            for metric in metrics:
                val = alg_dom_df[metric].values[0]
                metric_values[metric][alg_name] = val

        # Format with bold for best values
        for metric in metrics:
            values = metric_values[metric]
            max_val = max(values.values())
            min_val = min(values.values())

            for alg_name, val in values.items():
                val_fmt = f"{val:.2f}"
                if metric in ['false_plans_ratio']:
                    if val == min_val:
                        eval_row[(metric, alg_name)] = f"$\\mathbf{{{val_fmt}}}$"
                    else:
                        eval_row[(metric, alg_name)] = f"${val_fmt}$"
                else:
                    if val == max_val:
                        eval_row[(metric, alg_name)] = f"$\\mathbf{{{val_fmt}}}$"
                    else:
                        eval_row[(metric, alg_name)] = f"${val_fmt}$"

        df = pd.concat([df, pd.DataFrame([eval_row])], ignore_index=True)

    # # Transpose it
    # df = df.transpose()
    # # Optionally reset the index to make it a column in LaTeX output
    # df.reset_index(inplace=True)

    # Save to LaTeX
    df.to_latex(
        # f"{RES_DIR}/{'_'.join(metrics)}.tex",
        f"{RES_DIR}/all_metrics.tex",
        index=False,
        escape=False,
        # column_format=f"l|{'|'.join([''.join('c' for _ in algs) for _ in metrics])}",
        # label=f"tab:something",
        # caption="something"
    )


def print_best_table():

    # evaluated algorithms to be included in the table
    algs = ['SAM', 'OffLAM', 'ROSAME', 'NOLAM']

    # evaluation metrics to be included in the table
    metrics = ['domain', 'app precision', 'app recall',
               'predicted_effects precision', 'predicted_effects recall',
               'solving_ratio', 'false_plans_ratio']

    # get metrics for each algorithm averaged over all runs
    labeled_dfs = dict()
    for i, alg in enumerate(algs):
        all_run_dfs = []
        for run_dir in os.listdir(f"{RES_DIR}/{alg}"):
            run_df = pd.read_excel(f"{RES_DIR}/{alg}/{run_dir}/metrics.xlsx")
            all_run_dfs.append(run_df)

        assert len(all_run_dfs) > 0, f'There is no run directory (e.g. "run0") in {RES_DIR}/{alg}.'

        # extract numeric columns
        numeric_cols = run_df.select_dtypes(include='number').columns

        # average only numeric parts
        avg_numeric_df = pd.concat([df[numeric_cols] for df in all_run_dfs]).groupby(level=0).mean()

        # merge non-numeric (i.e. 'domain') from the original dataframe
        non_numeric_cols = run_df.drop(columns=numeric_cols)
        alg_df = pd.concat([non_numeric_cols, avg_numeric_df], axis=1)
        labeled_dfs[str(i + 1)] = alg_df[metrics]

    # sam = pd.read_excel(f"{RES_DIR}/SAM/{run}/metrics.xlsx")[metrics]
    # offlam = pd.read_excel(f"{RES_DIR}/OffLAM/{run}/metrics.xlsx")[metrics]
    # nolam = pd.read_excel(f"{RES_DIR}/NOLAM/{run}/metrics.xlsx")[metrics]
    # rosame = pd.read_excel(f"{RES_DIR}/ROSAME/{run}/metrics.xlsx")[metrics]
    #
    # # Label the dataframes
    # labeled_dfs = {'1': sam, '2': offlam, '3': rosame, '4': nolam}

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
    final_result.to_latex(f'{RES_DIR}/res_bests.tex', index=False, float_format="%.2f",
                          caption="Best metric values for every domain obtained among "
                                  f"{','.join([f'{i+1}: {k}' for i, k in enumerate(algs)])}"
                          )


if __name__ == '__main__':

    BENCHMARK_DIR = "benchmarks"
    RES_DIR = "../res"

    logging.basicConfig(level=logging.INFO)

    colors = cycle(['blue', 'orange', 'red', 'purple'])
    markers = cycle(['s', 'd', '*', '.'])

    palette = seaborn.color_palette("Paired")
    color_map = {
        "lightblue": palette[0],  # Default "lightblue" color in the pastel palette
        "blue": palette[1],  # Default "blue" color in the pastel palette
        "orange": palette[7],  # Default "orange" color
        "green": palette[3],   # ...
        "purple": palette[9],
        "brown": palette[11],
        "red": palette[5],
    }

    # Concatenate and save all algorithm results
    # save_results_dataframe('results.xlsx')

    # Generate metric barplot grouped by domain for every algorithm
    # barplot_metric('syn precision', f"{RES_DIR}/syn_precision.png")
    # barplot_metric('syn recall', f"{RES_DIR}/syn_recall.png")
    # barplot_metric('app precision', f"{RES_DIR}/app_precision.png")
    # barplot_metric('app recall', f"{RES_DIR}/app_recall.png")
    # barplot_metric('predicted_effects precision', f"{RES_DIR}/predeffs_precision.png")
    # barplot_metric('predicted_effects recall', f"{RES_DIR}/predeffs_recall.png")
    # barplot_metric('solving_ratio', f"{RES_DIR}/solving.png")
    # barplot_metric('false_plans_ratio', f"{RES_DIR}/false_plans.png")

    # Generate metric lineplot grouped by domain for every algorithm
    lineplot_metric('syn precision', f"{RES_DIR}/syn_precision_line.png")
    lineplot_metric('syn recall', f"{RES_DIR}/syn_recall_line.png")
    lineplot_metric('app precision', f"{RES_DIR}/app_precision_line.png")
    lineplot_metric('app recall', f"{RES_DIR}/app_recall_line.png")
    lineplot_metric('predicted_effects precision', f"{RES_DIR}/predeffs_precision_line.png")
    lineplot_metric('predicted_effects recall', f"{RES_DIR}/predeffs_recall_line.png")
    lineplot_metric('solving_ratio', f"{RES_DIR}/solving_line.png")
    lineplot_metric('false_plans_ratio', f"{RES_DIR}/false_plans_line.png")

    # Print a table for the given metrics
    # metrics = [
    #     # "syn precision",
    #     # "syn recall",
    #     # "app precision",
    #     # "app recall",
    #     # "predicted_effects precision",
    #     # "predicted_effects recall",
    #     "solving_ratio",
    #     # "false_plans_ratio"
    # ]
    # print_metrics_table(metrics)

    # Print the best results achieved for every domain among all algorithms
    # print_best_table()

    # Plot metric results for preconditions/effects
    # for metric in [
    #     # ['syntactic', 'precs_pos_precision'],
    #     # ['syntactic', 'precs_neg_precision'],
    #     # ['syntactic', 'pos_precision'],
    #     # ['syntactic', 'neg_precision'],
    #     ['syntactic', 'precs_pos_recall'],
    #     # ['syntactic', 'pos_recall'],
    #     # ['syntactic', 'neg_recall']
    # ]:
    #     plot_metric(metric, f"{RES_DIR}/{metric[-1]}.png")
