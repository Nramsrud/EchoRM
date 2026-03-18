# 0007 SDSS-RM Silver Ingestion Plan

## Goal

Ingest a published-lag SDSS-RM subset into the canonical schema layer with explicit release provenance and raw-product separation.

## Implementation Approach

Use an SDSS-RM-specific ingest package that separates raw acquisition, object-level metadata, spectral-epoch indexing, and canonical tabular derivatives so later reverberation and spectral work starts from stable interfaces.

## Steps

1. Create the SDSS-RM ingest package and acquisition helpers for the published-lag subset targeted by the benchmark program.
2. Preserve raw spectral files, release identifiers, and survey metadata separately from canonical derivatives.
3. Build canonical object-manifest, spectral-epoch, and photometry products for the selected subset.
4. Add tests that validate identifier preservation, release provenance, line-coverage metadata, and separation of raw and derived products.

## Expected File Changes

### New Files

- `src/echorm/ingest/sdss_rm/__init__.py` - SDSS-RM ingest package marker
- `src/echorm/ingest/sdss_rm/acquire.py` - public-product acquisition helpers
- `src/echorm/ingest/sdss_rm/normalize.py` - canonical-output builders
- `src/echorm/ingest/sdss_rm/manifests.py` - object and release metadata helpers
- `tests/fixtures/sdss_rm/` - representative SDSS-RM metadata fixtures
- `tests/test_sdss_rm_ingestion.py` - ingest and normalization tests

### Modified Files

- `manifests/datasets.yaml` - SDSS-RM dataset metadata

## Validation

- `python3 -m pytest tests/test_sdss_rm_ingestion.py`
- `python3 -m mypy src tests`

## Exit Criteria

- A published-lag SDSS-RM subset is available in canonical object and spectral products.
- Raw spectral assets remain separate from derived tabular outputs.
- Tests preserve release identifiers, aliases, line coverage, and literature labels.

## Risks

| Risk | Mitigation |
|------|------------|
| Survey products mix acquisition metadata with derived content | Keep acquisition, raw indexing, and canonical normalization in separate modules |
| Literature-lag subset definitions drift from source releases | Pin the subset to explicit release and catalog metadata in manifests and tests |

## Dependencies

- `0004`
- `0005`
