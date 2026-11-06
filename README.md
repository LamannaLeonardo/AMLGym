# AMLGym: benchmarking action model learning
<!-- Define badges -->
<div style="display: flex; gap: 10px;">
   
  <a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" height="20"/></a>
    
  <a href="https://pypi.python.org/pypi/amlgym" target="_blank">
    <img src="https://badge.fury.io/py/amlgym.svg" height="20"/></a>
    
  <a href="https://amlgym.readthedocs.io/en/latest/" target="_blank">
    <img src="https://img.shields.io/readthedocs/amlgym/latest?label=docs" height="20"/></a>

</div>


Framework for experimenting with action model 
learning approaches and evaluating planning domain models.
AMLGym provides:
- **algorithms**: state-of-the-art passive and active action model learning algorithms;
- **benchmarks**: 20+ classical planning domains with pre-generated trajectories, problems, and test states;
- **metrics**: syntactic similarity, problem solving, and predictive power.


### Installation
```bash
pip install amlgym
```
AMLGym requires Python 3.10 or later.

### Example usage
Learn a domain model from a set of trajectories (passive learning):
```python
from amlgym.algorithms import get_algorithm
from amlgym.benchmarks import get_domain_path, get_trajectories_path
from amlgym.util.util import empty_domain

# Input domain: types, constants, predicates, and operator signatures, with no preconditions and effects
domain_path = get_domain_path('blocksworld')
input_domain_path = empty_domain(domain_path)

# Learn a domain model from the benchmark trajectories
agent = get_algorithm('OffLAM')
model = agent.learn(input_domain_path, get_trajectories_path('blocksworld'))
print(model)
```
To learn from your custom data, pass your PDDL domain path and a list of trajectory file paths to `learn`.

Learn a domain model by interacting with a simulator (active learning):
```python
from unified_planning.io import PDDLReader
from unified_planning.shortcuts import SequentialSimulator
from amlgym.algorithms import get_algorithm
from amlgym.benchmarks import get_domain_path, get_problems_path
from amlgym.util.util import empty_domain

domain_path = get_domain_path('blocksworld')
problem_path = get_problems_path('blocksworld', kind='learning')[0]
simulator = SequentialSimulator(problem=PDDLReader().parse_problem(domain_path, problem_path))

agent = get_algorithm('OLAM', input_domain_path=empty_domain(domain_path))
model, trajectory = agent.learn(simulator, max_steps=100)
print(model)
```

### Documentation
Tutorials and API documentation are available on [Read the Docs](https://amlgym.readthedocs.io/en/latest/).


## State-of-the-art Algorithms
AMLGym provides seamless integration with state-of-the-art algorithms 
for learning classical planning domains, either offline from an input set of 
trajectories (**passive**) or online by interacting with a simulator (**active**):

| Algorithm       | Learning | Observability | Noisy states | Reference                                      |
|-----------------|----------|---------------|-------------|------------------------------------------------|
| `SAM`           | passive  | full          | No          | [1]                                            |
| `OffLAM`        | passive  | partial       | No          | [2]                                            |
| `NOLAM`         | passive  | full          | Yes         | [3]                                            |
| `ROSAME`        | passive  | full          | Yes         | [4]                                            |
| `OLAM`          | active   | full          | No          | [5]                                            |
| `RandomAgent`   | active   | full          | No          | baseline: random exploration followed by SAM  |

Active algorithms assume a fully observable and deterministic environment.
Run `from amlgym.algorithms import print_algorithms; print_algorithms()` to list
the available algorithms with their parameters.

[1] ["Safe Learning of Lifted Action Models"](https://proceedings.kr.org/2021/36/), B. Juba, H. S. Le, and R. Stern, 
Proceedings of the 18th International Conference on Principles of Knowledge 
Representation and Reasoning, 2021.

[2] ["Lifted Action Models Learning from Partial Traces"](https://www.sciencedirect.com/science/article/abs/pii/S0004370224001929), 
L. Lamanna, L. Serafini, A. Saetti, A. Gerevini, and P. Traverso, Artificial Intelligence Journal, 2025.

[3] ["Action Model Learning from Noisy Traces: a Probabilistic Approach"](https://ojs.aaai.org/index.php/ICAPS/article/view/31493), 
L. Lamanna and L. Serafini, Proceedings of the Thirty-Fourth International Conference on 
Automated Planning and Scheduling, 2024.

[4] ["Neuro-Symbolic Learning of Lifted Action Models from Visual Traces"](https://ojs.aaai.org/index.php/ICAPS/article/download/31528/33688), 
K. Xi, S. Gould, and S. Thiébaux, Proceedings of the Thirty-Fourth International Conference on 
Automated Planning and Scheduling, 2024.

[5] ["Online Learning of Action Models for PDDL Planning"](https://doi.org/10.24963/ijcai.2021/566), 
L. Lamanna, A. Saetti, L. Serafini, A. Gerevini, and P. Traverso, Proceedings of the Thirtieth 
International Joint Conference on Artificial Intelligence, 2021.


### Adding an algorithm
PRs with new or existing state-of-the-art algorithms are welcome:

1. Create `amlgym/algorithms/YourAlgorithm.py` with a class named `YourAlgorithm` (same as the file name) that
   inherits from `PassiveAlgorithmAdapter` (learning from trajectory files) or `ActiveAlgorithmAdapter`
   (learning by interacting with a simulator) and implements the `learn` method.
2. Add the algorithm PyPI package (if any) to `requirements.txt`.

No registration is needed: algorithms are discovered automatically and available via `get_algorithm('YourAlgorithm')`.
`OffLAM.py` and `OLAM.py` are reference implementations of a passive and an active algorithm, respectively.
The `/add-passive-algorithm` and `/add-active-algorithm` 
skills guide you through the integration.


## Evaluation

AMLGym can evaluate a planning domain model with respect to a reference model by means of several metrics (`amlgym.metrics`):
1. _Syntactic similarity_: precision and recall of the learned preconditions and effects
   (`syntactic_precision`, `syntactic_recall`).
2. _Problem solving_: ratio of problems solved with the learned model, where plans are validated
   in the reference model (`problem_solving`).
3. _Predicted applicability and predicted effects_: agreement between the learned and reference models on
   action applicability and effects over a set of test states (`applicability`, `predicted_effects`,
   or `predictive_power` for both).

```python
from amlgym.benchmarks import get_domain_path, get_problems_path
from amlgym.metrics import syntactic_precision, syntactic_recall, problem_solving

with open('learned.pddl', 'w') as f:
    f.write(model)

domain_path = get_domain_path('blocksworld')
print(syntactic_precision('learned.pddl', domain_path))
print(syntactic_recall('learned.pddl', domain_path))
print(problem_solving('learned.pddl', domain_path, get_problems_path('blocksworld')))
```

## Benchmarking
AMLGym includes 20+ classical planning domains, most of them from the IPC learning tracks.
Domains, trajectories, problems, and test states are accessible through `amlgym.benchmarks`,
see the [benchmark](https://github.com/LamannaLeonardo/AMLGym/blob/main/amlgym/benchmarks/README.md) package for details.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/LamannaLeonardo/AMLGym/blob/main/LICENSE.md) file for details.

## Citing
Not yet available
