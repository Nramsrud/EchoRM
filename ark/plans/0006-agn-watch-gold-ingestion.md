# 0006 AGN Watch Gold Ingestion Plan

## Goal

Ingest the first gold benchmark objects from AGN Watch into the canonical schema layer while preserving raw-source fidelity.

## Implementation Approach

Build a survey-specific ingest package with parser families for the heterogeneous AGN Watch files, preserve raw metadata verbatim, and normalize outputs into the canonical object, photometry, and spectra contracts.

## Steps

1. Create the AGN Watch ingest package and a raw-source manifest format for downloaded files and object-level metadata.
2. Implement parser families for the initial AGN Watch file-format variants needed by NGC 5548 and one additional gold object.
3. Convert parsed content into canonical object-manifest and photometry or spectral products without mutating raw-source content.
4. Add fixture-backed tests that validate file parsing, metadata preservation, unit handling, and canonical-output construction.

## Expected File Changes

### New Files

- `src/echorm/ingest/agn_watch/__init__.py` - AGN Watch ingest package marker
- `src/echorm/ingest/agn_watch/parsers.py` - AGN Watch parser families
- `src/echorm/ingest/agn_watch/normalize.py` - canonical-output builders
- `src/echorm/ingest/agn_watch/manifests.py` - raw-source and object-manifest helpers
- `tests/fixtures/agn_watch/` - representative AGN Watch source fixtures
- `tests/test_agn_watch_ingestion.py` - parser and normalization tests

### Modified Files

- `manifests/datasets.yaml` - AGN Watch dataset metadata

## Validation

- `python3 -m pytest tests/test_agn_watch_ingestion.py`
- `python3 -m mypy src tests`

## Exit Criteria

- NGC 5548 and one additional gold object can be ingested into canonical outputs.
- Raw-source comments, units, and provenance remain preserved.
- Fixture-backed tests cover the supported AGN Watch format families.

## Risks

| Risk | Mitigation |
|------|------------|
| Heterogeneous legacy formats produce brittle parsers | Group formats into explicit parser families and lock them with fixtures |
| Normalization drops archival metadata needed later | Preserve raw metadata alongside canonical outputs and test for its presence |

## Dependencies

- `0004`
- `0005`
