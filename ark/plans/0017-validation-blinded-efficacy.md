# 0017 Validation and Blinded Efficacy Plan

## Goal

Validate the pipeline on benchmark objects and implement the blinded efficacy framework for plot-only, audio-only, and combined-modality review.

## Implementation Approach

Build validation as a reporting layer over canonical benchmark outputs, then add a separate blinded-task framework so performance metrics, comparison tables, and memos are produced from structured inputs rather than ad hoc review.

## Steps

1. Add validation pipelines for gold and silver benchmark objects using canonical lag, spectral, and sonification outputs.
2. Implement the required metric calculations for lag recovery, interval calibration, false positives, disagreement, runtime, and regime-specific performance.
3. Implement blinded efficacy-task definitions, task packaging, and result capture for plot-only, audio-only, and combined-modality review.
4. Add report builders for literature comparison tables, mapping-comparison memos, leaderboards, and blinded-efficacy summaries, plus tests on representative benchmark records.

## Expected File Changes

### New Files

- `src/echorm/eval/validation.py` - benchmark validation metrics
- `src/echorm/eval/efficacy.py` - blinded-task metrics and scoring
- `src/echorm/reports/leaderboards.py` - validation and efficacy report builders
- `src/echorm/reports/memos.py` - structured memo generation helpers
- `tests/test_validation_efficacy.py` - validation and blinded-task tests

### Modified Files

- `src/echorm/reports/render_bundle.py` - blinded-task packaging helpers if needed

## Validation

- `python3 -m pytest tests/test_validation_efficacy.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Gold and silver benchmark validation metrics are computed from structured outputs.
- Blinded efficacy tasks and result capture exist for all required comparison modes.
- Reports can emit comparison tables, leaderboards, and mapping-comparison memos.

## Risks

| Risk | Mitigation |
|------|------------|
| Validation logic becomes tightly coupled to one benchmark family | Build validation against canonical outputs and benchmark metadata rather than survey-specific assumptions |
| Blinded efficacy tasks leak task identity or benchmark labels | Keep task packaging separate from scoring inputs and test blinded-output structure explicitly |

## Dependencies

- `0006`
- `0007`
- `0012`
- `0013`
- `0015`
- `0016`
