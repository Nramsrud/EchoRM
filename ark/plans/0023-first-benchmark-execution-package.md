# 0023 First Benchmark Execution Package Plan

## Goal

Execute the first bounded benchmark package and express its scientific evidence level clearly enough that readiness is no longer confused with validation.

## Implementation Approach

Build a benchmark-package layer on top of the readiness bundle that assembles real-fixture ingestion checks, synthetic lag-recovery evaluations, explicit evidence-level labeling, and a human-readable benchmark dossier consumable by the review web interface.

## Steps

1. Add typed first-benchmark case and package contracts that encode evidence level, metric family, benchmark type, and claims boundaries.
2. Implement fixture-backed benchmark cases for the initial AGN Watch and SDSS-RM objects using the committed public fixtures and canonical normalization surfaces.
3. Implement synthetic lag-recovery benchmark cases over the current reverberation adapters and validation metrics.
4. Add benchmark dossier and index outputs that state demonstrated capability, non-demonstrated capability, limitations, and next required benchmark work.
5. Extend the benchmark CLI and workflow stack to materialize the first benchmark package into tracked artifacts compatible with the review web interface.
6. Add tests that validate benchmark taxonomy, evidence-level integrity, dossier language, and deterministic package generation.
7. Update the local documentation standard, lessons learned, and role documents so all agents treat scientific scope, claims, and benchmark evidence rigorously.

## Expected File Changes

### New Files

- `src/echorm/eval/first_benchmark.py` - first benchmark case assembly and package logic
- `src/echorm/reports/benchmark_dossier.py` - benchmark dossier and claims-boundary summaries
- `tests/test_first_benchmark_package.py` - first benchmark package tests

### Modified Files

- Local documentation standard - scientific development and claims-boundary rules
- `ark/resources/lessons-learned.md` - benchmark-scope lesson
- `.ark/roles/architect.md` - scientific-rigor operating guidance
- `.ark/roles/builder.md` - scientific-rigor operating guidance
- `.ark/roles/evolve-builder.md` - scientific-rigor operating guidance
- `.ark/roles/evolve-orchestrator.md` - scientific-rigor operating guidance
- `.ark/roles/evolve-curator.md` - scientific-rigor operating guidance
- `src/echorm/cli/benchmark.py` - first benchmark package command
- `workflows/Snakefile` - first benchmark workflow registration
- `workflows/rules/common.smk` - first benchmark workflow rule

## Validation

- `python3 -m pytest tests/test_first_benchmark_package.py`
- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`
- `snakemake --snakefile workflows/Snakefile --dry-run`
- `python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id first_benchmark first-benchmark`

## Exit Criteria

- The repository can materialize a first benchmark package with explicit evidence-level labeling and benchmark taxonomy.
- The benchmark dossier states demonstrated capability, limitations, and next required scientific work without overstating the evidence.
- Role and standards documents explicitly require rigorous benchmark-scope labeling and claims discipline.

## Risks

| Risk | Mitigation |
|------|------------|
| The first benchmark is misread as broad scientific validation | Encode evidence-level labels and claims boundaries in both JSON and human-readable summaries |
| Synthetic and real-fixture evidence get conflated in reporting | Keep benchmark type and metric family explicit on every case and aggregate them separately |

## Dependencies

- `0006`
- `0007`
- `0010`
- `0016`
- `0017`
- `0021`
- `0022`
