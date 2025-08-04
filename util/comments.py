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
import pandas as pd

if __name__ == '__main__':

    BENCHMARK_DIR = "benchmarks"
    RES_DIR = "../res"

    # get metrics for each algorithm and run
    algs = [a for a in os.listdir(RES_DIR) if '.' not in a]
    for alg in algs:
        print(f"\n\n\n###############################################"
              f"\n#################### {alg} ####################"
              f"\n###############################################")
        for run in sorted([d for d in os.listdir(os.path.join(RES_DIR, alg)) if '.DS_' not in d],
                          key=lambda x: int(x.replace('run', ''))):
            print(f"\n\n#################### {run} ####################")

            with open(f"{RES_DIR}/{alg}/{run}/metrics.json", 'r') as f:
                alg_df = pd.DataFrame.from_dict(
                    {
                        domain: {
                            # metric[-1]: reduce(lambda d, key: d.get(key) if d else None, metric, values),
                            'app_prec': values.get('applicability').get('avg_precision'),
                            'app_rec': values.get('applicability').get('avg_recall'),
                            'syn_prec': values.get('syntactic').get('overall_precision'),
                            'syn_recall': values.get('syntactic').get('overall_recall'),
                            'predeff_prec': values.get('predicted_effects').get('avg_precision'),
                            'predeff_recall': values.get('predicted_effects').get('avg_recall'),
                            'precs_prec': values.get('syntactic').get('precs_pos_precision'),
                            'precs_recall': values.get('syntactic').get('precs_pos_recall'),
                            'pos_prec': values.get('syntactic').get('pos_precision'),
                            'neg_prec': values.get('syntactic').get('neg_precision'),
                            'pos_recall': values.get('syntactic').get('pos_recall'),
                            'neg_recall': values.get('syntactic').get('neg_recall'),
                            'solve': values.get('problem_solving').get('solving_ratio'),
                        }
                        for domain, values in json.load(f).items()
                    },
                    orient='index'
                ).reset_index().rename(columns={'index': 'domain'})

            for d in alg_df.domain:
                d_df = alg_df[alg_df['domain'] == d]

                # if d_df['predeff_prec'].values[0] == 1. and float(d_df['pos_prec'].values[0]) < 1. and float(d_df['neg_prec'].values[0]) < 1.:
                #     print(f"{d}")
                #     print(f"Predicted effects precision is {d_df['predeff_prec'].values[0]},"
                #           f"positive effects precision is {d_df['pos_prec'].values[0]}"
                #           f"negative effects precision is {d_df['neg_prec'].values[0]}")

                # if d_df['app_prec'].values[0] == 1. and float(d_df['precs_recall'].values[0]) < 1.:
                #     print(f"{d}")
                #     print(f"Applicability precision is {d_df['predeff_prec'].values[0]}, "
                #           f"positive preconditions recall is {d_df['precs_recall'].values[0]}")

                # if d_df['predeff_recall'].values[0] == 1. and float(d_df['pos_recall'].values[0]) < 1. and float(d_df['neg_recall'].values[0]) < 1.:
                #     print(f"{d}")
                #     print(f"Predicted effects recall is {d_df['predeff_recall'].values[0]},"
                #           f"positive effects recall is {d_df['pos_recall'].values[0]}"
                #           f"negative effects recall is {d_df['neg_recall'].values[0]}")

                # if d_df['solve'].values[0] == 1. and float(d_df['syn_prec'].values[0]) < 1. and float(d_df['syn_recall'].values[0]) < 1.:
                #     print(f"{d}")
                #     print(f"Solving ratio is {d_df['solve'].values[0]},"
                #           f"syntactic precision is {d_df['syn_prec'].values[0]}"
                #           f"syntactic recall is {d_df['syn_recall'].values[0]}")

                # if d_df['solve'].values[0] == 0. and float(d_df['syn_prec'].values[0]) > .8 and float(d_df['syn_recall'].values[0]) > .8:
                #     print(f"{d}")
                #     print(f"Solving ratio is {d_df['solve'].values[0]},"
                #           f"syntactic precision is {d_df['syn_prec'].values[0]}"
                #           f"syntactic recall is {d_df['syn_recall'].values[0]}")

                # if d_df['predeff_recall'].values[0] < 1. and (float(d_df['pos_recall'].values[0]) < 1. or float(d_df['neg_recall'].values[0]) < 1.):
                #     print(f"[{d}]\nPredicted effects recall is {d_df['predeff_recall'].values[0]},"
                #           f" positive effects recall is {d_df['pos_recall'].values[0]}"
                #           f" negative effects recall is {d_df['neg_recall'].values[0]}")

                # if d_df['predeff_prec'].values[0] < 1. and (float(d_df['pos_prec'].values[0]) < 1. or float(d_df['neg_prec'].values[0]) < 1.):
                #     print(f"[{d}]\nPredicted effects precision is {d_df['predeff_prec'].values[0]},"
                #           f" positive effects recall is {d_df['pos_prec'].values[0]}"
                #           f" negative effects recall is {d_df['neg_prec'].values[0]}")