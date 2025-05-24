import difflib
import os
import re
import shutil
import subprocess
import numpy as np


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


def get_applicable_actions(problem_file, domain_file):

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


if __name__ == '__main__':
    print_actions_with_no_effs('../benchmarks/trajectories')
