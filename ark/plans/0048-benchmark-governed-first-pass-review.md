# 0048 Benchmark-Governed First-Pass Review Plan

## Goal

Implement a repository-local first-pass review package that converts the current benchmark and discovery artifacts into a deterministic review sequence for the hold-out pool.

## Implementation Approach

Consume the tracked validation, discovery, and audit packages, encode explicit review-wave rules and dispositions, and emit a machine-readable package plus a concise report without weakening the existing claims boundary.

## Steps

1. Add a first-pass package builder and tracked CLI entry point that read the required benchmark, discovery, and audit artifacts.
2. Encode the benchmark anchor set from `NGC 5548`, `NGC 3783`, and the tracked silver, continuum, efficacy, and root-authority package summaries.
3. Encode the primary-wave rule as `transition_detected=true`, `lag_state_change>=1.2`, `line_response_ratio<=0.55`, and `rank_score>=0.76`, with all other candidates deferred to a later wave.
4. Emit structured anchor records, candidate-review records, and a concise report with explicit limitations, required next actions, and the real-data-rerun requirement for every candidate.
5. Add tests that verify package completeness, deterministic phasing, and claims-boundary preservation.
6. Run the first-pass command against the tracked artifact root and preserve the resulting report.

## Expected File Changes

### Modified Files

- `ark/projectlist.md`
- `src/echorm/cli/benchmark.py`
- `tests/test_documentation_state.py`
- `tests/test_root_authority_closeout.py`

### Added Files

- `ark/specs/0048-benchmark-governed-first-pass-review.md`
- `ark/plans/0048-benchmark-governed-first-pass-review.md`
- `ark/playbooks/0048-benchmark-governed-first-pass-review.md`
- `src/echorm/eval/first_pass.py`
- `tests/test_first_pass_review.py`

## Validation

- `python3 -m pytest tests/test_first_pass_review.py tests/test_root_authority_closeout.py tests/test_documentation_state.py -q`
- `python3 -m ruff check src/echorm/eval/first_pass.py tests/test_first_pass_review.py`
- `python3 -m mypy src tests`

## Exit Criteria

- The repository can materialize a reproducible first-pass review package from tracked artifacts.
- The resulting package records anchor calibrators, review waves, candidate dispositions, and explicit claims boundaries without ambiguity.

## Dependencies

- `0026`
- `0027`
- `0028`
- `0029`
- `0043`
- `0045`
