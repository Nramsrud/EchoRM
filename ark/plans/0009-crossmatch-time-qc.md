# 0009 Crossmatch, Time Standards, and Quality Control Plan

## Goal

Create the shared identity, time-standard, normalization, and quality-control layer used across all surveys.

## Implementation Approach

Centralize survey-to-survey identity handling, observed and rest-frame time conversion, normalization transforms, and quality scoring in shared modules so later ingestion and inference code do not reimplement them inconsistently.

## Steps

1. Add shared models for canonical object identity, aliases, survey identifiers, and crossmatch resolution.
2. Implement observed-frame and rest-frame time handling, including explicit per-object reference-epoch support.
3. Implement raw, science-normalized, and sonification-normalized photometric representations with explicit transform metadata.
4. Add quality-control scoring for cadence, masking, gaps, line coverage, and review priority, and lock the behavior with tests on representative survey inputs.

## Expected File Changes

### New Files

- `src/echorm/crossmatch/models.py` - object identity and alias models
- `src/echorm/calibrate/time.py` - observed and rest-frame time conversion
- `src/echorm/calibrate/normalize.py` - normalization transforms and metadata
- `src/echorm/eval/qc.py` - quality-score and review-priority logic
- `tests/test_crossmatch_time_qc.py` - shared calibration and QC tests

### Modified Files

- `src/echorm/schemas/objects.py` - crossmatch and identifier fields if needed
- `src/echorm/schemas/photometry.py` - normalization and QC fields if needed

## Validation

- `python3 -m pytest tests/test_crossmatch_time_qc.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Identity, alias, and survey-resolution rules are encoded once in shared modules.
- Observed-frame and rest-frame time handling are explicit and test-covered.
- Normalization transforms and quality scores preserve provenance and support downstream review.

## Risks

| Risk | Mitigation |
|------|------------|
| Survey-specific edge cases leak into the shared layer | Keep survey readers thin and route shared logic through common interfaces only |
| Hidden normalization choices undermine later scientific interpretation | Preserve transform metadata and test that raw and normalized representations remain linked |

## Dependencies

- `0005`
- `0006`
- `0007`
- `0008`
