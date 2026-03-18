# 0008 ZTF Access Layer

## Summary

Define the public-light-curve access layer for the discovery pool, with release pinning and query provenance.

## Scope

- Define small and medium retrieval through public APIs.
- Define bulk-access and parquet pathways for larger retrieval jobs.
- Preserve query constraints, source release identifiers, bad-flag policies, and crossmatch keys.
- Define cached raw-response storage and normalized tabular products.

## Non-Goals

- Discovery ranking.
- Continuum-lag inference at scale.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Data release identifiers and query provenance must remain explicit.

## Acceptance Criteria

- The access layer supports both interactive retrieval and bulk-scale access planning.
- Cached responses preserve release identifiers, query parameters, and quality flags.
- Canonical products remain traceable to the public source and retrieval policy.

## Dependencies

- `0004`
- `0005`
