import json
import pathlib
import signal
import string
import subprocess
import sys
import time

from typing import Dict, Any

JOB_ID_MESSAGE = 'echo -e "\\nSLURM_JOBID:\\t\\t" $SLURM_JOBID'
JOB_NODELIST_MESSAGE = 'echo -e "SLURM_JOB_NODELIST:\\t" $SLURM_JOB_NODELIST "\\n\\n"'

FIRST_BREAKPOINT = 10
EXPERIMENTS_CONFIG_STR = "experiment_configurations"


def sigint_handler(sig_num, frame):
    signal.signal(signal.SIGINT, sigint_handler)
    print("\nCtrl-C pressed. Do you want to quit? (y/n): ", end="")
    response = input().strip().lower()
    if response in ["y", "yes"]:
        print("Deleting temp.sbatch file.")
        pathlib.Path("temp.sbatch").unlink()
        exit(0)


def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    percent_to_show = int(percent) // 2
    bar = "❚" * percent_to_show + "-" * (50 - percent_to_show)
    print(f"\r|{bar}| {percent:.2f}%", end="\r")


def write_sbatch_and_submit_job(sbatch_code: str):
    with open("temp.sbatch", "w+", newline="\n") as output_file:
        output_file.write(sbatch_code)

    data = subprocess.check_output(["sbatch", "temp.sbatch", "--parsable"]).decode()
    time.sleep(1)
    return int(data.split()[-1])


def get_configurations() -> Dict[str, Any]:
    print("Reading the configuration file.")
    configuration_file_path = sys.argv[1]
    with open(configuration_file_path, "rt") as configuration_file:
        return json.load(configuration_file)


def get_environment_variables(configurations: Dict[str, Any]) -> Dict[str, Any]:
    environment_variables_path = configurations["environment_variables_file_path"]
    with open(environment_variables_path, "rt") as environment_variables_file:
        return json.load(environment_variables_file)


def validate_job_running(sid: int):
    job_exists_command = ["squeue", "--job", f"{sid}"]
    try:
        result = subprocess.check_output(job_exists_command, shell=True).decode()
        if str(sid) in result:
            return sid

        return None

    except subprocess.CalledProcessError:
        return None


def setup_experiments_folds_job(
    code_directory, environment_variables, experiment, internal_iterations, experiment_size, should_create_random_trajectories: bool = True
):
    print(f"Working on the experiment with domain {experiment['domain_file_name']}\n")
    fold_creation_sid = submit_job(
        conda_env="online_nsam",
        mem="4G",
        python_file=f"{code_directory}/folder_creation_for_parallel_execution.py",
        jobname=f"create_folds_job_{experiment['domain_file_name']}",
        suppress_output=False,
        arguments=[
            f"--working_directory_path {experiment['working_directory_path']}",
            f"--domain_file_name {experiment['domain_file_name']}",
            f"--learning_algorithms {','.join([str(e) for e in experiment['compared_versions']])}",
            f"--internal_iterations {','.join([str(e) for e in internal_iterations])}",
            f"--problem_prefix {experiment['problems_prefix']}",
            f"--experiment_size {experiment_size}",
            f"--no_random_trajectories" if not should_create_random_trajectories else "",
        ],
        environment_variables=environment_variables,
        logs_directory=pathlib.Path(experiment["working_directory_path"]) / "logs",
    )
    print(f"Submitted job with sid {fold_creation_sid}\n")
    time.sleep(1)
    print("Removing the temp.sbatch file")
    pathlib.Path("temp.sbatch").unlink()
    return fold_creation_sid


def create_execution_arguments(experiment, fold, compared_version):
    arguments = []
    arguments.append(f"--fold_number {fold}")
    arguments.append(f"--learning_algorithm {compared_version}")
    for key, value in experiment.items():
        if key != "compared_versions" and key != "parallelization_data":
            arguments.append(f"--{key} {value}")

    return arguments


def create_internal_iterations_list(parallelization_data):
    max_train_size = (
        int(parallelization_data["experiment_size"] * 0.8) + 1 if "experiment_size" in parallelization_data else parallelization_data["max_index"] + 1
    )
    if parallelization_data["hop"] == 100:
        return [1] + list(range(10, 100, 10)) + list(range(100, max_train_size, 100))

    return list(range(1, FIRST_BREAKPOINT)) + list(range(FIRST_BREAKPOINT, max_train_size, parallelization_data["hop"]))


def create_experiment_folders(code_directory, environment_variables, experiment, should_create_random_trajectories: bool = True):
    print(f"Creating the directories containing the folds datasets for the experiments.")
    parallelization_data = experiment["parallelization_data"]
    internal_iterations = create_internal_iterations_list(parallelization_data)
    print(f"Internal iterations: {internal_iterations}")
    sid = setup_experiments_folds_job(
        code_directory=code_directory,
        environment_variables=environment_variables,
        experiment=experiment,
        internal_iterations=internal_iterations,
        experiment_size=parallelization_data.get("experiment_size", 100),
        should_create_random_trajectories=should_create_random_trajectories,
    )
    return internal_iterations, sid


def create_all_experiments_folders(code_directory, environment_variables, configurations, should_create_random_trajectories: bool = True):
    print("Creating the directories containing the folds datasets for the experiments.")
    jobs_sids = []
    output_internal_iterations = []
    for experiment_index, experiment in enumerate(configurations[EXPERIMENTS_CONFIG_STR]):
        internal_iterations, fold_creation_sid = create_experiment_folders(
            code_directory, environment_variables, experiment, should_create_random_trajectories
        )
        jobs_sids.append(fold_creation_sid)
        output_internal_iterations.append(internal_iterations)
        print(
            f"Submitted fold datasets folder creation job with the id {fold_creation_sid} for the experiment with domain {experiment['domain_file_name']}\n"
        )

    while any([validate_job_running(sid) is not None for sid in jobs_sids]):
        print("Waiting for the fold creation jobs to finish.")
        time.sleep(5)

    print("Finished building the experiment folds!")
    return output_internal_iterations


def submit_job(
    dependency=None,
    mem=None,
    runtime=None,
    jobname=None,
    cpus_per_task=None,
    suppress_error=False,
    error_file=None,
    suppress_output=False,
    output_file=None,
    conda_env=None,
    python_file=None,
    arguments=None,
    environment_variables=None,
    logs_directory=None,
):
    with open("experiments/cluster_scripts/template.sbatch", "rt", newline="\n") as template_file:
        text = template_file.read()
        sbatch_template = string.Template(text)

    # Complete the template code with the correct values
    all_environment_variables = [
        "export LOCAL_LOGS_PATH=/scratch/${SLURM_JOB_USER}/${SLURM_JOB_ID}",
        *[f"export {env_variable}={value}" for env_variable, value in environment_variables.items()],
    ]
    template_mapping = {
        "job_name": jobname if jobname else "job",
        "cpus_per_task": cpus_per_task if cpus_per_task else 1,
        "dependency_exists": "#" if not dependency else "",
        "dependency": dependency or "",
        "mem": mem or "8G",
        "conda_env": conda_env or "online_nsam",
        "script": python_file,
        "arguments": " ".join(arguments) if arguments else "",
        "environment_variables": "\n".join(all_environment_variables) if environment_variables else "",
        "job_info_print": JOB_ID_MESSAGE + "\n" + JOB_NODELIST_MESSAGE,
        "cluster_temp_logs_path": "$LOCAL_LOGS_PATH",
        "logs_dir": logs_directory or "/dev/null",
        "error": "#" if suppress_error else "",
    }

    sbatch_code = sbatch_template.substitute(template_mapping)
    try:
        return write_sbatch_and_submit_job(sbatch_code)

    except subprocess.CalledProcessError as e:
        template_mapping["dependency_exists"] = "#"  # Remove the dependency if it exists
        template_mapping["dependency"] = ""  # Remove the dependency if it exists
        sbatch_code = sbatch_template.substitute(template_mapping)
        return write_sbatch_and_submit_job(sbatch_code)


def submit_job_and_validate_execution(
    code_directory, configurations, experiment, fold, arguments, environment_variables, job_name, fold_creation_sid=None, python_file=None
):
    dependency_argument = None if not fold_creation_sid else f"afterok:{fold_creation_sid}"
    sid = submit_job(
        conda_env="online_nsam",
        mem="16G",
        python_file=python_file or f"{code_directory}/{configurations['experiments_script_path']}",
        jobname=job_name,
        dependency=dependency_argument,
        suppress_output=False,
        arguments=arguments,
        environment_variables=environment_variables,
        logs_directory=pathlib.Path(experiment["working_directory_path"]) / "logs",
        suppress_error=True,
    )
    time.sleep(2)
    return validate_job_running(sid)
