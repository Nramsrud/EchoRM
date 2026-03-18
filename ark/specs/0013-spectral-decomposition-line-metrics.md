# 0013 Spectral Decomposition and Line Metrics

## Summary

Implement multi-epoch spectral decomposition, line extraction, and fit diagnostics.

## Scope

- Define the spectral preprocessing sequence from wavelength validation through rest-frame conversion.
- Preserve multiple continuum-subtraction variants.
- Define line extraction and fitted metrics for the primary broad-line set.
- Preserve fit uncertainty, residual diagnostics, and calibration-state metadata.

## Non-Goals

- Reverberation inference.
- Audio rendering.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- No single decomposition variant may be treated as uniquely authoritative.

## Acceptance Criteria

- The line-metric contract includes flux, equivalent width, width, centroid, asymmetry, uncertainty, and fit-model provenance.
- Multiple continuum-subtraction variants remain comparable and reviewable.
- Calibration confidence and residual diagnostics are explicit for each fitted epoch.

## Dependencies

- `0005`
- `0007`
- `0009`
