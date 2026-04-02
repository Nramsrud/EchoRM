# 0043 Hold-Out Discovery and CLAGN Real-Data Analysis Plan

## Goal

Replace fixture-authored discovery evidence with real-data anomaly ranking and CLAGN analysis on the frozen hold-out pool.

## Implementation Approach

Build discovery features from validated benchmark-calibrated outputs, tighten the anomaly and CLAGN modules to require structured evidence inputs, and emit review-ready catalogs and memos.

## Steps

1. Replace authored hold-out fixture scores with features derived from real validated pipeline outputs.
2. Update anomaly ranking and CLAGN transition logic to consume structured evidence rather than fixed hand-authored values.
3. Generate ranked catalogs, candidate memos, and transition timelines from the frozen hold-out pool.
4. Add tests that fail when discovery artifacts rely on authored scores or back-fit thresholds.

## Expected File Changes

### Modified Files

- `src/echorm/anomaly/*`
- `src/echorm/eval/root_closeout.py`
- `src/echorm/reports/catalog.py`
- `src/echorm/reports/candidate_memos.py`
- `src/echorm/reports/review_app.py`
- `src/echorm/cli/benchmark.py`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Discovery and CLAGN artifacts derive from validated real-data evidence on the frozen hold-out pool.
- Authored-score discovery evidence no longer appears in root-closeout outputs.

## Dependencies

- `0019`
- `0040`
- `0041`
- `0042`
- `0035`
- `0038`
