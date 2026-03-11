---
name: add-offline-algorithm
description: Add a new offline learning algorithm to AMLGym. Use when the user wants to integrate an algorithm that learns from pre-collected trajectory files.
---

# Add an Offline Algorithm

Create a new offline algorithm adapter in `amlgym/algorithms/`.

## Steps

1. **Create** `amlgym/algorithms/$ARGUMENTS.py` (class name must match filename, PascalCase, case-insensitive)

2. **Inherit** from `OfflineAlgorithmAdapter` and implement `learn()`:

```python
from dataclasses import dataclass
from typing import List
from amlgym.algorithms.OfflineAlgorithmAdapter import OfflineAlgorithmAdapter

@dataclass
class $ARGUMENTS(OfflineAlgorithmAdapter):
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
    my_param: float = 1.0

    def learn(self,
              domain_path: str,
              trajectory_paths: List[str]) -> str:
        # domain_path: input PDDL domain with predicates/operator signatures (no preconditions/effects)
        # trajectory_paths: list of trajectory file paths
        # Return: learned PDDL domain string
        ...
```

3. **Add external dependencies** to `requirements.txt` if needed

4. **No registration needed** — `amlgym/algorithms/__init__.py` auto-discovers all algorithm files

## Reference implementation

Study `amlgym/algorithms/SAM.py` for the canonical offline adapter pattern:
- Preprocessing trajectories into algorithm-specific format
- Invoking the learning algorithm
- Cleaning up temp files
- Returning the learned PDDL model as a string

## Trajectory format

Trajectory files use PDDL-like format with alternating `(:state ...)` and `(:action ...)` blocks.
See `amlgym/benchmarks/trajectories/` for examples.

## Testing

```python
from amlgym.algorithms import get_algorithm
from amlgym.benchmarks import get_domain_path, get_trajectories_path
from amlgym.util.util import empty_domain
from amlgym.metrics import syntactic_precision, syntactic_recall

domain = 'blocksworld'
agent = get_algorithm('$ARGUMENTS')
domain_path = get_domain_path(domain)
input_domain = empty_domain(domain_path)
traj_paths = get_trajectories_path(domain)
model = agent.learn(input_domain, traj_paths)

# Write learned model and evaluate
with open('learned.pddl', 'w') as f:
    f.write(model)
print("Precision:", syntactic_precision('learned.pddl', domain_path))
print("Recall:", syntactic_recall('learned.pddl', domain_path))
```
