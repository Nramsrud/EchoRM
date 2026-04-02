# 0045 Literal Root Authority Conformance Audit and Final Readiness Gate Plan

## Goal

Maintain a repository-local root-authority audit that aggregates the integrated closeout packages and preserves their claims boundary explicitly.

## Implementation Approach

Keep the audit aligned to the generated closeout packages, preserve explicit conditions and package references, and surface the result through the analyst workbench and release bundle.

## Steps

1. Keep the audit condition set aligned to the integrated closeout packages.
2. Preserve package references, limitations, and non-demonstrated capabilities in the emitted audit.
3. Integrate the audit into workflow outputs, release bundles, and review pages.
4. Add tests that prove the audit preserves its repository-local claims boundary under downgrade scenarios.

## Expected File Changes

### Modified Files

- `src/echorm/eval/root_closeout.py`
- `src/echorm/reports/review_app.py`
- `src/echorm/reports/release.py`
- `src/echorm/cli/benchmark.py`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- The root-authority audit remains explicit about the packages it aggregates and the limitations it preserves.
- Review and release surfaces can consume the audit without overstating what it demonstrates.

## Dependencies

- `0041`
- `0042`
- `0043`
- `0044`
- `0038`
