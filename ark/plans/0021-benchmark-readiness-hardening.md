# 0021 Benchmark Readiness Hardening Plan

## Goal

Make the repository benchmark-ready by turning fixture-backed checks and synthetic benchmark outputs into structured run bundles with explicit readiness reporting.

## Implementation Approach

Build a tracked benchmark-run surface that assembles ingest checks, synthetic benchmark outputs, validation summaries, and verification records into one reproducible artifact bundle, then expose that bundle through command-line and workflow entry points.

## Steps

1. Add typed benchmark-run and readiness-report contracts plus JSON serialization helpers under `src/echorm/`.
2. Implement benchmark bundle assembly over the existing AGN Watch, SDSS-RM, synthetic benchmark, validation, and render-bundle surfaces.
3. Capture repository verification and tool-availability outcomes in structured readiness records with explicit warnings rather than implicit success assumptions.
4. Add a CLI entry point and workflow rule that materialize the readiness bundle into a tracked artifact directory.
5. Add tests that validate bundle completeness, readiness-state calculation, and deterministic output structure.

## Expected File Changes

### New Files

- `src/echorm/eval/readiness.py` - benchmark-run and readiness-report assembly
- `src/echorm/reports/benchmark_index.py` - human-readable benchmark readiness summaries
- `src/echorm/cli/benchmark.py` - benchmark readiness CLI entry point
- `tests/test_benchmark_readiness.py` - readiness-bundle tests

### Modified Files

- `configs/experiments/default.yaml` - benchmark run defaults if needed
- `workflows/Snakefile` - benchmark readiness workflow registration
- `workflows/rules/common.smk` - benchmark readiness workflow rule

## Validation

- `python3 -m pytest tests/test_benchmark_readiness.py`
- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`

## Exit Criteria

- The repository can materialize a benchmark readiness bundle from tracked fixtures and synthetic families.
- Readiness outputs record verification, tool availability, metrics, and artifacts in structured form.
- Tests protect the readiness bundle from structural drift.

## Risks

| Risk | Mitigation |
|------|------------|
| Readiness logic becomes another ad hoc reporting layer | Build it from typed records and canonical outputs rather than raw strings |
| Tool-availability checks create false confidence | Record unavailable tools as explicit warnings and readiness degradations |

## Dependencies

- `0004`
- `0006`
- `0007`
- `0015`
- `0016`
- `0017`
