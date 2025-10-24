
# Numeric Safe Action Model Learning Framework
SAM learning algorithm for numeric action model learning.

## Installation

The following explains how to install the SAM-Learning framework.
Notice, the code works on linux machines due to its dependencies on planners and validators that only work on linux machines.
Required version - 3.10 or higher.

### Needed external tools:
1. **ENHSP solver** - can be downloaded from [here](https://sites.google.com/view/enhsp/). 
   2.  **Note** - for this code we require the binary code of the latest version of ENHSP (20 currently) with the jar file. 
2. **Metric-FF planner** - can be downloaded from [here](https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html). In this algorithm, we use version 2.1 of Metric-FF which is the latest version.
3. **VAL validation algorithm** - can be downloaded from [here](https://github.com/KCL-Planning/VAL). Use the instructions given in the repository to install VAL.


### Environment variables

* 'METRIC_FF_DIRECTORY': Directory of the compiled metric-FF planner.
  * \<path to containing directory>/Metric-FF-v2.1/
* 'ENHSP_FILE_PATH': Path to the compiled ENHSP planner (the jar file).
  * \<path to containing directory>/enhsp.jar
* 'CONVEX_HULL_ERROR_PATH': Path to the file that will contain the errors raised from the convex hull algorithm. Used for future debugging purposes.
  * \<path to containing directory>/convex_hull_error.txt
* 'VALIDATOR_DIRECTORY': Directory containing VAL compiled code.
  * \<path to containing directory>/VAL/

### Code initialization

* Clone the content of the repository from [GitHub](https://github.com/Search-BGU/numeric-sam.git).
* Install the dependencies using `pip install -r requirements.txt`.
* Set the required environment variables.
* Run the tests using `pytest` on the code to validate the installation.

## Usage

Most of the experiments were conducted on a SLURM cluster so this documentation covers this type of execution. 
Furthermore, we assume that by this part you already installed the dependencies and the required external tools.

* First, you need to create your dataset. 
    * This stage requires having a problem generator at hand that can generate the problems you want to solve.
    * The generator should be able to generate the problems in the format of the PDDL files.
    * After creating the problems dataset, you should create the trajectories and the solutions for each problem.
    * This can be done using the \`[experiments_dataset_generator.py](../experiments/experiments_dataset_generator.py)` script.
    * run the script with the following command:
    ```python experiments/experiments_dataset_generator.py --help``` to see the options and the required command line arguments.
* After creating the dataset run the script [folder_creation_for_parallel_execution.py](../experiments/concurrent_execution/folder_creation_for_parallel_execution.py).
  * This script creates the train-test split and for each experiment iteration it creates a separate folder with the required files. 
  * This ensures that the experiments are independent and can be run in parallel.
  * The folder names are in the format: "fold_{fold_number}\_{learning_algorithm_index}_{iteration_number}".
  * Since the code is designed to run on a SLURM cluster, the folder structure is created in a way that each folder can be submitted as a separate job.
  * Notice - for reproducibility, the configuration of the experiments is saved in the folder with the name "folds.json".
  * The code also creates a separate dataset for performance evaluation.
    * This dataset contains both the test set trajectories and additional random trajectories that are generated using random walks.
    * This performance evaluation dataset is used to evaluate the performance of the learned action models, i.e., the precision, recall and MSE.
* After creating the experiments folders, you can either run the experiments by creating a job that will execute the experiments in parallel or run them sequentially.
* To run the experiments in parallel, you can use the SLURM job scheduler. 
  * The script [numeric_experiments_sbatch_runner.py](../experiments/cluster_scripts/numeric_experiments_sbatch_runner.py) was used to create the jobs for the SLURM cluster.
  * The script requires an environment variable file to load all the environment variables.
  * The script also requires a configuration file that contains the configuration for the experiments.
  * To run the script use the following command:
  ```python ../experiments/cluster_scripts/numeric_experiments_sbatch_runner.py <path to configuration file>```.
* If you want to run the experiments locally, just select the fold, tested algorithm and the current iteration you want to run and run the script [parallel_numeric_experiment_runner.py](../experiments/concurrent_execution/parallel_numeric_experiment_runner.py) with the following command:
```python ../experiments/parallel_numeric_experiment_runner.py <path to configuration file> <fold number> <algorithm index> <iteration number>```
* Notice - the experiments output their statistics in a designated CSV file for each type of statistics.

Example configuration file:
```json
{
  "environment_variables_file_path": "path to environment.json file",
  "code_directory_path": "path to the code directory (current directory)",
  "experiments_script_path": "parallel_numeric_experiment_runner.py",
  "num_folds": 5,
  "RAM": "32G --- or whichever is the required RAM for your experiments",
  "experiment_configurations": [
	{
      "parallelization_data": {
        "min_index": 0,
        "max_index": 80,
        "hop": 10
      },
      "compared_versions": [
        3,  
		5, 
        15 
      ],
      "working_directory_path": "path to the farmland experiment directory",
      "domain_file_name": "farmland.pddl",
      "problems_prefix": "pfile",
      "polynom_degree": 0
    },
	{
      "parallelization_data": {
        "min_index": 0,
        "max_index": 80,
        "hop": 10
      },
      "compared_versions": [
        3,
		5,
        15
      ],
      "working_directory_path": "path to the zenotravel (the polynomial domain) experiment directory",
      "domain_file_name": "zenonumeric.pddl",
      "solver_type": 3,
      "problems_prefix": "pfile",
      "polynom_degree": 1, 
	  "fluents_map_path": "path to the zenotravel_fluents_map.json"
    }
	]
}
```

## License

This work is licensed under the MIT License.