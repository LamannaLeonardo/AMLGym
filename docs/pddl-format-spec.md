# PDDL Format Specification

This document standardizes the PDDL formats accepted and produced by AMLGym at each layer of the framework.

## Trajectory Format

### Native AMLGym format

All benchmark trajectories in `amlgym/benchmarks/trajectories/` use this format:

```
(:trajectory
  (:state (pred1 obj1 obj2) (pred2 obj3) ...)
  (:action (action_name arg1 arg2))
  (:state (pred1 obj1 obj2) ...)
  (:action (action_name arg1))
  (:state (pred1 obj1 obj2) ...)
)
```

Rules:
- Outer wrapper: `(:trajectory ... )`
- States: `(:state ...)` containing positive ground literals only
- Actions: `(:action (name arg1 arg2 ...))` — single ground action per block
- Alternating state-action-state pattern; starts and ends with a state
- All names use underscores and lowercase (normalized by `fix_domain_format()`)

### Algorithm-specific formats

Adapters preprocess the native format into algorithm-specific formats via `_preprocess_trace()`.

#### SAM / ROSAME format (pddl-plus-parser)

```
(
  (:init (pred1 obj1 obj2) (pred2 obj3) ...)
  (operator: (action_name arg1 arg2))
  (:state (pred1 obj1 obj2) ...)
  (operator: (action_name arg1))
  (:state (pred1 obj1 obj2) ...)
)
```

Transformations from native:
- `(:trajectory` → `(`
- First `(:state` → `(:init` (only the first occurrence)
- `(:action` → `(operator:`

#### OffLAM / NOLAM format (with explicit negatives)

```
(:observation
  (:state (pred1 obj1 obj2) ... (not (pred3 obj1)) (not (pred4 obj2 obj3)) ...)
  (:action (action_name arg1 arg2))
  (:state ...)
)
```

Transformations from native:
- `(:trajectory` → `(:observation`
- Each state enriched with `(not (pred ...))` for all false predicates relevant to the surrounding actions' objects
- Object types inferred from domain predicate signatures: `domain.fluent(pred).signature[k].type.name`

## Domain PDDL Requirements

### What metrics support

The framework's metrics make the following assumptions about domain PDDL:

| Feature | Supported | Notes |
|---------|-----------|-------|
| `:strips` | Yes | Core supported requirement |
| `:typing` | Yes | Must include `:requirements :typing` if using types |
| `:negative-preconditions` | Yes | `(not (pred ...))` in preconditions |
| `:equality` | Partial | Parsed but not deeply evaluated |
| `:functions` | **No** | `SimpleDomainReader` silently strips `:functions` sections |
| `:action-costs` | **No** | Silently removed from requirements |
| Numeric fluents | **No** | Predictive metrics assume all fluents are boolean |
| Conditional effects | **No** | Not parsed by `SimpleDomainReader` |

### Normalization rules

All benchmark domains are normalized by `fix_domain_format()` (`amlgym/util/util.py`):

1. **Hyphens → underscores**: `pick-up` becomes `pick_up` (applied between word characters)
2. **Lowercase**: entire domain content lowercased
3. **Special case**: `(not_eq` → `(noteq` (Ferry domain workaround)

**Learned PDDL output must match these conventions.** Syntactic metrics compare predicate/action names verbatim — mismatches cause silently wrong results.

| Element | Must normalize | Example |
|---------|---------------|---------|
| Action names | Yes | `pick_up`, not `pick-up` |
| Predicate names | Yes | `on_table`, not `on-table` |
| Type names | Yes | `block_type`, not `block-type` |
| Parameter names | No | `SimpleDomainReader` normalizes to `?param_1`, `?param_2`, etc. |

Safe normalization pattern:
```python
import re
normalized = re.sub(r'(?<=\w)-(?=\w)', '_', learned_pddl)
normalized = normalized.lower()
```

### Domain output post-processing

Common fixes needed on learned PDDL before evaluation:

1. **Missing `:requirements :typing`** — Some algorithms (e.g., OffLAM) omit this. Add it if the domain uses typed predicates/objects.

2. **Domain name suffix** — `unified-planning`'s `PDDLWriter` may produce `(domain name-domain)` instead of `(domain name)`. Fix with:
   ```python
   domain_str = domain_str.replace(f"(domain {name}-domain)", f"(domain {name})")
   ```

3. **Hyphen normalization** — Apply the regex pattern above to ensure underscore convention.

## Known Limitations

### Silent failures (wrong results, no error)

- `:functions` in learned domain → silently ignored by syntactic metrics
- `:action-costs` in requirements → silently removed
- Hyphenated names (e.g., `pick-up`) → syntactic metrics won't match against reference `pick_up`
- Missing operators in learned domain → precision returns 1.0 for missing operators (treated as "no predictions, no false positives")

### Hard failures (errors raised)

- Malformed PDDL syntax → `PDDLReader` or `SimpleDomainReader` raises parse error
- Missing `:typing` with typed objects → `PDDLReader` parse failure
- Operator count mismatch between learned and reference → assertion error in syntactic metrics

## Metric-specific PDDL behavior

### Syntactic metrics (`_syntactic.py`)

- Uses `SimpleDomainReader` (custom regex-based parser)
- Converts underscores back to hyphens internally for operator matching (lines 55-57)
- Parameter names are normalized to `?param_1`, `?param_2`, etc.
- Compares preconditions and effects as sets of `(predicate, param1, param2, ...)` tuples
- Returns per-action and aggregate precision/recall

### Problem solving (`_solving.py`)

- Uses `unified-planning`'s `PDDLReader` for parsing
- Uses `OneshotPlanner` (fast-downward) for plan generation
- Uses `PlanValidator` for plan validation against reference domain
- No external VAL validator invocation (despite `get_applicable_actions_val()` existing as dead code in `util.py`)

### Predictive metrics (`_predictive.py`)

- Operates on `UPEnv` simulator instances, not PDDL files directly
- Computes applicability and effect prediction accuracy
- States represented as sets of positive literals (boolean only)
- Effects computed as set differences: `(next_state - current_state)` for add effects
