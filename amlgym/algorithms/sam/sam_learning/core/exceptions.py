"""Module for exceptions that will be used in the algorithms."""
from sam_learning.core.learning_types import EquationSolutionType


class NotSafeActionError(Exception):
    """An exception type indicating that the learning process is not safe.

    Note:
        The exception contains the reason for the action not being safe to learn. Can be used in the reports.
    """
    action_name: str
    reason: str
    solution_type: EquationSolutionType

    def __init__(self, name: str, reason: str, solution_type: EquationSolutionType):
        self.action_name = name
        self.reason = reason
        self.solution_type = solution_type

    def __str__(self):
        return f"The action {self.action_name} is not safe to use! The reason - {self.reason}"
