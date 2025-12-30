import abc
from dataclasses import dataclass
from typing import List


@dataclass
class OfflineAlgorithmAdapter(abc.ABC):
    """
    An abstract class for an action model learning algorithm, which defines the abstract interface that must be
    implemented by every (subclass) algorithm adapter to enable automated evaluation.
    """

    @abc.abstractmethod
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
        raise NotImplementedError
