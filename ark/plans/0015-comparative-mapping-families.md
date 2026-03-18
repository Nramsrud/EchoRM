# 0015 Comparative Mapping Families and Render Bundles Plan

## Goal

Add the direct-audification and feature-token mapping families plus the standardized render bundle for finalized objects.

## Implementation Approach

Build the additional mapping families on the shared sonification core, then standardize the output bundle so every finalized object has comparable audio, provenance, and explanatory artifacts.

## Steps

1. Implement the direct-audification mapping family on top of the shared sonification core.
2. Implement the feature-token mapping family for compressed anomaly-review use cases.
3. Add bundle builders for channel stems, synchronized visual outputs, legends, and provenance records.
4. Add tests that verify cross-family comparability, bundle completeness, and preservation of mapping metadata.

## Expected File Changes

### New Files

- `src/echorm/sonify/direct_audification.py` - direct-audification mapping family
- `src/echorm/sonify/token_stream.py` - feature-token mapping family
- `src/echorm/reports/render_bundle.py` - finalized object bundle builders
- `tests/test_mapping_families.py` - comparative mapping and bundle tests

### Modified Files

- `src/echorm/sonify/base.py` - family registration helpers if needed
- `src/echorm/schemas/sonifications.py` - bundle-facing provenance fields if needed

## Validation

- `python3 -m pytest tests/test_mapping_families.py`
- `python3 -m mypy src tests`

## Exit Criteria

- The direct-audification and feature-token families are implemented on the shared core.
- Finalized object bundles include the required audio, provenance, and explanatory artifacts.
- Tests protect comparability across mapping families.

## Risks

| Risk | Mitigation |
|------|------------|
| Additional mapping families diverge from the shared contract | Require both families to use the same configuration and provenance surfaces |
| Bundle outputs become inconsistent across objects | Build bundles through one standardized report module and test for completeness |

## Dependencies

- `0014`
