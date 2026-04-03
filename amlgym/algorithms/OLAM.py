from dataclasses import dataclass
from typing import Tuple, ClassVar, OrderedDict

from unified_planning.model import UPState
from unified_planning.shortcuts import SequentialSimulator

from amlgym.algorithms.ActiveAlgorithmAdapter import ActiveAlgorithmAdapter
from amlgym.modeling.trajectory import Trajectory
from olam.OLAM import OLAM as OLAMLearner


@dataclass
class OLAM(ActiveAlgorithmAdapter):
    """
    Adapter class for running the OLAM algorithm: "Online Learning of Action Models
    for PDDL Planning", L. Lamanna, A. Saetti, L. Serafini, A. Gerevini, and P. Traverso,
    Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, 2021.
    https://doi.org/10.24963/ijcai.2021/566

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
            olam = get_algorithm('OLAM', input_domain_path=input_domain_path)
            model, trajectory = olam.learn(env)

            print("##################### Learned model #####################")
            print(model)

            print("################# Generated trajectory ##################")
            print(trajectory)

    Args:
        planning_timeout (int): Time limit in seconds for each planning call (default: 30)
        max_length (int): Maximum number of uncertain preconditions/effects considered in
            goal conjunctions (default: 8)
        max_subproblems (int): Maximum number of subproblems when handling object type
            ambiguity (default: 5)
        max_goals (int): Maximum number of disjunctions in a goal formula used
                              during planning for learning preconditions and effects.
                              When the number of generated goals exceeds this limit,
                              some goals are discarded. (default: 10000)
    """
    _reference: ClassVar[OrderedDict[str, str]] = {
        'Authors': "L. Lamanna, A. Saetti, L. Serafini, A. Gerevini, and P. Traverso",
        'Title': "Online Learning of Action Models for PDDL Planning",
        'Venue': "International Joint Conference on Artificial Intelligence",
        'Year': 2021,
        'URL': "https://doi.org/10.24963/ijcai.2021/566",
    }

    planning_timeout: int = 30
    max_length: int = 8
    max_subproblems: int = 5
    max_goals: int = 10000

    def __post_init__(self):
        self._learner = OLAMLearner(
            domain_path=self.input_domain_path,
            planning_timeout=self.planning_timeout,
            max_length=self.max_length,
            max_subproblems=self.max_subproblems,
            max_goals=self.max_goals,
        )

    def learn(self,
              simulator: SequentialSimulator,
              max_steps: int = 10000,
              seed: int = 123) -> Tuple[str, Trajectory]:
        """
        Learns a PDDL action model from:
         (i)   a simulator of the environment to learn from
         (ii)    a (possibly empty) input model which is required to specify the predicates and operators signature
                 (set via the input_domain_path attribute at instantiation time);

        :parameter simulator: environment simulator
        :parameter max_steps: maximum number of interaction steps with the simulator
        :parameter seed: random seed for reproducibility

        :return: a string representing the learned PDDL model, and a JSON specification of the trajectory
        """

        domain_str, olam_traj = self._learner.run(simulator, max_steps=max_steps)

        # Convert OLAM trajectory (SymbolicObservation states) to AMLGym Trajectory (UPState states)
        UPState.MAX_ANCESTORS = None
        states = [UPState(obs.fluents, simulator._problem) for obs in olam_traj.observations]
        trajectory = Trajectory(states, olam_traj.actions)

        return domain_str, trajectory
