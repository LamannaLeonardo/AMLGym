"""The Safe Action Model Learning algorithm module."""

import logging
import time
from collections import defaultdict
from itertools import combinations
from typing import List, Tuple, Dict, Set

from pddl_plus_parser.models import (
    Observation,
    Predicate,
    ActionCall,
    State,
    Domain,
    ObservedComponent,
    PDDLObject,
    Action,
)

from sam_learning.core import (
    PredicatesMatcher,
    extract_discrete_effects,
    LearnerDomain,
    contains_duplicates,
    VocabularyCreator,
    EnvironmentSnapshot,
)
from utilities import NegativePreconditionPolicy


class SAMLearner:
    """Class that represents the safe action model learner algorithm.

    Notice: This class does not support domains with constants or with the same object mapped to multiple parameters.
    """

    logger: logging.Logger
    partial_domain: Domain
    matcher: PredicatesMatcher
    observed_actions: List[str]
    safe_actions: List[str]
    triplet_snapshot: EnvironmentSnapshot
    current_trajectory_objects: Dict[str, PDDLObject]
    learning_start_time: float
    learning_end_time: float
    vocabulary_creator: VocabularyCreator
    cannot_be_effect: Dict[str, Set[Predicate]]
    negative_preconditions_policy: NegativePreconditionPolicy

    def __init__(
        self,
        partial_domain: Domain,
        negative_preconditions_policy: NegativePreconditionPolicy = NegativePreconditionPolicy.no_remove,
        should_enforce_injective_binding: bool = False,
    ):

        self.logger = logging.getLogger(__name__)
        self.partial_domain = partial_domain
        self.matcher = PredicatesMatcher(partial_domain)
        self.vocabulary_creator = VocabularyCreator()
        self.triplet_snapshot = EnvironmentSnapshot(partial_domain=partial_domain)
        self.observed_actions = []
        self.safe_actions = []
        self.current_trajectory_objects = {}
        self.learning_start_time = 0
        self.learning_end_time = 0
        self.cannot_be_effect = {action: set() for action in self.partial_domain.actions}
        self._action_signatures = {action_name: action.signature for action_name, action in partial_domain.actions.items()}
        self.negative_preconditions_policy = negative_preconditions_policy
        self.should_enforce_injective_binding = should_enforce_injective_binding

    def _handle_unobserved_actions(self):
        """Removes the actions that were not observed from the partial domain."""
        self.logger.debug("Removing unobserved actions from the partial domain")
        unobserved_actions = [action for action in self.partial_domain.actions if action not in self.observed_actions]
        for action in unobserved_actions:
            preconditions_superset = self.vocabulary_creator.create_lifted_vocabulary(
                self.partial_domain, self.partial_domain.actions[action].signature
            )
            for precondition in preconditions_superset:
                self.partial_domain.actions[action].preconditions.add_condition(precondition)

    def _handle_consts_in_effects(self, grounded_action: ActionCall) -> None:
        """The function filters out literals that cannot be effects because they are not observed in the next state.

        :param grounded_action: the grounded action that was executed according to the trajectory.
        """
        action_predicate_vocabulary = self.vocabulary_creator.create_lifted_vocabulary(
            self.partial_domain, self.partial_domain.actions[grounded_action.name].signature
        )
        lifted_next_state_predicates = self.matcher.get_possible_literal_matches(
            grounded_action, list(self.triplet_snapshot.next_state_predicates)
        )
        lifted_next_state_predicates_str = {predicate.untyped_representation for predicate in lifted_next_state_predicates}
        for predicate in action_predicate_vocabulary:
            if predicate.untyped_representation not in lifted_next_state_predicates_str:
                self.cannot_be_effect[grounded_action.name].add(predicate)

        for predicate in self.cannot_be_effect[grounded_action.name]:
            self.partial_domain.actions[grounded_action.name].discrete_effects.discard(predicate)

    def _handle_action_effects(self, grounded_action: ActionCall) -> Tuple[List[Predicate], List[Predicate]]:
        """Finds the effects generated from the previous and the next state on this current step.

        :param grounded_action: the grounded action that was executed according to the trajectory.
        :return: the effect containing the add and del list of predicates.
        """
        self.logger.debug(f"Starting to learn the effects of {str(grounded_action)}.")
        grounded_add_effects, grounded_del_effects = extract_discrete_effects(
            self.triplet_snapshot.previous_state_predicates, self.triplet_snapshot.next_state_predicates
        )
        self.logger.debug("Updating the negative state predicates based on the action's execution.")
        lifted_add_effects = self.matcher.get_possible_literal_matches(grounded_action, list(grounded_add_effects))
        lifted_delete_effects = self.matcher.get_possible_literal_matches(grounded_action, list(grounded_del_effects))
        return lifted_add_effects, lifted_delete_effects

    def _update_action_preconditions(self, grounded_action: ActionCall) -> None:
        """Updates the preconditions of an action after it was observed at least once.

        :param grounded_action: the grounded action that is being executed in the trajectory component.
        """
        current_action = self.partial_domain.actions[grounded_action.name]
        previous_state_predicates = set(
            self.matcher.get_possible_literal_matches(grounded_action, list(self.triplet_snapshot.previous_state_predicates))
        )

        conditions_to_remove = []
        for current_precondition in current_action.preconditions.root.operands:
            # assuming that the predicates in the preconditions are NOT nested.
            if isinstance(current_precondition, Predicate) and current_precondition not in previous_state_predicates:
                conditions_to_remove.append(current_precondition)

        for condition in conditions_to_remove:
            current_action.preconditions.remove_condition(condition)

    def _add_new_action_preconditions(self, grounded_action: ActionCall) -> None:
        """General method to add new action's discrete preconditions.

        :param grounded_action: the action that is currently being executed.
        """
        self.logger.debug(f"Adding the preconditions of {grounded_action.name} to the action model.")
        current_action = self.partial_domain.actions[grounded_action.name]
        previous_state_predicates = set(
            self.matcher.get_possible_literal_matches(grounded_action, list(self.triplet_snapshot.previous_state_predicates))
        )

        for predicate in previous_state_predicates:
            current_action.preconditions.add_condition(predicate)

    def _construct_learning_report(self) -> Dict[str, str]:
        """Constructs the learning report of the learned actions.

        :return: the learning report.
        """
        observed_unsafe_actions = set(self.observed_actions).difference(self.safe_actions)
        unobserved_actions = set(self.partial_domain.actions.keys()).difference(self.observed_actions)

        learning_report = {action_name: "OK" for action_name in self.safe_actions}
        learning_report.update(
            {action_name: "NOT SAFE" for action_name in self.partial_domain.actions if action_name in observed_unsafe_actions}
        )
        learning_report.update({action_name: "UNOBSERVED" for action_name in unobserved_actions})
        learning_report["learning_time"] = str(self.learning_end_time - self.learning_start_time)
        return learning_report

    def add_new_action(self, grounded_action: ActionCall, previous_state: State, next_state: State) -> None:
        """Create a new action in the domain.

        :param grounded_action: the grounded action that was executed according to the trajectory.
        :param previous_state: the state that the action was executed on.
        :param next_state: the state that was created after executing the action on the previous
        """

        self.logger.info(f"Adding the action {str(grounded_action)} to the domain.")
        # adding the preconditions each predicate is grounded in this stage.
        observed_action = self.partial_domain.actions[grounded_action.name]
        self._add_new_action_preconditions(grounded_action)
        lifted_add_effects, lifted_delete_effects = self._handle_action_effects(grounded_action)

        observed_action.discrete_effects.update(set(lifted_add_effects).union(lifted_delete_effects))
        self.observed_actions.append(observed_action.name)
        self.logger.debug(f"Finished adding the action {grounded_action.name}.")

    def update_action(self, grounded_action: ActionCall, previous_state: State, next_state: State) -> None:
        """Create a new action in the domain.

        :param grounded_action: the grounded action that was executed according to the trajectory.
        :param previous_state: the state that the action was executed on.
        :param next_state: the state that was created after executing the action on the previous
            state.
        """
        action_name = grounded_action.name
        observed_action = self.partial_domain.actions[action_name]
        self._update_action_preconditions(grounded_action)
        lifted_add_effects, lifted_delete_effects = self._handle_action_effects(grounded_action)

        observed_action.discrete_effects.update(set(lifted_add_effects).union(lifted_delete_effects))
        if len(self.partial_domain.constants) > 0:
            self._handle_consts_in_effects(grounded_action)

        self.logger.debug(f"Done updating the action - {grounded_action.name}")

    def _verify_parameter_duplication(self, grounded_action: ActionCall) -> bool:
        """Verifies if the action was called with duplicated objects in a trajectory component.

        :param grounded_action: the grounded action observed in the trajectory triplet.
        :return: whether the action contains duplicated parameters.
        """
        has_duplicates = contains_duplicates(grounded_action.parameters)
        if has_duplicates:
            action = self.partial_domain.actions[grounded_action.name]
            grounded_signature_map = defaultdict(list)
            for grounded_param, lifted_param in zip(grounded_action.parameters, action.parameter_names):
                grounded_signature_map[grounded_param].append(lifted_param)

            for lifted_duplicates_list in grounded_signature_map.values():
                for obj1, obj2 in combinations(lifted_duplicates_list, 2):
                    action.preconditions.root.inequality_preconditions.discard((obj1, obj2))

        return has_duplicates

    def _complete_possibly_missing_actions(self):
        """Completes the actions that were not observed in the trajectory.

        Note:
            This allows SAM to be used multiple times on different trajectories.
            In case some actions were deleted in previous iterations they will be added back.
        """
        for action_name, action_signature in self._action_signatures.items():
            if action_name not in self.partial_domain.actions:
                action = Action()
                action.name = action_name
                action.signature = action_signature
                self.partial_domain.actions[action_name] = action

    def handle_single_trajectory_component(self, component: ObservedComponent) -> None:
        """Handles a single trajectory component as a part of the learning process.

        :param component: the trajectory component that is being handled at the moment.
        """
        previous_state = component.previous_state
        grounded_action = component.grounded_action_call
        next_state = component.next_state

        if self._verify_parameter_duplication(grounded_action):
            self.logger.warning(
                f"{str(grounded_action)} contains duplicated parameters! Not supported in SAM." f"aborting learning from component"
            )
            return

        self.triplet_snapshot.create_triplet_snapshot(
            previous_state=previous_state,
            next_state=next_state,
            current_action=grounded_action,
            observation_objects=self.current_trajectory_objects,
        )
        if grounded_action.name not in self.observed_actions:
            self.add_new_action(grounded_action, previous_state, next_state)

        else:
            self.update_action(grounded_action, previous_state, next_state)

    def deduce_initial_inequality_preconditions(self) -> None:
        """Tries to deduce which objects in the actions' signature cannot be equal."""
        if not self.should_enforce_injective_binding:
            return

        self.logger.debug("Starting to deduce inequality preconditions")
        for action_name, action_data in self.partial_domain.actions.items():
            for lifted_param1, lifted_param2 in combinations(action_data.parameter_names, 2):
                if action_data.signature[lifted_param1] == action_data.signature[lifted_param2]:
                    action_data.preconditions.root.inequality_preconditions.add((lifted_param1, lifted_param2))

    def remove_negative_preconditions(self):
        """Removes all negative preconditions"""
        for action in self.partial_domain.actions.values():
            new_preconditions = set()

            for precondition in action.preconditions.root.operands:
                if isinstance(precondition, Predicate) and not precondition.is_positive:
                    action_add_effects = [effect.untyped_representation for effect in action.discrete_effects if effect.is_positive]
                    copy_precondition_positive = precondition.copy(is_negated=True)
                    if (
                        not self.negative_preconditions_policy == NegativePreconditionPolicy.soft
                    ) or copy_precondition_positive.untyped_representation in action_add_effects:
                        continue

                new_preconditions.add(precondition)

            action.preconditions.root.operands = new_preconditions

    def handle_negative_preconditions_policy(self):
        if not self.negative_preconditions_policy == NegativePreconditionPolicy.no_remove:
            self.remove_negative_preconditions()

    def construct_safe_actions(self) -> None:
        """Constructs the single-agent actions that are safe to execute."""
        pass

    def start_measure_learning_time(self) -> None:
        """Starts measuring the learning time."""
        self.logger.info("Starting to measure the time it takes to learn the action model!")
        self.learning_start_time = time.time()

    def end_measure_learning_time(self) -> None:
        """Ends measuring the learning time."""
        self.learning_end_time = time.time()
        self.logger.info(f"Finished learning the action model in " f"{self.learning_end_time - self.learning_start_time} seconds.")

    def learn_action_model(self, observations: List[Observation]) -> Tuple[LearnerDomain, Dict[str, str]]:
        """Learn the SAFE action model from the input trajectories.

        :param observations: the list of trajectories that are used to learn the safe action model.
        :return: a domain containing the actions that were learned.
        """
        self.logger.info("Starting to learn the action model!")
        self.start_measure_learning_time()
        self.deduce_initial_inequality_preconditions()
        self._complete_possibly_missing_actions()
        for observation in observations:
            self.current_trajectory_objects = observation.grounded_objects
            for component in observation.components:
                if not component.is_successful:
                    self.logger.warning("Skipping the transition because it was not successful.")
                    continue

                self.handle_single_trajectory_component(component)

        self.construct_safe_actions()
        self._handle_unobserved_actions()
        self.handle_negative_preconditions_policy()
        self.end_measure_learning_time()
        learning_report = self._construct_learning_report()
        return self.partial_domain, learning_report
