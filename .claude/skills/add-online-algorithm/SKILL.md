---
name: add-online-algorithm
description: Add a new online learning algorithm to AMLGym. Use when the user wants to integrate an algorithm that interacts with a simulator to collect its own experience.
argument-hint: "[AlgorithmName or description]"
---

# Add an Online Algorithm

Create a new online algorithm adapter in `amlgym/algorithms/`.

## Context gathering

Before writing any code, gather the following information from the user. If the user provides a repo path or package, explore it to find this information automatically.

1. **Package name** — PyPI package or local repo path (e.g., `pip install information-gain-aml` or `/path/to/repo`)
2. **Main algorithm class and import path** — e.g., `from information_gain_aml.algorithms import InformationGainLearner`
3. **Key methods the algorithm exposes**:
   - Init signature (what does the constructor need — domain file? problem file? config params?)
   - Action selection method (e.g., `select_action(state) -> (action_name, objects)`)
   - Observation/update method (e.g., `observe(state, action, objects, success, next_state)`)
   - Model export method (e.g., `to_pddl_string() -> str`)
   - Convergence check (optional, e.g., `has_converged() -> bool`)
4. **PDDL library** — does it use `pddl-plus-parser`, `unified-planning`, or something else?
5. **State/action format** — what format does the algorithm expect states in? (e.g., `Set[str]` like `{"on_a_b"}`, UP `State` objects, `pddl_plus_parser.models.State`)
6. **Paper reference** (optional) — for the `_reference` metadata field

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
- Grounds all actions via `tarski.LPGroundingStrategy` (requires `clingo`)
- Randomly selects and executes actions, collecting a trajectory
- Filters failed actions, then delegates to offline SAM learner for model extraction
- Shows the tarski grounding pattern with dummy-fluent workaround

**`amlgym/algorithms/InformationGainAgent.py`** — active learning with external package:
- Imports `InformationGainLearner` from `information-gain-aml` PyPI package
- Converts UP states to algorithm's `Set[str]` format via `UPAdapter.up_state_to_fluent_set()`
- Writes temp problem file from `simulator._problem` (see "Accessing simulator internals")
- Handles success/failure observations separately
- Uses convergence detection (`"no_action"` return) for early termination
- Constructs `ActionInstance` from algorithm's `(action_name, objects)` output

## Key utilities

- `amlgym/modeling/trajectory.py` — `Trajectory(states, actions)` dataclass with `.write()` method
- `amlgym/util/util.py` — `empty_domain()` strips preconditions/effects, `fix_domain_format()` normalizes hyphens
- `amlgym/modeling/UPEnv.py` — `UPEnv(domain_path, problem_path)` environment wrapper (needed for predictive metrics)
- `unified_planning.io.PDDLWriter` — write temp problem files from `simulator._problem`
- `unified_planning.plans.ActionInstance` — construct actions for `simulator.apply()`
- Action grounding: use `tarski.LPGroundingStrategy` + `convert_problem_to_tarski()` (see `RandomAgent._ground_actions()`)

## PDDL normalization rules

All benchmark domains are pre-normalized: hyphens replaced with underscores, all lowercase (via `fix_domain_format()` in `amlgym/util/util.py`). Example: `pick-up` becomes `pick_up`.

**Your learned PDDL output must match this convention**, or syntactic metrics will silently produce wrong results (predicate names in preconditions/effects are compared verbatim and won't match if they use hyphens instead of underscores).

What must match:
- **Action names**: underscores, lowercase (e.g., `pick_up`, not `pick-up`)
- **Predicate names**: underscores, lowercase (e.g., `on_table`, not `on-table`)
- **Type names**: underscores, lowercase

What doesn't matter:
- **Parameter names**: `SimpleDomainReader` (used by syntactic metrics) normalizes all parameter names to `?param_1`, `?param_2`, etc. So `?x` vs `?block1` doesn't affect evaluation.

Safe normalization pattern for the output PDDL:
```python
import re
# Only replace hyphens between word characters (preserves PDDL keywords like :pre-condition)
normalized = re.sub(r'(?<=\w)-(?=\w)', '_', learned_pddl)
normalized = normalized.lower()
```

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

## Algorithm interface recommendations

For maximum modularity between the algorithm library and the AMLGym adapter, the algorithm should expose:

| Method | Purpose |
|--------|---------|
| `__init__(domain_file, problem_file, **params)` | Init from PDDL files |
| `select_action(state) -> (name, objects)` | Choose next action to execute |
| `observe(state, action, objects, success, next_state)` | Update model from observation |
| `to_pddl_string() -> str` | Export learned model as PDDL |
| `has_converged() -> bool` | Check if learning is done (optional) |

**Key principle**: the adapter handles all UP-specific conversions (states, actions, temp files). The algorithm stays framework-agnostic (works with strings/sets, not UP types). This means algorithm improvements (new PyPI versions) don't require AMLGym adapter changes.

**State conversion in the adapter** (UP → algorithm format):

If the algorithm provides its own converter, use it — it will handle edge cases correctly:
```python
# Preferred: use the algorithm's own converter
from my_algorithm import StateConverter
state_set = StateConverter.from_up_state(up_state, problem)
```

Fallback regex approach if no converter is available:
```python
# Fallback: extract literals from UP state string representation
import re
state_str = str(up_state)
literals = set(re.findall(r'(\w+(?:\([^\)]*\))?)\s*:\s*true', state_str))
```

> **Note:** This regex depends on `unified-planning`'s `str()` format for states, which may change across versions. Prefer the algorithm's own converter when available.

## Common integration challenges

**1. Action grounding:**
The simulator does not expose ground actions. To enumerate all possible actions, use tarski (requires `clingo`). See `RandomAgent._ground_actions()` for the full pattern, including a dummy-fluent workaround needed to make tarski grounding work with empty preconditions/effects.

**2. Domain name suffix:**
`PDDLWriter` may append `-domain` to the domain name. If your output needs to match the input domain name, post-process:
```python
domain_str = domain_str.replace(f"(domain {name}-domain)", f"(domain {name})")
```

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
