import argparse
import csv
import logging
from pathlib import Path
from typing import List, Optional

from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import Domain

from experiments.plotting.plot_nsam_results import plot_results
from experiments.plotting.plot_nsam_solo_results import plot_solo_results
from statistics.learning_statistics_manager import LEARNED_ACTIONS_STATS_COLUMNS
from statistics.numeric_performance_calculator import NUMERIC_PERFORMANCE_STATS
from statistics.semantic_performance_calculator import SEMANTIC_PRECISION_STATS
from utilities import LearningAlgorithmType
from validators.safe_domain_validator import SOLVING_STATISTICS

FOLD_FIELD = "fold"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Creates the folds directories for the slurm tasks to work on.")
    parser.add_argument("--working_directory_path", required=True, help="The path to the directory where the domain is")
    parser.add_argument("--domain_file_name", required=True, help="the domain file name including the extension")
    parser.add_argument("--learning_algorithms", required=True, help="the list of algorithms that will run in parallel")
    parser.add_argument("--num_folds", required=True, help="the number of folds to that were created", type=int, default=5)
    parser.add_argument("--internal_iterations", required=True, help="The internal iterations that the algorithm will run in parallel.")
    args = parser.parse_args()
    return args


class DistributedResultsCollector:
    logger: logging.Logger

    def __init__(
        self,
        working_directory_path: Path,
        domain_file_name: str,
        learning_algorithms: List[str] = None,
        num_folds: int = 5,
        iterations: List[int] = None,
    ):
        self.domain_file_name = domain_file_name
        self.working_directory_path = working_directory_path
        self.learning_algorithms = [LearningAlgorithmType(int(e)) for e in learning_algorithms]
        self.num_folds = num_folds
        self.iterations = iterations
        self.logger = logging.getLogger("ClusterRunner")

    def _combine_statistics_data(
        self,
        file_path_template: str,
        combined_statistics_data: List[dict],
        exclude_algorithm: Optional[LearningAlgorithmType] = None,
        using_triplets: bool = False,
    ) -> None:
        """Combines the statistics data from the statistics files in the results directory to a single file.

        :param file_path_template: the template of the file path to use to find the statistics files.
        :param combined_statistics_data: the list to append the combined statistics data to.
        :param exclude_algorithm: the algorithm to exclude and not include in the combined statistics.
        :param using_triplets: whether to use triplets or not.
        """
        results_directory = self.working_directory_path / "results_directory"
        algorithms_to_iterate = (
            self.learning_algorithms
            if exclude_algorithm is None
            else [algorithm for algorithm in self.learning_algorithms if algorithm != exclude_algorithm]
        )
        for fold in range(self.num_folds):
            for iteration in self.iterations:
                for learning_algorithm in algorithms_to_iterate:
                    solving_statistics_file_path = (
                        results_directory / file_path_template.format(fold=fold, iteration=iteration, learning_algorithm=learning_algorithm.name)
                        if not using_triplets
                        else results_directory / file_path_template.format(fold=fold, learning_algorithm=learning_algorithm.name)
                    )
                    with open(solving_statistics_file_path, "rt") as statistics_file:
                        reader = csv.DictReader(statistics_file)
                        combined_statistics_data.extend([{FOLD_FIELD: fold, **row} for row in reader])

    def _collect_solving_statistics(self, collecting_triplets: bool = False) -> None:
        """Collects the statistics from the statistics files in the results directory based on the given parameters.

        :param collecting_triplets: whether to collect the statistics based on triplets or not.
        """
        self.logger.info("Collecting the solving statistics from the results directory.")
        results_directory = self.working_directory_path / "results_directory"
        combined_statistics_file_path = (
            results_directory / "solving_combined_statistics.csv"
            if not collecting_triplets
            else results_directory / "solving_combined_statistics_with_triplets.csv"
        )
        combined_statistics_data = []
        file_path_template = (
            "{learning_algorithm}_problem_solving_stats_fold_{fold}_{iteration}_trajectories.csv"
            if not collecting_triplets
            else "{learning_algorithm}_problem_solving_stats_fold_{fold}.csv"
        )
        self._combine_statistics_data(file_path_template, combined_statistics_data, using_triplets=collecting_triplets)

        with open(combined_statistics_file_path, "wt") as combined_statistics_file:
            writer = csv.DictWriter(combined_statistics_file, fieldnames=[FOLD_FIELD, *SOLVING_STATISTICS])
            writer.writeheader()
            writer.writerows(combined_statistics_data)

    def _collect_numeric_semantic_performance_statistics(self, collecting_triplets: bool = False) -> None:
        self.logger.info("Collecting the numeric performance statistics from the results directory.")
        domain = DomainParser(self.working_directory_path / self.domain_file_name).parse_domain()
        combined_statistics_file_path = (
            self.working_directory_path / "results_directory" / "numeric_performance_combined_statistics.csv"
            if not collecting_triplets
            else self.working_directory_path / "results_directory" / "numeric_performance_combined_statistics_with_triplets.csv"
        )
        file_path_template = (
            "{learning_algorithm}_" + domain.name + "_numeric_learning_performance_stats_fold_{fold}_{iteration}.csv"
            if not collecting_triplets
            else "{learning_algorithm}_" + domain.name + "_numeric_learning_performance_stats_fold_{fold}.csv"
        )
        combined_statistics_data = []
        self._combine_statistics_data(file_path_template, combined_statistics_data, using_triplets=collecting_triplets)
        with open(combined_statistics_file_path, "wt") as combined_statistics_file:
            writer = csv.DictWriter(combined_statistics_file, fieldnames=[FOLD_FIELD, *NUMERIC_PERFORMANCE_STATS])
            writer.writeheader()
            writer.writerows(combined_statistics_data)
        self.logger.info("Done collecting the statistics from the results directory!")

    def _collect_semantic_performance_statistics(
        self, domain: Domain, exclude_algorithm: Optional[LearningAlgorithmType] = None, using_triplets: bool = False
    ) -> None:
        """Collects the semantic performance statistics from the results directory.

        :param domain: the domain to collect the statistics for.
        """
        self.logger.info("Collecting the semantic performance statistics from the results directory.")
        combined_semantic_performance_file_path = (
            self.working_directory_path / "results_directory" / "semantic_performance_combined_statistics.csv"
            if not using_triplets
            else self.working_directory_path / "results_directory" / "semantic_performance_combined_statistics_with_triplets.csv"
        )
        combined_semantic_performance_statistics_data = []
        file_path_template = (
            "{learning_algorithm}_" + domain.name + "_{fold}_{iteration}_semantic_performance.csv"
            if not using_triplets
            else "{learning_algorithm}_" + domain.name + "_{fold}_semantic_performance.csv"
        )
        self._combine_statistics_data(file_path_template, combined_semantic_performance_statistics_data, exclude_algorithm=exclude_algorithm)
        with open(combined_semantic_performance_file_path, "wt") as combined_statistics_file:
            writer = csv.DictWriter(combined_statistics_file, fieldnames=[FOLD_FIELD, *SEMANTIC_PRECISION_STATS])
            writer.writeheader()
            writer.writerows(combined_semantic_performance_statistics_data)

    def _collect_syntactic_performance_statistics(
        self, domain: Domain, exclude_algorithm: Optional[LearningAlgorithmType] = None, using_triplets: bool = False
    ) -> None:
        """Collects the syntactic performance statistics from the results directory.

        :param domain: the domain to collect the statistics for.
        """
        self.logger.info("Collecting the syntactic performance statistics from the results directory.")
        combined_syntactic_performance_file_path = (
            self.working_directory_path / "results_directory" / "syntactic_performance_combined_statistics.csv"
            if not using_triplets
            else self.working_directory_path / "results_directory" / "syntactic_performance_combined_statistics_with_triplets.csv"
        )
        combined_action_performance_statistics_data = []
        action_performance_path_template = (
            "{learning_algorithm}_" + domain.name + "_action_stats_fold_{fold}_{iteration}.csv"
            if not using_triplets
            else "{learning_algorithm}_" + domain.name + "_action_stats_fold_{fold}.csv"
        )
        self._combine_statistics_data(
            action_performance_path_template, combined_action_performance_statistics_data, exclude_algorithm=exclude_algorithm
        )
        with open(combined_syntactic_performance_file_path, "wt") as combined_statistics_file:
            writer = csv.DictWriter(combined_statistics_file, fieldnames=[FOLD_FIELD, *LEARNED_ACTIONS_STATS_COLUMNS])
            writer.writeheader()
            writer.writerows(combined_action_performance_statistics_data)
