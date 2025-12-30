import os

import itertools
import shutil
from collections import defaultdict
from dataclasses import dataclass

from unified_planning.model import Fluent
import re
from typing import List, Dict, Set, ClassVar, OrderedDict
from amlgym.algorithms.OfflineAlgorithmAdapter import OfflineAlgorithmAdapter
from unified_planning.io import PDDLReader

from nolam.algorithm.Learner import Learner


@dataclass
class NOLAM(OfflineAlgorithmAdapter):
    """
    Adapter class for running the NOLAM algorithm: "Action Model Learning from Noisy
    Traces: a Probabilistic Approach", L. Lamanna and L. Serafini, Proceedings of the
    Thirty-Fourth International Conference on Automated Planning and Scheduling, 2024.
    https://ojs.aaai.org/index.php/ICAPS/article/view/31493

    Args:
        noise (float): The observation noise.

    Example:
        .. code-block:: python

            from amlgym.algorithms import get_algorithm
            nolam = get_algorithm('NOLAM')
            model = nolam.learn('path/to/domain.pddl', ['path/to/trace0', 'path/to/trace1'])
            print(model)

    """
    _reference: ClassVar[OrderedDict[str, str]] = {
        'Authors': "L. Lamanna and L. Serafini",
        'Title': "Action Model Learning from Noisy Traces: a Probabilistic Approach",
        'Venue': "International Conference on Automated Planning and Scheduling",
        'Year': 2024,
        'URL': "https://ojs.aaai.org/index.php/ICAPS/article/view/31493",
    }

    noise: float = 0.

    def learn(self,
              domain_path: str,
              trajectory_paths: List[str]) -> str:

        # Fill input trajectories with some (i.e. `relevant`) missing literals
        if os.path.exists('tmp'):
            if not os.path.isdir("tmp"):
                os.remove("tmp")
            else:
                shutil.rmtree('tmp')

        os.makedirs('tmp', exist_ok=True)
        filled_traj_paths = []
        for i, traj_path in enumerate(trajectory_paths):
            filled_traj = self._preprocess_trace(domain_path, traj_path)  # add relevant negative literals
            filled_traj_paths.append(f"tmp/{i}_traj_filled")
            with open(f"tmp/{i}_traj_filled", "w") as f:
                f.write(filled_traj)

        # Learn an action model
        model = Learner().learn(domain_path, filled_traj_paths, e=self.noise)  # noise set to 0.0

        # Remove temporary files
        shutil.rmtree('tmp')

        return str(model)

    def _preprocess_trace(self, domain_path: str, traj_path: str) -> str:
        """
        Format the trajectory to make it compliant with the algorithm, by explicitly
        stating negative literals.

        :parameter domain_path: path to the input domain file
        :parameter traj_path: path to the trajectory file

        :return: a string representing the formatted trajectory
        """

        # Inner helper function
        def ground_atoms(atom: Fluent,
                         objects: Dict[str, Set[str]]) -> Set[str]:
            """
            Ground a lifted atom with a set of objects by checking object types are in the atom signature

            :param atom: a lifted atom
            :param objects: dictionary where keys are object ids and values object types

            :return: list of grounded atoms
            """
            atom_objs = [[o for o, o_types in objects.items() if param.type.name in o_types]
                         for param in atom.signature]
            if len(atom_objs) == 0:
                return {f"({atom.name})"}
            return {f"({atom.name} {' '.join(comb)})" for comb in itertools.product(*atom_objs)}

        domain = PDDLReader().parse_problem(domain_path)
        with open(traj_path, 'r') as f:
            traj_str = f.read()
            traj_str = re.sub(r' +', ' ', traj_str)  # format extra spaces

        states = [r for r in traj_str.split('\n') if r.strip().startswith('(:state ')]
        actions = [{'name': a.split()[0], 'objs': a.split()[1:] if len(a.split()) > 1 else list()}
                   for a in re.findall(r"\(:action\s+\((.*?)\)\)", traj_str)]
        states = [{
            'pos': {e.strip() for e in re.findall(r"\([^()]*\)", s)
                    if not len(e.replace('(and', '').replace(')', '').strip()) == 0},
            'neg': set()}
            for s in states]

        # for every object, get all types compatible with the predicate signature of observable atoms
        objects_types = defaultdict(set)

        for i in range(len(states)):
            s = states[i]
            for l in s['pos']:
                terms = l.strip()[1:-1].split()
                pred = terms[0]
                objs = list(terms[1:]) if len(terms) > 1 else list()
                for k, o in enumerate(objs):
                    objects_types[o].add(domain.fluent(pred).signature[k].type.name)

        for i in range(len(states) - 1):
            s = states[i]

            # Compute all literals involving next action objects
            action_objs = {o: objects_types[o] for o in actions[i]['objs']}

            relevant_literals = set()
            for atom in domain.fluents:
                # relevant_literals = relevant_literals.union(ground_atoms(atom, objects_types))
                relevant_literals = relevant_literals.union(ground_atoms(atom, action_objs))

            # Add missing negative literals to prev state
            neg = relevant_literals - s['pos']
            s['neg'] = s['neg'].union({f"(not {l})" for l in neg})

            # Add missing negative literals to next state
            neg = relevant_literals - states[i+1]['pos']
            states[i+1]['neg'] = states[i+1]['neg'].union({f"(not {l})" for l in neg})

        traj_str = "(:observation "
        for i in range(len(states) - 1):
            traj_str += f"\n\n(:state {' '.join(states[i]['pos'].union(states[i]['neg']))})"
            if len(actions[i]['objs']) > 0:
                traj_str += f"\n\n(:action ({actions[i]['name']} {' '.join(actions[i]['objs'])}))"
            else:
                traj_str += f"\n\n(:action ({actions[i]['name']}))"

        traj_str += f"\n\n(:state {' '.join(states[-1]['pos'].union(states[-1]['neg']))})\n\n)"

        return traj_str
