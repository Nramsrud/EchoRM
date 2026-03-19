# 0027 Silver Benchmark Population Validation

## Summary

Validate a broad SDSS-RM published-lag benchmark population with population metrics, null controls, regime breakdowns, and failure-mode reporting.

## Scope

- Evaluate a broad published-lag SDSS-RM benchmark population from the frozen silver manifest.
- Compute lag-recovery, coverage, disagreement, false-positive, runtime, and regime-specific metrics from tracked benchmark outputs.
- Include null and shuffled-pair controls and report their outcomes explicitly.
- Materialize leaderboards, literature comparison tables, and failure-mode summaries suitable for review and claims audit.

## Non-Goals

- Replace gold object case studies.
- Replace continuum-RM benchmark expansion.
- Claim broad validation without null controls, regime breakdowns, and literature comparison.

## Global Constraints

- Silver-benchmark reporting must remain population-level and stratified by declared benchmark regimes.
- Null and shuffled controls must be reported alongside main metrics rather than hidden in appendices or omitted entirely.
- Population metrics must remain reproducible from tracked benchmark outputs and frozen manifests.

## Acceptance Criteria

- A broad SDSS-RM published-lag benchmark population is evaluated in tracked artifacts with lag-recovery, coverage, false-positive, disagreement, runtime, and regime metrics.
- The package records coverage at or above 0.75, null false-positive rate at or below 0.10, and inter-method disagreement rate at or below 0.50 for the declared benchmark slice.
- Null and shuffled-pair controls are included with explicit labeling and reported false-positive behavior.
- The package produces a benchmark leaderboard, a literature comparison table, runtime summaries, and failure-mode summaries with explicit scope, evidence level, and limitations.

## Dependencies

- `0012`
- `0013`
- `0017`
- `0025`
