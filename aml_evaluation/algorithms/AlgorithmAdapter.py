import abc
from dataclasses import dataclass
from typing import List


@dataclass
class AlgorithmAdapter(abc.ABC):
    """
    An abstract class for an action model learning algorithm, which defines the abstract interface that must be
    implemented by every (subclass) algorithm adapter to enable automated evaluation.
    """

    @abc.abstractmethod
    def learn(self,
              domain_file: str,
              trajectory_files: List[str]) -> str:
        """
        Learns an action model from:
         (i)    a (possibly empty input) model which is required to specify the predicates and operators signature;
         (ii)   a list of trajectory file paths.
        :param domain_file: input PDDL domain file path
        :param trajectory_files: list of trajectory file paths
        :return: a string representing the action model
        """
        raise NotImplementedError
