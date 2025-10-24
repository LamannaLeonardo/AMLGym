"""Extension to SAM Learning that can learn numeric state variables."""

from typing import List, Dict, Optional

from pddl_plus_parser.models import ActionCall, State, Domain

from sam_learning.core import NumericFunctionMatcher
from sam_learning.core.numeric_learning import NumericFluentStateStorage
from sam_learning.learners.numeric_sam import NumericSAMLearner
from utilities import NegativePreconditionPolicy


class IncrementalNumericSAMLearner(NumericSAMLearner):
    """The Extension of SAM that is able to learn numeric state variables."""

    storage: Dict[str, NumericFluentStateStorage]
    function_matcher: NumericFunctionMatcher
    preconditions_fluent_map: Dict[str, List[str]]

    def __init__(
        self,
        partial_domain: Domain,
        polynomial_degree: int = 0,
        allow_unsafe: bool = False,
        negative_preconditions_policy: NegativePreconditionPolicy = NegativePreconditionPolicy.soft,
        epsilon: float = 0.0,
        qhull_options: str = "",
        relevant_fluents: Optional[Dict[str, List[str]]] = None,
    ):
        super().__init__(
            partial_domain,
            negative_preconditions_policy=negative_preconditions_policy,
            polynomial_degree=polynomial_degree,
            relevant_fluents=relevant_fluents,
            epsilon=epsilon,
            qhull_options=qhull_options,
            allow_unsafe=allow_unsafe,
        )

    def add_new_action(self, grounded_action: ActionCall, previous_state: State, next_state: State) -> None:
        """Adds a new action to the learned domain.

        :param grounded_action: the grounded action that was executed according to the observation.
        :param previous_state: the state that the action was executed on.
        :param next_state: the state that was created after executing the action on the previous
        """
        super().add_new_action(grounded_action, previous_state, next_state, incremental=True)
