# 0034 Benchmark-Governed Optimization and Agent Loop Completion

## Summary

Implement the root-scope optimization layer with tracked orchestration, immutable benchmark guards, and auditable experiment outputs.

## Scope

- Extend the optimization layer to model `Ray Tune`, `Optuna`, and `Ax` backends explicitly.
- Encode Pareto-style science, sonification, and engineering objectives.
- Enforce immutable benchmark labels, manifest boundaries, and prohibited mutation zones.
- Materialize tracked optimization artifacts with backend records, objective surfaces, and guard outcomes.

## Non-Goals

- Discovery scoring on hold-out data.
- Public release packaging.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Optimization must remain downstream of fixed benchmark manifests and explicit objective metrics.
- Hold-out discovery data may not be optimized against directly or indirectly.

## Acceptance Criteria

- Optimization artifacts record backend name, mutation surface, objective values, and guard results for every trial set.
- Pareto-style objectives include science, sonification, and engineering metrics.
- Guard failures are explicit and tested.
- The optimization package is integrated into workflows, review pages, and the root closeout audit.

## Dependencies

- `0018`
- `0032`
- `0033`
