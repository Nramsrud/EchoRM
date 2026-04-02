# 0042 Root Optimization Orchestration and Objective Completion Plan

## Goal

Maintain a repository-local optimization closeout package with explicit backend coverage, guard accounting, and hold-out protections.

## Implementation Approach

Keep optimizer adapters aligned across `Ray Tune`, `Optuna`, and `Ax`, persist their repository-local summaries into structured packages, and surface their guard accounting consistently.

## Steps

1. Keep optimizer backend registration, mutation-surface registries, and hold-out guards explicit and shared.
2. Preserve backend, trial, and guarded-target summaries in the optimization-closeout package.
3. Keep release and audit builders aligned to those repository-local summaries.
4. Add tests that fail on hold-out leakage or missing backend accounting.

## Expected File Changes

### Modified Files

- `src/echorm/eval/root_closeout.py`
- `src/echorm/eval/search.py`
- `src/echorm/eval/objectives.py`
- `src/echorm/reports/review_app.py`
- `src/echorm/cli/benchmark.py`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Optimization-closeout artifacts remain traceable to benchmark-governed runs with explicit guard accounting.
- Review and audit surfaces can consume those summaries without ambiguity.

## Dependencies

- `0018`
- `0040`
- `0041`
- `0034`
- `0038`
