# 0010 Classical Lag Wrappers

## Summary

Implement the classical cross-correlation lag methods and the method-level lag-result interface.

## Scope

- Define the wrapper contract for PyCCF.
- Define the wrapper contract for pyZDCF.
- Map method outputs into the canonical lag-result schema.
- Preserve uncertainty, significance, runtime, and configuration metadata.

## Non-Goals

- Consensus lag construction.
- Model-based lag methods.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Method wrappers must remain thin and preserve method-specific outputs rather than re-deriving them.

## Acceptance Criteria

- PyCCF outputs include centroid or peak estimates and FR/RSS uncertainty products in canonical form.
- pyZDCF outputs preserve sparse-sampling diagnostics and uncertainty information in canonical form.
- Both wrappers emit method metadata required for later agreement and alias analysis.

## Dependencies

- `0005`
- `0009`
