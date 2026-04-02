# 0040 Full Corpus Acquisition, Raw Preservation, and Freeze Plan

## Goal

Maintain repository-local corpus manifests with explicit provenance fields, immutable hashes, and clear hold-out governance.

## Implementation Approach

Route corpus builders through one manifest schema, preserve tier-level comparisons and hashes, and keep hold-out governance explicit in the generated package.

## Steps

1. Consolidate gold, silver, and discovery manifest builders around explicit inclusion, exclusion, hash, and release fields.
2. Ensure discovery manifests preserve crossmatch keys, evidence levels, and hold-out policy.
3. Keep corpus-scaleout comparisons and object summaries aligned to those manifests.
4. Add tests that fail when required manifest fields or hold-out controls are missing.

## Expected File Changes

### Modified Files

- `src/echorm/eval/root_closeout.py`
- `src/echorm/eval/literal_corpora.py`
- `src/echorm/cli/benchmark.py`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Corpus-scaleout artifacts preserve traceable repository-local manifests across all tracked tiers.
- Discovery hold-out governance remains explicit end to end.

## Dependencies

- `0006`
- `0007`
- `0008`
- `0009`
- `0033`
- `0038`
