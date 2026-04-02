# 0051 Transition-Supported First-Pass Governance Correction Plan

## Goal

Implement a repository-local first-pass review rule that admits every promoted supported transition into the primary wave while preserving deterministic review order, precursor separation, and the real-data-rerun boundary.

## Implementation Approach

Update the first-pass package builder to treat repaired transition-support evidence as the sole primary-wave admission contract, retain directional fields for reporting and interpretation only, and extend tests so the new governance remains deterministic and bounded.

## Steps

1. Update `src/echorm/eval/first_pass.py` so primary-wave admission requires only:
   - `state_transition_supported=true`
   - `transition_detected=true`
2. Keep same-state supported or transition-negative candidates in the deferred wave with explicit rationale, without reintroducing signed lag-change or line-response thresholds as exclusion rules.
3. Preserve `lag_state_change`, `line_response_ratio`, `rank_score`, benchmark links, and review priority in candidate records and reports as interpretation and ordering fields rather than hard admission criteria.
4. Make primary-wave and deferred-wave ordering deterministic using only tracked `review_priority`, `rank_score`, `benchmark_links`, and `object_uid` fields, with no free-form override path.
5. Update tests in `tests/test_first_pass_review.py` and `tests/test_root_authority_closeout.py` so they verify:
   - supported transitions enter the primary wave
   - same-state precursor cases remain deferred
   - transition-negative cases remain deferred
   - signed lag-change and line-response fields remain present in outputs
   - ordering is deterministic and traceable to tracked fields
6. Update documentation tracking in `ark/projectlist.md`, `ark/playbooks/0051-transition-supported-first-pass-governance-correction.md`, and `tests/test_documentation_state.py` so the repository records the full spec-plan-review package.

## Expected File Changes

### Modified Files

- `ark/projectlist.md`
- `ark/playbooks/0051-transition-supported-first-pass-governance-correction.md`
- `src/echorm/eval/first_pass.py`
- `tests/test_documentation_state.py`
- `tests/test_first_pass_review.py`
- `tests/test_root_authority_closeout.py`

### Added Files

- `ark/plans/0051-transition-supported-first-pass-governance-correction.md`

## Validation

- `python3 -m pytest tests/test_first_pass_review.py tests/test_root_authority_closeout.py tests/test_documentation_state.py -q`
- `python3 -m ruff check src/echorm/eval/first_pass.py tests/test_first_pass_review.py tests/test_root_authority_closeout.py tests/test_documentation_state.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Every promoted supported transition enters the primary wave in `first_pass_review`.
- Same-state precursor and transition-negative candidates remain deferred with explicit rationale.
- Directional fields remain visible in outputs without acting as hard first-pass exclusion thresholds.
- Review ordering remains deterministic and traceable to tracked fields.
- The emitted package still preserves repository-local scope, benchmark linkage, manual review, and the real-data-rerun requirement.

## Dependencies

- `0035`
- `0043`
- `0048`
- `0049`
- `0050`
