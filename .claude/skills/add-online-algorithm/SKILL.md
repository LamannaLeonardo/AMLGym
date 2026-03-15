---
name: add-online-algorithm
description: Add a new online learning algorithm to AMLGym. Use when the user wants to integrate an algorithm that interacts with a simulator to collect its own experience.
argument-hint: "[AlgorithmName or description]"
---

# Add an Online Algorithm

Create a new online algorithm adapter in `amlgym/algorithms/`.

## Context gathering

Before writing any code:

1. **Get from the user**: package name or repo path, and optionally a paper reference
2. **Explore the algorithm's code** to determine:
   - Main class and import path (e.g., `from information_gain_aml.algorithms import InformationGainLearner`)
   - Constructor signature (domain file? problem file? config params?)
   - Action selection method (e.g., `select_action(state) -> (action_name, objects)`)
   - Observation/update method (e.g., `observe(state, action, objects, success, next_state)`)
   - Model export method (e.g., `to_pddl_string() -> str`)
   - Convergence check if available (e.g., `has_converged() -> bool`)
   - What state/action format the algorithm expects (e.g., `Set[str]`, UP objects, custom types)
3. If exploration is insufficient, ask the user targeted questions about specific API details

## Steps

1. **Create** `amlgym/algorithms/<AlgorithmName>.py`

   Replace `<AlgorithmName>` with the PascalCase name for your algorithm (e.g., `ESAM`, `MyNewAgent`). This becomes both the filename and class name. The name matching is case-insensitive.

2. **Inherit** from `OnlineAlgorithmAdapter` and implement `learn()`:

```python
from dataclasses import dataclass
from typing import Tuple
from unified_planning.shortcuts import SequentialSimulator
from amlgym.algorithms.OnlineAlgorithmAdapter import OnlineAlgorithmAdapter
from amlgym.modeling.trajectory import Trajectory

@dataclass
class <AlgorithmName>(OnlineAlgorithmAdapter):
    """Docstring with paper reference and usage example."""

    # Optional: add paper reference metadata (used by registry for display)
    # _reference: ClassVar[OrderedDict[str, str]] = {
    #     'Authors': "Author names",
    #     'Title': "Paper title",
    #     'Venue': "Conference/journal",
    #     'Year': "2024",
    #     'URL': "https://...",
    # }

    # Algorithm parameters as dataclass fields with defaults
    max_steps: int = 100

    def learn(self,
              simulator: SequentialSimulator,
              input_domain_path: str,
              seed: int = 123) -> Tuple[str, Trajectory]:
        # simulator: environment to interact with
        # input_domain_path: PDDL domain with predicates/operator signatures (no preconditions/effects)
        # seed: random seed for reproducibility
        #
        # Key simulator methods:
        #   simulator.get_initial_state() -> UPState
        #   simulator.apply(state, action) -> UPState or None (if inapplicable)
        #
        # Return: (learned_pddl_string, Trajectory(states_list, actions_list))
        ...
```

3. **Add external dependencies** to `requirements.txt` if needed

4. **No registration needed** — `amlgym/algorithms/__init__.py` auto-discovers all algorithm files

## Reference implementations

Study these two adapters for different integration patterns:

**`amlgym/algorithms/RandomAgent.py`** — random exploration baseline:
- baselinr implementation - sets a basic example for inheriting the `OnlineAlgorithmAdapter` class.
- Grounds all actions via `tarski.LPGroundingStrategy` (requires `clingo`)
- Randomly selects and executes actions, collecting a trajectory
- Filters failed actions, then delegates to offline SAM learner for model extraction

**`amlgym/algorithms/InformationGainAgent.py`** — active learning with external package:
- Integrates an external PyPI package (`information-gain-aml`)
- Converts UP states to algorithm's expected format using the algorithm's own converter (importable `UPAdapter`)
- Writes temp problem file from `simulator._problem` (see "Accessing simulator internals")
- Handles success/failure observations separately
- Constructs `ActionInstance` from algorithm's `(action_name, objects)` output

## Key utilities

- `amlgym/modeling/trajectory.py` — `Trajectory(states, actions)` dataclass with `.write()` method
- `amlgym/util/util.py` — `empty_domain()` strips preconditions/effects, `fix_domain_format()` normalizes hyphens
- `amlgym/modeling/UPEnv.py` — `UPEnv(domain_path, problem_path)` environment wrapper (needed for predictive metrics)
- `unified_planning.io.PDDLWriter` — write temp problem files from `simulator._problem`
- `unified_planning.plans.ActionInstance` — construct actions for `simulator.apply()`
- Action grounding: use `tarski.LPGroundingStrategy` + `convert_problem_to_tarski()` (see `RandomAgent._ground_actions()`)

> See `docs/pddl-format-spec.md` for normalization rules, trajectory format, and output post-processing.

## Accessing simulator internals

The `SequentialSimulator` API only exposes `get_initial_state()` and `apply()`, but adapters typically need more. Use these undocumented but required patterns:

**Getting the UP Problem** (for object/action/fluent lookups):
```python
problem = simulator._problem
```

**Writing a temp problem file** (when the algorithm requires file paths for initialization):
```python
import tempfile
from unified_planning.io import PDDLWriter

with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = f"{tmpdir}/problem.pddl"
    PDDLWriter(simulator._problem).write_problem(tmp_path)
    # ... use tmp_path for algorithm initialization ...
# tmpdir auto-cleaned
```

**Creating ActionInstance from algorithm output:**
```python
from unified_planning.plans import ActionInstance

action_name, objects = algorithm.select_action(state)  # e.g., ("pick_up", ["b1"])
up_action = problem.action(action_name)
up_objects = tuple(problem.object(o) for o in objects)
action_instance = ActionInstance(up_action, up_objects)
```

**Handling inapplicable actions:**
```python
next_state = simulator.apply(state, action_instance)
if next_state is None:
    # Action was inapplicable — no exception raised
    algorithm.observe(state, action_name, objects, success=False, next_state=None)
```

## What to look for in the algorithm's API

When exploring the algorithm's code, identify these components:

| Component | What to find | Example |
|-----------|-------------|---------|
| Initialization | Constructor params — domain file? problem file? config? | `Learner(domain_file, problem_file)` |
| Action selection | Method that picks next action given current state | `select_action(state) -> (name, objects)` |
| Observation | Method to update model after executing action | `observe(state, action, success, next_state)` |
| Export | How to get PDDL string out | `to_pddl_string() -> str` |
| Convergence | Optional early stopping check | `has_converged() -> bool` |

The adapter's job: handle all UP-specific conversions (states, actions, temp files). For state conversion, prefer the algorithm's own converter if available (see `InformationGainAgent.py` for an example). If none exists, inspect `str(up_state)` output to understand the format and write a custom converter.

## Common integration challenges

**1. Action grounding:**
The simulator does not expose ground actions. To enumerate all possible actions, use tarski (requires `clingo`). See `RandomAgent._ground_actions()` for the full pattern, including a dummy-fluent workaround needed to make tarski grounding work with empty preconditions/effects.

**2. Domain output post-processing:**
See "PDDL Conventions" in CLAUDE.md for common output fixes (domain name suffix, hyphen normalization).

**3. Temp file cleanup:**
Both reference implementations write temp files. Always use `try/finally` to ensure cleanup, even if the algorithm raises an exception.

**4. Trajectory construction:**
`Trajectory(states, actions)` expects `states` to have length `len(actions) + 1` (includes initial state). States may contain `None` entries where actions were inapplicable.

## Testing

```python
from unified_planning.io import PDDLReader
from unified_planning.shortcuts import SequentialSimulator
from amlgym.algorithms import get_algorithm
from amlgym.benchmarks import get_domain_path, get_problems_path
from amlgym.util.util import empty_domain
from amlgym.metrics import syntactic_precision, syntactic_recall

domain = 'blocksworld'
domain_path = get_domain_path(domain)
input_domain = empty_domain(domain_path)
problem_path = get_problems_path(domain, kind='learning')[0]
problem = PDDLReader().parse_problem(domain_path, problem_path)
simulator = SequentialSimulator(problem=problem)

agent = get_algorithm('<AlgorithmName>')
model, trajectory = agent.learn(simulator, input_domain)

# Write learned model and evaluate
with open('learned.pddl', 'w') as f:
    f.write(model)
print("Precision:", syntactic_precision('learned.pddl', domain_path))
print("Recall:", syntactic_recall('learned.pddl', domain_path))
```

## Checklist

- [ ] File name matches class name (PascalCase, case-insensitive)
- [ ] Inherits from `OnlineAlgorithmAdapter`
- [ ] Implements `learn(simulator, input_domain_path, seed) -> Tuple[str, Trajectory]`
- [ ] Learned PDDL uses underscores (not hyphens) and lowercase
- [ ] Temp files are cleaned up in `finally` blocks
- [ ] `Trajectory` constructed from `(states_list, actions_list)` — states includes initial state
- [ ] Algorithm parameters are dataclass fields with defaults
- [ ] External dependencies added to `requirements.txt`
- [ ] Tested against at least one benchmark domain (e.g., blocksworld)
