# 0014 Sonification Core and Echo Ensemble

## Summary

Implement the stable sonification contract, the uncertainty-encoding policy, and the first echo-ensemble mapping family.

## Scope

- Define the stable mapping contract between scientific quantities and audio parameters.
- Implement the required uncertainty encodings.
- Define the science-audio normalization policy.
- Specify the echo-ensemble mapping for continuum drivers, delayed line responses, gaps, line width, asymmetry, and strength.

## Non-Goals

- Comparative evaluation across all mapping families.
- Discovery-scale rendering.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Uncertainty must remain explicit rather than cosmetically suppressed.

## Acceptance Criteria

- The sonification contract is stable enough to support cross-object comparison.
- Echo-ensemble mappings preserve the intended interpretations for disc-like delays, line echoes, contamination, and state changes.
- Science-audio products preserve provenance, normalization policy, and uncertainty mode.

## Dependencies

- `0005`
- `0012`
- `0013`
