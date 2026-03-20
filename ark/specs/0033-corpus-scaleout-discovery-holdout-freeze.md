# 0033 Corpus Scale-Out and Discovery Hold-Out Freeze

## Summary

Scale the benchmark and discovery corpora to the full root-scope manifests with explicit hold-out governance, benchmark strata, and provenance.

## Scope

- Expand the frozen benchmark manifest layer to include full-scope gold, broad silver, and discovery-hold-out records.
- Record immutable inclusion criteria, exclusions, benchmark strata, release identifiers, and manifest hashes.
- Add tracked discovery-hold-out fixtures and manifest outputs for ZTF and CLAGN-oriented analysis.
- Materialize a package-level artifact that reports corpus coverage, hold-out governance, and provenance completeness.

## Non-Goals

- Optimization runs.
- Discovery scoring and candidate ranking.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Discovery manifests must encode hold-out boundaries explicitly and may not be reused as optimization targets.
- Manifest artifacts must preserve provenance, release identifiers, and exclusion reasons directly.

## Acceptance Criteria

- Gold, silver, and discovery manifest artifacts exist with hashes, strata counts, inclusion criteria, and explicit exclusions.
- Discovery records include release pinning, crossmatch keys, and hold-out governance metadata.
- The corpus-scaleout package is integrated into the workflow and review surface.
- Tests verify manifest completeness, hash stability, and hold-out boundaries.

## Dependencies

- `0006`
- `0007`
- `0008`
- `0009`
- `0025`
