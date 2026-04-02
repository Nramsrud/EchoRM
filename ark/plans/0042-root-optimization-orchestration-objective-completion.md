# 0042 Root Optimization Orchestration and Objective Completion Plan

## Goal

Replace the scaffolded optimization layer with literal optimizer orchestration and full root-objective accounting.

## Implementation Approach

Introduce optimizer adapters and experiment runners around `Ray Tune`, `Optuna`, and `Ax`, wire them to the frozen benchmark artifacts, and persist guardrail and Pareto outputs into structured packages and review views.

## Steps

1. Add optimizer backends, objective definitions, mutation-surface registries, and hold-out guards.
2. Execute tracked optimizer runs against the frozen benchmark packages.
3. Persist experiment dashboards, Pareto-front summaries, retain or discard decisions, and provenance.
4. Add tests that fail on simulated optimizer evidence or discovery-pool leakage.

## Expected File Changes

### Modified Files

- `src/echorm/eval/objectives.py`
- `src/echorm/eval/search.py`
- `src/echorm/eval/root_closeout.py`
- `src/echorm/reports/review_app.py`
- `src/echorm/cli/benchmark.py`
- `workflows/rules/optimization.smk`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Optimization artifacts are produced by literal optimizer runs with full guardrail accounting.
- Simulated optimizer evidence no longer appears in root-closeout outputs.

## Dependencies

- `0018`
- `0040`
- `0041`
- `0034`
- `0038`
