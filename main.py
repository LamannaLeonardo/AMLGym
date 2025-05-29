import json
import logging
import os
import sys
import time
from pddl import parse_domain
import algorithms


def empty_domain(domain_path: str, empty_domain_path: str = 'empty.pddl'):

    # Load the domain using pddl library
    pddl_domain = parse_domain(domain_path)

    # Loop through all actions and remove preconditions and effects
    for action in pddl_domain.actions:
        action._precondition = tuple()
        action._effect = tuple()

    # Write the modified domain back to a file
    with open(empty_domain_path, 'w') as f:
        pddl_domain = str(pddl_domain)
        f.write(str(pddl_domain))

    return empty_domain_path


if __name__ == '__main__':

    TRAJ_DIR = 'benchmarks/trajectories/learning'
    DOM_DIR = 'benchmarks/domains'
    RES_DIR = 'res'

    logging.basicConfig(
        # filename='out.log',
        # level=logging.INFO
    )

    methods = ['SAM', 'OffLAM', 'NOLAM']

    for alg_class in methods:

        print(f'##################### Running {alg_class} #####################')

        # Instantiate learning algorithm
        agent = getattr(algorithms, alg_class)()

        # Create results log directory and metrics dataframe
        os.makedirs(f"{RES_DIR}/{alg_class}", exist_ok=True)
        run_dir = f"{RES_DIR}/{alg_class}/run{len(os.listdir(f'{RES_DIR}/{alg_class}'))}"
        os.makedirs(run_dir, exist_ok=True)
        metrics = dict()

        to_be_avoided = []

        for domain in [d for d in sorted(os.listdir(TRAJ_DIR)) if d not in to_be_avoided]:

            print(f'Processing domain {domain}...')

            # Trace CPU time
            run_start = time.perf_counter()

            # Reference domain path
            domain_path = f"{DOM_DIR}/{domain}.pddl"

            # Get empty domain path
            empty_domain_path = empty_domain(domain_path)

            # Get trajectory paths
            traj_paths = sorted([f"{TRAJ_DIR}/{domain}/{t}" for t in os.listdir(f"{TRAJ_DIR}/{domain}")],
                                key=lambda x: int(x.split('/')[-1].split('_')[0]))

            # Redirect stdout to temporary log file
            old_stdout = sys.stdout
            with open("stdout.log", "w") as log_file:
                sys.stdout = log_file

                # Learn action model
                model = agent.learn(empty_domain_path, traj_paths)

            # Clear temporary files
            sys.stdout = old_stdout
            os.remove("stdout.log")
            os.remove(empty_domain_path)

            # Store learned model
            model_path = f"{run_dir}/{domain}_learned.pddl"
            with open(f"{run_dir}/{domain}_learned.pddl", 'w') as f:
                f.write(model)

            # Evaluate CPU time model
            metrics[domain] = {
                'CPU time (s)': round((time.perf_counter() - run_start), 2),
            }

        with open(f"{run_dir}/metrics.json", 'w') as f:
            json.dump(metrics, f, indent=2)
