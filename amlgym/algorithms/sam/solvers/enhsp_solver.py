"""Module responsible for running the Expressive Numeric Heuristic Planner (ENHSP)."""
import logging
import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Dict

from jdk4py import JAVA

ENHSP_FILE_PATH = os.environ["ENHSP_FILE_PATH"]
MAX_RUNNING_TIME = 5  # seconds

TIMEOUT_ERROR_CODE = b"Timeout has been reached"
PROBLEM_SOLVED = b"Problem Solved"
NO_SOLUTION_FOR_PROBLEM = b"Problem Detected as Unsolvable"
OTHER_NO_SOLUTION_TYPE = b"Problem unsolvable"
GOAL_NOT_REACHABLE = b"Goal is not reachable"
ERROR_TYPE_NO_SOLUTION = b'"this.plan" is null'


class ENHSPSolver:
    """Class designated to use to activate the metric-FF solver on the cluster and parse its result."""

    logger: logging.Logger

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _run_enhsp_process(
        self, run_command: str, problem_file_path: Path, solving_stats: Dict[str, str], solving_timeout: int = MAX_RUNNING_TIME
    ) -> bool:
        """Runs the ENHSP process and monitors its execution time.

        :param run_command: the command to run the ENHSP process.
        :param problem_file_path: the path to the problem file.
        :param solving_stats: the statistics of the solving process.
        :return: whether the process finished successfully.
        """
        self.logger.info(f"Starting to run ENHSP process for the problem - {problem_file_path.stem}")
        process = subprocess.Popen(run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            process.wait(timeout=solving_timeout)

        except subprocess.TimeoutExpired:
            self.logger.warning(f"ENHSP did not finish after {solving_timeout} secs while trying to solve - {problem_file_path.stem}")
            solving_stats[problem_file_path.stem] = "timeout"
            os.kill(process.pid, signal.SIGTERM)
            os.system(f"pkill -f {ENHSP_FILE_PATH}")
            return True

        if process.returncode is None:
            solving_stats[problem_file_path.stem] = "timeout"
            self.logger.warning(f"ENHSP did not finish in time so was killed while trying to solve - {problem_file_path.stem}")
            return True

        self.logger.info("ENHSP finished its execution!")
        stdout = process.stdout.read()
        stderr = process.stderr.read()

        if PROBLEM_SOLVED in stdout:
            self.logger.info(f"Solver succeeded in solving problem - {problem_file_path.stem}")
            solving_stats[problem_file_path.stem] = "ok"
            return True

        elif NO_SOLUTION_FOR_PROBLEM in stdout or OTHER_NO_SOLUTION_TYPE in stdout or ERROR_TYPE_NO_SOLUTION in stderr:
            self.logger.warning(f"Solver could not solve problem - {problem_file_path.stem}")
            solving_stats[problem_file_path.stem] = "no_solution"
            return True

        elif GOAL_NOT_REACHABLE in stderr:
            self.logger.warning("Solver declared goal unreachable!")
            solving_stats[problem_file_path.stem] = "no_solution"
            return True

        else:
            self.logger.critical(f"While solving problem {problem_file_path.stem} encountered unknown error! " f"STDOUT - {stdout}")
            self.logger.critical(f"While solving problem {problem_file_path.stem} encountered unknown error! " f"STDERR - {stderr}")
            solving_stats[problem_file_path.stem] = "solver_error"
            return False

    def solve_problem(
        self,
        domain_file_path: Path,
        problem_file_path: Path,
        problems_directory_path: Path,
        solving_stats: Dict[str, str],
        solving_timeout: int,
        tolerance: float,
    ) -> None:
        """Solves a single problem using the ENHSP algorithm.

        :param domain_file_path: the path to the domain file.
        :param problem_file_path: the path to the problem file.
        :param problems_directory_path: the path to the problems' directory.
        :param solving_stats: the statistics of the solving process.
        :param solving_timeout: the timeout for the solver.
        :param tolerance: the numeric tolerance to use.
        """
        num_retries = 0
        self.logger.debug(f"Starting to work on solving problem - {problem_file_path.stem}")
        solution_path = problems_directory_path / f"{problem_file_path.stem}.solution"
        running_options = [
            "-o",
            str(domain_file_path.absolute()),
            "-f",
            str(problem_file_path.absolute()),
            "-planner",
            "sat-hmrphj",
            "-tolerance",
            f"{tolerance}",
            "-gro",
            "naive",
            "-sp",
            str(solution_path.absolute()),
        ]
        run_command = f"{str(JAVA)} -jar {ENHSP_FILE_PATH} {' '.join(running_options)}"
        solver_output_ok = self._run_enhsp_process(run_command, problem_file_path, solving_stats, solving_timeout)
        while not solver_output_ok and num_retries < 3:
            solver_output_ok = self._run_enhsp_process(run_command, problem_file_path, solving_stats, solving_timeout)
            num_retries += 1

    def execute_solver(
        self,
        problems_directory_path: Path,
        domain_file_path: Path,
        solving_timeout: int = MAX_RUNNING_TIME,
        tolerance: float = 0.1,
        problems_prefix: str = "pfile",
    ) -> Dict[str, str]:
        """Solves numeric and PDDL+ problems using the ENHSP algorithm, automatically outputs the solution into a file.

        :param problems_directory_path: the path to the problems directory.
        :param domain_file_path: the path to the domain file.
        :param solving_timeout: the timeout for the solver.
        :param tolerance: the numeric tolerance to use.
        :param problems_prefix: the prefix of the problems to solve.
        """
        solving_stats = {}
        self.logger.info("Starting to solve the input problems using ENHSP solver.")
        for problem_file_path in problems_directory_path.glob(f"{problems_prefix}*.pddl"):
            self.solve_problem(domain_file_path, problem_file_path, problems_directory_path, solving_stats, solving_timeout, tolerance)

        return solving_stats


if __name__ == "__main__":
    args = sys.argv
    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
    solver = ENHSPSolver()
    solver.solve_problem(
        domain_file_path=Path(args[1]),
        problem_file_path=Path(args[2]),
        problems_directory_path=Path(args[3]),
        solving_stats={},
        solving_timeout=int(args[4]),
        tolerance=float(args[5]),
    )
