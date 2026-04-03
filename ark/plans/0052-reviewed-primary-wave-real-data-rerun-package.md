# 0052 Reviewed Primary-Wave Real-Data Rerun Package Plan

## Goal

Implement a repository-local rerun package that re-materializes discovery evidence for the manually advanced primary-wave shortlist and compares those rerun outputs to the promoted snapshot baseline.

## Implementation Approach

Add a focused rerun materializer that reads the reviewed shortlist, reloads the selected hold-out discovery records, rebuilds candidate bundles with the repaired transition-alignment logic, and emits per-candidate baseline-versus-rerun comparisons plus a concise package summary.

## Steps

1. Add a rerun package builder in `src/echorm/eval` that loads:
   - the promoted discovery snapshot
   - the first-pass review package
   - the local primary-wave manual review artifact
2. Extend the literal discovery loader so the rerun package can request only the selected candidate subset without changing the default broad discovery behavior.
3. Reuse the existing discovery candidate-build logic to materialize rerun candidate bundles for the approved shortlist rather than inventing a separate scoring path.
4. Compare each rerun candidate to its promoted-snapshot baseline, recording:
   - transition and alignment status preservation
   - score and metric deltas
   - support-count changes
   - evidence-level or fallback changes
5. Add a CLI entry point for the rerun package and tests that verify shortlist enforcement, comparison completeness, and the repository-local claims boundary.
6. Run the rerun package on the three reviewed `advance` candidates and preserve the local report.

## Expected File Changes

### Modified Files

- `ark/projectlist.md`
- `src/echorm/cli/benchmark.py`
- `src/echorm/eval/literal_corpora.py`
- `src/echorm/eval/root_closeout.py`
- `tests/test_documentation_state.py`
- `tests/test_root_authority_closeout.py`

### Added Files

- `ark/specs/0052-reviewed-primary-wave-real-data-rerun-package.md`
- `ark/plans/0052-reviewed-primary-wave-real-data-rerun-package.md`
- `ark/playbooks/0052-reviewed-primary-wave-real-data-rerun-package.md`
- `src/echorm/eval/primary_wave_rerun.py`
- `tests/test_primary_wave_rerun.py`

## Validation

- `python3 -m pytest tests/test_primary_wave_rerun.py tests/test_documentation_state.py tests/test_root_authority_closeout.py -q`
- `python3 -m ruff check src/echorm/eval/primary_wave_rerun.py src/echorm/eval/literal_corpora.py src/echorm/eval/root_closeout.py src/echorm/cli/benchmark.py tests/test_primary_wave_rerun.py tests/test_documentation_state.py tests/test_root_authority_closeout.py`
- `python3 -m mypy src tests`

## Exit Criteria

- The repository can materialize a rerun package for exactly the reviewed shortlist.
- Every rerun candidate records both the baseline promoted payload and the rerun payload with explicit comparison fields.
- The rerun package summary preserves the repository-local claims boundary and reports transition-support preservation or degradation explicitly.

## Dependencies

- `0035`
- `0043`
- `0048`
- `0049`
- `0050`
- `0051`
