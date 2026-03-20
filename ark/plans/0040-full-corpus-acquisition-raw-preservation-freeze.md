# 0040 Full Corpus Acquisition, Raw Preservation, and Freeze Plan

## Goal

Replace fixture-slice corpus evidence with literal public-data acquisition, raw preservation, and immutable freeze artifacts.

## Implementation Approach

Build acquisition helpers and freeze builders at the ingest layer, store large raw products under dedicated artifact roots, and expose normalized manifests back into the tracked benchmark pipeline.

## Steps

1. Add AGN Watch acquisition and raw-manifest helpers for the gold benchmark set.
2. Add SDSS-RM / SDSS-V RM acquisition and normalization helpers for the benchmark population and published-lag metadata.
3. Add ZTF DR24+ and CLAGN catalog acquisition helpers with cached responses, crossmatch keys, and hold-out governance.
4. Emit freeze manifests, hashes, and provenance bundles consumed by root-closeout validation and discovery packages.

## Expected File Changes

### Modified Files

- `src/echorm/ingest/agn_watch/*`
- `src/echorm/ingest/sdss_rm/*`
- `src/echorm/ingest/ztf/*`
- `src/echorm/eval/benchmark_corpus.py`
- `src/echorm/cli/benchmark.py`
- `workflows/Snakefile`
- `workflows/rules/common.smk`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Root-closeout corpus artifacts derive from real public acquisition records, not fixture-only inputs.
- Freeze manifests preserve raw-source and hold-out provenance end to end.

## Dependencies

- `0006`
- `0007`
- `0008`
- `0009`
- `0033`
- `0038`
