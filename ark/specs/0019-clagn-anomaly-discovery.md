# 0019 CLAGN and Anomaly Discovery Extension

## Summary

Extend the validated pipeline into ZTF-scale anomaly ranking, CLAGN transition analysis, and follow-up prioritization.

## Scope

- Define continuum-lag outlier discovery.
- Define line-response anomaly analysis.
- Define CLAGN transition and precursor analysis.
- Define ranked follow-up products and anomaly-taxonomy outputs.

## Non-Goals

- Benchmark optimization.
- Publication packaging.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- The discovery pool remains a hold-out resource rather than an optimization target.

## Acceptance Criteria

- The discovery layer can rank objects by interpretable anomaly criteria rather than opaque scores alone.
- CLAGN-oriented analyses preserve transition timing, lag-state changes, and line-response evidence.
- Follow-up outputs include ranked targets, anomaly categories, and the evidence needed for scientific review.

## Dependencies

- `0008`
- `0012`
- `0015`
- `0017`
