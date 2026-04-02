# 0039 Real Backend and Spectral Backend Integration Plan

## Goal

Maintain a repository-local advanced-rigor package that records structured advanced-backend and spectral-fit evidence with explicit diagnostics and limitations.

## Implementation Approach

Centralize backend descriptors, capture diagnostics and evidence labels consistently, and route the advanced-rigor package, review surface, and audits through those structured records.

## Steps

1. Consolidate backend descriptors, availability checks, version capture, and diagnostic serialization for the advanced backend set.
2. Ensure advanced-rigor records preserve runtime, warnings, diagnostics, and artifact paths or explicit limitations.
3. Keep the review surface and root-authority audit aligned to those repository-local records.
4. Add tests that fail when advanced-rigor records become incomplete or silently downgrade their evidence labels.

## Expected File Changes

### Modified Files

- `src/echorm/rm/*.py`
- `src/echorm/spectra/pyqsofit.py`
- `src/echorm/eval/root_closeout.py`
- `src/echorm/reports/review_app.py`
- `src/echorm/cli/benchmark.py`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- The advanced-rigor package materializes consistent structured records with explicit limitations.
- Review and audit paths consume those records without overstating corpus or readiness scope.

## Dependencies

- `0011`
- `0013`
- `0032`
- `0038`
