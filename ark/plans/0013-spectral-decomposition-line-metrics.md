# 0013 Spectral Decomposition and Line Metrics Plan

## Goal

Implement the spectral preprocessing, continuum-subtraction variants, line extraction, and fit diagnostics needed for broad-line response work.

## Implementation Approach

Separate spectral preprocessing, continuum modeling, and line extraction so multiple decomposition variants remain comparable and calibration evidence is preserved with every derived metric.

## Steps

1. Add spectral preprocessing helpers for wavelength validation, extinction handling, rest-frame conversion, and derived-grid construction.
2. Implement multiple continuum-subtraction pathways, including local, pseudo-continuum, and full decomposition variants.
3. Add line-extraction routines for the primary broad-line set and serialize the resulting metrics into the canonical line-metric schema.
4. Add tests that validate fit outputs, calibration-state metadata, residual diagnostics, and cross-variant comparability on representative spectra.

## Expected File Changes

### New Files

- `src/echorm/spectra/preprocess.py` - spectral preprocessing helpers
- `src/echorm/spectra/continuum.py` - continuum-subtraction variants
- `src/echorm/spectra/lines.py` - line extraction and metric builders
- `src/echorm/spectra/diagnostics.py` - fit and calibration diagnostics
- `tests/test_spectral_line_metrics.py` - preprocessing and line-metric tests

### Modified Files

- `src/echorm/schemas/line_metrics.py` - fit-model and diagnostic helpers if needed

## Validation

- `python3 -m pytest tests/test_spectral_line_metrics.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Multiple continuum-subtraction variants exist and remain comparable.
- Primary broad-line metrics serialize into the canonical schema with uncertainty and provenance.
- Calibration-state and residual diagnostics are explicit and test-covered.

## Risks

| Risk | Mitigation |
|------|------------|
| One decomposition path becomes the accidental default truth | Keep every variant explicit in code, outputs, and tests |
| Calibration artifacts are hidden during preprocessing | Preserve calibration-state metadata and residual diagnostics throughout the pipeline |

## Dependencies

- `0005`
- `0007`
- `0009`
