import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, ClassVar, OrderedDict

from pddl_plus_parser.lisp_parsers import DomainParser, TrajectoryParser
from sam_learning.learners import SAMLearner

from amlgym.algorithms.OfflineAlgorithmAdapter import OfflineAlgorithmAdapter


@dataclass
class SAM(OfflineAlgorithmAdapter):
    """
    Adapter class for running the SAM algorithm: "Safe Learning of Lifted Action Models",
    B. Juba and H. S. Le, and R. Stern, Proceedings of the 18th International Conference
    on Principles of Knowledge Representation and Reasoning, 2021.
    https://proceedings.kr.org/2021/36/

    Example:
        .. code-block:: python

            from amlgym.algorithms import get_algorithm
            sam = get_algorithm('SAM')
            model = sam.learn('path/to/domain.pddl', ['path/to/trace0', 'path/to/trace1'])
            print(model)

    """
    _reference: ClassVar[OrderedDict[str, str]] = {
        'Authors': "B. Juba and H. S. Le, and R. Stern",
        'Title': "Safe Learning of Lifted Action Models",
        'Venue': "International Conference on Principles of Knowledge Representation and Reasoning",
        'Year': 2021,
        'URL': "https://proceedings.kr.org/2021/36/",
    }

    def learn(self,
              domain_path: str,
              trajectory_paths: List[str]) -> str:
        """
        Learns a PDDL action model from:
         (i)    a (possibly empty) input model which is required to specify the predicates and operators signature;
         (ii)   a list of trajectory file paths.

        :parameter domain_path: input PDDL domain file path
        :parameter trajectory_paths: list of trajectory file paths

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

        # Instantiate SAM algorithm
        partial_domain = DomainParser(Path(domain_path), partial_parsing=True).parse_domain()
        sam = SAMLearner(partial_domain=partial_domain)
        allowed_observations = []
        for k, traj_path in enumerate(sorted(filled_traj_paths,
                                             key=lambda x: int(x.split('/')[-1].split('_')[0]))):
            allowed_observations.append(TrajectoryParser(partial_domain).parse_trajectory(traj_path))

        # Learn action model
        learned_model, learning_report = sam.learn_action_model(allowed_observations)

        # Remove temporary files
        shutil.rmtree('tmp')

        return learned_model.to_pddl()

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
