"""Matches predicates to their corresponding actions based on the common types."""
import logging
from typing import List, Tuple, Optional

from pddl_plus_parser.models import Domain, Predicate, GroundedPredicate, ActionCall, PDDLObject

from sam_learning.core.matching_utils import contains_duplicates, create_signature_permutations


class PredicatesMatcher:
    """Class that matches predicates according to the needed properties in the learning process."""

    matcher_domain: Domain
    logger: logging.Logger

    def __init__(self, domain: Domain):
        self.logger = logging.getLogger(__name__)
        self.matcher_domain = domain

    @staticmethod
    def _extract_combinations_data(possible_combinations: Tuple[Tuple[str]]) -> Tuple[List[str], List[str]]:
        """extracts the data of the combinations so that the matcher would be able to use it.

        :param possible_combinations: the possible combinations of the parameters.
        :return: the extracted parameters and the objects.
        """
        call_objects = []
        lifted_params = []
        for obj, param in possible_combinations:
            call_objects.append(obj)
            lifted_params.append(param)

        return call_objects, lifted_params

    def _filter_out_impossible_combinations(
        self, grounded_predicate: GroundedPredicate, possible_matches: List[Predicate], possible_grounded_params: List[List[str]]
    ) -> List[Predicate]:
        """Filters out signature permutations that don't match the original predicate's order.

        :param grounded_predicate: the grounded predicate that is being matches.
        :param possible_matches: the possible matching permutations generated.
        :param possible_grounded_params: the list of objects that represent the lifted parameters.
            used to filter out wrong permutations.
        :return: the correct possible matches that fit the original parameters order.
        """
        self.logger.debug("Filtering out impossible matches from the matches list.")
        filtered_matches = []
        for match, grounded_matching_objects in zip(possible_matches, possible_grounded_params):
            is_possible_match = True
            if grounded_predicate.grounded_objects != grounded_matching_objects:
                continue

            for signature_item_type, grounded_predicate_signature_item_type in zip(match.signature.values(), grounded_predicate.signature.values()):
                if not grounded_predicate_signature_item_type.is_sub_type(signature_item_type):
                    is_possible_match = False
                    break

            if is_possible_match:
                filtered_matches.append(match)

        return filtered_matches

    def match_predicate_to_action_literals(
        self, grounded_predicate: GroundedPredicate, action_call: ActionCall, extra_grounded_object: str = None, extra_lifted_object: str = None
    ) -> List[Predicate]:
        """Matches the action objects to the predicate objects.

        :param grounded_predicate: the grounded predicate that was observed.
        :param action_call: the action that was called in the observation.
        :return: lifted predicates with signatures matching the action.
        :param extra_grounded_object: an additional object that is not part of the action call.
            Used in cases where we observe universal effects / preconditions.
        :param extra_lifted_object: the additional lifted object matching the grounded observed one.
        """
        self.logger.debug(
            f"Trying to match the grounded predicate - {grounded_predicate.untyped_representation} " f"to the action call {str(action_call)}"
        )
        if len(grounded_predicate.signature) == 0:
            self.logger.debug("The predicate has no parameters, by default matches the action!")
            return [Predicate(name=grounded_predicate.name, signature={}, is_positive=grounded_predicate.is_positive)]

        lifted_action_data = self.matcher_domain.actions[action_call.name]
        constants = self.matcher_domain.constants
        grounded_predicate_call = grounded_predicate.grounded_objects

        constants_in_predicate = [obj for obj in grounded_predicate_call if obj in constants]
        action_grounded_objects = (
            action_call.parameters + constants_in_predicate if extra_grounded_object is None else action_call.parameters + [extra_grounded_object]
        )
        lifted_action_params = (
            list(lifted_action_data.signature.keys()) + constants_in_predicate
            if extra_lifted_object is None
            else list(lifted_action_data.signature.keys()) + [extra_lifted_object]
        )

        if contains_duplicates(action_call.parameters):
            self.logger.debug(f"Action {str(action_call)} was executed with duplicated objects!")

        possible_parameter_permutations = create_signature_permutations(action_grounded_objects, lifted_action_params, len(grounded_predicate_call))
        possible_matches = []
        grounded_base_params = []
        for possible_permutation in possible_parameter_permutations:
            possible_match_action_objects, lifted_parameters = self._extract_combinations_data(possible_permutation)
            if set(possible_match_action_objects) == set(grounded_predicate_call):
                combined_types = {**lifted_action_data.signature}
                combined_types.update({name: constants[name].type for name in constants_in_predicate})
                if extra_lifted_object is not None:
                    self.logger.debug(f"Adding the extra lifted object {extra_lifted_object} to the signature.")
                    additional_lifted_parameter = [
                        key for key in grounded_predicate.object_mapping if grounded_predicate.object_mapping[key] == extra_grounded_object
                    ][0]
                    combined_types[extra_lifted_object] = grounded_predicate.signature[additional_lifted_parameter]

                possible_matches.append(
                    Predicate(
                        name=grounded_predicate.name,
                        signature={lifted_parameter_name: combined_types[lifted_parameter_name] for lifted_parameter_name in lifted_parameters},
                        is_positive=grounded_predicate.is_positive,
                    )
                )
                grounded_base_params.append(possible_match_action_objects)

        possible_matches = self._filter_out_impossible_combinations(grounded_predicate, possible_matches, grounded_base_params)
        return possible_matches

    def get_injective_match(self, grounded_predicate: GroundedPredicate, action_call: ActionCall) -> Optional[Predicate]:
        """Get the injective match for the predicate and the action.

        :param grounded_predicate: the grounded predicate that was observed.
        :param action_call: the action that was called in the observation.
        :return: lifted predicates with signatures matching the action.
        """
        possible_matches = self.match_predicate_to_action_literals(grounded_predicate, action_call)
        if len(possible_matches) == 1:
            lifted_match = possible_matches[0]
            lifted_match.is_positive = grounded_predicate.is_positive
            return lifted_match

        return None

    def get_possible_literal_matches(
        self,
        grounded_action_call: ActionCall,
        state_literals: List[GroundedPredicate],
        extra_grounded_object: str = None,
        extra_lifted_object: str = None,
    ) -> List[Predicate]:
        """Get a list of possible preconditions for the action according to the previous state.

        :param grounded_action_call: the grounded action that was executed according to the trajectory.
        :param state_literals: the list of literals that we try to match according to the action.
        :param extra_grounded_object: an additional object that is not part of the action call.
            Used in cases where we observe universal effects / preconditions.
        :param extra_lifted_object: the additional lifted object matching the grounded observed one.
        :return: a list of possible preconditions for the action that is being executed.
        """
        self.logger.debug(f"Finding the possible matches for the grounded action - {str(grounded_action_call)}")
        possible_matches = []
        for state_predicate in state_literals:
            if extra_grounded_object is None or extra_grounded_object not in state_predicate.grounded_objects:
                possible_matches.extend(self.match_predicate_to_action_literals(state_predicate, grounded_action_call))
                continue

            possible_matches.extend(
                self.match_predicate_to_action_literals(state_predicate, grounded_action_call, extra_grounded_object, extra_lifted_object)
            )

        return possible_matches
