# 0028 Continuum-RM Benchmark Expansion Plan

## Goal

Establish the broader continuum-RM benchmark package needed before contamination, hierarchy, or stability claims can be promoted scientifically.

## Implementation Approach

Extend the continuum benchmark layer with broader suite definitions, literature-inspired benchmark objects, and explicit classification and stability metrics derived from tracked benchmark artifacts.

## Steps

1. Define the expanded continuum benchmark suites and their evidence labels, including hierarchy, contamination, state-change, and failure cases.
2. Add literature-inspired or known-like ZTF benchmark objects and cadence-degradation scenarios to the benchmark corpus where they fit the declared scope.
3. Execute the selected reverberation and classification paths over the expanded continuum benchmark package.
4. Aggregate recovery, contaminated-versus-clean classification, and cadence-stability metrics into tracked reports.
5. Add tests that validate suite labeling, metric structure, and package reproducibility.

## Expected File Changes

### New Files

- expanded continuum benchmark assembly and reporting modules under `src/echorm/eval/` and `src/echorm/reports/`
- tests covering suite labeling, classification outputs, and cadence-stability summaries

### Modified Files

- ZTF access and normalization modules as needed for benchmark-object support
- synthetic benchmark modules for broader continuum task coverage
- workflow and CLI surfaces for continuum benchmark package materialization

## Validation

- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`
- tracked continuum benchmark package command over the declared suite set

## Exit Criteria

- Broader continuum benchmark suites are materialized in tracked artifacts with explicit evidence labels.
- Recovery, contamination, and cadence-stability metrics are reported explicitly.
- The package states what the continuum benchmark evidence does and does not demonstrate.

## Risks

| Risk | Mitigation |
|------|------------|
| Continuum reporting blurs synthetic and literature-inspired evidence | Keep evidence labels explicit on every suite and top-level summary |
| Cadence effects are observed but not quantified | Make cadence-degradation metrics and summaries required outputs |

## Dependencies

- `0008`
- `0009`
- `0016`
- `0017`
- `0025`
