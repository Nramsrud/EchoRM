# 0006 AGN Watch Gold Ingestion

## Summary

Ingest the gold benchmark archive with raw preservation, object manifests, and canonical tables.

## Scope

- Preserve AGN Watch raw files exactly as downloaded.
- Define parser families for heterogeneous AGN Watch formats.
- Produce object manifests and canonical photometry or spectra products for the initial gold objects.
- Establish fixture-backed parser validation for the first gold benchmark objects.

## Non-Goals

- Large-scale population ingestion.
- Reverberation inference or sonification.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Raw files must remain immutable and traceable to source.

## Acceptance Criteria

- NGC 5548 and one additional gold object can be ingested into the canonical schema layer.
- Raw-source provenance, metadata, comments, and units are preserved.
- Parser fixtures and validation rules cover the supported AGN Watch format families.

## Dependencies

- `0004`
- `0005`
