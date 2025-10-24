import sys
import os
sys.path.append(os.path.abspath("aml_evaluation/algorithms/rosame"))

from amlgym.algorithms.AlgorithmAdapter import AlgorithmAdapter
from typing import List
import shutil
from pathlib import Path
from pddl_plus_parser.lisp_parsers import DomainParser, TrajectoryParser
from pddl_plus_parser.lisp_parsers import ProblemParser

from amlgym.algorithms.rosame.experiment_runner.rosame_runner import Rosame_Runner


class ROSAME(AlgorithmAdapter):
    """
    Adapter class for running the ROSAME algorithm: "Neuro-Symbolic Learning
    of Lifted Action Models from Visual Traces", Kai Xi1, Stephen Gould1,
    Sylvie Thiebaux, ICAPS 2024
    """

    def __init__(self, **kwargs):
        super(ROSAME, self).__init__(**kwargs)

    def learn(self,
              domain_file: str,
              trajectory_files: List[str],
              use_problems: bool = True) -> str:

        # Format input trajectories
        os.makedirs('tmp', exist_ok=True)
        filled_traj_paths = []
        for i, traj_path in enumerate(sorted(trajectory_files,
                                             key=lambda x: int(x.split('/')[-1].split('_')[0]))):
            filled_traj = self.preprocess_trace(traj_path)
            filled_traj_paths.append(f"tmp/{i}_traj_filled")
            with open(f"tmp/{i}_traj_filled", "w") as f:
                f.write(filled_traj)

        # Instantiate ROSAME algorithm
        partial_domain = DomainParser(Path(domain_file), partial_parsing=True).parse_domain()
        rosame = Rosame_Runner(domain_file)

        # Parse input trajectories TODO: TO BE REMOVED (if not ...)
        if not use_problems:
            allowed_observations = [TrajectoryParser(partial_domain).parse_trajectory(traj_path)
                                    for traj_path in sorted(filled_traj_paths,
                                                            key=lambda x: int(x.split('/')[-1].split('_')[0]))]
        else:
            # allowed_observations = []
            for k, traj_path in enumerate(sorted(filled_traj_paths,
                                                 key=lambda x: int(x.split('/')[-1].split('_')[0]))):
                problem_path = trajectory_files[k].replace('trajectories', 'problems').replace('_traj', '_prob.pddl')
                problem = ProblemParser(Path(problem_path), partial_domain).parse_problem()
                rosame.add_problem(problem)
                # Learn the observation
                observation = TrajectoryParser(partial_domain, problem).parse_trajectory(traj_path)
                rosame.ground_new_trajectory()
                rosame.learn_rosame(observation)
                # allowed_observations.append(TrajectoryParser(partial_domain, problem).parse_trajectory(traj_path))

        # # Learn action model
        # learned_model, learning_report = sam.learn_action_model(allowed_observations)

        # Remove temporary files
        shutil.rmtree('tmp')

        return rosame.rosame_to_pddl()

    def preprocess_trace(self, traj_path: str) -> str:

        with open(traj_path, 'r') as f:
            traj_str = f.read()

        # Remove initial 'observation' keyword
        traj_str = traj_str.replace('(:trajectory', '(')

        # Rename `action` into `operator`
        traj_str = traj_str.replace('(:action ', '(operator: ')

        # Rename the first state into `init`
        traj_str = traj_str.replace('(:state ', '(:init ', 1)

        return traj_str
