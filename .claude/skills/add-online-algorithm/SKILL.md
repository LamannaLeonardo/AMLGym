---
name: add-online-algorithm
description: Add a new online learning algorithm to AMLGym. Use when the user wants to integrate an algorithm that interacts with a simulator to collect its own experience.
---

# Add an Online Algorithm

Create a new online algorithm adapter in `amlgym/algorithms/`.

## Steps

1. **Create** `amlgym/algorithms/$ARGUMENTS.py` (class name must match filename, PascalCase, case-insensitive)

2. **Inherit** from `OnlineAlgorithmAdapter` and implement `learn()`:

```python
from dataclasses import dataclass
from typing import Tuple
from unified_planning.shortcuts import SequentialSimulator
from amlgym.algorithms.OnlineAlgorithmAdapter import OnlineAlgorithmAdapter
from amlgym.modeling.trajectory import Trajectory

@dataclass
class $ARGUMENTS(OnlineAlgorithmAdapter):
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
        #     Wrap with try/except UPInvalidActionError (from unified_planning.exceptions)
        #
        # Return: (learned_pddl_string, Trajectory(states_list, actions_list))
        ...
```

3. **Add external dependencies** to `requirements.txt` if needed

4. **No registration needed** — `amlgym/algorithms/__init__.py` auto-discovers all algorithm files

## Reference implementation

Study `amlgym/algorithms/RandomAgent.py` for the canonical online adapter pattern:
- Grounding actions via `tarski.LPGroundingStrategy` (requires `clingo`)
- Interacting with the simulator to collect trajectories
- Filtering failed actions (`simulator.apply()` returns `None` for inapplicable actions, but may also raise `UPInvalidActionError` — always wrap in try/except)
- Building a `Trajectory` from collected states and actions
- Optionally delegating to an offline learner (e.g., `SAM`) for model extraction

## Key utilities

- `amlgym/modeling/trajectory.py` — `Trajectory(states, actions)` dataclass with `.write()` method
- `amlgym/util/util.py` — `empty_domain()` strips preconditions/effects, `fix_domain_format()` normalizes hyphens
- Action grounding: use `tarski.LPGroundingStrategy` + `convert_problem_to_tarski()` (see `RandomAgent._ground_actions()`)

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

agent = get_algorithm('$ARGUMENTS')
model, trajectory = agent.learn(simulator, input_domain)

# Write learned model and evaluate
with open('learned.pddl', 'w') as f:
    f.write(model)
print("Precision:", syntactic_precision('learned.pddl', domain_path))
print("Recall:", syntactic_recall('learned.pddl', domain_path))
```
