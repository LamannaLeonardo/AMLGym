"""Extension to SAM Learning that can learn numeric state variables."""

from typing import List, Dict, Tuple, Optional

from pddl_plus_parser.models import Observation, ActionCall, State, Domain, Precondition, NumericalExpressionTree

from sam_learning.core import (
    LearnerDomain,
    NumericFluentStateStorage,
    NumericFunctionMatcher,
    NotSafeActionError,
    LearnerAction,
)
from sam_learning.core.learner_domain import DISJUNCTIVE_PRECONDITIONS_REQ
from sam_learning.learners.sam_learning import SAMLearner
from utilities import NegativePreconditionPolicy


class NumericSAMLearner(SAMLearner):
    """The Extension of SAM that is able to learn numeric state variables."""

    storage: Dict[str, NumericFluentStateStorage]
    function_matcher: NumericFunctionMatcher
    relevant_fluents: Dict[str, List[str]]

    def __init__(
        self,
        partial_domain: Domain,
        relevant_fluents: Optional[Dict[str, List[str]]] = None,
        allow_unsafe: bool = False,
        polynomial_degree: int = 0,
        negative_preconditions_policy: NegativePreconditionPolicy = NegativePreconditionPolicy.no_remove,
        epsilon: float = 0.0,
        qhull_options: str = "",
        **kwargs,
    ):
        super().__init__(partial_domain, negative_preconditions_policy=negative_preconditions_policy)
        self.storage = {}
        self.function_matcher = NumericFunctionMatcher(partial_domain)
        self.relevant_fluents = relevant_fluents
        self._allow_unsafe = allow_unsafe
        self.polynom_degree = polynomial_degree
        self._epsilon = epsilon
        self._qhull_options = qhull_options

    def _remove_deprecated_numeric_preconditions(self, action: LearnerAction) -> None:
        """Removes the deprecated numeric preconditions from the input action (used when the learning process is iterative).

        :param action: the action that the preconditions are removed from.
        """
        self.logger.debug(f"Removing the deprecated numeric preconditions from the action - {action.name}.")
        non_numeric_preconditions = Precondition("and")
        for condition in action.preconditions.root.operands:
            if not isinstance(condition, NumericalExpressionTree):
                non_numeric_preconditions.add_condition(condition)

        action.preconditions.root = non_numeric_preconditions

    def _construct_safe_numeric_preconditions(self, action: LearnerAction) -> None:
        """Constructs the safe preconditions for the input action.

        :param action: the action that the preconditions are constructed for.
        """
        action_name = action.name
        self._remove_deprecated_numeric_preconditions(action)
        if self.relevant_fluents is None:
            learned_numeric_preconditions = self.storage[action_name].construct_safe_linear_inequalities()

        elif len(self.relevant_fluents[action_name]) == 0:
            self.logger.debug(f"The action {action_name} has no numeric preconditions.")
            return

        else:
            learned_numeric_preconditions = self.storage[action_name].construct_safe_linear_inequalities(self.relevant_fluents[action_name])

        if learned_numeric_preconditions.binary_operator == "and":
            self.logger.debug("The learned preconditions are a conjunction. Adding the internal numeric conditions.")
            for condition in learned_numeric_preconditions.operands:
                action.preconditions.add_condition(condition)

            return

        self.logger.debug("The learned preconditions are not a conjunction. Adding them as a separate condition.")
        action.preconditions.add_condition(learned_numeric_preconditions)
        self.partial_domain.requirements.append(DISJUNCTIVE_PRECONDITIONS_REQ)

    def _construct_safe_numeric_effects(self, action: LearnerAction) -> bool:
        """Constructs the safe numeric effects for the input action.

        :param action: the action that its effects are constructed for.
        :return: whether the effects were learned perfectly.
        """
        if self.relevant_fluents is not None and len(self.relevant_fluents[action.name]) == 0:
            self.logger.debug(f"The action - {action.name} has no numeric effects.")
            action.numeric_effects = set()
            return True

        effects, numeric_preconditions, learned_perfectly = self.storage[action.name].construct_assignment_equations(
            allow_unsafe=self._allow_unsafe, relevant_fluents=self.relevant_fluents[action.name] if self.relevant_fluents is not None else None
        )
        if effects is not None and len(effects) > 0:
            action.numeric_effects = effects

        else:
            self.logger.debug(f"The action - {action.name} has no numeric effects.")
            action.numeric_effects = set()

        self.logger.debug(f"No feature selection applied, using the numeric preconditions as is.")
        return learned_perfectly

    def add_new_action(self, grounded_action: ActionCall, previous_state: State, next_state: State, incremental: bool = False) -> None:
        """Adds a new action to the learned domain.

        :param grounded_action: the grounded action that was executed according to the observation.
        :param previous_state: the state that the action was executed on.
        :param next_state: the state that was created after executing the action on the previous state.
        :param incremental: whether the learning process is incremental or not.
        """
        super().add_new_action(grounded_action, previous_state, next_state)
        self.logger.debug(f"Creating the new storage for the action - {grounded_action.name}.")
        previous_state_lifted_matches = self.function_matcher.match_state_functions(grounded_action, self.triplet_snapshot.previous_state_functions)
        next_state_lifted_matches = self.function_matcher.match_state_functions(grounded_action, self.triplet_snapshot.next_state_functions)
        possible_bounded_functions = self.vocabulary_creator.create_lifted_functions_vocabulary(
            domain=self.partial_domain, possible_parameters=self.partial_domain.actions[grounded_action.name].signature
        )
        self.storage[grounded_action.name] = NumericFluentStateStorage(
            action_name=grounded_action.name,
            domain_functions=possible_bounded_functions,
            polynom_degree=self.polynom_degree,
            epsilon=self._epsilon,
            qhull_options=self._qhull_options,
            incremental=incremental,
        )
        self.storage[grounded_action.name].add_to_previous_state_storage(previous_state_lifted_matches)
        self.storage[grounded_action.name].add_to_next_state_storage(next_state_lifted_matches)
        self.logger.debug(f"Done creating the numeric state variable storage for the action - {grounded_action.name}")

    def update_action(self, grounded_action: ActionCall, previous_state: State, next_state: State) -> None:
        """Updates the action's data according to the new input observed triplet.

        :param grounded_action: the grounded action that was observed.
        :param previous_state: the state that the action was executed on.
        :param next_state: the state that was created after executing the action on the previous
            state.
        """
        action_name = grounded_action.name
        super().update_action(grounded_action, previous_state, next_state)
        self.logger.debug(f"Adding the numeric state variables to the numeric storage of action - {action_name}.")
        previous_state_lifted_matches = self.function_matcher.match_state_functions(grounded_action, self.triplet_snapshot.previous_state_functions)
        next_state_lifted_matches = self.function_matcher.match_state_functions(grounded_action, self.triplet_snapshot.next_state_functions)
        self.storage[action_name].add_to_previous_state_storage(previous_state_lifted_matches)
        self.storage[action_name].add_to_next_state_storage(next_state_lifted_matches)
        self.logger.debug(f"Done updating the numeric state variable storage for the action - {grounded_action.name}")

    def _create_safe_action(self, action_name: str) -> LearnerAction:
        """Creates a safe action that can be executed in the environment.

        :param action_name: the name of the action to create.
        :return: the safe action that can be executed in the environment.
        """
        action = self.partial_domain.actions[action_name]
        self._construct_safe_numeric_preconditions(action)
        self._construct_safe_numeric_effects(action)
        self.logger.info(f"Done learning the action - {action_name}!")
        return action

    def _create_safe_action_model(self) -> Tuple[Dict[str, LearnerAction], Dict[str, str]]:
        """Crates the safe action model learned by the algorithm.

        :return: the actions that are allowed to execute and the metadata about the learning.
        """
        allowed_actions = {}
        learning_metadata = {}
        for action_name, action in self.partial_domain.actions.items():
            if action_name not in self.storage:
                self.logger.debug(f"The action - {action_name} has not been observed in the trajectories!")
                continue

            try:
                safe_action = self._create_safe_action(action_name)
                allowed_actions[action_name] = safe_action
                learning_metadata[action_name] = "OK"

            except NotSafeActionError as e:
                self.logger.debug(f"The action - {e.action_name} is not safe for execution, reason - {e.reason}")
                action.preconditions = Precondition("and")
                action.discrete_effects = set()
                action.numeric_effects = set()
                learning_metadata[action_name] = e.solution_type.name

        self.partial_domain.actions = allowed_actions
        return allowed_actions, learning_metadata

    def learn_action_model(self, observations: List[Observation]) -> Tuple[LearnerDomain, Dict[str, str]]:
        """Learn the SAFE action model from the input observations.

        :param observations: the list of trajectories that are used to learn the safe action model.
        :return: a domain containing the actions that were learned and the metadata about the learning.
        """
        self.logger.info("Starting to learn the action model!")
        if len(self.partial_domain.functions) == 0:
            self.logger.info(f"The domain {self.partial_domain.name} does not have any numeric state variables.")
            return super().learn_action_model(observations)

        # The domain has numeric state variables.
        super().start_measure_learning_time()
        super().deduce_initial_inequality_preconditions()
        self._complete_possibly_missing_actions()
        for observation in observations:
            self.current_trajectory_objects = observation.grounded_objects
            for component in observation.components:
                if not component.is_successful:
                    self.logger.warning("Skipping the transition because it was not successful.")
                    continue

                self.handle_single_trajectory_component(component)

        self.handle_negative_preconditions_policy()
        allowed_actions, learning_metadata = self._create_safe_action_model()

        super().end_measure_learning_time()
        learning_metadata["learning_time"] = str(self.learning_end_time - self.learning_start_time)
        return self.partial_domain, learning_metadata
