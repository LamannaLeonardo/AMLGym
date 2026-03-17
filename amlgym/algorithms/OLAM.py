import logging
import os
import random
import tempfile
from dataclasses import dataclass
from typing import ClassVar, Dict, Tuple

import numpy as np
from unified_planning.io import PDDLWriter
from unified_planning.plans import ActionInstance
from unified_planning.shortcuts import SequentialSimulator

from amlgym.algorithms.OnlineAlgorithmAdapter import OnlineAlgorithmAdapter
from amlgym.modeling.trajectory import Trajectory

from olam_aml import OLAMLearner
from information_gain_aml.core import UPAdapter

logger = logging.getLogger(__name__)


@dataclass
class OLAM(OnlineAlgorithmAdapter):
    """
    OLAM: Online Learning of Action Models (Lamanna et al., IJCAI 2021).

    Two-tier action selection: local greedy learning (precondition exclusion,
    effect confirmation) + planner-based exploration for states with no
    local learning opportunity.

    Args:
        max_steps (int): Maximum number of learning steps
        require_injective (bool): Require injective parameter bindings
        model_mode (str): "safe" (all possible preconditions, confirmed effects only)
            or "complete" (certain preconditions only, all possible effects)

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
            olam = get_algorithm('OLAM', max_steps=100)
            model, trajectory = olam.learn(env, input_domain_path)

            print("##################### Learned model #####################")
            print(model)

            print("################# Generated trajectory ##################")
            print(trajectory)

    """

    max_steps: int = 500
    require_injective: bool = True
    model_mode: str = "safe"

    _reference: ClassVar[Dict] = {
        "Authors": "L. Lamanna, A. Saetti, A. Gerevini, A. Zanella, and L. Serafini",
        "Title": "Online Learning of Action Models for PDDL Planning",
        "Venue": "International Joint Conference on Artificial Intelligence",
        "Year": 2021,
    }

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

        # Write problem to temp file for learner init
        tmp_problem = tempfile.NamedTemporaryFile(
            mode='w', suffix='.pddl', delete=False
        )
        tmp_problem_path = tmp_problem.name
        tmp_problem.close()
        PDDLWriter(problem).write_problem(tmp_problem_path)

        try:
            # Initialize learner
            learner = OLAMLearner(
                domain_file=input_domain_path,
                problem_file=tmp_problem_path,
                max_iterations=self.max_steps,
                require_injective=self.require_injective,
                seed=seed,
            )

            # Get initial state
            up_state = simulator.get_initial_state()

            trace_states = [up_state]
            trace_actions = []

            for _ in range(self.max_steps):
                if learner.has_converged():
                    logger.info("OLAM algorithm converged")
                    break

                # Convert UP state to fluent set for the algorithm
                state_set = UPAdapter.up_state_to_fluent_set(up_state, problem)

                # Select action
                result = learner.select_action(state_set)

                if result is None:
                    logger.info("No action available, stopping")
                    break

                action_name, objects = result

                # Create ActionInstance for simulator
                up_action = problem.action(action_name)
                up_objects = tuple(problem.object(o) for o in objects)
                action_instance = ActionInstance(up_action, up_objects)

                # Execute via simulator
                try:
                    next_up_state = simulator.apply(up_state, action_instance)
                    success = next_up_state is not None
                except Exception:
                    next_up_state = None
                    success = False

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
