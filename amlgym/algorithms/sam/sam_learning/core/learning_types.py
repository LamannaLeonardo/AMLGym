"""Module to store types related to the learning output."""
from enum import Enum


class ConditionType(Enum):
    conjunctive = 1
    disjunctive = 2


class EquationSolutionType(Enum):
    """The solution types possible as output to the learning algorithm."""
    no_solution_found = 1
    not_enough_data = 2
    convex_hull_not_found = 3
    ok = 4
