# 0018 Optimization Infrastructure

## Summary

Define the benchmark-driven optimization layer for experiments, mappings, and controlled program optimization.

## Scope

- Define the fixed benchmark suite and objective metrics used for optimization.
- Define allowed mutation surfaces for mappings, experiment settings, and controlled program components.
- Define the search infrastructure around Ray Tune, Optuna, and Ax.
- Define the guardrails that prevent leakage from the discovery pool into optimization.

## Non-Goals

- New benchmark creation.
- Discovery ranking on real survey data.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Optimization must operate only against fixed benchmark suites, immutable labels, and explicit objective metrics.

## Acceptance Criteria

- The allowed mutation surfaces and prohibited targets are explicit.
- Search objectives, constraints, and retention rules are defined before optimization begins.
- The optimization layer preserves reproducibility, benchmark integrity, and auditability.

## Dependencies

- `0004`
- `0016`
- `0017`
