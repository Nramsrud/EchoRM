# 0033 Corpus Scale-Out and Discovery Hold-Out Freeze Plan

## Goal

Implement the full-scope manifest and hold-out-governance layer required by the root authority documents.

## Implementation Approach

Extend the existing benchmark-corpus loaders with additional tracked discovery fixtures and emit one dedicated corpus-freeze package that summarizes benchmark and discovery scope together.

## Steps

1. Add tracked discovery-hold-out fixtures and normalized records for ZTF and CLAGN-style objects.
2. Extend manifest builders to capture release identifiers, strata, exclusions, hold-out policy, and manifest hashes.
3. Implement a corpus-scaleout package that writes benchmark and discovery manifests plus a governance summary.
4. Add tests that verify manifest hashes, discovery hold-out boundaries, and provenance metadata.

## Expected File Changes

### New Files

- `tests/fixtures/ztf/discovery_holdout_population.json`

### Modified Files

- `src/echorm/eval/benchmark_corpus.py`
- `src/echorm/cli/benchmark.py`
- `workflows/Snakefile`
- `workflows/rules/common.smk`
- `tests/test_root_authority_closeout.py`

## Validation

- `python3 -m pytest tests/test_root_authority_closeout.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Full-scope manifest artifacts are generated from tracked commands.
- Discovery-hold-out records are explicit, hashable, and excluded from optimization surfaces.
- The corpus-scaleout package is inspectable through the review application.

## Risks

| Risk | Mitigation |
|------|------------|
| Discovery manifests blur benchmark and hold-out roles | Encode corpus type and hold-out policy directly in each manifest and test the guard paths |
| Manifest scale-out introduces unstable hashes | Build hashes from canonical ordered fields only and verify them in tests |

## Dependencies

- `0006`
- `0007`
- `0008`
- `0009`
- `0025`
