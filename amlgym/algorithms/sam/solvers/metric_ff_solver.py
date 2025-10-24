import logging
import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Dict

from pddl_plus_parser.exporters import MetricFFParser

METRIC_FF_DIRECTORY = os.environ["METRIC_FF_DIRECTORY"]

MAX_RUNNING_TIME = 5  # seconds


class MetricFFSolver:
    """Class designated to use to activate the metric-FF solver on the cluster and parse its result."""

    logger: logging.Logger

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.parser = MetricFFParser()

    @staticmethod
    def _extract_solver_error(solution_path: Path) -> str:
        """Extracts the error from the solution file.

        :param solution_path: the path to the solution file.
        :return: the error message.
        """
        with open(solution_path, "rb") as solution_file:
            solution_content = solution_file.read()
            return solution_content.decode("utf-8", errors="ignore")

    def _run_metric_ff_process(
        self, run_command: str, solution_path: Path, problem_file_path: Path, solving_stats: Dict[str, str], solving_timeout: int = MAX_RUNNING_TIME,
    ) -> None:
        """Runs the metric-ff process."""
        self.logger.info(f"Metric-FF solver is working on - {problem_file_path.stem}")
        process = subprocess.Popen(run_command, shell=True)
        try:
            process.wait(timeout=solving_timeout)
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Metric-FF solver took more than {solving_timeout} seconds to finish.")
            os.kill(process.pid, signal.SIGTERM)
            os.system("pkill -f ./ff")
            solution_path.unlink(missing_ok=True)
            solving_stats[problem_file_path.stem] = "timeout"
            return

        if process.returncode is None:
            solving_stats[problem_file_path.stem] = "timeout"
            solution_path.unlink(missing_ok=True)
            return

        if process.returncode != 0:
            self.logger.warning(f"Metric FF Solver returned status code {process.returncode}.")
            if not solution_path.exists():
                solving_stats[problem_file_path.stem] = "solver_error"
                return

            solving_status = self.parser.get_solving_status(solution_path)[0]
            if solving_status != "ok" and solving_status != "no-solution":
                solving_stats[problem_file_path.stem] = "solver_error"
                error = self._extract_solver_error(solution_path)
                self.logger.warning(f"Metric FF Solver encountered an error - {problem_file_path.stem}")
                self.logger.warning(error)
                solution_path.unlink(missing_ok=True)
                return

        self.logger.info("Metric FF Solver finished its execution!")
        solving_status = self.parser.get_solving_status(solution_path)[0]
        if solving_status == "ok":
            self.logger.info(f"Solver succeeded in solving problem - {problem_file_path.stem}")
            solving_stats[problem_file_path.stem] = solving_status
            self.parser.parse_plan(solution_path, solution_path)

        elif solving_status == "no-solution":
            self.logger.warning(f"Metric FF Solver could not solve problem - {problem_file_path.stem}")
            solving_stats[problem_file_path.stem] = "no_solution"
            solution_path.unlink(missing_ok=True)

    def solve_problem(
        self,
        domain_file_path: Path,
        problem_file_path: Path,
        problems_directory_path: Path,
        solving_stats: Dict[str, str],
        solving_timeout: int,
        tolerance: float,
    ) -> None:
        """Solves a single problem using the Metric FF algorithm.

        :param domain_file_path: the path to the domain file.
        :param problem_file_path: the path to the problem file.
        :param problems_directory_path: the path to the problems' directory.
        :param solving_stats: the statistics of the solving process.
        :param solving_timeout: the timeout for the solver.
        :param tolerance: the numeric tolerance to use.
        """
        os.chdir(METRIC_FF_DIRECTORY)
        self.logger.debug(f"Starting to work on solving problem - {problem_file_path.stem}")
        solution_path = problems_directory_path / f"{problem_file_path.stem}.solution"
        run_command = f"./ff -o {domain_file_path} -f {problem_file_path} -s 0 -t {tolerance} > {solution_path}"
        self._run_metric_ff_process(run_command, solution_path, problem_file_path, solving_stats, solving_timeout)

    def execute_solver(
        self,
        problems_directory_path: Path,
        domain_file_path: Path,
        solving_timeout: int = MAX_RUNNING_TIME,
        problems_prefix: str = "pfile",
        tolerance: float = 0.1,
    ) -> Dict[str, str]:
        """Solves numeric and PDDL+ problems using the Metric-FF algorithm and outputs the solution into a file.

        :param problems_directory_path: the path to the problems directory.
        :param domain_file_path: the path to the domain file.
        :param solving_timeout: the timeout for the solver.
        :param problems_prefix: the prefix of the problems files.
        :param tolerance: the numeric tolerance for errors in the Metric-FF solver.
        """
        solving_stats = {}
        self.logger.info("Starting to solve the input problems using Metic-FF solver.")
        for problem_file_path in problems_directory_path.glob(f"{problems_prefix}*.pddl"):
            self.solve_problem(domain_file_path, problem_file_path, problems_directory_path, solving_stats, solving_timeout, tolerance)

        return solving_stats


if __name__ == "__main__":
    args = sys.argv
    logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    solver = MetricFFSolver()
    solver.execute_solver(
        problems_directory_path=Path(args[1]), domain_file_path=Path(args[2]), problems_prefix=args[3], solving_timeout=int(args[4])
    )
