import json
from importlib import resources
from pprint import pprint
from typing import List, Dict, Sequence


def get_domain_names() -> List[str]:
    """
    List all benchmark domain names.
    """
    pkg = f"amlgym.benchmarks.domains"
    return [f.name.split('.')[0] for f in resources.files(pkg).iterdir() if f.is_file()]


def print_domains() -> None:
    """
    Print all benchmark domain names.
    """
    pprint(get_domain_names())


def get_domain(domain_name: str) -> str:
    """
    Read the content of a PDDL domain file as text.
    """
    pkg = f"amlgym.benchmarks.domains"
    domain_file = f"{domain_name}.pddl" if '.pddl' not in domain_name else domain_name
    with resources.open_text(pkg, domain_file) as f:
        return f.read()


def get_trajectories(domain_name: str,
                     kind: str = 'learning') -> List[str]:
    """
    Return a list of trajectory strings for a PDDL domain in the benchmarks.trajectories package.
    """
    base_pkg = "amlgym.benchmarks.trajectories"

    possible_kinds = sorted([p.name for p in resources.files(base_pkg).iterdir()
                             if p.is_dir() and not p.name.startswith("_")])

    assert kind in possible_kinds, f'`kind` must be in {possible_kinds}'

    pkg = f"{base_pkg}.{kind}.{domain_name.split('.')[0]}"
    trajectories = []
    for traj_file in sorted(resources.files(pkg).iterdir(),
                            key=lambda x: int(x.name.split('_')[0])):
        with resources.open_text(pkg, traj_file.name) as f:
            trajectories.append(f.read())
    return trajectories


def get_domain_path(domain_name: str) -> str:
    """
    Return the absolute path of a PDDL domain file in the benchmarks.domains package.
    """
    pkg = "amlgym.benchmarks.domains"
    domain_name = f"{domain_name}.pddl" if '.pddl' not in domain_name else domain_name
    # get absolute path of pddl domain file
    domain_path = resources.files(pkg).joinpath(domain_name)
    return str(domain_path)


def get_trajectories_path(domain_name: str,
                          kind: str = 'learning') -> List[str]:
    """
    Return the absolute path of a PDDL domain trajectory files in the benchmarks.trajectories package.
    """
    base_pkg = "amlgym.benchmarks.trajectories"

    possible_kinds = sorted([p.name for p in resources.files(base_pkg).iterdir()
                             if p.is_dir() and not p.name.startswith("_")])

    assert kind in possible_kinds, f'`kind` must be in {possible_kinds}'

    pkg = f"{base_pkg}.{kind}.{domain_name.split('.')[0]}"

    trajectories_path = [str(f) for f in resources.files(pkg).iterdir() if f.is_file()]
    return sorted(trajectories_path, key=lambda x: int(x.split('/')[-1].split('_')[0]))


def get_problems_path(domain_name: str,
                      kind: str = 'solving') -> List[str]:
    """
    Return the absolute path of a PDDL domain problem files in the benchmarks.problems package.
    """
    base_pkg = "amlgym.benchmarks.problems"

    possible_kinds = sorted([p.name for p in resources.files(base_pkg).iterdir()
                             if p.is_dir() and not p.name.startswith("_")])

    assert kind in possible_kinds, f'`kind` must be in {possible_kinds}'

    pkg = f"{base_pkg}.{kind}.{domain_name.split('.')[0]}"
    problems_path = [str(f) for f in resources.files(pkg).iterdir() if f.is_file()]
    return sorted(problems_path, key=lambda x: int(x.split('/')[-1].split('_')[0]))


def get_test_states(domain_name: str,
                    kind: str = 'predictive_power') -> Dict[str, Sequence[object]]:
    """
    Return a set of test states from some JSON format for a PDDL domain in the
    benchmarks.states package. The returned set of test states is a dictionary
    where keys are PDDL problem files and values are list of test states.
    """
    base_pkg = "amlgym.benchmarks.states"

    possible_kinds = sorted([p.name for p in resources.files(base_pkg).iterdir()
                             if p.is_dir() and not p.name.startswith("_")])

    assert kind in possible_kinds, f'`kind` must be in {possible_kinds}'

    pkg = f"{base_pkg}.{kind}.{domain_name.split('.')[0]}"

    try:
        states_path = str(next(f for f in resources.files(pkg).iterdir() if f.is_file()))
    except StopIteration:
        raise FileNotFoundError(f"No files found in package {pkg}.")

    with open(states_path, 'r') as f:
        test_set = json.load(f)

    return test_set
