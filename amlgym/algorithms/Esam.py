import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List

from pddl_plus_parser.lisp_parsers import DomainParser, TrajectoryParser

from amlgym.algorithms.OfflineAlgorithmAdapter import OfflineAlgorithmAdapter


@dataclass
class Esam(OfflineAlgorithmAdapter):
    """
    Adapter class for running the Extended SAM (ESAM) algorithm, which extends SAM
    to handle non-injective parameter bindings through proxy action creation and
    CNF-based effect learning.

    ESAM uses the same trajectory format and PDDL parser as SAM (pddl-plus-parser).

    Example:
        .. code-block:: python

            from amlgym.algorithms import get_algorithm
            esam = get_algorithm('Esam')
            model = esam.learn('path/to/domain.pddl', ['path/to/trace0', 'path/to/trace1'])
            print(model)

    """

    negative_preconditions_policy: str = "hard"
    """Negative preconditions policy: 'no_remove', 'soft', or 'hard' (default)."""

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

        from sam_learning.learners import ExtendedSamLearner
        from utilities import NegativePreconditionPolicy

        # Resolve policy enum
        policy_map = {
            "no_remove": NegativePreconditionPolicy.no_remove,
            "soft": NegativePreconditionPolicy.soft,
            "hard": NegativePreconditionPolicy.hard,
        }
        policy = policy_map.get(self.negative_preconditions_policy)
        if policy is None:
            raise ValueError(
                f"Invalid negative_preconditions_policy '{self.negative_preconditions_policy}'. "
                f"Valid values: {list(policy_map.keys())}"
            )

        # Format input trajectories
        with tempfile.TemporaryDirectory() as tmpdir:
            filled_traj_paths = []
            for i, traj_path in enumerate(trajectory_paths):
                filled_traj = self._preprocess_trace(traj_path)
                out_path = f"{tmpdir}/{i}_traj_filled"
                filled_traj_paths.append(out_path)
                with open(out_path, "w") as f:
                    f.write(filled_traj)

            # Instantiate ESAM algorithm
            partial_domain = DomainParser(Path(domain_path), partial_parsing=True).parse_domain()
            esam = ExtendedSamLearner(
                partial_domain=partial_domain,
                negative_preconditions_policy=policy,
            )
            allowed_observations = []
            for traj_path in sorted(filled_traj_paths,
                                    key=lambda x: int(x.split('/')[-1].split('_')[0])):
                allowed_observations.append(TrajectoryParser(partial_domain).parse_trajectory(traj_path))

            # Learn action model
            learned_model, learning_report = esam.learn_action_model(allowed_observations)

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
