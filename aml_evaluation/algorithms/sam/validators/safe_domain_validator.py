"""Module to validate the correctness of the learned action models that were generated."""
import csv
import logging
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

from pddl_plus_parser.models import Observation, MultiAgentObservation

from solvers import FastDownwardSolver, MetricFFSolver, ENHSPSolver, FFADLSolver
from utilities import LearningAlgorithmType, SolverType, SolutionOutputTypes, NegativePreconditionPolicy, MappingElement, MacroActionParser
from validators.common import AGGREGATED_SOLVING_FIELDS
from validators.validator_script_data import VALID_PLAN, INAPPLICABLE_PLAN, GOAL_NOT_REACHED, run_validate_script

SOLVER_TYPES = {
    SolverType.fast_downward: FastDownwardSolver,
    SolverType.metric_ff: MetricFFSolver,
    SolverType.enhsp: ENHSPSolver,
    SolverType.fast_forward: FFADLSolver,
}

SOLVING_STATISTICS = [
    "learning_algorithm",
    "num_trajectories",
    "num_trajectory_triplets",
    "policy",
    "learning_time",
    "solving_time",
    "solver",
    "ok",
    "no_solution",
    "timeout",
    "solver_error",
    "not_applicable",
    "goal_not_achieved",
    "validated_against_expert_plan",
    "not_validated_against_expert_plan",
    "problems_ok",
    "problems_no_solution",
    "problems_timeout",
    "problems_solver_error",
    "problems_not_applicable",
    "problems_goal_not_achieved",
    "problems_validated_against_expert_plan",
    "problems_not_validated_against_expert_plan",
    "percent_ok",
    "percent_no_solution",
    "percent_timeout",
    "percent_solver_error",
    "percent_not_applicable",
    "percent_goal_not_achieved",
    "percent_validated_against_expert_plan",
    "percent_not_validated_against_expert_plan",
]

DEBUG_STATISTICS = [
    "problems_ok",
    "problems_no_solution",
    "problems_timeout",
    "problems_solver_error",
    "problems_not_applicable",
    "problems_goal_not_achieved",
    "problems_validated_against_expert_plan",
    "problems_not_validated_against_expert_plan",
]

VALIDATED_AGAINST_EXPERT_PLAN = "validated_against_expert_plan"
NOT_VALIDATED_AGAINST_EXPERT_PLAN = "not_validated_against_expert_plan"

NUMERIC_STATISTICS_LABELS = [
    *[solution_type.name for solution_type in SolutionOutputTypes],
    VALIDATED_AGAINST_EXPERT_PLAN,
    NOT_VALIDATED_AGAINST_EXPERT_PLAN,
]


ACTION_LINE_REGEX = r"(\[\d+, \d+\]): \(.*\)"


class DomainValidator:
    """Validates that the learned domain can create plans.

    Note:
        There is no validation on the plan content since the learning process is safe.
    """

    logger: logging.Logger
    solving_stats: List[Dict[str, Any]]
    aggregated_solving_stats: List[Dict[str, Any]]
    learning_algorithm: LearningAlgorithmType
    working_directory_path: Path
    reference_domain_path: Path
    results_dir_path: Path
    problem_prefix: str

    def __init__(
        self, working_directory_path: Path, learning_algorithm: LearningAlgorithmType, reference_domain_path: Path, problem_prefix: str = "pfile",
    ):
        self.logger = logging.getLogger(__name__)
        self.solving_stats = []
        self.aggregated_solving_stats = []
        self.learning_algorithm = learning_algorithm
        self.results_dir_path = working_directory_path / "results_directory"
        self.reference_domain_path = reference_domain_path
        self.problem_prefix = problem_prefix
        self.working_directory_path = working_directory_path

    @staticmethod
    def _clear_plans(test_set_directory: Path) -> None:
        """Clears the plan filed from the directory.

        :param test_set_directory: the path to the directory containing the plans.
        """
        for solver_output_path in test_set_directory.glob("*.solution"):
            solver_output_path.unlink(missing_ok=True)

    def _validate_against_expert_plan(
        self, solution_file_path: Path, problem_file_path: Path, iteration_statistics: Dict[str, Union[int, List[str]]], tested_domain_path: Path
    ) -> None:
        """Validates that the expert solution can be used against the learned domain.

        :param solution_file_path: the path to the solution file.
        :param problem_file_path: the path to the problem file.
        :param iteration_statistics: the statistics of the current iteration.
        :param tested_domain_path: the path to the domain file to validate against.
        """
        validation_file_path = run_validate_script(
            domain_file_path=tested_domain_path, problem_file_path=problem_file_path, solution_file_path=solution_file_path
        )
        with open(validation_file_path, "r") as validation_file:
            validation_file_content = validation_file.read()
            if VALID_PLAN in validation_file_content:
                self.logger.info("The expert plan is valid on the learned domain.")
                iteration_statistics[VALIDATED_AGAINST_EXPERT_PLAN] += 1
                iteration_statistics[f"problems_{VALIDATED_AGAINST_EXPERT_PLAN}"].append(problem_file_path.name)

            else:
                self.logger.info("The expert plan is not valid on the learned domain.")
                iteration_statistics[NOT_VALIDATED_AGAINST_EXPERT_PLAN] += 1
                iteration_statistics[f"problems_{NOT_VALIDATED_AGAINST_EXPERT_PLAN}"].append(problem_file_path.name)

        validation_file_path.unlink(missing_ok=True)

    def _validate_solution_content(
        self, solution_file_path: Path, problem_file_path: Path, iteration_statistics: Dict[str, Union[int, List[str]]]
    ) -> None:
        """Validates that the solution file contains a valid plan.

        :param solution_file_path: the path to the solution file.
        :param problem_file_path: the path to the problem file.
        :param iteration_statistics: the statistics of the current iteration.
        """
        validation_file_path = run_validate_script(
            domain_file_path=self.reference_domain_path, problem_file_path=problem_file_path, solution_file_path=solution_file_path
        )

        with open(validation_file_path, "r", encoding="utf-8") as validation_file:
            validation_file_content = validation_file.read()
            if VALID_PLAN in validation_file_content:
                self.logger.info("The plan is valid.")
                iteration_statistics["ok"] += 1
                iteration_statistics["problems_ok"].append(problem_file_path.name)

            elif INAPPLICABLE_PLAN in validation_file_content:
                self.logger.info("The plan is not applicable.")
                iteration_statistics["not_applicable"] += 1
                iteration_statistics["problems_not_applicable"].append(problem_file_path.name)

            elif GOAL_NOT_REACHED in validation_file_content:
                self.logger.info("The plan did not reach the required goal.")
                iteration_statistics["goal_not_achieved"] += 1
                iteration_statistics["problems_goal_not_achieved"].append(problem_file_path.name)

        validation_file_path.unlink(missing_ok=True)

    @staticmethod
    def _extract_num_triplets(used_observations: Union[List[Observation], List[MultiAgentObservation], List[Path]] = None) -> int:
        """Extracts the number of trajectory triplets from the observations.

        :param used_observations: the observations used to generate the plans.
        :return: the number of trajectory triplets in the used observations.
        """
        if not used_observations:
            return 0

        for observation in used_observations:
            if isinstance(observation, Path):
                with open(observation, "r") as observation_file:
                    num_operators = 0
                    for line in observation_file.readlines():
                        match = re.match(ACTION_LINE_REGEX, line)
                        num_operators = num_operators + 1 if match else num_operators

                    return num_operators

        num_triplets = sum([len(observation.components) for observation in used_observations])
        return num_triplets

    @staticmethod
    def _calculate_expert_validation_statistics(solving_stats: Dict[str, Any]) -> None:
        """Calculates the expert validation statistics.

        :param solving_stats: the solving statistics.
        """
        total_validated = sum([solving_stats[statistic] for statistic in [VALIDATED_AGAINST_EXPERT_PLAN, NOT_VALIDATED_AGAINST_EXPERT_PLAN]])
        total_validated = total_validated if total_validated > 0 else 1

        for statistic in [VALIDATED_AGAINST_EXPERT_PLAN, NOT_VALIDATED_AGAINST_EXPERT_PLAN]:
            solving_stats[f"percent_{statistic}"] = 100 * (solving_stats[statistic] / total_validated)

    def _calculate_solving_percentages(self, solving_stats: Dict[str, Any]) -> None:
        """Calculates the percentage of solved problems.

        :param solving_stats:  the solving statistics.
        """
        total_problems = sum([solving_stats[statistic] for statistic in AGGREGATED_SOLVING_FIELDS])
        total_problems = total_problems if total_problems > 0 else 1
        for statistic in AGGREGATED_SOLVING_FIELDS:
            percentage_statistic = 100 * (solving_stats[statistic] / total_problems)
            solving_stats[f"percent_{statistic}"] = percentage_statistic
            self.logger.info(f"{statistic} percentage: {percentage_statistic:.2f}%")

    @staticmethod
    def adapt_solution_file(solution_path: Path, mapping: Dict[str, MappingElement]):
        """
        Post-processing solution files with macro actions and adapt them to something validators can work with.
        That essentially means replacing macro action lines with its consisting solo actions lines.

        :param solution_path: the path to the solution file output from the learned domain.
        :param mapping: the macro actions mapping of the learned domain.
        """
        with open(solution_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            extracted_lines = MacroActionParser.extract_actions_from_macro_action(action_line=line, mapper=mapping)
            new_lines.extend([extracted_line if extracted_line.endswith("\n") else f"{extracted_line}\n" for extracted_line in extracted_lines])

        with open(solution_path, "w") as file:
            file.writelines(new_lines)

    def validate_domain(
        self,
        tested_domain_file_path: Path,
        test_set_directory_path: Optional[Path] = None,
        used_observations: Union[List[Union[Observation, MultiAgentObservation]], List[Path]] = None,
        tolerance: float = 0.01,
        timeout: int = 5,
        learning_time: float = 0,
        solvers_portfolio: List[SolverType] = None,
        preconditions_removal_policy: NegativePreconditionPolicy = NegativePreconditionPolicy.no_remove,
        mapping: Dict[str, MappingElement] = None,
    ) -> None:
        """Validates that using the input domain problems can be solved.

        :param tested_domain_file_path: the path of the domain that was learned using POL.
        :param test_set_directory_path: the path to the directory containing the test set problems.
        :param used_observations: the observations that were used to learn the domain.
        :param timeout: the timeout for the solver.
        :param tolerance: the numeric tolerance to use.
        :param learning_time: the time it took to learn the domain (in seconds).
        :param solvers_portfolio: the solvers to use for the validation, can be one or more and each will try to solve each planning problem at most once.
        :param preconditions_removal_policy: the policy used to remove the negative discrete preconditions.
        :param mapping: the learned model mapper from macro action to mapping element.
        """
        num_triplets = self._extract_num_triplets(used_observations)
        solving_stats: Dict[str, Any] = {label: 0 for label in NUMERIC_STATISTICS_LABELS}
        for debug_statistic in DEBUG_STATISTICS:
            solving_stats[debug_statistic] = []

        self.logger.info("Solving the test set problems using the learned domain!")
        problem_solving_times = []
        for problem_path in test_set_directory_path.glob(f"{self.problem_prefix}*.pddl"):
            problem_solving_report = {}
            problem_solved = False
            problem_file_name = problem_path.stem
            for solver_type in solvers_portfolio:
                start_time = time.time()
                solver = SOLVER_TYPES[solver_type]()
                solver.solve_problem(
                    problems_directory_path=test_set_directory_path,
                    domain_file_path=tested_domain_file_path,
                    problem_file_path=problem_path,
                    tolerance=tolerance,
                    solving_timeout=timeout,
                    solving_stats=problem_solving_report,
                )
                end_time = time.time()
                if problem_solving_report[problem_file_name] == SolutionOutputTypes.ok.name:
                    problem_solving_times.append(end_time - start_time)  # time in seconds
                    problem_solved = True
                    solution_file_path = test_set_directory_path / f"{problem_file_name}.solution"

                    if mapping:
                        self.adapt_solution_file(solution_path=solution_file_path, mapping=mapping)

                    self._validate_solution_content(
                        solution_file_path=solution_file_path, problem_file_path=problem_path, iteration_statistics=solving_stats
                    )
                    break

            if problem_solved:
                continue

            expert_plan_path = self.working_directory_path / f"{problem_file_name}.solution"
            solving_outcome = problem_solving_report[problem_file_name]
            solving_stats[solving_outcome] += 1
            solving_stats[f"problems_{solving_outcome}"].append(problem_file_name)
            self._validate_against_expert_plan(
                solution_file_path=expert_plan_path,
                problem_file_path=problem_path,
                iteration_statistics=solving_stats,
                tested_domain_path=tested_domain_file_path,
            )

        solving_stats["solving_time"] = (
            sum(problem_solving_times) / len(problem_solving_times) if len(problem_solving_times) > 0 else 0
        )  # average time in seconds for all solved problems
        self._calculate_solving_percentages(solving_stats)
        self._calculate_expert_validation_statistics(solving_stats)
        num_trajectories = len(used_observations)
        self.solving_stats.append(
            {
                "learning_algorithm": self.learning_algorithm.name,
                "num_trajectories": num_trajectories,
                "policy": preconditions_removal_policy.name,
                "num_trajectory_triplets": num_triplets,
                "learning_time": learning_time,
                "solver": [solver.name for solver in solvers_portfolio],
                **solving_stats,
            }
        )
        self._clear_plans(test_set_directory_path)

    def write_statistics(self, fold_num: int, iteration: Optional[int] = None) -> None:
        """Writes the statistics of the learned model into a CSV file.

        :param fold_num: the index of the fold that is currently being tested.
        :param iteration: the index of the iteration that is currently being tested.
        """
        output_statistics_path = self.results_dir_path / (
            f"{self.learning_algorithm.name}"
            f"_problem_solving_stats_fold_{fold_num}"
            f"{f'_{iteration}_trajectories' if iteration is not None else ''}.csv"
        )
        with open(output_statistics_path, "wt", newline="") as csv_file:
            test_set_writer = csv.DictWriter(csv_file, fieldnames=SOLVING_STATISTICS)
            test_set_writer.writeheader()
            test_set_writer.writerows(self.solving_stats)

    def write_complete_joint_statistics(self, fold: Optional[int] = None) -> None:
        """Writes a statistics file containing all the folds combined data."""

        output_path = (
            self.results_dir_path / f"{self.learning_algorithm.name}_all_folds_solving_stats.csv"
            if fold is None
            else self.results_dir_path / f"{self.learning_algorithm.name}_problem_solving_stats_{fold}.csv"
        )
        with open(output_path, "wt", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=SOLVING_STATISTICS)
            writer.writeheader()
            writer.writerows(self.aggregated_solving_stats)

    def clear_statistics(self) -> None:
        """Clears the statistics so that each fold will have no relation to its predecessors."""
        self.aggregated_solving_stats.extend(self.solving_stats)
        self.solving_stats.clear()
