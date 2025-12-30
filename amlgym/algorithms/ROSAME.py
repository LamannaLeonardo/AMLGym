import re
import os

from amlgym.algorithms.OfflineAlgorithmAdapter import OfflineAlgorithmAdapter
from typing import List, ClassVar, OrderedDict
import shutil
from pathlib import Path
from pddl_plus_parser.lisp_parsers import DomainParser, TrajectoryParser
from pddl_plus_parser.lisp_parsers import ProblemParser

from amlgym.algorithms.rosame.experiment_runner.rosame_runner import Rosame_Runner


class ROSAME(OfflineAlgorithmAdapter):
    """
    Adapter class for running an *unofficial* implementation of the ROSAME
    algorithm: "Neuro-Symbolic Learning of Lifted Action Models from
    Visual Traces", Kai Xi, Stephen Gould, Sylvie Thiebaux, Proceedings of the
    Thirty-Fourth International Conference on Automated Planning and Scheduling, 2024.
    https://ojs.aaai.org/index.php/ICAPS/article/download/31528/33688

    Example:
        .. code-block:: python

            from amlgym.algorithms import get_algorithm
            rosame = get_algorithm('ROSAME')
            model = rosame.learn('path/to/domain.pddl', ['path/to/trace0', 'path/to/trace1'])
            print(model)

    """
    _reference: ClassVar[OrderedDict[str, str]] = {
        'Authors': "K. Xi, S. Gould, and S. Thiebaux",
        'Title': "Neuro-Symbolic Learning of Lifted Action Models from Visual Traces",
        'Venue': "International Conference on Automated Planning and Scheduling",
        'Year': 2024,
        'URL': "https://ojs.aaai.org/index.php/ICAPS/article/download/31528/33688"
    }

    def __init__(self, **kwargs):
        super(ROSAME, self).__init__(**kwargs)

    def learn(self,
              domain_path: str,
              trajectory_paths: List[str],
              use_problems: bool = True) -> str:
        """
        Learns a PDDL action model from:
         (i)    a (possibly empty) input model which is required to specify the predicates and operators signature;
         (ii)   a list of trajectory file paths.

        :parameter domain_path: input PDDL domain file path
        :parameter trajectory_paths: list of trajectory file paths
        :parameter use_problems: boolean flag indicating whether to provide the set of objects
            specified in the problem from which the trajectories have been generated

        :return: a string representing the learned PDDL model
        """

        # Format input trajectories
        os.makedirs('tmp', exist_ok=True)
        filled_traj_paths = []
        for i, traj_path in enumerate(trajectory_paths):
            filled_traj = self._preprocess_trace(traj_path)
            filled_traj_paths.append(f"tmp/{i}_traj_filled")
            with open(f"tmp/{i}_traj_filled", "w") as f:
                f.write(filled_traj)

        # Instantiate ROSAME algorithm
        partial_domain = DomainParser(Path(domain_path), partial_parsing=True).parse_domain()
        rosame = Rosame_Runner(domain_path)

        # Parse input trajectories TODO: TO BE REMOVED (if not ...)
        if not use_problems:
            allowed_observations = [TrajectoryParser(partial_domain).parse_trajectory(traj_path)
                                    for traj_path in sorted(filled_traj_paths,
                                                            key=lambda x: int(x.split('/')[-1].split('_')[0]))]
        else:
            # allowed_observations = []
            for k, traj_path in enumerate(sorted(filled_traj_paths,
                                                 key=lambda x: int(x.split('/')[-1].split('_')[0]))):
                problem_path = trajectory_paths[k].replace('trajectories', 'problems').replace('_traj', '_prob.pddl')
                problem = ProblemParser(Path(problem_path), partial_domain).parse_problem()
                rosame.add_problem(problem)
                # Learn the observation
                observation = TrajectoryParser(partial_domain, problem).parse_trajectory(traj_path)
                rosame.ground_new_trajectory()
                rosame.learn_rosame(observation)
                # allowed_observations.append(TrajectoryParser(partial_domain, problem).parse_trajectory(traj_path))

        # Remove temporary files
        shutil.rmtree('tmp')

        return rosame.rosame_to_pddl()

    def _preprocess_trace(self, traj_path: str) -> str:
        """
        Format the trajectory to make it compliant with the algorithm, by replacing
        initial state and action keywords.

        :parameter traj_path: path to the trajectory file

        :return: a string representing the formatted trajectory
        """

        with open(traj_path, 'r') as f:
            traj_str = f.read()

        # Format extra spaces
        traj_str = re.sub(r' +', ' ', traj_str)

        # Remove initial 'observation' keyword
        traj_str = traj_str.replace('(:trajectory', '(')

        # Rename `action` into `operator`
        traj_str = traj_str.replace('(:action ', '(operator: ')

        # Rename the first state into `init`
        traj_str = traj_str.replace('(:state ', '(:init ', 1)

        return traj_str
