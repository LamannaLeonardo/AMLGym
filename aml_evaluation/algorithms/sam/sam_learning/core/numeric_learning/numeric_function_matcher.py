"""Module to match action call parameters to the functions observed in the state."""
import itertools
import logging
from itertools import permutations
from typing import List, Dict, Union

from pddl_plus_parser.models import Domain, PDDLFunction, ActionCall, Action


class NumericFunctionMatcher:
    """Class that matched numeric functions to the actions according to their parameters."""

    matcher_domain: Domain
    logger: logging.Logger

    def __init__(self, domain: Domain):
        self.logger = logging.getLogger(__name__)
        self.matcher_domain = domain

    @staticmethod
    def create_possible_function_signatures(action_parameters: List[str], numeric_function: PDDLFunction) -> List[str]:
        """Create all possible grounded calls of the function.

        Note: Assuming the input function has less or the same number of parameters as the action.

        :param action_parameters: the parameters that the action was called with.
        :param numeric_function:the numeric function that is defined in the domain.
        :return: possible unsigned representations that will be used to map the correct state function.
        """
        num_function_params = len(numeric_function.signature)
        possible_parameters = permutations(action_parameters, num_function_params)
        possible_untyped_signatures = []
        for permutation in possible_parameters:
            untyped_signature_str = " ".join(permutation)
            possible_untyped_signatures.append(f"({numeric_function.name} {untyped_signature_str})")

        return possible_untyped_signatures

    def lift_matched_parameters(
        self, executed_action: Action, grounded_call_parameters: List[str], grounded_function: PDDLFunction
    ) -> List[PDDLFunction]:
        """Matches the parameters of the function to the lifted action definition.

        :param executed_action: the lifted action that was called in the observation.
        :param grounded_call_parameters: the observed action call objects.
        :param grounded_function: the observed numeric function.
        :return: the lifted function definition with the value set according to the observation.
        """
        self.logger.debug("Starting to lift the matched parameters!")
        object_to_parameter_mapping = [
            {grounded_obj: lifted_param}
            for grounded_obj, lifted_param in zip(grounded_call_parameters, executed_action.parameter_names)
        ]
        object_to_parameter_mapping.extend([{const: const} for const in self.matcher_domain.constants])
        lifted_params_and_consts = {
            **executed_action.signature,
            **{const_name: const.type for const_name, const in self.matcher_domain.constants.items()},
        }
        grounded_objects = list(grounded_function.signature.keys())
        map_permutations = list(itertools.product(object_to_parameter_mapping, repeat=len(grounded_objects)))
        lifted_matches = []
        for permutation in map_permutations:
            possible_grounded_execution = [list(item.keys())[0] for item in permutation]
            if possible_grounded_execution == grounded_objects:
                lifted_matched_signature = {}
                for item in permutation:
                    lifted_param_name = item[list(item.keys())[0]]
                    lifted_matched_signature[lifted_param_name] = lifted_params_and_consts[lifted_param_name]

                lifted_state_function = PDDLFunction(name=grounded_function.name, signature=lifted_matched_signature)
                lifted_state_function.set_value(grounded_function.value)
                lifted_matches.append(lifted_state_function)

        return lifted_matches

    def match_state_functions(
        self, action_call: ActionCall, grounded_state_fluents: Dict[str, PDDLFunction]
    ) -> Dict[str, PDDLFunction]:
        """Match the state functions to the action according to the grounded object names.

        :param action_call: the action that was called in the observation.
        :param grounded_state_fluents: the numeric state fluents.
        :return: a dictionary containing the lifted numeric state function with their assigned values.
        """
        self.logger.debug(f"Starting to search for matches for the grounded action - {str(action_call)}")
        possible_matches = {}
        for domain_function in self.matcher_domain.functions.values():
            if len(domain_function.signature) > len(action_call.parameters) and len(self.matcher_domain.constants) == 0:
                self.logger.debug(f"Function - {domain_function.name} has too many parameters, skipping.")
                continue

            if len(domain_function.signature) == 0:
                grounded_function = grounded_state_fluents[domain_function.untyped_representation]
                self.logger.debug(
                    f"Function {domain_function.name} has zero parameters. " f"Instantly considering as match."
                )
                matched_function = PDDLFunction(name=domain_function.name, signature={})
                matched_function.set_value(grounded_function.value)
                possible_matches[domain_function.untyped_representation] = matched_function
                continue

            call_parameters = action_call.parameters + list(self.matcher_domain.constants.keys())
            possible_function_signatures = self.create_possible_function_signatures(call_parameters, domain_function)
            for unsigned_representation in possible_function_signatures:
                if unsigned_representation in grounded_state_fluents:
                    self.logger.debug(
                        f"found a possible match to the action " f"{action_call.name} - {unsigned_representation}"
                    )

                    matched_lifted_functions = self.lift_matched_parameters(
                        executed_action=self.matcher_domain.actions[action_call.name],
                        grounded_call_parameters=action_call.parameters,
                        grounded_function=grounded_state_fluents[unsigned_representation],
                    )
                    for match in matched_lifted_functions:
                        possible_matches[match.untyped_representation] = match

        return possible_matches
