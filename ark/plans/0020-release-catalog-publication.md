# 0020 Release, Catalog, and Publication Artifacts Plan

## Goal

Package the validated methods outputs, anomaly products, audio bundles, and publication-facing materials for external release.

## Implementation Approach

Build release assembly around validated manifests, benchmark outputs, and candidate products so every published bundle is traceable to reviewed inputs, configurations, and provenance records.

## Steps

1. Define the release assembly process for methods outputs, catalog products, audio bundles, and benchmark archives.
2. Implement provenance-aware packaging for code, configuration, manifests, benchmark tables, and audio products.
3. Add publication-facing report builders and release indexes that remain concise, precise, and externally reviewable.
4. Add tests that verify bundle completeness, provenance coverage, and consistency between release indexes and packaged artifacts.

## Expected File Changes

### New Files

- `src/echorm/reports/release.py` - release assembly helpers
- `src/echorm/reports/catalog.py` - catalog package builders
- `docs/releases/` - public release-facing documentation and indexes
- `tests/test_release_artifacts.py` - release-bundle tests

### Modified Files

- `README.md` - public release pointers when the release exists

## Validation

- `python3 -m pytest tests/test_release_artifacts.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Release bundles include code, configuration, manifests, benchmark outputs, and audio products with provenance.
- Publication-facing documentation is generated from structured release inputs.
- Tests verify bundle completeness and provenance consistency.

## Risks

| Risk | Mitigation |
|------|------------|
| Release packaging omits provenance needed for external review | Make provenance coverage a tested exit condition for every bundle |
| Publication-facing summaries drift from packaged content | Generate release indexes from the same structured records used for packaging |

## Dependencies

- `0017`
- `0018`
- `0019`
