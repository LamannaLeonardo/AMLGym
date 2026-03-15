# AMLGym - Project Guide

AMLGym is a benchmarking framework for **Action Model Learning (AML)** — learning classical planning domain models (PDDL) from execution traces. It provides state-of-the-art algorithms, 25 benchmark domains, and evaluation metrics.

**Primary workflow in this repo**: integrating and assessing new learning algorithms (offline or online) within the framework.

## Codebase Structure

```
amlgym/
├── algorithms/       # Algorithm adapters (SAM, OffLAM, NOLAM, ROSAME, RandomAgent, InformationGainAgent)
│   ├── __init__.py   # Auto-discovery registry, get_algorithm()
│   ├── OfflineAlgorithmAdapter.py  # Base class for offline algorithms
│   └── OnlineAlgorithmAdapter.py   # Base class for online algorithms
├── benchmarks/       # 25 domains, trajectories, problems, test states, generation configs
├── metrics/          # syntactic_precision/recall, problem_solving, applicability, predictive_power
├── modeling/         # Env base class, UPEnv simulator wrapper, Trajectory dataclass
└── util/             # empty_domain(), fix_domain_format(), SimpleDomainReader, benchmark generators
```

## Development Setup

- Python 3.10+, pip-based
- Install for development: `pip install -e .` then `pip install -r requirements.txt`
- `clingo` ASP solver required (used by `tarski` for action grounding in online algorithms; installation can be tricky on macOS)
- ROSAME has its own setup: `amlgym/algorithms/rosame/setup.py`
- Core deps: `unified-planning` (simulation/PDDL), `tarski` (grounding), `pddl-plus-parser`
- Algorithm deps: `n-sam`, `offlam`, `nolam`, `information-gain-aml` (external PyPI packages)

## Configuration

- **Benchmark configs**: `amlgym/benchmarks/problems_*.yaml` — define problem generation parameters per domain
- **Algorithm parameters**: dataclass fields with defaults, pass via `get_algorithm('RandomAgent', max_steps=200)` or direct instantiation
- **Benchmark data access**: `amlgym.benchmarks` module — `get_domain_names()`, `get_domain_path()`, `get_trajectories_path()`, `get_problems_path()`, `get_test_states()` (use `kind` param: `'learning'`, `'applicability'`, `'predictive_power'`, `'solving'`)

## Experimenting

See tutorial notebooks for usage examples:
- Offline/online learning: `docs/source/tutorials_learning/`
- Evaluation metrics: `docs/source/tutorials_evaluating/`

## Adding a New Algorithm

Use the Claude Code skills for guided workflows:
- **Offline** (learns from trajectory files): `/add-offline-algorithm YourAlgorithm`
- **Online** (interacts with simulator): `/add-online-algorithm YourAlgorithm`

The skills cover context gathering, step-by-step implementation, PDDL normalization, integration challenges, and testing checklists. Create `amlgym/algorithms/YourAlgorithm.py` (class name must match filename, PascalCase, case-insensitive), inherit from the appropriate base class, implement `learn()`, and evaluate with `amlgym.metrics`.

## PDDL Conventions

See `docs/pddl-format-spec.md` for the full format specification (trajectory format, normalization rules, metric-specific behavior, known limitations).

**Critical — silent failures if not followed:**
- Learned PDDL **must** use underscores and lowercase (not hyphens) for action/predicate/type names, or syntactic metrics silently produce wrong results. Safe pattern: `re.sub(r'(?<=\w)-(?=\w)', '_', pddl).lower()`
- `SimpleDomainReader` silently strips `:functions` and `:action-costs` — these are not evaluated
- `simulator._problem` is a private `unified-planning` API used by online adapters — may break across UP versions

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
