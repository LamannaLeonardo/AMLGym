"""Module to create the dataset for the experiments."""
import argparse
import logging
from pathlib import Path
from typing import Literal, Union

from solvers import MetricFFSolver, ENHSPSolver
from trajectory_creators import ExperimentTrajectoriesCreator
from trajectory_creators.random_walk_trajectories_creator import RandomWalkTrajectoriesCreator
from utilities import SolverType

MAX_RUNNING_TIME = 600  # seconds

SOLVER_TYPES = {
    SolverType.metric_ff: MetricFFSolver,
    SolverType.enhsp: ENHSPSolver,
}

TRAJECTORY_CREATOR_TYPES = {
    "regular": ExperimentTrajectoriesCreator,
    "random": RandomWalkTrajectoriesCreator,
}


class DatasetGenerator:
    """Creates the dataset for the experiments.

    Notice: The class assumes that the problems for the experiments are already created (using some sort of generator).
    """

    problems_directory_path: Path
    domain_file_path: Path
    solving_timeout: int
    problems_prefix: str
    solver_type: SolverType
    trajectory_generator: Union[ExperimentTrajectoriesCreator, RandomWalkTrajectoriesCreator]

    def __init__(
        self,
        problems_directory_path: Path,
        domain_file_path: Path,
        solving_timeout: int = MAX_RUNNING_TIME,
        problems_prefix: str = "pfile",
        solver_type: SolverType = SolverType.fast_downward,
        trajectory_creation_method: Literal["regular", "random"] = "regular",
    ):
        """Initializes the dataset generator with the given problems."""
        self.problems_directory_path = problems_directory_path
        self.domain_file_path = domain_file_path
        self.solving_timeout = solving_timeout
        self.problems_prefix = problems_prefix
        self.solver_type = SolverType(solver_type)
        self.trajectory_generator = TRAJECTORY_CREATOR_TYPES[trajectory_creation_method](
            domain_file_name=domain_file_path.name, working_directory_path=problems_directory_path
        )
        self.logger = logging.getLogger("experiments_dataset_generator")

    def generate_dataset(self):
        """Generates the dataset for the experiments."""
        self.logger.info(f"Generating the experimental dataset for the domain {self.domain_file_path.stem}...")
        self.logger.info(f"Using the solver {self.solver_type.name}...")
        solver = SOLVER_TYPES[self.solver_type]()
        solver.execute_solver(
            problems_directory_path=self.problems_directory_path,
            domain_file_path=self.domain_file_path,
            solving_timeout=self.solving_timeout,
            problems_prefix=self.problems_prefix,
        )
        self.logger.info("Finished executing the solver on the problems' dataset.")
        self.logger.info("Starting to generate the trajectories...")
        self.trajectory_generator.create_domain_trajectories()
        self.logger.info("Finished generating the trajectories.")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Runs the code responsible to create the trajectory dataset for the experiments.")
    parser.add_argument("--problems_directory_path", required=True, help="The path to the directory where the domain and problems are located.")
    parser.add_argument("--domain_file_path", required=True, help="the path to the domain file.")
    parser.add_argument(
        "--solving_timeout", required=False, type=int, help="The timeout to use when running the solver algorithm.", default=60,
    )
    parser.add_argument(
        "--solver_type",
        required=False,
        type=int,
        choices=[2, 3],
        help="The solver that should be used for the sake of validation.\nMetric-FF - 2, ENHSP - 3.",
        default=3,
    )
    parser.add_argument("--problems_prefix", required=False, help="The prefix of the problems' file names", type=str, default="pfile")
    parser.add_argument(
        "--trajectory_creation_method",
        required=False,
        help="The type of trajectories to create for the experiments",
        type=str,
        choices=["regular", "random"],
        default="regular",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    args = parse_arguments()
    dataset_generator = DatasetGenerator(
        problems_directory_path=Path(args.problems_directory_path),
        domain_file_path=Path(args.domain_file_path),
        solving_timeout=args.solving_timeout,
        problems_prefix=args.problems_prefix,
        solver_type=args.solver_type,
        trajectory_creation_method=args.trajectory_creation_method,
    )
    dataset_generator.generate_dataset()
