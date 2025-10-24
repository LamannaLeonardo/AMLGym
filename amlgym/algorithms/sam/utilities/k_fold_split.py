"""Create a train and test set split for the input directory for the action model learning algorithms to use."""
import json
import logging
import random
import shutil
from pathlib import Path
from typing import Tuple, List, Iterator, Generator, Dict

from sklearn.model_selection import train_test_split, KFold

RANDOM_STATE = 42  # it is always good to seed something according to the most important number in the world!
DEFAULT_TEST_SIZE = 0.2

FOLDS_CONFIG_FILE_NAME = "folds.json"
FOLDS_LABEL = "fold"


def create_test_set_indices(array_size: int, n_split: int, only_train_test: bool = False) -> Iterator[Tuple[List[int], List[int]]]:
    """Creates the indices to use to create the train and the test set of the problems.

    :param array_size: the size of the array containing the problems.
    :param n_split: the number of splits to divide the dataset to.
    :param only_train_test: whether to only split to train and test.
    :return: the train and the test set indices for each fold.
    """
    indices = list(range(array_size))
    if not only_train_test:
        kf = KFold(n_splits=n_split, random_state=RANDOM_STATE, shuffle=True)
        for train, test in kf.split(indices):
            yield train, test

    else:
        train, test = train_test_split(indices, test_size=DEFAULT_TEST_SIZE, random_state=RANDOM_STATE, shuffle=True)
        yield train, test


def save_fold_settings(workdir_path: Path, folds_configuration: Dict[str, Dict[str, List[str]]]) -> None:
    """Saves the fold settings to a json file.

    :param workdir_path: the path to the working directory.
    :param folds_configuration: the folds configuration, i.e. the train and test problems.
    """
    with open(workdir_path / FOLDS_CONFIG_FILE_NAME, "wt") as folds_file:
        json.dump(folds_configuration, folds_file)


def load_fold_settings(workdir_path: Path) -> Dict[str, Dict[str, List[Path]]]:
    """Loads the fold settings from a json file.

    :param workdir_path: the path to the working directory.
    :return: the folds configuration, i.e. the train and test problems.
    """
    if not (workdir_path / FOLDS_CONFIG_FILE_NAME).exists():
        return {}

    folds_configurations = {}
    with open(workdir_path / FOLDS_CONFIG_FILE_NAME, "rt") as folds_file:
        config_data = json.load(folds_file)
        for fold_name, fold in config_data.items():
            folds_configurations[fold_name] = {
                "train": [Path(problem) for problem in fold["train"]],
                "test": [Path(problem) for problem in fold["test"]],
            }

    return folds_configurations


def load_distributed_fold_settings(workdir_path: Path) -> Dict[str, Dict[str, List[Path]]]:
    """Loads the fold settings from a json file.

    :param workdir_path: the path to the working directory.
    :return: the folds configuration, i.e. the train and test problems.
    """
    if not (workdir_path / FOLDS_CONFIG_FILE_NAME).exists():
        return {}

    folds_configurations = {}
    with open(workdir_path / FOLDS_CONFIG_FILE_NAME, "rt") as folds_file:
        config_data = json.load(folds_file)
        for fold_name, fold in config_data.items():
            folds_configurations[fold_name] = {"train": fold["train"], "test": [Path(problem) for problem in fold["test"]]}

    return folds_configurations


class KFoldSplit:
    """Split the working directory into a train and test set directories."""

    logger: logging.Logger
    working_directory_path: Path
    n_split: int
    train_set_dir_path: Path
    test_set_dir_path: Path
    domain_file_path: Path
    only_train_test: bool

    def __init__(self, working_directory_path: Path, domain_file_name: str, n_split: int = 0, only_train_test: bool = False):
        self.logger = logging.getLogger(__name__)
        self.working_directory_path = working_directory_path
        self.n_split = n_split
        self.train_set_dir_path = working_directory_path / "train"
        self.test_set_dir_path = working_directory_path / "test"
        self.domain_file_path = working_directory_path / domain_file_name
        self.only_train_test = only_train_test

    def _copy_domain(self) -> None:
        """Copies the domain to the train set directory so that it'd be used in the learning process."""
        self.logger.debug("Copying the domain to the train set directory.")
        shutil.copy(self.domain_file_path, self.train_set_dir_path / self.domain_file_path.name)

    def remove_created_directories(self) -> None:
        """Deletes the train and test directories."""
        self.logger.debug("Deleting the train set directory!")
        shutil.rmtree(self.train_set_dir_path)
        self.logger.debug("Deleting the test set directory!")
        shutil.rmtree(self.test_set_dir_path)

    def create_directories_content(self, train_set_problems: List[Path], test_set_problems: List[Path], trajectory_paths: List[Path]) -> None:
        self.train_set_dir_path.mkdir(exist_ok=True)
        self.test_set_dir_path.mkdir(exist_ok=True)
        self._copy_domain()

        for problem in test_set_problems:
            shutil.copy(problem, self.test_set_dir_path / problem.name)

        for trajectory, problem in zip(trajectory_paths, train_set_problems):
            shutil.copy(trajectory, self.train_set_dir_path / trajectory.name)
            shutil.copy(problem, self.train_set_dir_path / problem.name)

    def create_k_fold(
        self, trajectory_suffix: str = "*.trajectory", max_items: int = 0, load_configuration: bool = True
    ) -> Generator[Tuple[Path, Path], None, None]:
        """Creates a generator that will be used for the next algorithm to know where the train and test set
            directories reside.

        :param trajectory_suffix: the suffix of the trajectory files to be used.
        :param max_items: the maximum number of items to be used in the train and test set together.
        :param load_configuration: whether to load folds settings from the configuration file.
        :return: a generator for the train and test set directories.
        """
        self.logger.info("Starting to create the folds for the cross validation process.")
        folds_data = load_fold_settings(self.working_directory_path)
        if load_configuration and len(folds_data) > 0:
            self.logger.info("Loading the folds settings from the configuration file.")
            for fold_name, fold_content in folds_data.items():
                train_set_trajectories = [self.working_directory_path / f"{problem_path.stem}.trajectory" for problem_path in fold_content["train"]]
                self.create_directories_content(fold_content["train"], fold_content["test"], train_set_trajectories)
                self.logger.debug("Finished creating fold!")
                yield self.train_set_dir_path, self.test_set_dir_path

                self.remove_created_directories()

            return

        problem_paths = []
        trajectory_paths = list(self.working_directory_path.glob(trajectory_suffix))
        trajectory_paths.sort()  # sort the trajectories so that the same order is used each time the algorithm runs
        items_per_fold = max_items if (0 < max_items <= len(trajectory_paths)) else len(trajectory_paths)
        trajectory_paths = random.sample(trajectory_paths, k=items_per_fold)
        for trajectory_file_path in trajectory_paths:
            problem_paths.append(self.working_directory_path / f"{trajectory_file_path.stem}.pddl")

        num_splits = len(trajectory_paths) if self.n_split == 0 else self.n_split
        for fold_index, (train_set_indices, test_set_indices) in enumerate(
            create_test_set_indices(len(problem_paths), num_splits, self.only_train_test)
        ):
            test_set_problems = [problem_paths[i] for i in test_set_indices]
            train_set_problems = [problem_paths[i] for i in train_set_indices]
            train_set_trajectories = [trajectory_paths[i] for i in range(len(trajectory_paths)) if i not in test_set_indices]
            self.logger.info(
                f"Created a new fold - train set has the following problems: {train_set_problems} "
                f"and test set had the following problems: {test_set_problems}"
            )
            self.create_directories_content(train_set_problems, test_set_problems, train_set_trajectories)
            folds_data[f"{FOLDS_LABEL}_{fold_index}"] = {
                "train": [str(p.absolute()) for p in train_set_problems],
                "test": [str(p.absolute()) for p in test_set_problems],
            }
            self.logger.debug("Finished creating fold!")
            yield self.train_set_dir_path, self.test_set_dir_path

            self.remove_created_directories()

        save_fold_settings(self.working_directory_path, folds_data)
