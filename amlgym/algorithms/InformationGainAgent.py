import logging
import os
import random
import tempfile
from dataclasses import dataclass
from typing import Tuple

import numpy as np
from unified_planning.exceptions import UPInvalidActionError
from unified_planning.io import PDDLWriter
from unified_planning.plans import ActionInstance
from unified_planning.shortcuts import SequentialSimulator

from amlgym.algorithms.OnlineAlgorithmAdapter import OnlineAlgorithmAdapter
from amlgym.modeling.trajectory import Trajectory

from information_gain_aml.algorithms import InformationGainLearner
from information_gain_aml.core import UPAdapter
logger = logging.getLogger(__name__)


@dataclass
class InformationGainAgent(OnlineAlgorithmAdapter):
    """
    Online action model learning via information gain.

    Uses CNF/SAT-based information-theoretic approach to select actions
    that maximize expected information gain about the action model.

    Args:
        max_steps (int): Maximum number of learning steps
        use_object_subset (bool): Enable object subset selection for reduced grounding
        spare_objects_per_type (int): Extra objects per type beyond minimum requirement
            (for subset selection)
        model_mode (str): "safe" (all possible preconditions, confirmed effects only)
            or "complete" (certain preconditions only, all possible effects)
        learn_negative_preconditions (bool): Whether to learn negative preconditions
        selection_strategy (str): Action selection strategy. One of:
            - "greedy" — always select highest information gain (default)
            - "epsilon_greedy" — explore with probability epsilon
            - "boltzmann" — softmax probabilistic selection
            - "lookahead" — depth-limited lookahead with discounted future gain
            - "mcts" — full UCT-based Monte Carlo Tree Search
        lookahead_depth (int): Lookahead depth for 'lookahead' strategy (default: 2)
        lookahead_top_k (int): Number of top actions to evaluate in lookahead (default: 5)
        lookahead_discount (float): Discount factor for future gain in lookahead (default: 0.9)
        mcts_iterations (int): Number of MCTS iterations per action selection (default: 50)
        mcts_rollout_depth (int): Simulation depth during MCTS rollout phase (default: 5)

    Example:
        .. code-block:: python

            from unified_planning.io import PDDLReader
            from unified_planning.shortcuts import SequentialSimulator
            from amlgym.algorithms import get_algorithm
            from amlgym.benchmarks import get_domain_path, get_problems_path
            from amlgym.util.util import empty_domain

            domain = 'blocksworld'
            domain_ref_path = get_domain_path(domain)
            input_domain_path = empty_domain(domain_ref_path)
            problem_path = get_problems_path(domain, kind='learning')[0]
            problem = PDDLReader().parse_problem(domain_ref_path, problem_path)

            env = SequentialSimulator(problem=problem)
            info_gain = get_algorithm('InformationGainAgent', max_steps=100)
            model, trajectory = info_gain.learn(env, input_domain_path)

            # With lookahead strategy
            info_gain = get_algorithm(
                'InformationGainAgent',
                max_steps=100,
                selection_strategy='lookahead',
                lookahead_depth=3,
            )
            model, trajectory = info_gain.learn(env, input_domain_path)

            print("##################### Learned model #####################")
            print(model)

            print("################# Generated trajectory ##################")
            print(trajectory)

    """

    max_steps: int = 500
    use_object_subset: bool = True
    spare_objects_per_type: int = 2
    model_mode: str = "safe"
    learn_negative_preconditions: bool = True
    selection_strategy: str = "greedy"
    lookahead_depth: int = 2
    lookahead_top_k: int = 5
    lookahead_discount: float = 0.9
    mcts_iterations: int = 50
    mcts_rollout_depth: int = 5

    def learn(self,
              simulator: SequentialSimulator,
              input_domain_path: str,
              seed: int = 123) -> Tuple[str, Trajectory]:
        """
        Learn a PDDL action model by interacting with the environment.

        :parameter simulator: environment simulator
        :parameter input_domain_path: input PDDL domain file path
        :parameter seed: random seed for reproducibility
        :return: (learned PDDL model string, trajectory)
        """
        random.seed(seed)
        np.random.seed(seed)

        problem = simulator._problem

        # Write problem to temp file for our learner's init
        tmp_problem = tempfile.NamedTemporaryFile(
            mode='w', suffix='.pddl', delete=False
        )
        tmp_problem_path = tmp_problem.name
        tmp_problem.close()
        PDDLWriter(problem).write_problem(tmp_problem_path)

        try:
            # Initialize our learner
            learner = InformationGainLearner(
                domain_file=input_domain_path,
                problem_file=tmp_problem_path,
                max_iterations=self.max_steps,
                use_object_subset=self.use_object_subset,
                spare_objects_per_type=self.spare_objects_per_type,
                learn_negative_preconditions=self.learn_negative_preconditions,
                seed=seed,
                selection_strategy=self.selection_strategy,
                lookahead_depth=self.lookahead_depth,
                lookahead_top_k=self.lookahead_top_k,
                lookahead_discount=self.lookahead_discount,
                mcts_iterations=self.mcts_iterations,
                mcts_rollout_depth=self.mcts_rollout_depth,
            )

            # Get initial state
            up_state = simulator.get_initial_state()

            trace_states = [up_state]
            trace_actions = []

            for _ in range(self.max_steps):
                # Convert UP state to fluent set for our algorithm
                state_set = UPAdapter.up_state_to_fluent_set(up_state, problem)

                # Select action
                action_name, objects = learner.select_action(state_set)

                if action_name == "no_action":
                    logger.info("Algorithm converged (no information gain)")
                    break

                # Create ActionInstance for simulator
                up_action = problem.action(action_name)
                up_objects = tuple(problem.object(o) for o in objects)
                action_instance = ActionInstance(up_action, up_objects)

                # Execute via simulator
                try:
                    next_up_state = simulator.apply(up_state, action_instance)
                except UPInvalidActionError:
                    next_up_state = None
                success = next_up_state is not None

                # Record trajectory
                trace_actions.append(action_instance)
                trace_states.append(next_up_state)

                # Observe result for learning
                if success:
                    next_state_set = UPAdapter.up_state_to_fluent_set(
                        next_up_state, problem
                    )
                    learner.observe(
                        state_set, action_name, objects, True, next_state_set
                    )
                    up_state = next_up_state
                else:
                    learner.observe(
                        state_set, action_name, objects, False, None
                    )

            # Generate PDDL model
            model_str = learner.to_pddl_string(mode=self.model_mode)
            trajectory = Trajectory(trace_states, trace_actions)

        finally:
            os.remove(tmp_problem_path)

        return model_str, trajectory
