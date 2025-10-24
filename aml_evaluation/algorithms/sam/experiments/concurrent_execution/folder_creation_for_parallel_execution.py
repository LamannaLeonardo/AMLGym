import argparse
import logging
import shutil
from pathlib import Path
from typing import List

from trajectory_creators.random_walk_trajectories_creator import RandomWalkTrajectoriesCreator
from utilities import DistributedKFoldSplit

DEFAULT_EXPERIMENT_SIZE = 100


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Creates the folds directories for the slurm tasks to work on.")
    parser.add_argument("--working_directory_path", required=True, help="The path to the directory where the domain is")
    parser.add_argument("--domain_file_name", required=True, help="the domain file name including the extension")
    parser.add_argument(
        "--problem_prefix", required=True, help="the prefix of the name of the problems to be able to generate trajectories from them."
    )
    parser.add_argument("--learning_algorithms", required=True, help="the list of algorithms that will run in parallel")
    parser.add_argument("--internal_iterations", required=True, help="The internal iterations that the algorithm will run in parallel.")
    parser.add_argument(
        "--experiment_size", required=False, help="The max items to use in each fold of the experiment.", default=DEFAULT_EXPERIMENT_SIZE, type=int
    )
    parser.add_argument(
        "--no_random_trajectories",
        action="store_false",
        dest="should_create_random_trajectories",
        help="If specified, no random trajectories would be created.",
    )
    parsed_args = parser.parse_args()
    return parsed_args


class FoldsCreator:
    k_fold: DistributedKFoldSplit
    logger: logging.Logger

    def __init__(
        self, working_directory_path: Path, domain_file_name: str, learning_algorithms: List[int] = None, internal_iterations: List[int] = None
    ):
        self.k_fold = DistributedKFoldSplit(
            working_directory_path=working_directory_path,
            domain_file_name=domain_file_name,
            n_split=5,
            learning_algorithms=learning_algorithms,
            internal_iterations=internal_iterations,
        )
        self.domain_file_name = domain_file_name
        self.working_directory_path = working_directory_path
        self.logger = logging.getLogger("cluster-folder-creator")

    def create_folds_from_cross_validation(self, experiment_size: int = DEFAULT_EXPERIMENT_SIZE) -> None:
        """Runs that cross validation process on the domain's working directory and validates the results."""
        (self.working_directory_path / "results_directory").mkdir(exist_ok=True)
        self.logger.info("Removing the old folds directories if exist.")
        self.k_fold.remove_created_directories()
        self.logger.info("Done removing the old folds directories!")
        self.logger.info("Creating a logs directory.")
        (self.working_directory_path / "logs").mkdir(exist_ok=True)
        self.logger.info("Creating the folds directories.")
        self.k_fold.create_k_fold(max_items=experiment_size)
        self.logger.info("Done creating the folds directories!")

    def create_random_performance_evaluation_trajectories(
        self, problem_prefix: str, learning_algorithm: int, should_include_random_trajectories: bool = True
    ) -> None:
        """Creates the random performance evaluation trajectories.

        :param problem_prefix: the prefix of the name of the problems to be able to generate trajectories from them.
        :param learning_algorithm: the learning algorithm that will be used to create the trajectories (index).
        :param should_include_random_trajectories: whether to include the random trajectories or not.
        """
        self.logger.info("Creating the random performance evaluation trajectories.")
        performance_evaluation_dir = self.working_directory_path / "performance_evaluation_trajectories"
        performance_evaluation_dir.mkdir(exist_ok=True)

        for fold in range(self.k_fold.n_split):
            output_directory_path = performance_evaluation_dir / f"fold_{fold}"
            output_directory_path.mkdir(exist_ok=True)
            # this is the directory containing the test samples that will be used to create the random trajectories
            test_set_directory = self.k_fold.test_set_dir_path / f"fold_{fold}_{learning_algorithm}_1"
            shutil.copy(self.working_directory_path / self.domain_file_name, test_set_directory)
            if should_include_random_trajectories:
                random_trajectories_creator = RandomWalkTrajectoriesCreator(
                    domain_file_name=self.domain_file_name, working_directory_path=test_set_directory
                )
                random_trajectories_creator.create_domain_trajectories(problems_prefix=problem_prefix, output_directory_path=output_directory_path)

            # copy the test set problems, solution and trajectories to use in case none of the random trajectories are valid
            for test_set_problem in test_set_directory.glob(f"{problem_prefix}*.pddl"):
                shutil.copy(test_set_problem, output_directory_path)
                shutil.copy(self.working_directory_path / f"{test_set_problem.stem}.solution", output_directory_path)
                shutil.copy(self.working_directory_path / f"{test_set_problem.stem}.trajectory", output_directory_path)

            (test_set_directory / self.domain_file_name).unlink()

        self.logger.info("Done creating the random performance evaluation trajectories!")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    args = parse_arguments()
    experiment_learning_algorithms = args.learning_algorithms.split(",")
    internal_iterations = [int(val) for val in args.internal_iterations.split(",")]
    if len(internal_iterations) > 0:
        print(f"Internal iterations: {internal_iterations}")

    folds_creator = FoldsCreator(
        working_directory_path=Path(args.working_directory_path),
        domain_file_name=args.domain_file_name,
        learning_algorithms=experiment_learning_algorithms,
        internal_iterations=internal_iterations,
    )
    folds_creator.create_folds_from_cross_validation(experiment_size=args.experiment_size)
    folds_creator.create_random_performance_evaluation_trajectories(
        problem_prefix=args.problem_prefix,
        learning_algorithm=int(experiment_learning_algorithms[0]),
        should_include_random_trajectories=args.should_create_random_trajectories,
    )
