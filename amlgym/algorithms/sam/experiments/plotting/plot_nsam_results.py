import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_results(results_directory_path: Path, file_template: str = "*solving_combined_statistics.csv", using_triplets: bool = False) -> None:
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
        df = df[df["learning_algorithm"] != "incremental_nsam"]  # Remove max_percent_ok from the plot
        group_by_columns = ["num_trajectories", "learning_algorithm"] if not using_triplets else ["num_trajectory_triplets", "learning_algorithm"]
        grouped_data = df.groupby(group_by_columns, as_index=False).agg(avg_percent_ok=("percent_ok", "mean"), std_percent_ok=("percent_ok", "std"),)
        labels = {
            "numeric_sam": "NSAM*",
            "naive_nsam": "NSAM",
            "plan_miner": "Plan Miner",
        }

        # Plotting
        sns.set(style="whitegrid")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

        legend_order = [0, 2, 1]

        x_lim = max(grouped_data["num_trajectories"]) * 1.25 if not using_triplets else max(grouped_data["num_trajectory_triplets"]) * 1.25
        # Plot a line for each learning algorithm
        for index, algo in enumerate(df["learning_algorithm"].unique()):
            algo_data = grouped_data[grouped_data["learning_algorithm"] == algo]
            plot_x_axis = algo_data["num_trajectories"] if not using_triplets else algo_data["num_trajectory_triplets"]

            ax1.plot(
                plot_x_axis,
                algo_data["avg_percent_ok"],
                linestyle=line_styles_iterator[index],
                label=labels[algo],
                marker=markers[index],
                color=color_cycle[index],
                linewidth=3,
            )

            # Plot standard deviation as shaded area around the mean line
            ax1.fill_between(
                plot_x_axis,
                np.clip(algo_data["avg_percent_ok"] - algo_data["std_percent_ok"], 0, 100),
                np.clip(algo_data["avg_percent_ok"] + algo_data["std_percent_ok"], 0, 100),
                alpha=0.2,
            )

            ax2.plot(
                plot_x_axis,
                algo_data["avg_percent_ok"],
                linestyle=line_styles_iterator[index],
                label=labels[algo],
                marker=markers[index],
                color=color_cycle[index],
                linewidth=3,
            )

            # Plot standard deviation as shaded area around the mean line
            ax2.fill_between(
                plot_x_axis,
                np.clip(algo_data["avg_percent_ok"] - algo_data["std_percent_ok"], 0, 100),
                np.clip(algo_data["avg_percent_ok"] + algo_data["std_percent_ok"], 0, 100),
                alpha=0.2,
            )

            # Set plot labels and title
            x_axis_label = "# Triplets" if using_triplets else "# Trajectories"
            ax1.set_xlabel(x_axis_label, fontsize=28)
            ax1.set_ylabel("AVG % of solved", fontsize=28)
            ax1.set_ylim(0, 100)
            ax1.tick_params(axis="both", which="major", labelsize=24)

            ax2.set_xlabel(f"{x_axis_label} (0-{int(x_lim * 0.1)})", fontsize=28)
            ax2.set_xlim(1, x_lim * 0.1)
            ax2.set_ylim(0, 100)
            ax2.tick_params(axis="both", which="major", labelsize=24)

        ax1.grid(True)
        ax2.grid(True)

        # Add a legend
        handles1, legend_labels1 = plt.gca().get_legend_handles_labels()
        ax1.legend([handles1[idx] for idx in legend_order], [legend_labels1[idx] for idx in legend_order], fontsize=28)

        handles2, legend_labels2 = plt.gca().get_legend_handles_labels()
        ax2.legend([handles2[idx] for idx in legend_order], [legend_labels2[idx] for idx in legend_order], fontsize=28)

        # Add a vertical dashed line at x = 5, with color changed to black
        ax1.axvline(x=x_lim * 0.1, color="black", linestyle="--", linewidth=4)
        # Add an annotation to show the zoom effect
        ax1.annotate(
            "Zoom up to\n here", xy=(x_lim * 0.1, 20), xytext=(x_lim * 0.15, 15), arrowprops=dict(facecolor="black", shrink=0.05), fontsize=18
        )

        output_file_path = file_path.parent / f"{file_path.stem}_plot.png"
        plt.savefig(output_file_path, bbox_inches="tight")


if __name__ == "__main__":
    results_path = Path(sys.argv[1])
    plot_results(results_path)
