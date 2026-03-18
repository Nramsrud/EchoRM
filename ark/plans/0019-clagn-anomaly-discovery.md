# 0019 CLAGN and Anomaly Discovery Extension Plan

## Goal

Extend the validated pipeline into anomaly ranking, CLAGN transition analysis, and follow-up prioritization on the hold-out discovery pool.

## Implementation Approach

Build interpretable anomaly scoring over canonical lag, spectral, and sonification outputs, keep CLAGN-specific transition logic separate from general anomaly ranking, and emit reviewable candidate products rather than opaque model outputs alone.

## Steps

1. Implement anomaly-ranking features and interpretable score composition for continuum-lag and line-response outliers.
2. Add CLAGN transition and precursor analysis that preserves timing, lag-state changes, and line-response evidence.
3. Build candidate-report outputs with ranked targets, anomaly categories, and evidence bundles for review.
4. Add tests that verify hold-out data handling, score traceability, and candidate-output completeness on representative discovery inputs.

## Expected File Changes

### New Files

- `src/echorm/anomaly/rank.py` - interpretable anomaly scoring
- `src/echorm/anomaly/clagn.py` - CLAGN transition analysis
- `src/echorm/anomaly/candidates.py` - ranked candidate builders
- `src/echorm/reports/candidate_memos.py` - follow-up report builders
- `tests/test_clagn_anomaly_discovery.py` - anomaly and candidate-output tests

### Modified Files

- `src/echorm/ingest/ztf/normalize.py` - discovery-facing fields if needed

## Validation

- `python3 -m pytest tests/test_clagn_anomaly_discovery.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Discovery ranking is interpretable and traceable to explicit evidence.
- CLAGN transition analysis preserves timing, lag-state, and line-response context.
- Candidate outputs include ranked targets, anomaly categories, and evidence bundles.

## Risks

| Risk | Mitigation |
|------|------------|
| Discovery ranking collapses into opaque aggregate scores | Preserve feature-level evidence and candidate explanations alongside scores |
| Hold-out discovery data is treated like a benchmark-training resource | Enforce separate discovery pathways and test that no optimization hooks target hold-out inputs |

## Dependencies

- `0008`
- `0012`
- `0015`
- `0017`
