import abc
from typing import List, TypeVar

ActionType = TypeVar('ActionType')
StateType = TypeVar('StateType')


class Env(abc.ABC):
    """
    An AMLGym environment interface that is required for measuring predictive power
     metrics. An example of AMLGym environment is a unified-planning sequential simulator
     that implements the :meth:`apply` and :meth:`applicable_actions` methods.
    """

    @abc.abstractmethod
    def apply(self, s: StateType, a: ActionType) -> StateType:  # TODO: support stochastic transitions?
        """
        Return the state obtained after exeucuting action `a` in the current state `s`
        :param s: the current state `s`
        :param a: the action `a` to execute
        :return: the state `s'` reached after executing action `a` in state `s`
        """
        pass

    @abc.abstractmethod
    def applicable_actions(self, state: StateType) -> List[ActionType]:
        """
        Returns the set of actions applicable in the current state `s`
        :param state: the current state `s`
        :return: the list of actions applicable in the current state `s`
        """
        pass
