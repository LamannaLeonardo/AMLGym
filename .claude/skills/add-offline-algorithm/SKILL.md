---
name: add-offline-algorithm
description: Add a new offline learning algorithm to AMLGym. Use when the user wants to integrate an algorithm that learns from pre-collected trajectory files.
argument-hint: "[AlgorithmName or description]"
---

# Add an Offline Algorithm

Create a new offline algorithm adapter in `amlgym/algorithms/`.

## Context gathering

Before writing any code:

1. **Get from the user**: package name or repo path, and optionally a paper reference
2. **Explore the algorithm's code** to determine:
   - Main class and import path (e.g., `from sam_learning.learners import SAMLearner`)
   - Constructor signature (parsed domain object? file path? config params?)
   - Learn method signature and return type (e.g., `learn(observations) -> (learned_domain, report)`)
   - Model export method (e.g., `learned_domain.to_pddl() -> str`)
   - What PDDL library it uses (`pddl-plus-parser`, `unified-planning`, or other)
   - What trajectory format it expects as input
3. If exploration is insufficient, ask the user targeted questions about specific API details

## Steps

1. **Create** `amlgym/algorithms/<AlgorithmName>.py`

   Replace `<AlgorithmName>` with the PascalCase name for your algorithm (e.g., `SAM`, `OffLAM`, `MyLearner`). This becomes both the filename and class name. The name matching is case-insensitive.

2. **Inherit** from `OfflineAlgorithmAdapter` and implement `learn()`:

```python
from dataclasses import dataclass
from typing import List
from amlgym.algorithms.OfflineAlgorithmAdapter import OfflineAlgorithmAdapter

@dataclass
class <AlgorithmName>(OfflineAlgorithmAdapter):
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

## Reference implementations

Study these adapters for different integration patterns:

**`amlgym/algorithms/SAM.py`** — simplest offline adapter:
- Uses `pddl-plus-parser` (`DomainParser` with `partial_parsing=True`, `TrajectoryParser`)
- Preprocesses trajectories with simple keyword replacement (~10 lines)
- Returns `learned_domain.to_pddl()` directly

**`amlgym/algorithms/OffLAM.py`** — partial observability adapter:
- Uses `unified-planning` (`PDDLReader`) for domain parsing
- Enriches trajectories with explicit negative literals (~60 lines of preprocessing)
- Post-processes output to add missing `:requirements :typing` declaration

**`amlgym/algorithms/NOLAM.py`** — noisy observations adapter:
- Same negative-literal enrichment pattern as OffLAM
- Different wrapper keyword: `(:observation` instead of `(:trajectory`

**`amlgym/algorithms/ROSAME.py`** — neuro-symbolic adapter:
- Uses `pddl-plus-parser` with both domain and problem files
- Incremental learning: processes each trajectory separately

Key pattern: every offline adapter has a `_preprocess_trace()` method that converts AMLGym's trajectory format to the algorithm's expected format. **This is the primary integration work.**

## Trajectory format

> See `docs/pddl-format-spec.md` for the native AMLGym trajectory format and normalization rules.

Each adapter preprocesses the native format into an algorithm-specific format. The key transformations:

**SAM/ROSAME expected format** (pddl-plus-parser):
```
(
(:init (clear b2) (clear b3) (handempty) (on b2 b1) (ontable b1) (ontable b3))
(operator: (pick_up b3))
(:state (clear b2) (holding b3) (on b2 b1) (ontable b1))
(operator: (put_down b3))
(:state (clear b2) (clear b3) (handempty) (on b2 b1) (ontable b1) (ontable b3))
)
```
Changes: `(:trajectory` to `(`, first `(:state` to `(:init` (only the first one), `(:action` to `(operator:`.

**NOLAM/OffLAM expected format** (with explicit negatives):
```
(:observation
(:state (clear b2) (clear b3) (handempty) (on b2 b1) (ontable b1) (ontable b3)
        (not (holding b1)) (not (holding b2)) (not (holding b3)) ...)
(:action (pick_up b3))
(:state ...)
)
```
Changes: `(:trajectory` to `(:observation`, each state enriched with `(not ...)` for all false predicates relevant to that action's objects.

**Common preprocessing pattern:**
```python
def _preprocess_trace(self, traj_path: str) -> str:
    with open(traj_path, 'r') as f:
        traj_str = f.read()
    traj_str = re.sub(r' +', ' ', traj_str)  # normalize whitespace
    # Algorithm-specific keyword replacements here
    return traj_str
```

## What to look for in the algorithm's API

When exploring the algorithm's code, identify these three components:

| Component | What to find | Example |
|-----------|-------------|---------|
| Initialization | Constructor params — does it need a parsed domain, file path, or config? | `SAMLearner(partial_domain=domain)` |
| Learning | Method that ingests trajectory data and learns | `sam.learn_action_model(observations)` |
| Export | How to get PDDL string out of the learned model | `learned_domain.to_pddl()` |

The adapter's job: preprocess trajectories (AMLGym format → algorithm format) and normalize the PDDL output. The PDDL library the algorithm uses determines the preprocessing approach — see reference implementations.

## Common integration challenges

**1. Trajectory preprocessing is the main work:**
Every offline adapter's primary job is converting AMLGym trajectories to the algorithm's expected format via `_preprocess_trace()`. Plan for this — study your algorithm's trajectory parser to understand what format it expects.

**2. Temp file management:**
Use `tempfile.TemporaryDirectory` for preprocessed trajectories (existing adapters use CWD-relative `tmp/` which is not safe for parallel execution).

**3. Domain output post-processing:**
See "PDDL Conventions" in CLAUDE.md for common output fixes (`:requirements :typing`, domain name suffix, hyphen normalization).

**4. Object type inference from trajectories:**
If your algorithm needs typed objects but trajectories only contain untyped literals, see `_preprocess_trace()` in NOLAM.py or OffLAM.py for examples of inferring types from domain predicate signatures.

## Testing

```python
from amlgym.algorithms import get_algorithm
from amlgym.benchmarks import get_domain_path, get_trajectories_path
from amlgym.util.util import empty_domain
from amlgym.metrics import syntactic_precision, syntactic_recall

domain = 'blocksworld'
agent = get_algorithm('<AlgorithmName>')
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

## Checklist

- [ ] File name matches class name (PascalCase, case-insensitive)
- [ ] Inherits from `OfflineAlgorithmAdapter`
- [ ] Implements `learn(domain_path, trajectory_paths) -> str`
- [ ] Learned PDDL uses underscores (not hyphens) and lowercase
- [ ] `_preprocess_trace()` handles AMLGym trajectory format correctly
- [ ] Temp files/directories are cleaned up
- [ ] Algorithm parameters are dataclass fields with defaults
- [ ] External dependencies added to `requirements.txt`
- [ ] Tested against at least one benchmark domain (e.g., blocksworld)
