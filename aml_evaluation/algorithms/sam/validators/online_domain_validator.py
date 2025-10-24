"""Module to validate the correctness of the learned action models that were generated."""
import csv
from pathlib import Path
from typing import Optional

from utilities import SolutionOutputTypes
from validators.safe_domain_validator import DomainValidator, DEBUG_STATISTICS

ACTION_LINE_REGEX = r"(\[\d+, \d+\]): \(.*\)"

ONLINE_SOLVING_STATISTICS = [
    "learning_algorithm",
    "episode_number",
    "number_of_steps_in_episode",
    "training_goal_achieved",
    "solver",
    "ok",
    "no_solution",
    "timeout",
    "solver_error",
    "not_applicable",
    "goal_not_achieved",
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
]


class OnlineLearningDomainValidator(DomainValidator):
    """Extension to th domain validator to support information relevant only to the online learning process."""

    def validate_domain(
            self, tested_domain_file_path: Path, test_set_directory_path: Optional[Path] = None,
            episode_number: Optional[int] = None, num_steps: Optional[int] = None,
            num_training_goal_achieved: int = 0, tolerance: float = 0.01) -> None:
        """Validates that using the input domain problems can be solved.

        :param tested_domain_file_path: the path of the domain that was learned using POL.
        :param test_set_directory_path: the path to the directory containing the test set problems.
        :param episode_number: the number of the current episode.
        :param num_steps: the number of steps that were taken in the current episode.
        :param num_training_goal_achieved: the number of times the training goal was achieved in the batch.
        :param tolerance: the tolerance to use when solving the problems.
        """
        self.logger.info("Solving the test set problems using the learned domain!")
        solving_report = self.solver.execute_solver(
            problems_directory_path=test_set_directory_path,
            domain_file_path=tested_domain_file_path,
            problems_prefix=self.problem_prefix,
            tolerance=tolerance
        )

        solving_stats = {solution_type.name: 0 for solution_type in SolutionOutputTypes}
        for debug_statistic in DEBUG_STATISTICS:
            solving_stats[debug_statistic] = []

        for problem_file_name, entry in solving_report.items():
            problem_file_path = test_set_directory_path / f"{problem_file_name}.pddl"
            if entry == SolutionOutputTypes.ok.name:
                solution_file_path = test_set_directory_path / f"{problem_file_name}.solution"
                self._validate_solution_content(solution_file_path=solution_file_path,
                                                problem_file_path=problem_file_path,
                                                iteration_statistics=solving_stats)

                continue

            solving_stats[entry] += 1
            solving_stats[f"problems_{entry}"].append(problem_file_name)

        self._calculate_solving_percentages(solving_stats)
        self.solving_stats.append({
            "learning_algorithm": self.learning_algorithm.name,
            "episode_number": episode_number,
            "number_of_steps_in_episode": num_steps,
            "training_goal_achieved": num_training_goal_achieved,
            "solver": self._solver_name,
            **solving_stats
        })
        self._clear_plans(test_set_directory_path)

    def write_statistics(self, fold_num: int) -> None:
        """Writes the statistics of the learned model into a CSV file.

        :param fold_num: the index of the fold that is currently being tested.
        """
        output_statistics_path = self.results_dir_path / f"online_nsam_{self.learning_algorithm.name}" \
                                                         f"_problem_solving_stats_{fold_num}.csv"
        with open(output_statistics_path, 'wt', newline='') as csv_file:
            test_set_writer = csv.DictWriter(csv_file, fieldnames=ONLINE_SOLVING_STATISTICS)
            test_set_writer.writeheader()
            test_set_writer.writerows(self.solving_stats)

    def write_complete_joint_statistics(self) -> None:
        """Writes a statistics file containing all the folds combined data."""
        output_path = self.results_dir_path / f"online_nsam_{self.learning_algorithm.name}_all_folds_solving_stats.csv"
        with open(output_path, 'wt', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=ONLINE_SOLVING_STATISTICS)
            writer.writeheader()
            writer.writerows(self.aggregated_solving_stats)
