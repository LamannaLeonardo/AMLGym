import abc
from dataclasses import dataclass
from typing import Tuple

from unified_planning.shortcuts import SequentialSimulator

from amlgym.modeling.trajectory import Trajectory


@dataclass
class ActiveAlgorithmAdapter(abc.ABC):
    """
    An abstract class for an active action model learning algorithm, which defines the abstract interface
    that must be implemented by every (subclass) algorithm adapter.
    """

    input_domain_path: str

    @abc.abstractmethod
    def learn(self,
              simulator: SequentialSimulator,
              max_steps: int = 100,
              seed: int = 123) -> Tuple[str, Trajectory]:
        """
        Learns a PDDL action model by acting within a simulated environment.

        :parameter simulator: environment simulator
        :parameter max_steps: maximum number of interaction steps with the simulator
        :parameter seed: random seed for reproducibility

        :return: a string representing the learned PDDL model, and a JSON specification of the trajectory
        """
        raise NotImplementedError
