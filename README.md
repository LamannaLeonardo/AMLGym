# Action Model Learning Benchmarking
<!-- Define badges -->
<div style="display: flex; gap: 10px;">
   
  <a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" height="20"/></a>

</div>

Official code for benchmark generation and evaluation of action model 
learning approaches.


## Getting Started

The following instructions have been tested on macOS Sequoia 15.3

1. Clone this repository and its submodules:
```
 git clone --recurse-submodules https://github.com/LamannaLeonardo/aml-evaluation.git
```

2. Create a Python 3.10 virtual environment using conda (or [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-a-new-virtual-environment)):
```
 conda create -n aml python=3.10
```

3. Activate the environment with conda (or [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#activate-a-virtual-environment)):
```
 conda activate aml
```

4. Install dependencies:
```
cd aml-evaluation && pip install -r requirements.txt
```


## State-of-the-art Algorithms
This repository provides seamless integration with state-of-the-art algorithms 
for offline learning classical planning domains from an input set of 
trajectories in the following settings:
1. **full** observability: SAM [1].
2. **partial** observability: OffLAM [2].
3. **full** and **noisy** observability: NOLAM [3].

It is possible to run the above algorithms as of the `main.py` script, 
which by default runs SAM, OffLAM and NOLAM on every domain and associated 
set of trajectories in `benchmarks/trajectories/learning`.


[1] ["Safe Learning of Lifted Action Models", B. Juba and H. S. Le, and R. Stern, 
Proceedings of the 18th International Conference on Principles of Knowledge 
Representation and Reasoning, 2021.](https://proceedings.kr.org/2021/36/)

[2] ["Lifted Action Models Learning from Partial Traces", L. Lamanna, L. Serafini,
A. Saetti, A. Gerevini, and P. Traverso, Artificial Intelligence Journal, 
2025.](https://www.sciencedirect.com/science/article/abs/pii/S0004370224001929)

[3] ["Action Model Learning from Noisy Traces: a Probabilistic Approach", L. Lamanna 
and L. Serafini, Proceedings of the Thirty-Fourth International Conference on 
Automated Planning and Scheduling, 2024.](
https://ojs.aaai.org/index.php/ICAPS/article/view/31493)

### Adding an algorithm
PRs with new or existing state-of-the-art algorithms are welcome:

1. Create a Python class in `algorithms` which inherits from `AlgorithmAdapter.py` and implements the `learn` method
3. Add the new class import in `algorithms/.__init__.py`
4. Add either the algorithm package in `requirements.txt` or a git submodule for the new algorithm repository:
```
git submodule add https://github.com/path/to/algorithm/newalg.git algorithms/newalg
```
When using git submodules, add `sys.path.append(os.path.abspath("algorithms/newalg"))` at the top level of the 
new class file, where `newalg` is the new algorithm name.


## Evaluation

We evaluate the learned models by means of several metrics:
1. _Syntactic_ precision and recall 
   - to compute the syntactic metrics, we adopted the IPC domain models 
   as reference ones;
2. _Predicted_ applicability and effects
   - for each domain, we generated a set of 100 traces by optimally solving 
   small-sized problems and interleaving plan execution with random action 
   executions with 20% probability, such that the problem does not become 
   unfeasible.
3. _Solvability_ metrics
   - to evaluate the problem solving metrics, we generated a test set of 10 
   small/medium-sized problems

> [!NOTE]
> **Reproducibility**: the benchmark generation process and evaluation results 
> are fully reproducible.



## Benchmark Generation
The following instructions have been tested on macOS Sequoia 15.3


1. Clone [`pddl-generators` repository](https://github.com/AI-Planning/pddl-generators) into `util` directory:
```
 cd util && git clone https://github.com/AI-Planning/pddl-generators
```

2. Build all PDDL generators:
```
cd pddl-generators && ./build_all
```

3. Move the `matchingbw` generator out of `blocksworld` for the trajectory 
generator to work correctly
```
mv blocksworld/matching matchingbw
cp -r blocksworld/bwstates.1 ./
```

4. Install `requirements.txt`
```
cd ../../ && pip install -r requirements.txt
```
5. Generate trajectories:
```
cd util && python generators.py
```

6. Optionally generate trajectory statistics and plots:
```
python stats.py
```


### Domain selection
The adopted domains are the ones adopted in previous IPC learning tracks:
1. [IPC 2008 Learning Track](https://ipc08.icaps-conference.org/learning/): `goldminer`, `matchingbw`, `npuzzle`, 
`parking` and `sokoban`
> [!WARNING]
> `thoughtful`: has not been considered since there is no problem generator neither in the IPC 
> resources nor in [`pddl-generators` repository](https://github.com/AI-Planning/pddl-generators).

2. [IPC 2011 Learning Track](https://icaps11.icaps-conference.org/proceedings/pal/fawcett-et-al.pdf): `barman`, 
`blocksworld`, `depots`, `gripper`, `parking`, `rovers`, `satellite`, `spanner` and `tpp`.
3. [IPC 2014 Learning Track](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2571): `elevators`,
`floortile`, `nomystery`, `parking`, `spanner` and `transport`.
4. [IPC 2023 Learning Track](https://github.com/ipc2023-learning/benchmarks): `blocksworld`,
`childsnack`, `ferry`, `floortile`, `miconic`, `rovers`, `satellite`, `sokoban`,
`spanner` and `transport`.
> [!WARNING]
> `childsnack`: for compatibility with the problems generator, we adopted the original domain 
> version without negative preconditions.

Therefore the following set of 20 classical planning domains:


<table class="dataframe">
  <thead>
<tr style="text-align: left;">
  <th rowspan="2">Domain name</th>
  <th rowspan="2">Operators</th>
  <th rowspan="2">Predicates</th>
  <th rowspan="2">Types</th>
  <th colspan="2">Max arity</th>
  <th colspan="2">Min arity</th>
</tr>
<tr>
  <th>Operators</th>
  <th>Predicates</th>
  <th>Operators</th>
  <th>Predicates</th>
</tr>
  </thead>
  <tbody>
    <tr>
      <td>barman</td>
      <td>12</td>
      <td>15</td>
      <td>9</td>
      <td>6</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>blocksworld</td>
      <td>4</td>
      <td>5</td>
      <td>1</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <td>childsnack</td>
      <td>6</td>
      <td>13</td>
      <td>6</td>
      <td>4</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>depots</td>
      <td>5</td>
      <td>6</td>
      <td>9</td>
      <td>4</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>elevators</td>
      <td>6</td>
      <td>8</td>
      <td>5</td>
      <td>5</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <td>ferry</td>
      <td>3</td>
      <td>5</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <td>floortile</td>
      <td>7</td>
      <td>10</td>
      <td>3</td>
      <td>4</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>goldminer</td>
      <td>7</td>
      <td>12</td>
      <td>1</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <td>grippers</td>
      <td>3</td>
      <td>4</td>
      <td>4</td>
      <td>4</td>
      <td>3</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <td>matchingbw</td>
      <td>10</td>
      <td>10</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>miconic</td>
      <td>4</td>
      <td>6</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>nomystery</td>
      <td>3</td>
      <td>6</td>
      <td>5</td>
      <td>6</td>
      <td>3</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <td>npuzzle</td>
      <td>1</td>
      <td>3</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>parking</td>
      <td>4</td>
      <td>5</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>rovers</td>
      <td>9</td>
      <td>25</td>
      <td>7</td>
      <td>6</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>satellite</td>
      <td>5</td>
      <td>8</td>
      <td>4</td>
      <td>4</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>sokoban</td>
      <td>2</td>
      <td>4</td>
      <td>3</td>
      <td>5</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>spanner</td>
      <td>3</td>
      <td>6</td>
      <td>5</td>
      <td>4</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td>tpp</td>
      <td>4</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>3</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <td>transport</td>
      <td>3</td>
      <td>5</td>
      <td>6</td>
      <td>5</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
