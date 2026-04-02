# 0043 Hold-Out Discovery and CLAGN Real-Data Analysis

## Summary

Materialize repository-local hold-out candidate bundles and CLAGN transition analyses from tracked discovery inputs with explicit evidence bundles.

## Scope

- Build anomaly ranking from lag, line-response, sonification, and state-change features on the tracked hold-out pool.
- Produce transition analyses, ranked candidate bundles, taxonomy labels, benchmark links, and follow-up priorities from structured evidence.
- Preserve method-support counts, review priority, evidence level, and limitations on every candidate record.
- Keep the benchmark-to-discovery linkage and the hold-out boundary explicit in the repository-local package surface.

## Non-Goals

- New benchmark creation.
- Publication release packaging.

## Global Constraints

- Discovery outputs must remain downstream of tracked benchmark and optimizer evidence.
- Hold-out evidence may not be used to refit thresholds or objectives.
- Candidate rankings are not final scientific claims and require manual review.

## Acceptance Criteria

- Discovery-analysis artifacts include ranked candidates, anomaly categories, transition records, and candidate memos.
- Every candidate record preserves score components, benchmark links, evidence level, method support, review priority, and limitations.
- CLAGN transition artifacts remain attached to candidate bundles with aligned temporal summaries.
- Tests verify hold-out enforcement, traceability, and candidate-package completeness.

## Dependencies

- `0019`
- `0040`
- `0041`
- `0042`
- `0035`
- `0038`
