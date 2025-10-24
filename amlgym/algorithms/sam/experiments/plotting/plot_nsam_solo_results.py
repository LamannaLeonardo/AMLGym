import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_solo_results(results_directory_path: Path, file_template: str = "*solving_combined_statistics.csv", using_triplets: bool = False):
    """Plot the results of the experiments."""
    for file_path in results_directory_path.glob(file_template):
        df = pd.read_csv(file_path)

        # Define color-blind friendly palette
        color_palette = sns.color_palette("colorblind", n_colors=len(df["learning_algorithm"].unique()))
        line_styles = ["-", "--", "-.", ":", "--", "-.", ":"]
        marker_options = ["o", "s", "D", "v", "^", ">", "<", "p", "P", "*", "X", "d"]
        line_styles_iterator = list(line_styles)
        color_cycle = list(color_palette)
        markers = list(marker_options)

        # Group the data by 'num_trajectories', 'learning_algorithm' and calculate the mean and std of 'percent_ok'
        df = df[~df["learning_algorithm"].isin(["incremental_nsam", "naive_nsam_no_dependency_removal"])]  # Remove max_percent_ok from the plot
        group_by_columns = ["num_trajectories", "learning_algorithm"] if not using_triplets else ["num_trajectory_triplets", "learning_algorithm"]
        grouped_data = df.groupby(group_by_columns, as_index=False).agg(avg_percent_ok=("percent_ok", "mean"), std_percent_ok=("percent_ok", "std"),)
        labels = {
            "numeric_sam": "NSAM*",
            "naive_nsam": "NSAM",
            "plan_miner": "Plan Miner",
        }

        # Plotting
        sns.set(style="whitegrid")
        stand_alone_fig = plt.figure(figsize=(12, 8))

        # Plot a line for each learning algorithm
        for index, algo in enumerate(df["learning_algorithm"].unique()):
            algo_data = grouped_data[grouped_data["learning_algorithm"] == algo]
            plot_x_axis = algo_data["num_trajectories"] if not using_triplets else algo_data["num_trajectory_triplets"]

            plt.plot(
                plot_x_axis,
                algo_data["avg_percent_ok"],
                linestyle=line_styles_iterator[index],
                label=labels[algo],
                marker=markers[index],
                color=color_cycle[index],
                linewidth=8,
            )

            plt.fill_between(
                plot_x_axis,
                np.clip(algo_data["avg_percent_ok"] - algo_data["std_percent_ok"], 0, 100),
                np.clip(algo_data["avg_percent_ok"] + algo_data["std_percent_ok"], 0, 100),
                alpha=0.2,
            )

        plt.xlabel(f"# {'Trajectories' if not using_triplets else 'Triplets'}", fontsize=44)
        plt.ylabel("AVG % of solved", fontsize=44)
        plt.ylim(0, 100)
        plt.tick_params(axis="both", which="major", labelsize=46)
        plt.grid(True)
        plt.legend(fontsize=44)

        output_file_path = file_path.parent / f"{file_path.stem}_plot_solo.pdf"
        plt.tight_layout()  # Ensures no overlap between plot elements
        plt.savefig(output_file_path, bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    results_path = Path(sys.argv[1])
    plot_solo_results(results_path)
