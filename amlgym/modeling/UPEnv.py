import os
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import List, TypeVar, Set, Dict, Any

from unified_planning.io import PDDLReader, PDDLWriter
from unified_planning.model import Problem, Fluent, UPState
from unified_planning.plans import ActionInstance
from unified_planning.shortcuts import SequentialSimulator, BoolType, FALSE, TRUE

from tarski.io import PDDLReader as tarskiPDDLReader
from tarski.grounding import LPGroundingStrategy

from amlgym.modeling.env import Env

ObservationType = TypeVar('ObservationType')


@dataclass
class UPEnv(Env):
    """
    A Gymnasium environment which simulates a PDDL problem
    through the unified-planning sequential simulator.
    """

    # The PDDL problem in unified-planning
    problem: Problem

    # The environment simulation engine
    _simulator: SequentialSimulator

    def __init__(self,
                 domain_path: str,
                 problem_path: str) -> None:
        """
        Set environment state and seed through :meth:`reset` for reproducibility
        """

        # Parse the PDDL environment in unified-planning
        self.problem = PDDLReader().parse_problem(domain_path, problem_path)

        # Instantiate the environment simulation engine
        self._simulator = SequentialSimulator(self.problem)

        self._problem_template = self._create_problem_template()

        self.cache_app_actions = dict()

        # TODO: Remove this tmp patch for childsnack and open issue on up
        constants = ''
        if 'childsnack' in domain_path:
            all_objects_str = '\n'.join([f"{o.name} - {o.type.name}"
                                        for o in self.problem.all_objects
                                        if o.name != 'kitchen'])

            constants = ' (:constants kitchen - place)'

        else:
            all_objects_str = '\n'.join([f"{o.name} - {o.type.name}"
                                        for o in self.problem.all_objects])


        self._problem_template_str = ("(define (problem dummy-problem) "
                                      f"\n (:domain {self.problem.name}-domain) "
                                      "\n (:objects "
                                      f"\n {all_objects_str} )"
                                      "\n(:init)"
                                      "\n (:goal (and ))"
                                      "\n)")

        writer = PDDLWriter(self._problem_template)
        self._domain_template_str = writer.get_domain()
        self._domain_template_str = self._domain_template_str.replace("(at_ ",
                                                                      "(at ")

        # TODO: Check
        if "constants" not in self._domain_template_str:
            self._domain_template_str = '\n'.join(self._domain_template_str.split('\n')[:3] + [constants] + self._domain_template_str.split('\n')[3:])

        # Create a fictitious state with all negated literals
        all_neg_fluents = {f: FALSE() for f, v in self.problem.initial_values.items()}
        UPState.MAX_ANCESTORS = None
        self.all_neg_state = UPState(all_neg_fluents)


        # Initialize actions grounder with tarski since unified-planning (1.2.0) grounder is inefficient
        _tmp_problem = PDDLReader().parse_problem(domain_path, problem_path)
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
        # remove problem goal to avoid tarski reachability issues
        _tmp_problem.clear_goals()
        tmp_domain_path = 'tmp_domain.pddl'
        tmp_problem_path = 'tmp_problem.pddl'
        PDDLWriter(_tmp_problem).write_domain(tmp_domain_path)
        PDDLWriter(_tmp_problem).write_problem(tmp_problem_path)
        reader = tarskiPDDLReader(raise_on_error=True)
        reader.parse_domain(tmp_domain_path)
        reader.parse_instance(tmp_problem_path)
        os.remove(tmp_domain_path)
        os.remove(tmp_problem_path)
        self._grounder = LPGroundingStrategy(reader.problem)

    @cached_property
    # def ground_actions(self) -> List[ActionInstance]:
    def ground_actions(self) -> Dict[str, Any]:
        """
        Return a list of all ground actions for the current environment.
        :return: ground actions list
        """
        # logging.info("Grounding actions with tarski...")
        ground_actions = self._grounder.ground_actions()
        # logging.info("Instantiating UP actions...")
        # ground_actions = [ActionInstance(self.problem.action(k.lower()), [self.problem.object(o.lower()) for o in objs])
        #                   for k, params in ground_actions.items()
        #                   for objs in params]
        # Sort actions by name and parameter string for deterministic ordering
        # ground_actions.sort(key=lambda a: (a.action.name, tuple(str(p) for p in a.actual_parameters)))
        # logging.info(f"Total grounded actions {len(ground_actions)}.")
        return ground_actions

    def _create_problem_template(self):

        problem = self.problem.clone()

        set_initial_value = problem.set_initial_value

        problem.clear_goals()

        # ---- Add `applicable` fluent once ----
        applicable_fluent = Fluent('applicable', BoolType())
        if applicable_fluent not in problem.fluents:
            problem.add_fluent(applicable_fluent)
        set_initial_value(applicable_fluent, True)

        # ---- Rebuild actions with no effects and additional `applicable` precondition ----
        for action in problem.actions:
            action.clear_effects()
            action.add_precondition(applicable_fluent)
            action.add_effect(applicable_fluent, False)

        return problem

    def _str_to_action(self, action_label: str) -> ActionInstance:
        """
        Get UP problem ground action from the action label
        :param action_label: action label string
        :return: unified planning action instance
        """
        action_split = action_label.strip()[1:-1].split()
        op_name = action_split[0]
        if len(action_split) > 1:
            obj_names = [o.strip() for o in action_split[1:]]
        else:
            obj_names = []
        up_op = self.problem.action(op_name)
        up_objs = [self.problem.object(o) for o in obj_names]
        return ActionInstance(up_op, up_objs)

    def apply(self, state, action):
        """
        Return the state :math:`s'` reached after executing action :math:`a`
        in state :math:`s`.
        :param state: current state :math:`s`
        :param action: action :math:`a` to be executed
        :return: future state :math:`s'`
        """
        if isinstance(action, str):
            action = self._str_to_action(action)

        if isinstance(state, Set) or isinstance(state, List):

            pos_literals = {l for l in state if not l.startswith('(not ')}

            prob_state_fluents = dict()
            for f in pos_literals:
                f_split = f[1:-1].split()
                f_name = f_split[0]
                f_objs = []
                if len(f_split) > 1:
                    f_objs = f_split[1:]

                prob_f = self.problem.fluent(f_name)
                prob_args = [self.problem.object(o) for o in f_objs]
                prob_state_fluents[prob_f(*prob_args)] = TRUE()

            state = self.all_neg_state.make_child(prob_state_fluents)

        next_state = self._simulator.apply(state, action)

        literals = set()
        for l, v in next_state._values.items():
            l_name = l.fluent().name
            l_objs = [str(o) for o in l.args]

            if len(l_objs) == 0:
                l_formatted = f"({l_name})"
            else:
                l_formatted = f"({l_name} {' '.join(l_objs)})"

            if v.is_true():
                literals.add(l_formatted)
            else:
                literals.add(f"(not {l_formatted})")

        return literals

    def applicable_actions(self, state) -> Dict[str, Set[str]]:

        # cached = self.cache_app_actions.get(frozenset(state), None)
        # if cached is not None:
        #     return cached

        if isinstance(state, Set) or isinstance(state, List):

            pos_literals = {l for l in state if not l.startswith('(not ')}

            prob_state_fluents = dict()
            for f in pos_literals:
                f_split = f[1:-1].split()
                f_name = f_split[0]
                f_objs = []
                if len(f_split) > 1:
                    f_objs = f_split[1:]

                prob_f = self.problem.fluent(f_name)
                prob_args = [self.problem.object(o) for o in f_objs]
                prob_state_fluents[prob_f(*prob_args)] = TRUE()

            state = self.all_neg_state.make_child(prob_state_fluents)

        applicable_actions = defaultdict(set)
        for op_name, param_combos in self.ground_actions.items():
            for args in param_combos:
                if self._simulator._is_applicable(state,
                                                  self.problem.action(op_name),
                                                  [self.problem.object(o.lower())
                                                   for o in args]):
                    if len(args) > 0:
                        action_label = f"({op_name} {' '.join(args)})"
                    else:
                        action_label = f"({op_name})"

                    applicable_actions[op_name].add(action_label)

        # self.cache_app_actions[frozenset(state)] = applicable_actions
        return applicable_actions

    # def applicable_actions(self, state) -> List[ActionInstance]:
    def applicable_actions_tarski(self, state) -> List[str]:
        """
        Return an iterator over all possible actions that can be executed
        in a given state.
        IMPORTANT NOTE: this method works only when preconditions are simple
        conjunctions of positive literals, otherwise the grounder relaxed
        reachability does not effectively filter from all ground actions
        the ones applicable in the given state.
        :param state: input state :math:`s`
        :return: ground actions applicable in :math:`s`
        """

        cached = self.cache_app_actions.get(frozenset(state), None)
        if cached is not None:
            return cached

        pos_literals = {l for l in state if not l.startswith("(not ")}

        problem_str = self._problem_template_str.replace("(:init)",
                                                         f"(:init {' '.join(list(pos_literals | {'(applicable)'}))})")

        _tarski_reader = tarskiPDDLReader(raise_on_error=True)
        _tarski_reader.parse_domain_string(self._domain_template_str)
        _tarski_reader.parse_instance_string(problem_str)

        grounder = LPGroundingStrategy(_tarski_reader.problem)
        ground_actions = grounder.ground_actions()

        applicable_actions = defaultdict(set)
        for name, param_combos in ground_actions.items():
            for params in param_combos:

                if len(params) > 0:
                    action_label = f"({name} {' '.join(params)})"
                else:
                    action_label = f"({name})"

                applicable_actions[name].add(action_label)

        self.cache_app_actions[frozenset(state)] = applicable_actions

        return applicable_actions
