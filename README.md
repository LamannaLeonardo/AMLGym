# Action Model Learning Benchmarking
<!-- Define badges -->
<div style="display: flex; gap: 10px;">
   
  <a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" height="20"/></a>

</div>

Official code for benchmark generation and evaluation of action model learning approaches.


## Benchmark generation
The following instructions have been tested on macOS Sequoia 15.3


1. Clone [`pddl-generators` repository](https://github.com/AI-Planning/pddl-generators) into `util` directory:
```
 cd util && git clone https://github.com/AI-Planning/pddl-generators
```

2. Update CMake minimum required version to `3.5` in `util/pddl-generators/nomystery/CMakeLists.txt`

3. Add to `util/pddl-generators/pathways/main.c` the following headers:
```
#include <unistd.h>   // For chdir()
#include <libgen.h>   // For dirname()
```

4. Build all PDDL generators:
```
cd pddl-generators && ./build_all
```

5. Move the `matchingbw` generator out of `blocksworld` in order to the trajectory 
generator to work correctly
```
mv blocksworld/matching matchingbw
cp -r blocksworld/bwstates.1 ./
```

6. Install `requirements.txt`
```
cd ../../ && pip install requirements.txt
```
6. Generate trajectories:
```
cd util && python generators.py
```

7. Optionally generate trajectory statistics:
```
python benchmark_stats.py
```

## Trajectory features:
1. **Reproducibility**: the trajectory generation process is fully reproducible and can be randomized according to 
a random seed.
2. **Bias mitigation**: the bias in the initial and final states of every trajectory is mitigated by: 
   1. planning to reach a random goal from a random initial state; 
   2. executing the plan by interleaving random actions according to some probability (set to `0.2`); the random
   actions are selected such that the problem remains feasible, and after executing a random action a new plan is produced.
   3. randomly selecting a subtrajectory from the ones generated in the two previous steps.
3. **Variability**: in terms of trajectory length (ranging from `5` to `30`) and number of problem objects.


### Required changes for reproducibility:
#### Blocksworld
1. modify the file `blocksworld/blocksworld` by adding a random `SEED` as third input argument:
```
#! /bin/bash

set -euo pipefail

OPS=$1  # Either 3 or 4.
BLOCKS=$2
SEED=$3

# Get full directory name of the script (https://stackoverflow.com/a/246128).
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

BS=${SCRIPT_DIR}/bwstates.1/bwstates
TR=${SCRIPT_DIR}/${OPS}ops/2pddl/2pddl

${BS} -s 2 -n ${BLOCKS} -r ${SEED}> STATES
${TR} -d STATES -n ${BLOCKS}

rm STATES
```


