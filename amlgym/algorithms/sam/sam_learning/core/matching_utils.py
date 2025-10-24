"""Auxiliary functions to help the matching process."""
from itertools import permutations
from typing import List, Tuple, Set

from pddl_plus_parser.models import GroundedPredicate


def create_signature_permutations(call_parameters: List[str], lifted_signature: List[str], subset_size: int) -> List[Tuple[Tuple[str]]]:
    """Choose r items our of a list size n.

    :param call_parameters: the parameters in which the action was called with.
    :param lifted_signature: the action's lifted signature definition including possible constants.
    :param subset_size: the size of the subset.
    :return: a list containing matches of grounded objects and their lifted action parameter name counterparts.
    """
    matching_signatures = zip(call_parameters, list(lifted_signature))
    matching_permutations = list(permutations(matching_signatures, subset_size))
    return matching_permutations


def contains_duplicates(parameter_objects: List[str]) -> bool:
    """Validate that the predicate has only one possible match in the literal.

    :param parameter_objects: the of objects to test if contains duplicates.
    :return: whether there are duplicates.
    """
    return len(set(parameter_objects)) != len(parameter_objects)


def extract_discrete_effects(
    previous_state: Set[GroundedPredicate], next_state: Set[GroundedPredicate]
) -> Tuple[Set[GroundedPredicate], Set[GroundedPredicate]]:
    """Extracts discrete the effects from the state object.

    :param previous_state: the previous state object containing the grounded literals.
    :param next_state: the next state object containing its grounded literals.
    :return: tuple containing the add and delete effects of the action.
    """
    add_effects = set([predicate.copy() for predicate in next_state.difference(previous_state) if predicate.is_positive])
    delete_effects = set([predicate.copy(is_negated=True) for predicate in previous_state.difference(next_state) if predicate.is_positive])
    return add_effects, delete_effects


def extract_not_effects(next_state_predicate: Set[GroundedPredicate]) -> Set[GroundedPredicate]:
    """Extracts all negations of grounded predicates that were in post state

    :param next_state_predicate: all the grounded literals in the next state (negative and positive predicates).
    :return: A tuple representing the predicates that cannot be add-effects and those that cannot be delete-effects.
    """
    return {predicate.copy(is_negated=predicate.is_positive) for predicate in next_state_predicate}
