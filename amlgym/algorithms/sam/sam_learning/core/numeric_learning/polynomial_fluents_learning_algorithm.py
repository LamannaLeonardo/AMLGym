"""Module that learns polynomial preconditions and effects from a domain."""
import itertools
from typing import Dict, List, Optional

import numpy
from pddl_plus_parser.models import PDDLFunction, Precondition

from sam_learning.core.numeric_learning.numeric_fluent_learner_algorithm import NumericFluentStateStorage


class PolynomialFluentsLearningAlgorithm(NumericFluentStateStorage):
    """Class that learns polynomial preconditions and effects from a domain.

    Note:
        If the polynom degree is 0 the algorithm reverts to its linear version.
        degree of 1 is the multiplication of each couple of state fluents.
        degree 2 and above is the maximal degree of the polynomial.
    """

    polynom_degree: int
    is_verbose: bool

    def __init__(
        self, action_name: str, polynom_degree: int, domain_functions: Dict[str, PDDLFunction], is_verbose: bool = False
    ):
        super().__init__(action_name, domain_functions)
        self.polynom_degree = polynom_degree
        self.is_verbose = is_verbose

    def _create_polynomial_string_recursive(self, fluents: List[str]) -> str:
        """Creates the polynomial string representing the equation recursively.

        :param fluents: the numeric fluents to create the polynomial string from.
        :return: the polynomial string representing the equation.
        """
        if len(fluents) == 1:
            return fluents[0]

        return f"(* {fluents[0]} {self._create_polynomial_string_recursive(fluents[1:])})"

    def create_polynomial_string(self, fluents: List[str]) -> str:
        """The auxiliary function that creates the polynomial string representing the equation.

        :param fluents: the numeric fluents to create the polynomial string from.
        :return: the polynomial string representing the equation.
        """
        return self._create_polynomial_string_recursive(fluents)

    def _add_polynom_to_storage(self, state_fluents: Dict[str, PDDLFunction], storage: Dict[str, List[float]]) -> None:
        """Adds the polynomial representation of the state fluents to the storage.

        :param state_fluents: the numeric fluents present in the input state.
        :param storage: the storage to update.
        """
        if self.polynom_degree == 1:
            for first_fluent, second_fluent in itertools.combinations(list(state_fluents.keys()), r=2):
                multiplied_fluent = self.create_polynomial_string([first_fluent, second_fluent])
                storage[multiplied_fluent].append(
                    state_fluents[first_fluent].value * state_fluents[second_fluent].value
                )
            return

        for degree in range(2, self.polynom_degree + 1):
            for fluent_combination in itertools.combinations_with_replacement(list(state_fluents.keys()), r=degree):
                polynomial_fluent = self.create_polynomial_string(list(fluent_combination))
                values = [state_fluents[fluent].value for fluent in fluent_combination]
                self.previous_state_storage[polynomial_fluent].append(numpy.prod(values))

    def add_to_previous_state_storage(self, state_fluents: Dict[str, PDDLFunction]) -> None:
        """Adds the matched lifted state fluents to the previous state storage.

        :param state_fluents: the lifted state fluents that were matched for the action.
        """
        super().add_to_previous_state_storage(state_fluents)
        if self.polynom_degree == 0:
            return

        self._add_polynom_to_storage(state_fluents, self.previous_state_storage)

    def add_to_next_state_storage(self, state_fluents: Dict[str, PDDLFunction]) -> None:
        """Adds the matched lifted state fluents to the next state storage.

        :param state_fluents: the lifted state fluents that were matched for the action.
        """
        super().add_to_next_state_storage(state_fluents)
        if self.polynom_degree == 0:
            return

        for fluent in self.next_state_storage:
            if len(self.previous_state_storage.get(fluent, [])) != len(self.next_state_storage[fluent]):
                self.logger.debug("This is a case where effects create new fluents - should adjust the previous state.")
                self.previous_state_storage[fluent].append(0)

    def construct_safe_linear_inequalities(self, relevant_fluents: Optional[List[str]] = None) -> Precondition:
        """Constructs the linear inequalities strings that will be used in the learned model later.

        :return: the inequality strings and the type of equations that were constructed (injunctive / disjunctive)
        """
        algorithm_relevant_fluents = relevant_fluents or list(self.previous_state_storage.keys())
        polynomial_relevant_fluents = [*algorithm_relevant_fluents]
        if self.polynom_degree == 0:
            return super().construct_safe_linear_inequalities(relevant_fluents)

        if self.is_verbose:
            self.logger.debug(f"Fluents are given as verbose - so only learning the fluents given as input!")
            return super().construct_safe_linear_inequalities(algorithm_relevant_fluents)

        if self.polynom_degree == 1:
            for first_fluent, second_fluent in itertools.combinations(relevant_fluents, r=2):
                polynomial_relevant_fluents.append(self.create_polynomial_string([first_fluent, second_fluent]))

            return super().construct_safe_linear_inequalities(polynomial_relevant_fluents)

        for degree in range(2, self.polynom_degree + 1):
            for fluent_combination in itertools.combinations_with_replacement(relevant_fluents, r=degree):
                polynomial_relevant_fluents.append(self.create_polynomial_string(list(fluent_combination)))

        return super().construct_safe_linear_inequalities(polynomial_relevant_fluents)
