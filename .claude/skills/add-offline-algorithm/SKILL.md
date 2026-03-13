---
name: add-offline-algorithm
description: Add a new offline learning algorithm to AMLGym. Use when the user wants to integrate an algorithm that learns from pre-collected trajectory files.
argument-hint: "[AlgorithmName or description]"
---

# Add an Offline Algorithm

Create a new offline algorithm adapter in `amlgym/algorithms/`.

## Context gathering

Before writing any code, gather the following information from the user. If the user provides a repo path or package, explore it to find this information automatically.

1. **Package name** — PyPI package or local repo path (e.g., `pip install n-sam` or `/path/to/repo`)
2. **Main algorithm class and import path** — e.g., `from sam_learning.learners import SAMLearner`
3. **Key methods the algorithm exposes**:
   - Init signature (what does the constructor need — parsed domain object? file path? config params?)
   - Learn method (e.g., `learn(observations) -> (learned_domain, report)`)
   - Model export (e.g., `learned_domain.to_pddl() -> str`)
4. **PDDL library** — does it use `pddl-plus-parser`, `unified-planning`, or something else?
5. **Trajectory format expected** — does the algorithm accept AMLGym's `(:trajectory` format directly, or does it need preprocessing? (e.g., SAM expects `(:init`/`(operator:` keywords instead of `(:state`/`(:action`)
6. **Paper reference** (optional) — for the `_reference` metadata field

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

AMLGym trajectories use PDDL-like format with alternating `(:state ...)` and `(:action ...)` blocks. See `amlgym/benchmarks/trajectories/` for examples.

**AMLGym native format:**
```
(:trajectory
(:state (clear b2) (clear b3) (handempty) (on b2 b1) (ontable b1) (ontable b3))
(:action (pick_up b3))
(:state (clear b2) (holding b3) (on b2 b1) (ontable b1))
(:action (put_down b3))
(:state (clear b2) (clear b3) (handempty) (on b2 b1) (ontable b1) (ontable b3))
)
```

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

## Algorithm interface recommendations

For maximum modularity between the algorithm library and the AMLGym adapter, the algorithm should expose:

| Method | Purpose |
|--------|---------|
| `__init__(domain, **params)` | Init with parsed domain (format depends on PDDL library) |
| `learn(observations) -> model` | Learn from trajectory data |
| `model.to_pddl() -> str` | Export learned model as PDDL string |

**Key principle**: the adapter handles trajectory preprocessing (AMLGym format → algorithm format) and PDDL normalization of the output. The algorithm stays focused on learning.

**PDDL parser choice determines the adapter's work:**
- `pddl-plus-parser`: adapter does keyword replacement in trajectories, uses `DomainParser(path, partial_parsing=True)` and `TrajectoryParser(domain).parse_trajectory(path)` — see SAM.py
- `unified-planning`: adapter may need to enrich trajectories with negative literals, uses `PDDLReader().parse_problem(domain, problem)` — see OffLAM.py
- Custom parser: adapter converts trajectories to whatever format the algorithm expects

## Common integration challenges

**1. Trajectory preprocessing is the main work:**
Every offline adapter's primary job is converting AMLGym trajectories to the algorithm's expected format via `_preprocess_trace()`. Plan for this — study your algorithm's trajectory parser to understand what format it expects.

**2. Temp file management:**
All offline adapters create temp files for preprocessed trajectories. Prefer `tempfile.TemporaryDirectory`:
```python
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    for i, traj_path in enumerate(trajectory_paths):
        processed = self._preprocess_trace(traj_path)
        out_path = f"{tmpdir}/{i}_traj"
        with open(out_path, 'w') as f:
            f.write(processed)
    # ... run learning on files in tmpdir ...
# tmpdir auto-cleaned
```

**3. Domain output post-processing:**
Some algorithms produce PDDL that needs fixing:
- Missing `:requirements :typing` — add it if the domain uses typed predicates/objects (see OffLAM.py)
- Domain name mismatches — `PDDLWriter` may append `-domain`
- Hyphens instead of underscores — apply normalization pattern above

**4. Object type inference from trajectories:**
If your algorithm needs typed objects but trajectories only contain untyped literals, you can infer types from the domain's predicate signatures. See the `_preprocess_trace()` in NOLAM/OffLAM which uses `domain.fluent(pred).signature[k].type.name` to resolve object types.

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
