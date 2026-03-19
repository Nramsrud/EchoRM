# 0025 Benchmark Corpus Freeze and Multi-Method Execution Plan

## Goal

Establish the frozen benchmark corpora and real multi-method execution layer required by all later broad-validation packages.

## Implementation Approach

Build benchmark-manifest and benchmark-run infrastructure that expands the current bounded benchmark artifacts into frozen gold and silver corpora with real method execution, explicit failure capture, and null-test outputs.

## Steps

1. Define frozen benchmark-manifest schemas and builders for the gold and silver corpora, including strata, literature labels, exclusion records, evidence labels, and manifest hashes.
2. Expand acquisition and normalization paths to support the benchmark corpus size selected for this package while preserving raw provenance, declared release metadata, and explicit response-evidence labeling.
3. Implement benchmark execution flows for PyCCF, pyZDCF, JAVELIN, and PyROA with structured runtime, posterior, convergence, and failure outputs for every selected object.
4. Add reversed-response, shuffled-pair, misaligned-pair, and sparse-cadence null-benchmark generation and execution paths.
5. Materialize method-level benchmark outputs, manifest indexes, and rerun-stability records in tracked artifact directories consumable by downstream validation packages.
6. Add tests that validate manifest freezing, method-output structure, failure capture, evidence labeling, null-benchmark labeling, and rerun reproducibility.

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

- Frozen gold and silver benchmark manifests exist as tracked artifacts with explicit labels, exclusions, strata counts, and hashes.
- Benchmark execution artifacts exist for PyCCF, pyZDCF, JAVELIN, and PyROA over the selected corpus slice with runtime, convergence, and failure metadata.
- Response evidence is labeled explicitly for every object, and proxy evidence is never conflated with direct real-series evidence.
- Null outputs are materialized for reversed-response, shuffled-pair, misaligned-pair, and sparse-cadence variants with explicit provenance and labels.

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
