import sys
sys.path.append("/Users/omarwattad/Documents/Action Model - Research/sam_learning")
from sam_learning.learners.numeric_sam import NumericSAMLearner
from sam_learning.learners.numeric_sam import *
from sam_learning.core import NumericFluentStateStorage
from typing import List, Dict, Tuple, Optional
sys.path.append("/Users/omarwattad/Documents/Action Model - Research/sam_learning/utilities")
from utilities import NegativePreconditionPolicy
from pddl_plus_parser.models import Observation, ActionCall, State, Domain, Precondition


class OnlyNumericSam(NumericSAMLearner):
    def __init__(
        self,
        partial_domain: Domain,
        relevant_fluents: Optional[Dict[str, List[str]]] = None,
        allow_unsafe: bool = False,
        polynomial_degree: int = 0,
        negative_preconditions_policy: NegativePreconditionPolicy = NegativePreconditionPolicy.no_remove,
        clean_data: bool = True,
        **kwargs,
    ):
        super().__init__(partial_domain, relevant_fluents, allow_unsafe, polynomial_degree, negative_preconditions_policy=negative_preconditions_policy)
        if not clean_data:
            self.learned_data = partial_domain
        else: self.learned_data = None

    def add_data_to_domain(self): # todo: CHECK IF NEEDED!
        if self.learned_data:
            for action_str , action in self.learned_data.actions.items():
                for condition in action.preconditions.root.operands:
                    self.partial_domain.actions[action_str].preconditions.add_condition(condition)
                self.partial_domain.actions[action_str].discrete_effects.update(action.discrete_effects)

    def add_new_action(self, grounded_action: ActionCall, previous_state: State, next_state: State) -> None:
        """Adds a new action to the learned domain.

        :param grounded_action: the grounded action that was executed according to the observation.
        :param previous_state: the state that the action was executed on.
        :param next_state: the state that was created after executing the action on the previous
        """
        # super().add_new_action(grounded_action, previous_state, next_state) # SAM Learner
        self.logger.debug(f"Creating the new storage for the action - {grounded_action.name}.")
        previous_state_lifted_matches = self.function_matcher.match_state_functions(grounded_action, self.triplet_snapshot.previous_state_functions)
        next_state_lifted_matches = self.function_matcher.match_state_functions(grounded_action, self.triplet_snapshot.next_state_functions)
        possible_bounded_functions = self.vocabulary_creator.create_lifted_functions_vocabulary(
            domain=self.partial_domain, possible_parameters=self.partial_domain.actions[grounded_action.name].signature
        )
        self.storage[grounded_action.name] = NumericFluentStateStorage(
            action_name=grounded_action.name, domain_functions=possible_bounded_functions, polynom_degree=self.polynom_degree,
        )
        observed_action = self.partial_domain.actions[grounded_action.name]
        self.observed_actions.append(observed_action.name)
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
        # super().update_action(grounded_action, previous_state, next_state) # SAM learner!
        self.logger.debug(f"Adding the numeric state variables to the numeric storage of action - {action_name}.")
        previous_state_lifted_matches = self.function_matcher.match_state_functions(grounded_action, self.triplet_snapshot.previous_state_functions)
        next_state_lifted_matches = self.function_matcher.match_state_functions(grounded_action, self.triplet_snapshot.next_state_functions)
        self.storage[action_name].add_to_previous_state_storage(previous_state_lifted_matches)
        self.storage[action_name].add_to_next_state_storage(next_state_lifted_matches)
        self.logger.debug(f"Done updating the numeric state variable storage for the action - {grounded_action.name}")

    def learn_action_model(self, observations: List[Observation]) -> Tuple[LearnerDomain, Dict[str, str]]:
        """Learn the SAFE action model from the input observations.

        :param observations: the list of trajectories that are used to learn the safe action model.
        :return: a domain containing the actions that were learned and the metadata about the learning.
        """
        self.logger.info("Starting to learn the action model!")
        super().start_measure_learning_time()
        super().deduce_initial_inequality_preconditions()
        self.add_data_to_domain()
        for observation in observations:
            self.current_trajectory_objects = observation.grounded_objects
            for component in observation.components:
                if not super().are_states_different(component.previous_state, component.next_state):
                    continue

                self.handle_single_trajectory_component(component)

        self.handle_negative_preconditions_policy()
        allowed_actions, learning_metadata = self._create_safe_action_model()

        super().end_measure_learning_time()
        learning_metadata["learning_time"] = str(self.learning_end_time - self.learning_start_time)
        return self.partial_domain, learning_metadata