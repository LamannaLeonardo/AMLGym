import logging
import os
import random
from dataclasses import dataclass
from typing import List, Tuple, Any

import numpy as np
from tarski.grounding import LPGroundingStrategy
from unified_planning.interop import convert_problem_to_tarski
from unified_planning.io import PDDLReader, PDDLWriter
from unified_planning.model import Fluent
from unified_planning.plans import ActionInstance
from unified_planning.shortcuts import SequentialSimulator, BoolType

from amlgym.algorithms.OnlineAlgorithmAdapter import OnlineAlgorithmAdapter
from amlgym.algorithms.SAM import SAM
from amlgym.modeling.trajectory import Trajectory


@dataclass
class RandomAgent(OnlineAlgorithmAdapter):
    """
    A simple baseline for online learning in a fully observable and deterministic
    environment by randomly executing actions. The baselines firstly generates
    a trajectory and then applies the SAM algorithm for offline learning a model
    from the generated trace.

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
            baseline = get_algorithm('RandomAgent')
            model, trajectory = baseline.learn(env, input_domain_path)

            print("##################### Learned model #####################")
            print(model)

            print("################# Generated trajectory ##################")
            print(trajectory)

    """
    max_steps: int = 100.

    def learn(self,
              simulator: SequentialSimulator,
              input_domain_path: str,
              seed: int = 123) -> Tuple[str, Trajectory]:
        """
        Learns a PDDL action model from:
         (i)   a simulator of the environment to learn from
         (ii)    a (possibly empty) input model which is required to specify the predicates and operators signature;

        :parameter simulator: environment simulator
        :parameter input_domain_path: input PDDL domain file path
        :parameter seed: random seed for reproducibility

        :return: a string representing the learned PDDL model, and a JSON specification of the trajectory
        """

        # Set seed for reproducibility
        random.seed(seed)
        np.random.seed(seed)

        # Ground actions
        problem_path = 'tmp.pddl'
        PDDLWriter(simulator._problem).write_problem(problem_path)
        ground_actions = self._ground_actions(input_domain_path, problem_path)
        os.remove(problem_path)

        # Get initial state
        state = simulator.get_initial_state()

        trace_actions = []
        trace_states = [state]

        for i in range(self.max_steps):

            action_label = random.choice(ground_actions)
            operator = simulator._problem.action(action_label[0])
            args = [simulator._problem.object(o) for o in action_label[1]]
            action = ActionInstance(operator, tuple(args))

            next_state = simulator.apply(state, action)

            if next_state is not None:
                state = next_state

            trace_states.append(next_state)
            trace_actions.append(action)

        # Store generated trajectory by filtering out failed actions
        trajectory_path = 'tmp_trajectory'
        success_states = [s for s in trace_states if s is not None]
        success_actions = [
            a for s, a in zip(trace_states[1:], trace_actions)
            if s is not None
        ]
        trajectory = Trajectory(success_states, success_actions)
        trajectory.write(trajectory_path)

        model = SAM().learn(input_domain_path, [trajectory_path])

        return model, Trajectory(trace_states, trace_actions)

    def _ground_actions(self, input_domain_path: str, problem_path: str) -> List[Any]:

        # Initialize actions grounder with tarski
        _tmp_problem = PDDLReader().parse_problem(input_domain_path, problem_path)
        # Add a dummy fluent to show `preconditions:` and `effects:` sections in the PDDL file
        dummy_fluent = Fluent('dummy', BoolType())
        if dummy_fluent not in _tmp_problem.fluents:
            _tmp_problem.add_fluent(dummy_fluent)
        _tmp_problem.set_initial_value(dummy_fluent, True)
        # Rebuild actions with no preconditions/effects
        for action in _tmp_problem.actions:
            action.clear_preconditions()
            action.clear_effects()
            # ensure `preconditions:` and `effects:` sections in the PDDL file
            action.add_precondition(dummy_fluent)
            action.add_effect(dummy_fluent, True)
        # Remove problem goal to avoid tarski reachability issues
        _tmp_problem.clear_goals()

        tarski_problem = convert_problem_to_tarski(_tmp_problem)
        grounder = LPGroundingStrategy(tarski_problem)

        logging.debug("Grounding actions with tarski...")
        ground_actions = grounder.ground_actions()

        ground_action_labels = list()
        for op_name, param_combos in ground_actions.items():
            for args in param_combos:
                ground_action_labels.append((op_name, args))

        return ground_action_labels
