# 0014 Sonification Core and Echo Ensemble Plan

## Goal

Implement the stable science-to-audio contract, the uncertainty-encoding policy, and the first echo-ensemble mapping family.

## Implementation Approach

Build a reusable sonification core that separates normalization policy, uncertainty encodings, and mapping logic, then implement the echo-ensemble family on top of that shared surface.

## Steps

1. Add the sonification core types for mapping configuration, provenance, normalization, and render inputs.
2. Implement the required uncertainty encodings and make them selectable through the mapping configuration rather than hard-coded behavior.
3. Implement the echo-ensemble mapping from continuum drivers, delayed line responses, gaps, line width, asymmetry, and strength into audio controls.
4. Add tests that validate mapping determinism, uncertainty-mode preservation, and canonical sonification-manifest construction.

## Expected File Changes

### New Files

- `src/echorm/sonify/base.py` - shared sonification types and configuration
- `src/echorm/sonify/uncertainty.py` - uncertainty-encoding implementations
- `src/echorm/sonify/echo_ensemble.py` - echo-ensemble mapping family
- `src/echorm/sonify/render.py` - science-audio render helpers
- `tests/test_echo_ensemble.py` - sonification-core tests

### Modified Files

- `src/echorm/schemas/sonifications.py` - sonification-manifest helpers if needed

## Validation

- `python3 -m pytest tests/test_echo_ensemble.py`
- `python3 -m mypy src tests`

## Exit Criteria

- The sonification core can represent normalization policy, provenance, and uncertainty mode explicitly.
- Echo-ensemble outputs preserve the intended delay and response relationships.
- Tests protect determinism and manifest construction.

## Risks

| Risk | Mitigation |
|------|------------|
| Mapping logic becomes entangled with rendering details | Separate mapping, uncertainty, and rendering into distinct modules |
| Uncertainty is visually or aurally suppressed for convenience | Make uncertainty mode a first-class, tested part of the render contract |

## Dependencies

- `0005`
- `0012`
- `0013`
