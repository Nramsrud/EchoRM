# 0037 Public Release and Publication Closeout Plan

## Goal

Assemble the provenance-complete release and root closeout audit required to satisfy the root authority documents.

## Implementation Approach

Extend the existing catalog and release helpers into structured package builders that consume benchmark, optimization, discovery, and review outputs, then emit one root closeout audit over the integrated program.

## Steps

1. Extend catalog and release builders to package benchmark outputs, discovery candidates, audio products, and provenance records together.
2. Add publication-facing index builders and release documentation generated from the structured release bundle.
3. Implement the root closeout audit that checks benchmark, advanced-method, corpus, optimization, discovery, review, and release gates together.
4. Add tests that verify bundle completeness, provenance coverage, and root audit outcomes.

## Expected File Changes

### Modified Files

- `src/echorm/reports/catalog.py`
- `src/echorm/reports/release.py`
- `src/echorm/cli/benchmark.py`
- `workflows/Snakefile`
- `workflows/rules/common.smk`
- `tests/test_release_artifacts.py`
- `tests/test_root_authority_closeout.py`

## Validation

- `python3 -m pytest tests/test_release_artifacts.py tests/test_root_authority_closeout.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Release bundles are generated from tracked structured artifacts and include provenance coverage.
- Publication-facing summaries are artifact-derived and suitable for external review.
- The root closeout audit determines whether the full root authority is satisfied.

## Risks

| Risk | Mitigation |
|------|------------|
| Release bundles drift from the underlying artifacts | Generate indexes and summaries directly from the structured release bundle |
| Root audit overstates completion | Require explicit conditions for every root-scope package and retain limitations in the audit output |

## Dependencies

- `0020`
- `0035`
- `0036`
