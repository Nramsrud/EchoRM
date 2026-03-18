# 0005 Canonical Schemas and Manifest Layer Plan

## Goal

Define the canonical data contracts that all later ingestion, inference, sonification, and reporting code will target.

## Implementation Approach

Represent the canonical contracts in typed Python modules, keep the schema surface explicit and reviewable, and add validation tests that lock the required columns, provenance fields, and quality metadata.

## Steps

1. Add a schema module under `src/echorm/` for object manifests, photometry, spectral epochs, line metrics, lag results, and sonification records.
2. Encode the required fields, provenance metadata, and quality-control columns in a form suitable for tabular export and validation.
3. Add manifest templates or helper constructors for dataset-level and object-level metadata under `manifests/`.
4. Add tests that verify required columns, field ordering or naming constraints, and compatibility with downstream serialization targets.

## Expected File Changes

### New Files

- `src/echorm/schemas/__init__.py` - schema package marker
- `src/echorm/schemas/objects.py` - object manifest contract
- `src/echorm/schemas/photometry.py` - photometry contract
- `src/echorm/schemas/spectra.py` - spectral-epoch contract
- `src/echorm/schemas/line_metrics.py` - line-metric contract
- `src/echorm/schemas/lags.py` - lag-result contract
- `src/echorm/schemas/sonifications.py` - sonification contract
- `manifests/datasets.yaml` - dataset-level manifest template
- `tests/test_schemas.py` - schema validation tests

### Modified Files

- `README.md` - public description of canonical data contracts if needed

## Validation

- `python3 -m pytest tests/test_schemas.py`
- `python3 -m mypy src tests`

## Exit Criteria

- All six canonical contracts exist in tracked code.
- Required provenance, quality, and comparison fields are encoded explicitly.
- Tests protect the schema surface from accidental drift.

## Risks

| Risk | Mitigation |
|------|------------|
| Schema definitions become too abstract to guide implementation | Encode concrete field names and validation rules directly in code and tests |
| Early contracts omit critical provenance or QC fields | Review each contract against the authority documents before freezing the first pass |

## Dependencies

- `0002`
- `0003`
