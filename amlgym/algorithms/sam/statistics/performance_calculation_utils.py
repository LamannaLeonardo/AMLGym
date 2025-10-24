"""Utilities for the performance calculation process."""

from typing import Dict

from pddl_plus_parser.models import Domain, Operator, ActionCall, State, PDDLObject


def _ground_executed_action(action_call: ActionCall, learned_domain: Domain, problem_objects: Dict[str, PDDLObject]) -> Operator:
    """Ground the tested action based on the trajectory data.

    :param action_call: the grounded action call in the observation component.
    :param learned_domain: the domain that was learned using the action model learning algorithm.
    :param problem_objects: the objects that were used in the problem definition.
    :return: the grounded operator.
    """
    grounded_operator = Operator(
        action=learned_domain.actions[action_call.name],
        domain=learned_domain,
        grounded_action_call=action_call.parameters,
        problem_objects=problem_objects,
    )
    grounded_operator.ground()
    return grounded_operator


def _calculate_single_action_applicability_rate(
    action_call: ActionCall,
    learned_domain: Domain,
    complete_domain: Domain,
    num_false_negatives: Dict[str, int],
    num_false_positives: Dict[str, int],
    num_true_positives: Dict[str, int],
    observed_state: State,
    problem_objects: Dict[str, PDDLObject],
):
    """Calculates the applicability rate for a single action.

    :param action_call: the grounded action that is currently being tested.
    :param learned_domain: the domain that was learned using the action model learning algorithm.
    :param complete_domain: the complete domain that was used to generate the trajectory data.
    :param num_false_negatives: the number of false negatives for each action.
    :param num_false_positives: the number of false positives for each action.
    :param num_true_positives: the number of true positives for each action.
    :param observed_state: the state that was observed in the trajectory data.
    :param problem_objects: the objects that were used in the problem definition.
    """
    learned_grounded_action = _ground_executed_action(action_call, learned_domain, problem_objects)
    model_grounded_action = _ground_executed_action(action_call, complete_domain, problem_objects)
    is_applicable_in_test = learned_grounded_action.is_applicable(observed_state)
    is_applicable_in_model = model_grounded_action.is_applicable(observed_state)
    num_true_positives[action_call.name] += int(is_applicable_in_test == is_applicable_in_model and is_applicable_in_test)
    num_false_positives[action_call.name] += int(is_applicable_in_test and not is_applicable_in_model)
    num_false_negatives[action_call.name] += int(not is_applicable_in_test and is_applicable_in_model)
