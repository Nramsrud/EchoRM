# 0007 SDSS-RM Silver Ingestion

## Summary

Ingest the scalable published-lag benchmark set with raw spectra, object manifests, and canonical tables.

## Scope

- Define acquisition for official SDSS-RM and related public products.
- Preserve raw spectral files and survey metadata.
- Produce canonical spectral-epoch, photometry, and object-manifest products for a published-lag subset.
- Separate spectral-epoch data from derived line products.

## Non-Goals

- Discovery-scale survey sweeps.
- Spectral decomposition or lag inference.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Published-lag benchmark subsets must remain traceable to the originating data release and literature source.

## Acceptance Criteria

- A published-lag SDSS-RM subset is representable in the canonical schema layer.
- Object identifiers, aliases, line coverage, cadence metadata, and literature lag labels are preserved.
- Raw spectral assets remain separate from derived tabular products.

## Dependencies

- `0004`
- `0005`
