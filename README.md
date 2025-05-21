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
cd ../../ && pip install -r requirements.txt
```
6. Generate trajectories:
```
cd util && python generators.py
```

7. Optionally generate trajectory statistics:
```
python benchmark_stats.py
```

## Domain selection:
The selected domains are the ones adopted in previous IPC learning tracks:
1. IPC 1998/2000/2002/2004/2006: no learning track
2. [IPC 2008 Learning Track](https://ipc08.icaps-conference.org/learning/): `goldminer`, `matchingbw`, `npuzzle`, 
`parking` and `sokoban`
    - `thoughtful` has not been considered since there is no problem generator neither in the IPC resources nor in
    [`pddl-generators` repository](https://github.com/AI-Planning/pddl-generators) 
3. [IPC 2011 Learning Track](https://icaps11.icaps-conference.org/proceedings/pal/fawcett-et-al.pdf): `barman`, 
`blocksworld`, `depots`, `gripper`, `parking`, `rovers`, `satellite`, `spanner` and `tpp`.
4. [IPC 2014 Learning Track](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2571): `elevators`,
`floortile`, `nomystery`, `parking`, `spanner` and `transport`.
5. [IPC 2023 Learning Track](https://github.com/ipc2023-learning/benchmarks): `blocksworld`,
`childsnack`, `ferry`, `floortile`, `miconic`, `rovers`, `satellite`, `sokoban`,
`spanner` and `transport`.
   - `childsnack`: for consistency with other domains, we adopted the original domain version 
      without negative preconditions.

Therefore the following list of 20 classical planning domains:
- `barman`
- `blocksworld`
- `childsnack`
- `depots`
- `elevators`
- `ferry`
- `floortile`
- `goldminer`
- `gripper`
- `matchingbw`
- `miconic`
- `nomystery`
- `npuzzle`
- `parking`
- `rovers`
- `satellite`
- `sokoban`
- `spanner`
- `tpp`
- `transport`

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

#### Matching-bw
1. modify the file `matchingbw/matching-bw-generator.sh` by adding a random seed as third input argument:

```
#! /bin/bash

# usage: matching-bw-generator.sh <base name> <n>

set -euo pipefail

cd "$(dirname "$0")"

./../bwstates.1/bwstates -n $2 -s 3 -r $3 > temp.blocks || true
./../bwstates.1/bwstates -n $2 -s 3 -r $3 >> temp.blocks || true

./2pddl-typed -d temp.blocks -n $2 > $1-typed.pddl
./2pddl-untyped -d temp.blocks -n $2 > $1-untyped.pddl

rm -f temp.blocks

```
