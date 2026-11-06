import os
import re
from dataclasses import dataclass, replace
from typing import ClassVar, Dict, List, OrderedDict, Set, Tuple

import rosame

from amlgym.algorithms.PassiveAlgorithmAdapter import PassiveAlgorithmAdapter

Atom = Tuple[str, Tuple[str, ...]]


@dataclass
class ROSAME(PassiveAlgorithmAdapter):
    """
    Adapter class for running the official implementation of the ROSAME algorithm
    (Python package ``rosame``): "Neuro-Symbolic Learning of Lifted Action Models from
    Visual Traces", K. Xi, S. Gould, and S. Thiébaux, Proceedings of the Thirty-Fourth
    International Conference on Automated Planning and Scheduling, 2024.
    https://ojs.aaai.org/index.php/ICAPS/article/download/31528/33688

    One model is trained on all trajectories at once, whatever their object sets and
    lengths. Objects and their types are inferred from the atoms and actions of each
    trajectory; constants declared in the input domain are added to every trajectory.
    When a trajectory has a problem file at the benchmark location (``.../trajectories/...
    /<i>_<domain>_traj`` -> ``.../problems/.../<i>_<domain>_prob.pddl``), objects it uses
    without declaring are domain constants missing from the input domain (``empty_domain()``
    does not keep ``:constants``); they are declared in the learned domain, so that problems
    using them can be parsed with it.

    Args:
        prior_weight (float): Weight of the prior that prefers preconditions (lambda in the
            paper). It decides facts that hold before and after every occurrence of an
            action, and tolerates noise: a fact remains a precondition while it is false
            in fewer than roughly this fraction of the action's occurrences.
        endpoint_weight (float): Extra weight of the terms involving each trajectory's first
            and last states (gamma in the paper); 1 gives every state the same weight.
        reduction (str): "transition" (every transition counts equally) or "trace" (each
            trajectory averaged over its own transitions and propositions, as in the paper).
        epochs (int): Maximum number of optimisation steps, each over all trajectories.
        min_epochs (int): Minimum number of optimisation steps.
        patience (int): Stop once the learned model has not changed for this many steps.
        lr (float): Adam learning rate.
        seed (int): Random seed of the model initialisation.
        device (str): Torch device, e.g. "cpu" or "cuda".

    Example:
        .. code-block:: python

            from amlgym.algorithms import get_algorithm
            rosame = get_algorithm('ROSAME')
            model = rosame.learn('path/to/domain.pddl', ['path/to/trace0', 'path/to/trace1'])
            print(model)

    """
    _reference: ClassVar[OrderedDict[str, str]] = {
        'Authors': "K. Xi, S. Gould, and S. Thiébaux",
        'Title': "Neuro-Symbolic Learning of Lifted Action Models from Visual Traces",
        'Venue': "International Conference on Automated Planning and Scheduling",
        'Year': 2024,
        'URL': "https://ojs.aaai.org/index.php/ICAPS/article/download/31528/33688"
    }

    prior_weight: float = 0.2
    endpoint_weight: float = 1.0
    reduction: str = "transition"
    epochs: int = 2000
    min_epochs: int = 200
    patience: int = 200
    lr: float = 1e-3
    seed: int = 0
    device: str = "cpu"

    def learn(self,
              domain_path: str,
              trajectory_paths: List[str]) -> str:
        """
        Learns a PDDL action model from:
         (i)    a (possibly empty) input model which is required to specify the predicates and operators signature;
         (ii)   a list of trajectory file paths.

        :parameter domain_path: input PDDL domain file path
        :parameter trajectory_paths: list of trajectory file paths

        :return: a string representing the learned PDDL model
        """
        pddl = rosame.io.read_pddl_domain(domain_path)
        traces, constants = [], {}
        for traj_path in trajectory_paths:
            states, actions = self._read_trajectory(traj_path)
            objects = self._infer_objects(pddl, states, actions)
            constants.update(self._undeclared_objects(traj_path, objects, pddl))
            traces.append(rosame.Trace(objects, states, actions))

        loss = rosame.ROSAMELoss(prior_weight=self.prior_weight, endpoint_weight=self.endpoint_weight,
                                 reduction=self.reduction)
        # Atoms that repeat an object, e.g. (adjacent c1 c1), have no ROSAME proposition: ignore them
        result = rosame.learn(pddl.domain, traces, loss=loss, epochs=self.epochs, min_epochs=self.min_epochs,
                              patience=self.patience, lr=self.lr, seed=self.seed, device=self.device,
                              on_unknown_atom="ignore")
        if constants:
            pddl = replace(pddl, constants=list(pddl.constants) + sorted(constants.items()))
        return result.to_pddl(pddl_domain=pddl)

    @staticmethod
    def _read_trajectory(traj_path: str) -> Tuple[List[List[Atom]], List[Atom]]:
        """
        Parse a trajectory "(:trajectory (:state ...) (:action (name args)) (:state ...) ...)".

        :parameter traj_path: path to the trajectory file

        :return: the list of states (each a list of true atoms) and the list of actions
        """
        with open(traj_path, 'r') as f:
            text = re.sub(r";[^\n]*", "", f.read()).lower()
        stack: list = [[]]
        for tok in re.findall(r"\(|\)|[^\s()]+", text):
            if tok == "(":
                stack.append([])
            elif tok == ")":
                last = stack.pop()
                stack[-1].append(last)
            else:
                stack[-1].append(tok)
        trajectory = stack[0][0]
        states, actions = [], []
        for item in trajectory[1:]:
            if item and item[0] in (":state", ":init"):
                states.append([(a[0], tuple(a[1:])) for a in item[1:] if isinstance(a, list) and a and a[0] != "and"])
            elif item and item[0] == ":action":
                actions.append((item[1][0], tuple(item[1][1:])))
        if len(states) != len(actions) + 1:
            raise ValueError(f"{traj_path}: {len(states)} states for {len(actions)} actions")
        return states, actions

    @staticmethod
    def _undeclared_objects(traj_path: str, objects: List[Tuple[str, str]], pddl) -> Dict[str, str]:
        """
        Objects of a trajectory that its problem file does not declare, i.e. domain constants
        missing from the input domain. Empty if the trajectory has no problem file at the
        benchmark location.

        :parameter traj_path: path to the trajectory file
        :parameter objects: the trajectory objects, as returned by _infer_objects
        :parameter pddl: the input domain, as read by rosame.io.read_pddl_domain

        :return: dictionary from object names to types
        """
        problem_path = traj_path.replace('trajectories', 'problems').replace('_traj', '_prob.pddl')
        if problem_path == traj_path or not os.path.isfile(problem_path):
            return {}
        declared = {name for name, _ in rosame.io.read_pddl_problem(problem_path).objects}
        declared |= {name for name, _ in pddl.constants}
        return {name: t for name, t in objects if name not in declared}

    @staticmethod
    def _infer_objects(pddl, states: List[List[Atom]], actions: List[Atom]) -> List[Tuple[str, str]]:
        """
        The objects of a trajectory with their types: the domain constants, then every other object
        in order of appearance, typed by the most specific type among the predicate and action
        parameters it fills.

        :parameter pddl: the input domain, as read by rosame.io.read_pddl_domain
        :parameter states: the trajectory states
        :parameter actions: the trajectory actions

        :return: the list of (object, type) pairs
        """
        domain = pddl.domain
        observed: Dict[str, Set] = {}
        uses = [(domain.get_predicate(p), args) for s in states for p, args in s]
        uses += [(domain.get_action_schema(a), args) for a, args in actions]
        for symbol, args in uses:
            if symbol is not None and len(args) == len(symbol.types):
                for obj, t in zip(args, symbol.types):
                    observed.setdefault(obj, set()).add(t)

        objects = list(pddl.constants)
        declared = {name for name, _ in objects}
        for obj, types in observed.items():
            if obj in declared:
                continue
            most_specific = [t for t in types if all(t.is_child_of(u) for u in types)]
            if not most_specific:
                raise ValueError(f"object '{obj}' is used with incompatible types {sorted(t.name for t in types)}")
            objects.append((obj, most_specific[0].name))
        return objects
