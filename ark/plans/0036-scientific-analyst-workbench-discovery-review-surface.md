# 0036 Scientific Analyst Workbench and Discovery Review Surface Plan

## Goal

Upgrade the review application into the analyst workbench required for full root-scope scientific review.

## Implementation Approach

Extend the existing run, group, and file views with additional package-aware routes and artifact-backed summaries rather than creating a second web surface.

## Steps

1. Add grouped detail routes and summaries for new package types, candidate records, release bundles, and optimization experiments.
2. Expose provenance, claims boundaries, hold-out governance, and review-priority metadata in run and detail pages.
3. Add tests that exercise the new workbench routes against generated artifacts.

## Expected File Changes

### Modified Files

- `src/echorm/reports/review_app.py`
- `tests/test_benchmark_review_app.py`
- `tests/test_root_authority_closeout.py`

## Validation

- `python3 -m pytest tests/test_benchmark_review_app.py tests/test_root_authority_closeout.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Benchmark, discovery, optimization, and release artifacts are navigable through one read-only application.
- Candidate and release review views expose the required metadata directly from tracked artifacts.
- The workbench is used by the root closeout audit as the inspection surface.

## Risks

| Risk | Mitigation |
|------|------------|
| Route growth makes the review surface inconsistent | Reuse the existing grouped-detail machinery and normalize new artifact shapes |
| Pages omit scientific-claims boundaries | Include claims-boundary panels on every new package and detail view |

## Dependencies

- `0033`
- `0035`
