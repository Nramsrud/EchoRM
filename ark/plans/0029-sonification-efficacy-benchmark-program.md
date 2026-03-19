# 0029 Sonification Efficacy Benchmark Program Plan

## Goal

Provide the real blinded efficacy evidence required for the project to claim that the sonification layer supports scientific analysis beyond presentation.

## Implementation Approach

Build a scored blinded-task benchmark program over tracked validation artifacts, then aggregate efficacy metrics across task modes, cohorts, and anomaly classes with explicit comparison to plot-only baselines.

## Steps

1. Define the blinded task sets, participant or agent cohort structure, training-level records, and agreement-calculation method for the efficacy benchmark program.
2. Materialize plot-only, audio-only, and plot-plus-audio task packages from tracked validation artifacts with answer keys separated from task views.
3. Implement scored response capture, confidence capture, timing capture, and repeated-response handling for the efficacy program.
4. Aggregate cohort-level metrics, calibration summaries, agreement summaries, confusion summaries, and baseline comparisons into tracked reports.
5. Add tests that validate blinding structure, response scoring, calibration, agreement, and efficacy-threshold evaluation.

## Expected File Changes

### New Files

- efficacy benchmark assembly and reporting modules under `src/echorm/eval/` and `src/echorm/reports/`
- tests covering task packaging, scoring, and cohort-level summaries

### Modified Files

- existing efficacy modules for richer scoring and cohort metadata
- workflow and CLI surfaces for efficacy package materialization

## Validation

- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`
- tracked efficacy benchmark package command over the declared task and cohort sets

## Exit Criteria

- Blinded efficacy task packages and scored results exist as tracked artifacts across the declared task modes.
- Cohort-level efficacy metrics, calibration summaries, agreement summaries, and confusion summaries are reported explicitly.
- Plot-only baseline comparisons are present in the package-level summary and satisfy the declared thresholds.

## Risks

| Risk | Mitigation |
|------|------------|
| The efficacy program measures preference rather than analysis performance | Restrict outputs to blinded tasks with explicit accuracy, timing, and calibration metrics |
| Cohort summaries hide important differences by experience level | Require performance-by-training-level reporting in the package outputs |

## Dependencies

- `0015`
- `0017`
- `0026`
- `0027`
- `0028`
