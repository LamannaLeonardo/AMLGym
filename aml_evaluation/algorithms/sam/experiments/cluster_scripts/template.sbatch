#!/bin/bash

################################################################################################
### sbatch configuration parameters must start with #SBATCH and must precede any other commands.
### To ignore, just add another # - like so: ##SBATCH
################################################################################################

#SBATCH --partition main			### specify partition name where to run a job. main: all nodes;
#SBATCH --time 7-00:00:00			### limit the time of job running. Make sure it is not greater than the partition time limit!! Format: D-H:MM:SS
#SBATCH --job-name ${job_name}				### name of the job
#SBATCH --cpus-per-task=${cpus_per_task}
#SBATCH --output slurm-%J.out			### output log for running job - %J for job number
${error}#SBATCH --error slurm-error-%J.out			### output log for running job - %J for job number
${dependency_exists}#SBATCH --dependency=${dependency}

# Note: the following 4 lines are commented out
##SBATCH --mail-type=ALL			### conditions for sending the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=${mem}				### amount of RAM memory, allocating more than 60G requires IT team's permission
#SBATCH --tmp=50G        ### amount of temporary storage space, used for node's local storage


################  Following lines will be executed by a compute node    #######################

### Print some data to output file ###
echo `date`
${job_info_print}
echo "Job name is: ${job_name}"

${environment_variables}

echo "${cluster_temp_logs_path}"
mkdir ${cluster_temp_logs_path}/logs
chmod -R 777 ${cluster_temp_logs_path}/logs

### Start your code below ####
module load anaconda				### load anaconda module (must be present when working with conda environments)
source activate ${conda_env}				### activate a conda environment, replace my_env with your conda environment
python ${script}	${arguments}			### this command executes python script – replace with your own command

cp -r ${cluster_temp_logs_path}/logs/* ${logs_dir}		### copy logs to the logs directory


