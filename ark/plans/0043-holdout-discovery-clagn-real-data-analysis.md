# 0043 Hold-Out Discovery and CLAGN Real-Data Analysis Plan

## Goal

Maintain a repository-local discovery-analysis package whose candidate bundles remain traceable, evidence-labeled, and hold-out governed.

## Implementation Approach

Build discovery features from tracked benchmark-calibrated outputs, keep anomaly and CLAGN records structured, and emit review-ready candidate bundles with explicit limitations.

## Steps

1. Preserve structured score components, benchmark links, evidence levels, and review priority across discovery outputs.
2. Keep CLAGN transition summaries aligned to the same candidate records.
3. Generate ranked catalogs and candidate memos from the tracked hold-out pool without weakening hold-out rules.
4. Add tests that fail when discovery artifacts lose traceability or hold-out enforcement.

## Expected File Changes

### Modified Files

- `src/echorm/anomaly/*`
- `src/echorm/eval/root_closeout.py`
- `src/echorm/reports/candidate_memos.py`
- `src/echorm/reports/review_app.py`
- `src/echorm/cli/benchmark.py`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Discovery-analysis artifacts remain traceable to structured hold-out evidence.
- Candidate bundles remain usable by review and audit surfaces without ambiguity.

## Dependencies

- `0019`
- `0040`
- `0041`
- `0042`
- `0035`
- `0038`
