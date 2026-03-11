import logging
import os
import random
import tempfile
from dataclasses import dataclass
from typing import Tuple

import numpy as np
from unified_planning.io import PDDLWriter
from unified_planning.plans import ActionInstance
from unified_planning.shortcuts import SequentialSimulator

from amlgym.algorithms.OnlineAlgorithmAdapter import OnlineAlgorithmAdapter
from amlgym.modeling.trajectory import Trajectory

from src.algorithms.information_gain import InformationGainLearner
from src.core.up_adapter import UPAdapter

logger = logging.getLogger(__name__)


@dataclass
class InformationGainAgent(OnlineAlgorithmAdapter):
    """
    Online action model learning via information gain.

    Uses CNF/SAT-based information-theoretic approach to select actions
    that maximize expected information gain about the action model.

    Parameters:
        max_steps: Maximum number of learning steps
        use_object_subset: Enable object subset selection for reduced grounding
        model_mode: "safe" (all possible preconditions, confirmed effects only)
                    or "complete" (certain preconditions only, all possible effects)
    """

    max_steps: int = 500
    use_object_subset: bool = True
    model_mode: str = "safe"

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
                seed=seed,
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
                next_up_state = simulator.apply(up_state, action_instance)
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
