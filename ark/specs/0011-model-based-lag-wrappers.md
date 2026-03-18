# 0011 Model-Based Lag Wrappers

## Summary

Implement the initial model-based lag methods and the required convergence and uncertainty diagnostics.

## Scope

- Define the wrapper contract for JAVELIN.
- Define the wrapper contract for PyROA.
- Map posterior summaries, convergence diagnostics, and configuration metadata into the canonical lag-result schema.
- Support multi-light-curve fits where method capability requires it.

## Non-Goals

- Consensus lag construction.
- Later-stage advanced methods such as LITMUS or MICA2.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Posterior and convergence metadata must remain available for downstream review.

## Acceptance Criteria

- JAVELIN outputs preserve lag summaries, uncertainty ranges, and method configuration metadata.
- PyROA outputs preserve posterior summaries, latent-driver context, and convergence diagnostics.
- The wrapper layer remains comparable with the canonical lag-result schema without erasing method-specific evidence.

## Dependencies

- `0005`
- `0009`
