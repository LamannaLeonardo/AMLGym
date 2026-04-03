# AMLGym - Project Guide

AMLGym is a benchmarking framework for **Action Model Learning (AML)** — learning classical planning domain models (PDDL) from execution traces. It provides state-of-the-art algorithms, 25 benchmark domains, and evaluation metrics.

**Primary workflow in this repo**: integrating and assessing new learning algorithms (passive or active) within the framework.

## Codebase Exploration Guide

```
amlgym/
├── algorithms/                  # All learning algorithms live here
│   ├── __init__.py              # Auto-registration registry, get_algorithm()
│   ├── PassiveAlgorithmAdapter.py  # Base class for passive algorithms
│   ├── ActiveAlgorithmAdapter.py   # Base class for active algorithms
│   ├── SAM.py                   # Full observability (passive)
│   ├── OffLAM.py                # Partial observability (passive)
│   ├── NOLAM.py                 # Noisy observations (passive)
│   ├── ROSAME.py                # Neuro-symbolic (passive)
│   ├── rosame/                  # ROSAME's internal implementation
│   ├── RandomAgent.py           # Active baseline (random exploration + SAM)
│   └── InformationGainAgent.py  # Full observability (active)
├── benchmarks/
│   ├── __init__.py              # API: get_domain_path(), get_trajectories_path(), etc.
│   ├── domains/                 # 25 PDDL domain files
│   ├── trajectories/            # Pre-generated traces (learning, applicability, etc.)
│   ├── problems/                # PDDL problem files per domain
│   ├── states/                  # Test states for predictive metrics
│   ├── problems_learning.yaml   # Problem generation configs
│   ├── problems_solving.yaml
│   ├── problems_applicability.yaml
│   └── problems_predictive_power.yaml
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
    └── util.py                  # empty_domain(), fix_domain_format(), etc.
```

### Key files for algorithm integration
- `amlgym/algorithms/PassiveAlgorithmAdapter.py` — base class for passive algorithms
- `amlgym/algorithms/ActiveAlgorithmAdapter.py` — base class for active algorithms
- `amlgym/algorithms/SAM.py` — reference implementation of an passive algorithm
- `amlgym/algorithms/RandomAgent.py` — reference implementation of an active algorithm
- `amlgym/algorithms/__init__.py` — auto-discovery registry (no modification needed)
- `amlgym/modeling/trajectory.py` — `Trajectory` dataclass (used by active `learn()`)
- `amlgym/modeling/UPEnv.py` — environment wrapper with `apply()` and `applicable_actions()`

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
class RandomAgent(ActiveAlgorithmAdapter):
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

### Passive learning
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

### Active learning
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
- **Passive** (learns from trajectory files): `/add-passive-algorithm YourAlgorithm`
- **Active** (interacts with simulator): `/add-active-algorithm YourAlgorithm`

Key points:
- Create `amlgym/algorithms/YourAlgorithm.py` — class name must match filename (PascalCase, case-insensitive)
- Inherit from `PassiveAlgorithmAdapter` or `ActiveAlgorithmAdapter` and implement `learn()`
- No registration needed — `__init__.py` auto-discovers all algorithm files
- Add external deps to `requirements.txt` if needed
- Evaluate with `amlgym.metrics` against reference domain models
- Reference implementations: `SAM.py` (passive), `RandomAgent.py` (active)

## Important Notes

### Dependencies
- Python 3.10+
- Core: `unified-planning` (simulation/PDDL), `tarski` (grounding), `pddl-plus-parser`
- Algorithms: `n-sam`, `offlam`, `nolam` (external PyPI packages)
- Install: `pip install amlgym` or `pip install -r requirements.txt`

### Conventions
- Algorithm class name **must** match its filename (e.g., `MyAgent` in `MyAgent.py`)
- `empty_domain()` creates the input domain with preconditions/effects stripped — this is what algorithms receive as input
- The `learn()` return type is `str` (PDDL domain) for passive algorithms and `Tuple[str, Trajectory]` for active algorithms
- Trajectories use PDDL-like format: alternating `(:state ...)` and `(:action ...)` blocks
- States in the simulator are `UPState` objects; use `str()` and regex to extract literals

### Gotchas
- `unified-planning` doesn't handle hyphens in names well — the framework normalizes to underscores (see `fix_domain_format()`)
- Action grounding uses `tarski.LPGroundingStrategy` — requires `clingo` ASP solver
- `simulator.apply()` returns `None` for inapplicable actions (not an exception)
- Some algorithms write temp files (`tmp.pddl`, `tmp_trajectory`) to cwd — these are cleaned up but be aware during debugging
- No unit test suite exists; validation is done via benchmark evaluation and notebooks in `docs/source/tutorials_*`

### Available benchmark domains (25)
barman, blocksworld, childsnack, depots, driverlog, elevators, ferry, floortile, goldminer, grid, grippers, hanoi, matchingbw, miconic, nomystery, npuzzle, parking, rovers, satellite, sokoban, spanner, tpp, transport, visitall, zenotravel
