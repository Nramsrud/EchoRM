# 0012 Consensus Lags and Null Diagnostics

## Summary

Build the consensus lag object, the agreement taxonomy, the alias diagnostics, and the null-control framework.

## Scope

- Define the consensus lag object across multiple methods.
- Classify results as agreement cluster, contested, likely spurious, or candidate anomaly.
- Define shuffled or null-pair controls and false-positive diagnostics.
- Propagate alias risk, agreement scores, and review-priority metadata.

## Non-Goals

- Implement additional lag backends.
- Conduct benchmark-scale validation studies.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- The project must not rely on a single lag method when higher-level conclusions are drawn.

## Acceptance Criteria

- The consensus object preserves method-level evidence rather than collapsing it into a single opaque number.
- Agreement, disagreement, alias risk, and null-control outcomes are explicitly represented.
- The classification policy can distinguish high-quality anomalies from low-quality or spurious cases.

## Dependencies

- `0010`
- `0011`
