# 0040 Full Corpus Acquisition, Raw Preservation, and Freeze

## Summary

Freeze the repository-local gold, silver, and discovery corpora with explicit hashes, inclusion criteria, release identifiers, and hold-out governance.

## Scope

- Emit gold, silver, and discovery manifests from the tracked corpus builders.
- Preserve evidence levels, release identifiers, inclusion criteria, exclusions, manifest hashes, and crossmatch keys in those manifests.
- Encode discovery hold-out policy, strata counts, and object inventories explicitly.
- Keep corpus artifacts explicit about tracked slices rather than inferring broader survey coverage.

## Non-Goals

- Lag inference.
- Discovery ranking.

## Global Constraints

- Manifest outputs must remain immutable, hashable, and traceable to their tracked inputs.
- Discovery hold-out artifacts may not be reused as optimization targets.
- Documentation may not infer full-survey coverage from curated tracked slices.

## Acceptance Criteria

- The corpus-scaleout package includes gold, silver, and discovery manifests with counts, hashes, and strata.
- Discovery manifests record release identifiers, crossmatch keys, evidence levels, and hold-out policy explicitly.
- Corpus artifacts preserve inclusion criteria, exclusions, and manifest comparisons across the tracked tiers.
- Tests verify manifest completeness, hash stability, and hold-out governance.

## Dependencies

- `0006`
- `0007`
- `0008`
- `0009`
- `0033`
- `0038`
