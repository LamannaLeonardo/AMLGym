# AMLGym - Project Guide

AMLGym is a benchmarking framework for **Action Model Learning (AML)** — learning classical planning domain models (PDDL) from execution traces. It provides state-of-the-art algorithms, 25 benchmark domains, and evaluation metrics.

**Primary workflow in this repo**: integrating and assessing new learning algorithms (offline or online) within the framework.

## Codebase Exploration Guide

```
amlgym/
├── algorithms/                  # All learning algorithms live here
│   ├── __init__.py              # Auto-registration registry, get_algorithm()
│   ├── OfflineAlgorithmAdapter.py  # Base class for offline algorithms
│   ├── OnlineAlgorithmAdapter.py   # Base class for online algorithms
│   ├── SAM.py                   # Full observability (offline)
│   ├── OffLAM.py                # Partial observability (offline)
│   ├── NOLAM.py                 # Noisy observations (offline)
│   ├── ROSAME.py                # Neuro-symbolic (offline)
│   ├── rosame/                  # ROSAME's internal implementation
│   ├── RandomAgent.py           # Online baseline (random exploration + SAM)
│   └── InformationGainAgent.py  # Full observability (online)
├── benchmarks/
│   ├── __init__.py              # API: get_domain_path(), get_trajectories_path(), etc.
│   ├── domains/                 # 25 PDDL domain files
│   ├── trajectories/            # Pre-generated traces (learning, applicability, etc.)
│   ├── problems/                # PDDL problem files per domain
│   ├── states/                  # Test states for predictive metrics
│   └── problems_*.yaml          # Problem/trajectory generation configs
├── metrics/
│   ├── __init__.py              # Exports all metrics
│   ├── _syntactic.py            # syntactic_precision(), syntactic_recall()
│   ├── _solving.py              # problem_solving()
│   └── _predictive.py           # applicability(), predicted_effects(), predictive_power()
├── modeling/
│   ├── env.py                   # Abstract Env base class
│   ├── UPEnv.py                 # Concrete environment (wraps unified-planning simulator)
│   └── trajectory.py            # Trajectory dataclass (states + actions)
└── util/
    ├── util.py                  # empty_domain(), fix_domain_format(), etc.
    ├── SimpleDomainReader.py    # Custom PDDL parser for syntactic metrics
    ├── gen_problems.py          # Benchmark problem generation
    ├── gen_trajs_learning.py    # Learning trajectory generation
    ├── gen_trajs_learning_hard.py # Hard learning trajectory generation
    ├── gen_trajs_predictability.py  # Predictive power trajectory generation
    ├── gen_probs_solving.py     # Solving problem generation
    └── gen_states_predictability.py # Test state generation
```

### Key files for algorithm integration
- `amlgym/algorithms/OfflineAlgorithmAdapter.py` — base class for offline algorithms
- `amlgym/algorithms/OnlineAlgorithmAdapter.py` — base class for online algorithms
- `amlgym/algorithms/SAM.py` — reference offline adapter
- `amlgym/algorithms/RandomAgent.py` — reference online adapter
- `amlgym/algorithms/__init__.py` — auto-discovery registry (no modification needed)
- `amlgym/modeling/trajectory.py` — `Trajectory` dataclass (used by online `learn()`)
- `amlgym/modeling/UPEnv.py` — environment wrapper with `apply()` and `applicable_actions()`

## Development Setup

- Python 3.10+, pip-based
- Install for development: `pip install -e .` then `pip install -r requirements.txt`
- `clingo` ASP solver required (used by `tarski` for action grounding in online algorithms; installation can be tricky on macOS)
- ROSAME has its own setup: `amlgym/algorithms/rosame/setup.py`
- Core deps: `unified-planning` (simulation/PDDL), `tarski` (grounding), `pddl-plus-parser`
- Algorithm deps: `n-sam`, `offlam`, `nolam`, `information-gain-aml` (external PyPI packages)

## Configuration

### Benchmark configs (YAML)
Located in `amlgym/benchmarks/problems_*.yaml`. These define problem generation parameters per domain:
```yaml
SEED: 123
domains:
  blocksworld:
    - ops: 4
      num: 3   # number of blocks
    - ops: 4
      num: 4
```

### Algorithm parameters
Algorithms are Python dataclasses — parameters are fields with defaults:
```python
@dataclass
class RandomAgent(OnlineAlgorithmAdapter):
    max_steps: int = 100
```
Pass params via `get_algorithm('RandomAgent', max_steps=200)` or direct instantiation.

### Benchmark data access
```python
from amlgym.benchmarks import (
    get_domain_names,       # list all 25 domain names
    get_domain_path,        # absolute path to a domain PDDL file
    get_trajectories_path,  # list of trajectory file paths
    get_problems_path,      # list of problem file paths
    get_test_states,        # test states dict for predictive metrics
)
# `kind` param: 'learning', 'applicability', 'predictive_power', 'solving'
```

## Experimenting

### Offline learning
```python
from amlgym.algorithms import get_algorithm
from amlgym.benchmarks import get_domain_path, get_trajectories_path
from amlgym.util.util import empty_domain

agent = get_algorithm('OffLAM')
domain_path = get_domain_path('blocksworld')
input_domain = empty_domain(domain_path)  # strips preconditions/effects
traj_paths = get_trajectories_path('blocksworld')
model = agent.learn(input_domain, traj_paths)
```

### Online learning
```python
from unified_planning.io import PDDLReader
from unified_planning.shortcuts import SequentialSimulator
from amlgym.algorithms import get_algorithm
from amlgym.benchmarks import get_domain_path, get_problems_path
from amlgym.util.util import empty_domain

domain_path = get_domain_path('blocksworld')
input_domain = empty_domain(domain_path)
problem_path = get_problems_path('blocksworld', kind='learning')[0]
problem = PDDLReader().parse_problem(domain_path, problem_path)
simulator = SequentialSimulator(problem=problem)

agent = get_algorithm('RandomAgent')
model, trajectory = agent.learn(simulator, input_domain)
```

### Evaluation
```python
from amlgym.metrics import syntactic_precision, syntactic_recall, problem_solving
from amlgym.metrics import applicability, predicted_effects, predictive_power

# Syntactic (compare learned vs reference PDDL)
precision = syntactic_precision('learned.pddl', 'reference.pddl')
recall = syntactic_recall('learned.pddl', 'reference.pddl')

# Problem solving (can the learned model solve benchmark problems?)
results = problem_solving('learned.pddl', 'reference.pddl', problem_paths, timeout=60)
# Returns: solving_ratio, false_plans_ratio, unsolvable_ratio, timed_out, syntax_errors

# Predictive metrics (applicability + effect prediction accuracy)
results = predictive_power(simulator_learned, simulator_ref, test_states)
```

## Adding a New Algorithm

Use the Claude Code skills for guided workflows:
- **Offline** (learns from trajectory files): `/add-offline-algorithm YourAlgorithm`
- **Online** (interacts with simulator): `/add-online-algorithm YourAlgorithm`

The skills cover context gathering, step-by-step implementation, PDDL normalization, integration challenges, and testing checklists.

Key points:
- Create `amlgym/algorithms/YourAlgorithm.py` — class name must match filename (PascalCase, case-insensitive)
- Inherit from `OfflineAlgorithmAdapter` or `OnlineAlgorithmAdapter` and implement `learn()`
- No registration needed — `__init__.py` auto-discovers all algorithm files
- Evaluate with `amlgym.metrics` against reference domain models

## Validation

No pytest test suite — validation is done via notebooks:

| Notebook | What it validates |
|----------|-------------------|
| `notebooks/test_information_gain.ipynb` | End-to-end online algorithm (all 3 metric types) |
| `docs/source/tutorials_learning/offline_algorithms.ipynb` | Offline algorithm usage |
| `docs/source/tutorials_learning/online_algorithms.ipynb` | Online algorithm usage |
| `docs/source/tutorials_evaluating/syntactic.ipynb` | Syntactic precision/recall metrics |
| `docs/source/tutorials_evaluating/predictive.ipynb` | Predictive power metrics |
| `docs/source/tutorials_evaluating/problem_solving.ipynb` | Problem solving metrics |

After modifying metrics, environments, or utility code, run the relevant notebooks to verify.

## Contributing

- Branch naming: `feature/topic` style (e.g., `information-gain/main`, `keps-2025`)
- No CI/CD — validate manually with notebooks before submitting PR
- No code quality tools configured (no linter, no mypy, no formatter)
- Algorithm adapters: use the `/add-offline-algorithm` or `/add-online-algorithm` skills
- Metrics, environments, and utilities: study existing code and validate with notebooks
- Some algorithms write temp files (`tmp.pddl`, `tmp_trajectory`) to cwd during execution — these are cleaned up but be aware during debugging

## Available benchmark domains (25)
barman, blocksworld, childsnack, depots, driverlog, elevators, ferry, floortile, goldminer, grid, grippers, hanoi, matchingbw, miconic, nomystery, npuzzle, parking, rovers, satellite, sokoban, spanner, tpp, transport, visitall, zenotravel
