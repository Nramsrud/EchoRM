# 0040 Full Corpus Acquisition, Raw Preservation, and Freeze

## Summary

Acquire, normalize, and freeze the literal gold, silver, and discovery corpora required by the root authority documents with preserved raw source products and provenance.

## Scope

- Acquire AGN Watch gold objects with raw-download preservation and parser-family metadata.
- Acquire SDSS-RM / SDSS-V RM benchmark objects with raw spectral assets, normalized derivatives, literature lag labels, and exclusion records.
- Acquire ZTF DR24+ discovery inputs and CLAGN catalog metadata with release pinning, query provenance, cached responses, and hold-out boundaries.
- Emit immutable freeze manifests with hashes, counts, strata, source identifiers, and provenance references.

## Non-Goals

- Lag inference.
- Discovery ranking.

## Global Constraints

- Raw-source products must remain immutable and traceable to public origin.
- Normalized products must remain linked to raw-source provenance, release identifiers, and query policy.
- Root-closeout promotion may not use fixture-only corpora as substitute evidence.

## Acceptance Criteria

- Gold, silver, and discovery freeze artifacts are generated from real acquired public data and include raw-preservation records.
- Freeze manifests record inclusion criteria, exclusions, strata, hashes, source URLs, release identifiers, and hold-out boundaries.
- Corpus artifacts distinguish raw, normalized, and derived products explicitly.
- Tests verify manifest completeness, raw-preservation traceability, and hold-out immutability.

## Dependencies

- `0006`
- `0007`
- `0008`
- `0009`
- `0033`
- `0038`
