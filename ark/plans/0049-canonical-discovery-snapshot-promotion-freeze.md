# 0049 Canonical Discovery Snapshot Promotion and Freeze Plan

## Goal

Implement one canonical promotion surface for `discovery_analysis` so first-pass review and any later scientific interpretation are tied to an explicit promoted snapshot rather than an implicit artifact root.

## Implementation Approach

Add a promotion package that snapshots the selected `discovery_analysis` run into a stable record with source references and digests, require first-pass review to consume that promotion record, and add divergence checks that block reuse of prior findings after an unpromoted discovery change.

## Steps

1. Add a discovery-snapshot promotion builder that reads a selected `discovery_analysis` run and emits a promotion artifact with:
   - promoted snapshot identifier
   - source run identifier and artifact path
   - repository revision or equivalent source reference
   - corpus reference
   - candidate inventory
   - candidate-order digest
   - package references and preserved claims-boundary fields
2. Add a tracked CLI entry point for the promotion package so canonical promotion is reproducible from repository commands rather than manual file selection.
3. Update the first-pass review package to require a promoted snapshot input and to record the promoted snapshot identifier and digest in every first-pass run.
4. Add divergence checks that compare a newly materialized `discovery_analysis` run to the promoted snapshot and fail when candidate count, candidate identifiers, candidate order, evidence level, benchmark links, or corpus reference differ.
5. Ensure the promotion artifact and the first-pass package both preserve hold-out governance, repository-local scope, limitations, and the real-data-rerun requirement.
6. Add tests that prove:
   - promotion records are complete and deterministic
   - first-pass review artifacts declare the promoted snapshot they analyze
   - divergence checks fail on unpromoted snapshot changes
   - stale first-pass findings cannot be reused after divergence
7. Update project metadata and documentation so `0049` is recorded as the canonical governance layer for discovery-snapshot reuse.

## Expected File Changes

### Modified Files

- `ark/projectlist.md`
- `ark/playbooks/0049-canonical-discovery-snapshot-promotion-freeze.md`
- `src/echorm/cli/benchmark.py`
- `src/echorm/eval/first_pass.py`
- `tests/test_documentation_state.py`
- `tests/test_first_pass_review.py`
- `tests/test_root_authority_closeout.py`

### Added Files

- `ark/plans/0049-canonical-discovery-snapshot-promotion-freeze.md`
- `src/echorm/eval/discovery_snapshot.py`
- `tests/test_discovery_snapshot.py`

## Validation

- `python3 -m pytest tests/test_discovery_snapshot.py tests/test_first_pass_review.py tests/test_root_authority_closeout.py tests/test_documentation_state.py -q`
- `python3 -m ruff check src/echorm/eval/discovery_snapshot.py src/echorm/eval/first_pass.py src/echorm/cli/benchmark.py tests/test_discovery_snapshot.py tests/test_first_pass_review.py tests/test_root_authority_closeout.py tests/test_documentation_state.py`
- `python3 -m mypy src tests`

## Exit Criteria

- The repository can promote exactly one canonical repository-local discovery snapshot through a tracked artifact.
- First-pass review artifacts are explicit about which promoted snapshot they analyze.
- Divergence between a newly materialized discovery run and the promoted snapshot blocks reuse of prior first-pass findings until re-promotion and rerun.
- The implementation preserves hold-out governance, repository-local scope, and the real-data-rerun requirement without ambiguity.

## Dependencies

- `0040`
- `0043`
- `0045`
- `0048`
