# 0043 Hold-Out Discovery and CLAGN Real-Data Analysis

## Summary

Run the discovery and CLAGN program on the frozen real hold-out pool using validated pipeline outputs rather than authored fixture scores.

## Scope

- Build anomaly ranking from validated lag, line-response, sonification, and state-change outputs on the frozen hold-out pool.
- Produce CLAGN transition and precursor analyses with aligned timelines and spectroscopic evidence.
- Emit ranked catalogs, candidate memos, taxonomy labels, and follow-up priorities from structured evidence.
- Preserve the benchmark-to-discovery linkage and the hold-out boundary explicitly.

## Non-Goals

- New benchmark creation.
- Publication release packaging.

## Global Constraints

- Discovery outputs must remain downstream of the frozen benchmark and optimizer evidence.
- Hold-out evidence may not be used to refit thresholds or objectives.
- Root-closeout promotion may not use authored anomaly scores as discovery evidence.

## Acceptance Criteria

- Discovery artifacts consume validated real-data outputs from the frozen hold-out corpora.
- CLAGN transition artifacts include aligned timelines, state comparisons, and spectroscopic evidence summaries.
- Ranked catalogs and candidate memos record anomaly taxonomy, evidence support, and follow-up priority.
- Tests verify that fixture-authored anomaly scores or threshold-only discovery logic fail the root-closeout path.

## Dependencies

- `0019`
- `0040`
- `0041`
- `0042`
- `0035`
- `0038`
