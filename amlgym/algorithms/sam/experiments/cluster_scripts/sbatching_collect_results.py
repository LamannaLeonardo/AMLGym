import pathlib
import time

from experiments.cluster_scripts.common import (
    submit_job,
    get_configurations,
    get_environment_variables,
    create_internal_iterations_list,
    EXPERIMENTS_CONFIG_STR,
)


def execute_statistics_collection_job(code_directory, configuration, environment_variables, experiment, internal_iterations):
    print(f"Creating the job that will collect the statistics from all the domain's experiments.")
    statistics_collection_job = submit_job(
        conda_env="online_nsam",
        mem="4G",
        python_file=f"{code_directory}/{configuration['results_collection_script_name']}",
        jobname=f"collect_statistics_{experiment['domain_file_name']}",
        suppress_output=False,
        arguments=[
            f"--working_directory_path {experiment['working_directory_path']}",
            f"--domain_file_name {experiment['domain_file_name']}",
            f"--learning_algorithms {','.join([str(e) for e in experiment['compared_versions']])}",
            f"--num_folds {configuration['num_folds']}",
            f"--internal_iterations {','.join([str(e) for e in internal_iterations])}",
        ],
        environment_variables=environment_variables,
    )
    print(f"Submitted job with sid {statistics_collection_job}\n")
    time.sleep(1)
    print("Removing the temp.sbatch for the statistics collection file")
    pathlib.Path("temp.sbatch").unlink()


def main():
    configurations = get_configurations()
    environment_variables = get_environment_variables(configurations)
    code_directory = configurations["code_directory_path"]
    for experiment_index, experiment in enumerate(configurations[EXPERIMENTS_CONFIG_STR]):
        parallelization_data = experiment["parallelization_data"]
        internal_iterations = create_internal_iterations_list(parallelization_data)
        execute_statistics_collection_job(
            code_directory, configurations, environment_variables, experiment, internal_iterations,
        )


if __name__ == "__main__":
    main()
