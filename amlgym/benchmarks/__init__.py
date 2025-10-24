from importlib import resources
from typing import List


def print_domains() -> None:
    """
    List all benchmark domains.
    """
    pkg = f"amlgym.benchmarks.domains"
    print([f.name.split('.')[0] for f in resources.files(pkg).iterdir() if f.is_file()])


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
    Return the absolute path of a PDDL domain trajectory files in the benchmarks.trajectories package.
    """
    possible_kinds = ['learning', 'learning_hard', 'applicability']
    assert kind in possible_kinds, f'`kind` must be one of {possible_kinds}'

    pkg = f"amlgym.benchmarks.trajectories.{kind}.{domain_name.split('.')[0]}"
    trajectories = []
    for traj_file in resources.files(pkg).iterdir():
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
    possible_kinds = ['learning', 'learning_hard', 'applicability']
    assert kind in possible_kinds, f'`kind` must be one of {possible_kinds}'

    pkg = f"amlgym.benchmarks.trajectories.{kind}.{domain_name.split('.')[0]}"
    trajectories_path = [str(f) for f in resources.files(pkg).iterdir() if f.is_file()]
    return sorted(trajectories_path, key=lambda x: int(x.split('/')[-1].split('_')[0]))
