import sys
import os
from dataclasses import dataclass

sys.path.append(os.path.abspath("aml_evaluation/algorithms/sam"))

from amlgym.algorithms.AlgorithmAdapter import AlgorithmAdapter
from typing import List
import shutil
from pathlib import Path
from pddl_plus_parser.lisp_parsers import DomainParser, TrajectoryParser

from amlgym.algorithms.sam.sam_learning.learners import SAMLearner
from pddl_plus_parser.lisp_parsers import ProblemParser


@dataclass
class SAM(AlgorithmAdapter):
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
        for i, traj_path in enumerate(sorted(trajectory_paths,
                                             key=lambda x: int(x.split('/')[-1].split('_')[0]))):
            filled_traj = self._preprocess_trace(traj_path)
            filled_traj_paths.append(f"tmp/{i}_traj_filled")
            with open(f"tmp/{i}_traj_filled", "w") as f:
                f.write(filled_traj)

        # Instantiate SAM algorithm
        partial_domain = DomainParser(Path(domain_path), partial_parsing=True).parse_domain()
        sam = SAMLearner(partial_domain=partial_domain)

        # Parse input trajectories
        if not use_problems:
            allowed_observations = [TrajectoryParser(partial_domain).parse_trajectory(traj_path)
                                    for traj_path in sorted(filled_traj_paths,
                                                            key=lambda x: int(x.split('/')[-1].split('_')[0]))]
        else:
            allowed_observations = []
            for k, traj_path in enumerate(sorted(filled_traj_paths,
                                                 key=lambda x: int(x.split('/')[-1].split('_')[0]))):
                problem_path = trajectory_paths[k].replace('trajectories', 'problems').replace('_traj', '_prob.pddl')
                problem = ProblemParser(Path(problem_path), partial_domain).parse_problem()
                allowed_observations.append(TrajectoryParser(partial_domain, problem).parse_trajectory(traj_path))

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

        # Remove initial 'observation' keyword
        traj_str = traj_str.replace('(:trajectory', '(')

        # Rename `action` into `operator`
        traj_str = traj_str.replace('(:action ', '(operator: ')

        # Rename the first state into `init`
        traj_str = traj_str.replace('(:state ', '(:init ', 1)

        return traj_str
