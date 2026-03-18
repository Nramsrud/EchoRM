# 0018 Optimization Infrastructure Plan

## Goal

Implement the benchmark-driven optimization layer for experiments, mappings, and controlled program components.

## Implementation Approach

Anchor optimization to fixed benchmark suites and explicit objective metrics, then expose the search surface through tracked configuration and workflow entry points rather than one-off scripts.

## Steps

1. Define the optimization configuration surfaces for objective metrics, search spaces, trial budgets, and prohibited mutation targets.
2. Implement tracked adapters for the selected search backends and route them through the workflow and configuration stack.
3. Add benchmark-integrity guards that prevent mutation of fixed labels, hold-out discovery data, or prohibited configuration surfaces.
4. Add tests that verify objective calculation, allowed mutation surfaces, and enforcement of benchmark-integrity guards.

## Expected File Changes

### New Files

- `configs/experiments/optimization.yaml` - optimization defaults
- `src/echorm/eval/objectives.py` - optimization objectives and constraints
- `src/echorm/eval/search.py` - search-backend adapters
- `workflows/rules/optimization.smk` - optimization workflow entry points
- `tests/test_optimization_infrastructure.py` - optimization-guard tests

### Modified Files

- `workflows/Snakefile` - optimization workflow registration

## Validation

- `python3 -m pytest tests/test_optimization_infrastructure.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Optimization runs are configured through tracked files and explicit objective definitions.
- Allowed mutation surfaces and prohibited targets are encoded in code and tests.
- Benchmark-integrity guards prevent optimization against fixed labels or hold-out discovery data.

## Risks

| Risk | Mitigation |
|------|------------|
| Search backends bypass benchmark-integrity rules | Centralize guard enforcement ahead of backend invocation |
| Objective definitions become detached from validation metrics | Reuse validation and benchmark score modules directly for optimization objectives |

## Dependencies

- `0004`
- `0016`
- `0017`
