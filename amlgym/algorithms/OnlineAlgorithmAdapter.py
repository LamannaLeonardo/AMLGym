import abc
from dataclasses import dataclass
from typing import Any, Tuple, Dict

from unified_planning.shortcuts import SequentialSimulator

from amlgym.modeling.trajectory import Trajectory


@dataclass
class OnlineAlgorithmAdapter(abc.ABC):
    """
    An abstract class for an online action model learning algorithm, which defines the abstract interface
    that must be implemented by every (subclass) algorithm adapter.
    """

    @abc.abstractmethod
    def learn(self,
              simulator: SequentialSimulator,
              input_domain_path: str,
              seed: int = 123) -> Tuple[str, Trajectory]:
        """
        Learns a PDDL action model from:
         (i)   a simulator of the environment to learn from
         (ii)    a (possibly empty) input model which is required to specify the predicates and operators signature;

        :parameter simulator: environment simulator
        :parameter input_domain_path: input PDDL domain file path
        :parameter seed: random seed for reproducibility

        :return: a string representing the learned PDDL model, and a JSON specification of the trajectory
        """
        raise NotImplementedError
