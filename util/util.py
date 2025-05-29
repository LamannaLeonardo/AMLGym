import difflib
import os
import re
import shutil
import subprocess
from typing import List, Tuple

import numpy as np
import yaml

from tarski.grounding import LPGroundingStrategy
from unified_planning.io import PDDLReader
from tarski.io import PDDLReader as tarskiPDDLReader
from unified_planning.shortcuts import SequentialSimulator


def remove_trajs(traj_dir: str,
                 num: int = np.inf) -> None:
    """
    Remove trajectories with an ID higher than the given one.
    :param traj_dir: directory with the set of trajectories
    :param traj_dir: maximum number of trajectories
    :return:
    """
    for d in os.listdir(traj_dir):
        for t in os.listdir(os.path.join(traj_dir, d)):
            if int(t.split('_')[0]) >= num:
                os.remove(os.path.join(traj_dir, d, t))


def print_actions_with_no_effs(traj_dir: str = '../benchmarks/trajectories') -> None:
    """
    Compare trajectories between two sets of trajectories.
    :param traj_dir: directory with the set of trajectories
    :return:
    """

    for d in os.listdir(traj_dir):

        for t in os.listdir(os.path.join(traj_dir, d)):
            with open(os.path.join(traj_dir, d, t), 'r') as f:
                traj = f.readlines()
            states = [r for r in traj if r.startswith('(:state ')]
            actions = [r for r in traj if r.startswith('(:action ')]

            for i in range(len(states) - 1):
                if states[i] == states[i + 1]:
                    print(f"Domain {d} action {actions[i]}")


def compare_trajs(traj_dir1: str = '../benchmarks/trajectories',
                  traj_dir2: str = '../benchmarks/trajectoriesbkp') -> None:
    """
    Compare trajectories between two sets of trajectories.
    :param traj_dir1: directory with the first set of trajectories
    :param traj_dir2: directory with the second set of trajectories
    """

    assert np.all(sorted(os.listdir(traj_dir1)) == sorted(os.listdir(traj_dir2)))

    for d in os.listdir(traj_dir1):
        assert np.all(sorted(os.listdir(f"{traj_dir1}/{d}")) == sorted(os.listdir(f"{traj_dir2}/{d}")))
        for t in os.listdir(os.path.join(traj_dir1, d)):
            with open(os.path.join(traj_dir1, d, t), 'r') as f:
                data1 = f.readlines()
            with open(os.path.join(traj_dir2, d, t), 'r') as f:
                data2 = f.readlines()

            for line in difflib.unified_diff(data1, data2, fromfile='file1', tofile='file2', lineterm=''):
                print(f'File: {t}')
                print(line)


def get_applicable_actions_val(problem_file, domain_file):

    tmp_domain_file = f"{domain_file}.tmp"
    tmp_problem_file = f"{problem_file}.tmp"
    shutil.copy(domain_file, tmp_domain_file)
    shutil.copy(problem_file, tmp_problem_file)

    with open(tmp_domain_file, 'r') as f:
        domain_text = f.read()

    new_text = re.sub(r":effect\s*\(and(?:\s*\(.*\))*", ":effect (and )", domain_text)

    with open(tmp_domain_file, 'w') as f:
        f.write(new_text)

    # Ground the problem using Val
    bash_command = ["./val/Instantiate", tmp_domain_file, tmp_problem_file]
    process = subprocess.run(bash_command, capture_output=True)
    output = str(process.stdout).split('\\n')

    os.remove(tmp_domain_file)
    os.remove(tmp_problem_file)

    all_actions = re.findall("\([^()]*\)", re.findall("so far.*literals", "".join(output))[0])
    all_actions = [a[1:-1].split() for a in all_actions]
    all_actions = {f"({a[0].rsplit('_', 1)[0]} {' '.join(a[1:])})" for a in all_actions}

    return all_actions


# TODO: test this
def get_applicable_actions(domain_file: str,
                           problem_file: str) -> List[Tuple[str, str]]:

    # Ground actions with tarski since unified-planning (1.2.0) grounder is inefficient
    tarski_reader = tarskiPDDLReader(raise_on_error=True)
    tarski_reader.parse_domain(domain_file)
    tarski_reader.parse_instance(problem_file)
    grounder = LPGroundingStrategy(tarski_reader.problem)
    ground_actions = grounder.ground_actions()

    problem = PDDLReader().parse_problem(domain_file, problem_file)

    with SequentialSimulator(problem=problem) as simulator:
        current_state = simulator.get_initial_state()

        applicable_actions = [(problem.action(k.lower()), [problem.object(o.lower()) for o in objs])
                              for k, params in ground_actions.items()
                              for objs in params
                              if simulator._is_applicable(current_state,
                                                          problem.action(k.lower()),
                                                          [problem.object(o.lower()) for o in objs])]
    return applicable_actions


# Replace "word-word" with "word_word", otherwise unified-planning does not correctly write the problem file
def fix_domain_format(dom_dir: str = '../benchmarks/domains') -> None:
    """
    Replace "word-word" with "word_word", otherwise unified-planning does not correctly write the problem file
    :param dom_dir: directory of domains
    :return:
    """

    for d in os.listdir(dom_dir):
        with open(f"{dom_dir}/{d}", 'r') as f:
            data = f.read()
        with open(f"{dom_dir}/{d}", 'w') as f:

            # Changhe hyphens for unified-planning
            data = re.sub(r'(?<=\w)-(?=\w)', '_', data)

            # Ferry: previous step change not-eq into not_eq --> remove not_ for OffLAM
            # --> TODO 1: open issue in OffLAM
            # --> TODO 2: open issue in unified-planning
            data = data.replace('(not_eq ', '(noteq ')

            # lower format
            # TODO: check goldminer without lower format
            data = data.lower()

            f.write(data)


def preprocess_trace(traj_path: str) -> None:

    for d in os.listdir(traj_path):
        dom_traj = dict()
        for t in os.listdir(f"{traj_path}/{d}"):
            with open(f"{traj_path}/{d}/{t}", 'r') as f:
                traj_str = f.readlines()
            states = [s for s in traj_str if s.startswith('(:state')]
            dom_traj[f"{traj_path}/{d}/{t}"] = len(states)


def reduce_problem_settings(in_problem_path: str,
                            out_problem_path: str) -> None:
    with open(in_problem_path, 'r') as f:
        settings = yaml.safe_load(f)

    for d in settings['domains']:
        settings['domains'][d] = settings['domains'][d][-2:]

    with open(out_problem_path, 'w') as f:
        yaml.dump(settings, f)



if __name__ == '__main__':

    # remove_trajs('../benchmarks/problems/applicability', 100)
    # remove_trajs('../benchmarks/trajectories/applicability', 100)

    # preprocess_trace('../benchmarks/trajectories/learning')

    reduce_problem_settings('../benchmarks/problems_learning.yaml',
                            '../benchmarks/problems_learning_hard.yaml')