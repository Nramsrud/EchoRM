# 0034 Benchmark-Governed Optimization and Agent Loop Completion Plan

## Goal

Upgrade the current optimization scaffold into the tracked benchmark-governed experiment loop required by the root authority documents.

## Implementation Approach

Reuse the existing objective and search modules, but extend them with backend-specific records, multi-objective scorecards, and explicit mutation-governance artifacts.

## Steps

1. Extend objective computation to produce Pareto-style science, sonification, and engineering scorecards.
2. Add backend adapters for `Ray Tune`, `Optuna`, and `Ax` that emit comparable trial records.
3. Add immutable benchmark and hold-out guards that reject prohibited mutation targets and discovery-pool inputs.
4. Implement an optimization closeout package with backend summaries, objective fronts, and guard outcomes.
5. Add tests that verify backend records, scorecard generation, and guard enforcement.

## Expected File Changes

### Modified Files

- `src/echorm/eval/objectives.py`
- `src/echorm/eval/search.py`
- `src/echorm/cli/benchmark.py`
- `workflows/rules/optimization.smk`
- `workflows/Snakefile`
- `tests/test_optimization_infrastructure.py`
- `tests/test_root_authority_closeout.py`

## Validation

- `python3 -m pytest tests/test_optimization_infrastructure.py tests/test_root_authority_closeout.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Optimization backends emit tracked, comparable trial records.
- Multi-objective scorecards and guard outcomes are inspectable in artifacts and tests.
- The package integrates with the root closeout audit.

## Risks

| Risk | Mitigation |
|------|------------|
| Multi-objective scoring drifts from benchmark metrics | Build scorecards directly from existing validation outputs and fixed thresholds |
| Backend outputs become incomparable | Normalize every backend record into one canonical experiment schema |

## Dependencies

- `0018`
- `0032`
- `0033`
