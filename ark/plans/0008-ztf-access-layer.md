# 0008 ZTF Access Layer Plan

## Goal

Build the public-light-curve access layer needed for later discovery and continuum-lag work while preserving release and query provenance.

## Implementation Approach

Separate interactive retrieval, bulk-access planning, cached raw responses, and canonical normalization so the ZTF layer remains traceable and scalable from the first implementation pass.

## Steps

1. Create the ZTF access package with interfaces for API retrieval, bulk-access planning, and cached response handling.
2. Define provenance objects that preserve release identifiers, query parameters, bad-flag handling, and crossmatch keys.
3. Normalize retrieved light-curve content into the canonical photometry contract without discarding raw-response context.
4. Add tests that validate provenance capture, quality-flag preservation, and normalization of representative responses.

## Expected File Changes

### New Files

- `src/echorm/ingest/ztf/__init__.py` - ZTF access package marker
- `src/echorm/ingest/ztf/client.py` - API and bulk-access interfaces
- `src/echorm/ingest/ztf/provenance.py` - release and query metadata objects
- `src/echorm/ingest/ztf/normalize.py` - canonical photometry builders
- `tests/fixtures/ztf/` - representative ZTF response fixtures
- `tests/test_ztf_access_layer.py` - access-layer tests

### Modified Files

- `manifests/datasets.yaml` - ZTF dataset metadata

## Validation

- `python3 -m pytest tests/test_ztf_access_layer.py`
- `python3 -m mypy src tests`

## Exit Criteria

- The access layer supports both small retrieval and bulk-scale planning.
- Cached raw responses preserve release identifiers, query parameters, and quality flags.
- Canonical photometry outputs remain traceable to the public source and retrieval policy.

## Risks

| Risk | Mitigation |
|------|------------|
| Interactive and bulk pathways drift into incompatible outputs | Normalize both paths through shared provenance and canonical-output code |
| Flag or query policies are lost during caching | Encode provenance as first-class objects and assert it in tests |

## Dependencies

- `0004`
- `0005`
