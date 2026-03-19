# 0025 Benchmark Corpus Freeze and Multi-Method Execution Plan

## Goal

Establish the frozen benchmark corpora and real multi-method execution layer required by all later broad-validation packages.

## Implementation Approach

Build benchmark-manifest and benchmark-run infrastructure that expands the current bounded benchmark artifacts into frozen gold and silver corpora with real method execution, explicit failure capture, and null-test outputs.

## Steps

1. Define frozen benchmark-manifest schemas and builders for the gold and silver corpora, including strata, literature labels, and exclusion records.
2. Expand acquisition and normalization paths to support the benchmark corpus size selected for this package while preserving raw provenance and declared release metadata.
3. Implement real benchmark execution flows for PyCCF, pyZDCF, JAVELIN, and PyROA with structured runtime, posterior, convergence, and failure outputs.
4. Add null, shuffled-pair, misaligned-pair, and cadence-stress benchmark generation and execution paths.
5. Materialize method-level benchmark outputs and manifest indexes in tracked artifact directories consumable by downstream validation packages.
6. Add tests that validate manifest freezing, method-output structure, failure capture, and null-benchmark labeling.

## Expected File Changes

### New Files

- benchmark-manifest and benchmark-run assembly modules under `src/echorm/eval/`
- tests covering corpus freezing, method execution, and null-benchmark outputs

### Modified Files

- ingestion modules for corpus expansion and release pinning
- reverberation-method modules for real benchmark execution and diagnostic outputs
- workflow and CLI surfaces for benchmark-manifest and method-run materialization

## Validation

- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`
- tracked benchmark-manifest and method-execution commands for the gold and silver corpora

## Exit Criteria

- Frozen gold and silver benchmark manifests exist as tracked artifacts with explicit labels and exclusions.
- Real benchmark execution artifacts exist for PyCCF, pyZDCF, JAVELIN, and PyROA over the selected corpus slice.
- Null and cadence-stress outputs are materialized with explicit provenance and labels.

## Risks

| Risk | Mitigation |
|------|------------|
| Benchmark manifests drift after reporting begins | Freeze manifests and store hashes before downstream validation packages consume them |
| Method wrappers appear benchmark-ready without real execution evidence | Require tracked method-level outputs, failures, and diagnostics for each benchmark run |

## Dependencies

- `0006`
- `0007`
- `0010`
- `0011`
- `0012`
- `0016`
- `0021`
- `0023`
- `0024`
