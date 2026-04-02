# 0035 Discovery Hold-Out and CLAGN Scientific Analysis Plan

## Goal

Implement the root-scope discovery and CLAGN analysis layer over the frozen hold-out corpus.

## Implementation Approach

Extend the current anomaly and candidate scaffolds into a structured package generator that emits interpretable ranking records, transition analyses, and follow-up memos from the hold-out manifest.

## Steps

1. Extend anomaly scoring to preserve feature components, method support, review priority, and evidence metadata.
2. Add richer CLAGN transition records with pre-state, transition, and post-state summaries.
3. Implement a discovery closeout package that writes candidate tables, taxonomy summaries, memos, and transition records.
4. Add tests that verify hold-out enforcement, ranking traceability, and candidate-package completeness.

## Expected File Changes

### Modified Files

- `src/echorm/anomaly/rank.py`
- `src/echorm/anomaly/clagn.py`
- `src/echorm/anomaly/candidates.py`
- `src/echorm/reports/candidate_memos.py`
- `src/echorm/cli/benchmark.py`
- `workflows/Snakefile`
- `workflows/rules/common.smk`
- `tests/test_clagn_anomaly_discovery.py`
- `tests/test_root_authority_closeout.py`

## Validation

- `python3 -m pytest tests/test_clagn_anomaly_discovery.py tests/test_root_authority_closeout.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Ranked hold-out discovery artifacts are generated through tracked commands.
- Candidate records preserve explicit evidence and transition context.
- The discovery package is inspectable through the review surface and the root closeout audit.

## Risks

| Risk | Mitigation |
|------|------------|
| Discovery records overstate scientific support | Encode evidence level, method support, and limitations on every candidate bundle |
| Transition analysis becomes detached from anomaly ranking | Preserve shared object identifiers and structured transition evidence in every candidate output |

## Dependencies

- `0019`
- `0032`
- `0033`
- `0034`
