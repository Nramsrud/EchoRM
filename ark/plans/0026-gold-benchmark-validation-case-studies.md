# 0026 Gold Benchmark Validation and Case Studies Plan

## Goal

Close the gold-benchmark validation gap with literature-rich, object-level validation artifacts rather than bounded ingest evidence alone.

## Implementation Approach

Build a gold validation package over the frozen gold corpus and real method outputs, then add object-level diagnostics, mapping comparisons, and case-study reports for the canonical AGN Watch benchmark objects.

## Steps

1. Select the gold benchmark object set from the frozen manifest and bind the literature comparison targets and evidence labels for each object.
2. Execute the required reverberation methods, consensus logic, rerun checks, and spectral diagnostics on each gold object.
3. Generate object-level lag comparison tables, method tables, line-fit diagnostics, and mapping-family audio artifacts.
4. Build mapping-comparison memos and package-level summaries that state demonstrated capability, limitations, residual gaps, and rerun stability.
5. Add tests that validate object coverage, artifact structure, literature-comparison record integrity, and package-level primary-metric thresholds.

## Expected File Changes

### New Files

- gold validation assembly and report modules under `src/echorm/eval/` and `src/echorm/reports/`
- tests covering gold object selection, report structure, and artifact completeness

### Modified Files

- spectral and sonification modules as needed for gold-object diagnostics and artifact generation
- workflow and CLI surfaces for gold validation package materialization

## Validation

- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`
- tracked gold validation package command over the selected AGN Watch object set

## Exit Criteria

- More than one gold benchmark object is validated against literature expectations in tracked artifacts.
- The package records a mean absolute lag error at or below the declared threshold and records rerun drift on the primary metrics.
- Each gold object exposes lag comparison, method table, line diagnostics, audio artifacts, and a mapping-comparison memo.
- The package-level summary states what the gold benchmark evidence does and does not demonstrate, with explicit evidence labels and residual uncertainty.

## Risks

| Risk | Mitigation |
|------|------------|
| Gold validation collapses into anecdotal case notes | Require standardized diagnostics, literature tables, and package-level summaries for every selected object |
| Audio artifacts become detached from the scientific diagnostics | Bind every audio artifact to the same object-level validation record and diagnostic bundle |

## Dependencies

- `0013`
- `0015`
- `0017`
- `0025`
