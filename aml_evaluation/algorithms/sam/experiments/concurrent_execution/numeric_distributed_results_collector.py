import argparse
import logging
from pathlib import Path
from typing import List

from pddl_plus_parser.lisp_parsers import DomainParser

from experiments.concurrent_execution.distributed_results_collector import DistributedResultsCollector
from experiments.plotting.plot_nsam_results import plot_results
from experiments.plotting.plot_nsam_solo_results import plot_solo_results


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Creates the folds directories for the slurm tasks to work on.")
    parser.add_argument("--working_directory_path", required=True, help="The path to the directory where the domain is")
    parser.add_argument("--domain_file_name", required=True, help="the domain file name including the extension")
    parser.add_argument("--learning_algorithms", required=True, help="the list of algorithms that will run in parallel")
    parser.add_argument("--num_folds", required=True, help="the number of folds to that were created", type=int, default=5)
    parser.add_argument("--internal_iterations", required=True, help="The internal iterations that the algorithm will run in parallel.")
    args = parser.parse_args()
    return args


class NumericResultsCollector(DistributedResultsCollector):
    logger: logging.Logger

    def __init__(
        self,
        working_directory_path: Path,
        domain_file_name: str,
        learning_algorithms: List[str] = None,
        num_folds: int = 5,
        iterations: List[int] = None,
    ):
        super().__init__(working_directory_path, domain_file_name, learning_algorithms, num_folds, iterations)

    def collect_numeric_statistics(self) -> None:
        """Collects the statistics from the results directory."""
        self._collect_solving_statistics(collecting_triplets=False)
        results_directory = self.working_directory_path / "results_directory"
        plot_results(results_directory, file_template="*solving_combined_statistics.csv")
        plot_solo_results(results_directory, file_template="*solving_combined_statistics.csv")
        domain = DomainParser(self.working_directory_path / self.domain_file_name).parse_domain()
        self._collect_syntactic_performance_statistics(domain)
        self._collect_numeric_semantic_performance_statistics(collecting_triplets=False)

    def collect_numeric_statistics_with_triplets_statistics(self) -> None:
        self._collect_solving_statistics(collecting_triplets=True)
        results_directory = self.working_directory_path / "results_directory"
        plot_results(results_directory, file_template="*solving_combined_statistics_with_triplets.csv", using_triplets=True)
        plot_solo_results(results_directory, file_template="*solving_combined_statistics_with_triplets.csv", using_triplets=True)
        domain = DomainParser(self.working_directory_path / self.domain_file_name).parse_domain()
        self._collect_syntactic_performance_statistics(domain)
        self._collect_numeric_semantic_performance_statistics(collecting_triplets=True)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    args = parse_arguments()
    experiment_learning_algorithms = args.learning_algorithms.split(",")
    internal_iterations = [int(val) for val in args.internal_iterations.split(",")]
    NumericResultsCollector(
        working_directory_path=Path(args.working_directory_path),
        domain_file_name=args.domain_file_name,
        learning_algorithms=experiment_learning_algorithms,
        num_folds=args.num_folds,
        iterations=internal_iterations,
    ).collect_numeric_statistics()
