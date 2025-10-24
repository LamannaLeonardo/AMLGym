"""Create a train and test set split for the input directory for the action model learning algorithms to use."""
import logging
import random
import shutil
from pathlib import Path
from typing import Tuple, List, Optional, Any, Dict

from .k_fold_split import create_test_set_indices, save_fold_settings, FOLDS_LABEL, load_distributed_fold_settings


class DistributedKFoldSplit:
    """Split the working directory into a train and test set directories."""

    logger: logging.Logger
    working_directory_path: Path
    n_split: int
    train_set_dir_path: Path
    test_set_dir_path: Path
    domain_file_path: Path
    only_train_test: bool

    def __init__(
        self,
        working_directory_path: Path,
        domain_file_name: str,
        n_split: int = 0,
        only_train_test: bool = False,
        learning_algorithms: List[int] = None,
        internal_iterations: List[int] = None,
    ):
        self.logger = logging.getLogger(__name__)
        self.working_directory_path = working_directory_path
        self.n_split = n_split
        self.train_set_dir_path = working_directory_path / "train"
        self.test_set_dir_path = working_directory_path / "test"
        self.domain_file_path = working_directory_path / domain_file_name
        self.only_train_test = only_train_test
        self._learning_algorithms = learning_algorithms
        self._internal_iterations = internal_iterations

    def _copy_domain(self, directory_path: Path) -> None:
        """Copies the domain to the train set directory so that it'd be used in the learning process."""
        self.logger.debug("Copying the domain to the train set directory.")
        shutil.copy(self.domain_file_path, directory_path / self.domain_file_path.name)

    def remove_created_directories(self) -> None:
        """Deletes the train and test directories."""

        self.logger.debug("Deleting the train set directory!")
        shutil.rmtree(self.train_set_dir_path, ignore_errors=True)
        self.logger.debug("Deleting the test set directory!")
        shutil.rmtree(self.test_set_dir_path, ignore_errors=True)

    def create_directories_content(
        self,
        test_set_problems: List[Path],
        selected_training_trajectories: Optional[List[Path]],
        fold_index: int,
        learning_algorithm: int,
        internal_iteration: Optional[int] = None,
        additional_suffix: str = "",
    ) -> Tuple[Path, Path]:
        """Creates the content of the train and test set directories."""
        fold_train_dir_path = (
            self.train_set_dir_path / f"fold_{fold_index}_{learning_algorithm}{additional_suffix}"
            f"{f'_{internal_iteration}' if internal_iteration is not None else ''}"
        )
        fold_test_dir_path = (
            self.test_set_dir_path / f"fold_{fold_index}_{learning_algorithm}{additional_suffix}"
            f"{f'_{internal_iteration}{additional_suffix}' if internal_iteration is not None else ''}"
        )
        fold_train_dir_path.mkdir(exist_ok=True)
        fold_test_dir_path.mkdir(exist_ok=True)
        self._copy_domain(fold_train_dir_path)

        for problem in test_set_problems:
            shutil.copy(problem, fold_test_dir_path / problem.name)

        for trajectory in selected_training_trajectories:
            shutil.copy(trajectory, fold_train_dir_path / trajectory.name)
            problem_path = self.working_directory_path / f"{trajectory.stem}.pddl"
            shutil.copy(problem_path, fold_train_dir_path / problem_path.name)

        return fold_train_dir_path, fold_test_dir_path

    def create_fold_from_scratch(self, folds_data: Dict[str, Any], max_items: int, trajectory_suffix: str) -> None:
        trajectory_paths = list(self.working_directory_path.glob(trajectory_suffix))
        items_per_fold = max_items if (0 < max_items <= len(trajectory_paths)) else len(trajectory_paths)
        self.logger.debug(f"Creating {items_per_fold} items per fold.")
        trajectory_paths = random.sample(trajectory_paths, k=items_per_fold)
        for fold_index, (train_set_indices, test_set_indices) in enumerate(
            create_test_set_indices(items_per_fold, self.n_split, self.only_train_test)
        ):
            test_set_problems = [self.working_directory_path / f"{trajectory_paths[i].stem}.pddl" for i in test_set_indices]
            train_set_trajectories = [trajectory_paths[i] for i in range(len(trajectory_paths)) if i not in test_set_indices]
            training_data = {"internal_iterations": {}}
            for num_used_trajectories in self._internal_iterations:
                self.logger.debug(f"Creating fold {fold_index} with {num_used_trajectories} trajectories.")
                selected_trajectories = train_set_trajectories[:num_used_trajectories]
                for learning_algorithm in self._learning_algorithms:
                    self.create_directories_content(
                        test_set_problems=test_set_problems,
                        selected_training_trajectories=selected_trajectories,
                        fold_index=fold_index,
                        learning_algorithm=learning_algorithm,
                        internal_iteration=num_used_trajectories,
                    )

                training_data["internal_iterations"][int(num_used_trajectories)] = [str(p.absolute()) for p in selected_trajectories]

            max_dataset_size = self._internal_iterations[-1]
            for learning_algorithm in self._learning_algorithms:
                self.create_directories_content(
                    test_set_problems=test_set_problems,
                    selected_training_trajectories=train_set_trajectories[:max_dataset_size],
                    fold_index=fold_index,
                    learning_algorithm=learning_algorithm,
                    additional_suffix="_triplets",
                )

            folds_data[f"{FOLDS_LABEL}_{fold_index}"] = {
                "train": training_data,
                "test": [str(p.absolute()) for p in test_set_problems],
            }
            self.logger.debug("Finished creating fold!")

        save_fold_settings(self.working_directory_path, folds_data)

    def create_k_fold(self, trajectory_suffix: str = "*.trajectory", max_items: int = 0, load_configuration: bool = True):
        """Creates a generator that will be used for the next algorithm to know where the train and test set
            directories reside.

        :param trajectory_suffix: the suffix of the trajectory files to be used.
        :param max_items: the maximum number of items to be used in the train and test set together.
        :param load_configuration: whether to load folds settings from the configuration file.
        :return: a generator for the train and test set directories.
        """
        self.logger.info("Starting to create the folds for the cross validation process.")
        self.train_set_dir_path.mkdir(exist_ok=True)
        self.test_set_dir_path.mkdir(exist_ok=True)
        folds_data = load_distributed_fold_settings(self.working_directory_path)
        train_test_paths = []
        if load_configuration and len(folds_data) > 0:
            self.logger.debug("Loading the folds settings from the configuration file.")
            for index, (fold_name, fold_content) in enumerate(folds_data.items()):
                for iteration_num, selected_trajectories in fold_content["train"]["internal_iterations"].items():
                    selected_trajectories_paths = [Path(p) for p in selected_trajectories]
                    for learning_algorithm in self._learning_algorithms:
                        self.logger.debug("Creating fold directories content for each learning algorithm.")
                        train_test_paths.append(
                            self.create_directories_content(
                                test_set_problems=fold_content["test"],
                                selected_training_trajectories=selected_trajectories_paths,
                                fold_index=index,
                                learning_algorithm=learning_algorithm,
                                internal_iteration=int(iteration_num),
                            )
                        )

                self.logger.debug("Finished creating fold!")
                # creating the folder to be used for the triplets based experiments
                largest_iteration = max([int(i) for i in fold_content["train"]["internal_iterations"].keys()])
                relevant_paths = [Path(p) for p in fold_content["train"]["internal_iterations"][str(largest_iteration)]]
                for learning_algorithm in self._learning_algorithms:
                    self.create_directories_content(
                        test_set_problems=fold_content["test"],
                        selected_training_trajectories=relevant_paths,
                        fold_index=index,
                        learning_algorithm=learning_algorithm,
                        additional_suffix="_triplets",
                    )

            return

        self.create_fold_from_scratch(folds_data, max_items, trajectory_suffix)
