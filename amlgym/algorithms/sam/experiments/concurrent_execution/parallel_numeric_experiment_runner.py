"""Runs experiments for the numeric model learning algorithms."""
import argparse
import json
import os
import shutil
import signal
import subprocess
import time
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Tuple, Any

from pddl_plus_parser.lisp_parsers import DomainParser
from pddl_plus_parser.models import Observation, Domain

from experiments.concurrent_execution.parallel_basic_experiment_runner import (
    ParallelExperimentRunner,
    configure_iteration_logger,
)
from experiments.experiments_consts import NUMERIC_SAM_ALGORITHM_VERSIONS
from sam_learning.core import LearnerDomain
from statistics import LearningStatisticsManager
from statistics.utils import init_semantic_performance_calculator
from trajectory_creators import PlanMinerTrajectoriesCreator
from utilities import LearningAlgorithmType
from validators import DomainValidator

PLAN_MINER_DIR_PATH = os.environ["PLAN_MINER_DIR_PATH"]
LEARNING_TIMEOUT = 600


class SingleIterationNSAMExperimentRunner(ParallelExperimentRunner):
    """Class to conduct offline numeric action model learning experiments."""

    def __init__(
        self,
        working_directory_path: Path,
        domain_file_name: str,
        polynom_degree: int,
        learning_algorithm: LearningAlgorithmType,
        fluents_map_path: Optional[Path],
        problem_prefix: str = "pfile",
        running_triplets_experiment: bool = False,
        plan_miner_workdir: Path = None,
        fold_num: int = 0,
    ):
        super().__init__(
            working_directory_path=working_directory_path,
            domain_file_name=domain_file_name,
            learning_algorithm=learning_algorithm,
            problem_prefix=problem_prefix,
            running_triplets_experiment=running_triplets_experiment,
        )
        self.fluents_map = None
        if fluents_map_path is not None:
            with open(fluents_map_path, "rt") as json_file:
                self.fluents_map = json.load(json_file)

        self.polynom_degree = polynom_degree
        self.fold_num = fold_num
        self.semantic_performance_calc = None
        self.plan_miner_domain_file_name = None
        self.plan_miner_workdir = plan_miner_workdir
        if learning_algorithm == LearningAlgorithmType.plan_miner:
            self.plan_miner_domain_file_name = f"{domain_file_name.split('.')[0]}_plan_miner.pddl"
            self.domain_validator = DomainValidator(
                working_directory_path=self.working_directory_path,
                learning_algorithm=learning_algorithm,
                reference_domain_path=self.plan_miner_workdir / self.plan_miner_domain_file_name,
                problem_prefix=problem_prefix,
            )

        else:
            self.domain_validator = DomainValidator(
                self.working_directory_path, learning_algorithm, self.working_directory_path / domain_file_name, problem_prefix=problem_prefix,
            )

    def _init_plan_miner_performance_evaluation(self) -> None:
        """Initializes the algorithm of the semantic precision - recall calculator - for plan miner only."""
        self.semantic_performance_calc = init_semantic_performance_calculator(
            working_directory_path=self.working_directory_path,
            domain_file_path=self.plan_miner_workdir / self.plan_miner_domain_file_name,
            learning_algorithm=self._learning_algorithm,
            test_set_dir_path=self.working_directory_path / "performance_evaluation_trajectories" / f"fold_{self.fold_num}",
            problem_prefix=self.problem_prefix,
            executing_agents=self.executing_agents,
        )

    def _handle_plan_miner_failure(self) -> Tuple[LearnerDomain, Dict[str, Any]]:
        plan_miner_domain = DomainParser(self.plan_miner_workdir / self.plan_miner_domain_file_name, partial_parsing=True).parse_domain()
        plan_miner_domain.actions = {}
        learned_domain = LearnerDomain(plan_miner_domain)
        return learned_domain, {"learning_time": -1}

    def _create_learned_domain_for_evaluation(self, plan_miner_output_domain_path: Path) -> LearnerDomain:
        """Creates the learned domain for evaluation purposes (The learner domain object).

        :param plan_miner_output_domain_path: the path to the Plan-Miner output domain.
        :return: the learned domain for evaluation.
        """
        self.logger.info("Creating the learned domain for PlanMiner's evaluation.")
        try:
            plan_miner_domain = DomainParser(plan_miner_output_domain_path).parse_domain()
            temp_domain = DomainParser(self.plan_miner_workdir / self.plan_miner_domain_file_name, partial_parsing=True).parse_domain()
            learned_domain = LearnerDomain(plan_miner_domain)
            learned_domain.name = temp_domain.name
            learned_domain.requirements = temp_domain.requirements

            for action_name, action_data in plan_miner_domain.actions.items():
                learned_domain.actions[action_name].signature = action_data.signature
                learned_domain.actions[action_name].preconditions = action_data.preconditions
                learned_domain.actions[action_name].discrete_effects = action_data.discrete_effects
                learned_domain.actions[action_name].numeric_effects = action_data.numeric_effects

        except Exception as e:
            self.logger.warning(f"Failed to parse the learned domain for PlanMiner. Probably PlanMiner created a domain with syntax errors.: {e}")
            plan_miner_domain = DomainParser(self.plan_miner_workdir / self.plan_miner_domain_file_name, partial_parsing=True).parse_domain()
            plan_miner_domain.actions = {}
            learned_domain = LearnerDomain(plan_miner_domain)

        with open(plan_miner_output_domain_path, "wt") as domain_file:
            # This should keep the domain name in the correct format and maintain the correct domain name in the PDDL file.
            domain_file.write(learned_domain.to_pddl(should_simplify=False))
            return learned_domain

    def _run_plan_miner_process(self, plan_miner_trajectory_file_path: Path) -> Optional[Path]:
        """Runs the Plan-Miner process to learn the action model.

        :param plan_miner_trajectory_file_path: the path to the Plan-Miner trajectory file.
        :return: the path to the learned action model (if successful).
        """
        plan_miner_domain_name = f"{self.domain_file_name.split('.')[0]}_{uuid.uuid4()}"
        os.chdir(PLAN_MINER_DIR_PATH)
        # cmd = ./PlanMiner {path to pts file} {domain name without extension}
        process = subprocess.Popen(f"./bin/PlanMiner {plan_miner_trajectory_file_path} {plan_miner_domain_name}", shell=True)
        try:
            process.wait(timeout=LEARNING_TIMEOUT)

        except subprocess.TimeoutExpired:
            self.logger.error("Plan-Miner failed to learn action model with the given timeout.")
            os.kill(process.pid, signal.SIGTERM)
            os.system("pkill -f ./bin/PlanMiner")

        except subprocess.CalledProcessError as e:
            self.logger.error(f"PlanMiner failed with the following return code: {e.returncode}")
            return None

        plan_miner_output_domain_path = Path(PLAN_MINER_DIR_PATH) / f"{plan_miner_domain_name}.pddl"
        if plan_miner_output_domain_path.exists():
            self.logger.info("PlanMiner finished successfully!")
            return plan_miner_output_domain_path

        self.logger.error("Plan-Miner failed to learn the action model.")
        return None

    def _apply_plan_miner(self, test_set_dir_path: Path) -> Tuple[LearnerDomain, Dict[str, Any]]:
        """Applies the learning algorithm Plan-Miner to learn the action model.

        :param test_set_dir_path: the path to the directory containing the test problems.
        :return: the learned action model and the learning statistics.
        """
        self.logger.info("Creating the formatted domain and the trajectories for Plan-Miner.")
        plan_miner_trajectory_creator = PlanMinerTrajectoriesCreator(
            domain_file_name=self.domain_file_name, working_directory_path=self.plan_miner_workdir
        )
        plan_miner_trajectory_creator.create_plan_miner_trajectories()
        # initializing the specific numeric performance calculator for Plan-Miner
        self._init_plan_miner_performance_evaluation()
        # Since only after this part the domain is created in the format that Plan-Miner can understand
        # we initialize the statistics manager here
        self.learning_statistics_manager = LearningStatisticsManager(
            working_directory_path=self.working_directory_path,
            domain_path=self.plan_miner_workdir / self.plan_miner_domain_file_name,
            learning_algorithm=self._learning_algorithm,
        )
        plan_miner_trajectory_file_path = self.plan_miner_workdir / "plan_miner_trajectories.pts"
        self.logger.info("Applying Plan-Miner to learn the action model.")
        plan_miner_start_time = time.time()
        plan_miner_output_domain_path = self._run_plan_miner_process(plan_miner_trajectory_file_path)
        learning_report = {
            "learning_time": time.time() - plan_miner_start_time,
        }
        if plan_miner_output_domain_path is None:
            self.logger.info("Plan-Miner failed to learn the action model.")
            return self._handle_plan_miner_failure()

        learned_domain = self._create_learned_domain_for_evaluation(plan_miner_output_domain_path)
        shutil.move(plan_miner_output_domain_path, test_set_dir_path / self.domain_file_name)
        return learned_domain, learning_report

    def _apply_learning_algorithm(
        self, partial_domain: Domain, allowed_observations: List[Observation], test_set_dir_path: Path
    ) -> Tuple[LearnerDomain, Dict[str, str]]:
        """Learns the action model using the numeric action model learning algorithms.

        :param partial_domain: the partial domain without the actions' preconditions and effects.
        :param allowed_observations: the allowed observations.
        :param test_set_dir_path: the path to the directory containing the test problems.
        :return: the learned action model and the learned action model's learning statistics.
        """
        if self._learning_algorithm == LearningAlgorithmType.plan_miner:
            return self._apply_plan_miner(test_set_dir_path)

        learner = NUMERIC_SAM_ALGORITHM_VERSIONS[self._learning_algorithm](
            partial_domain=partial_domain, polynomial_degree=self.polynom_degree, relevant_fluents=self.fluents_map
        )
        return learner.learn_action_model(allowed_observations)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Runs the numeric action model learning algorithms evaluation experiments.")
    parser.add_argument("--working_directory_path", required=True, help="The path to the directory where the domain is")
    parser.add_argument("--domain_file_name", required=True, help="the domain file name including the extension")
    parser.add_argument(
        "--learning_algorithm", required=True, type=int, choices=[3, 5, 15, 19, 20, 21],
    )
    parser.add_argument(
        "--fluents_map_path", required=False, help="The path to the file mapping to the preconditions' " "fluents", default=None,
    )
    parser.add_argument(
        "--polynom_degree", required=False, help="The degree of the polynomial to set in the learning algorithm.", default=0,
    )
    parser.add_argument("--problems_prefix", required=False, help="The prefix of the problems' file names", type=str, default="pfile")
    parser.add_argument("--fold_number", required=True, help="The number of the fold to run", type=int)
    parser.add_argument("--iteration_number", required=True, help="The current iteration to execute", type=int)
    parser.add_argument("--debug", required=False, help="Whether in debug mode.", type=bool, default=False)
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    configure_iteration_logger(args)
    learning_algorithm = LearningAlgorithmType(args.learning_algorithm)
    working_directory_path = Path(args.working_directory_path)
    iteration_number = int(args.iteration_number)
    plan_miner_workdir = (working_directory_path / "train") / f"fold_{args.fold_number}_{args.learning_algorithm}_{iteration_number}"
    offline_learner = SingleIterationNSAMExperimentRunner(
        working_directory_path=working_directory_path,
        domain_file_name=args.domain_file_name,
        learning_algorithm=learning_algorithm,
        fluents_map_path=Path(args.fluents_map_path) if args.fluents_map_path else None,
        polynom_degree=int(args.polynom_degree),
        problem_prefix=args.problems_prefix,
        plan_miner_workdir=plan_miner_workdir,
        fold_num=int(args.fold_number),
    )
    offline_learner.run_fold_iteration(
        fold_num=args.fold_number,
        train_set_dir_path=(working_directory_path / "train") / f"fold_{args.fold_number}_{args.learning_algorithm}_{iteration_number}",
        test_set_dir_path=(working_directory_path / "test") / f"fold_{args.fold_number}_{args.learning_algorithm}_{iteration_number}",
        iteration_number=int(args.iteration_number),
    )


if __name__ == "__main__":
    main()
