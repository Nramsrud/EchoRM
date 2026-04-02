# 0050 Discovery Transition-Window Alignment and Eligibility Plan

## Goal

Implement one deterministic adjacent-pair alignment rule for repository-local discovery objects so transition evidence, pair-dependent features, and promoted review candidates remain scientifically usable and traceable.

## Implementation Approach

Replace first-state and last-state midpoint compression with an adjacent-pair selector driven only by state-sequence order and raw band support, carry the selected-pair provenance through discovery artifacts, and gate transition labeling and downstream promotion on that explicit alignment record.

## Steps

1. Add an adjacent-pair analysis layer in `src/echorm/eval/literal_corpora.py` that:
   - records the full ordered spectroscopic state sequence for each discovery object
   - enumerates adjacent candidate pairs and their midpoint splits
   - measures per-side `g` and `r` support counts and split coverage against the raw photometric span
   - selects one pair deterministically by the `0050` support rule and tie-break rule
   - records whether the selected pair is changing-state, same-state, or alignment-ineligible
2. Rebuild repository-local discovery features from the selected pair in `src/echorm/eval/literal_corpora.py`, including:
   - `split_mjd`
   - pre-state and post-state lag proxies
   - pre-state and post-state line fluxes
   - pair-dependent anomaly features and window summaries
   - alignment provenance and exclusion metadata in `query_params` and notes
3. Update discovery package materialization in `src/echorm/eval/root_closeout.py` so every candidate payload records:
   - the full state sequence
   - selected-pair provenance
   - band-support counts and completeness status
   - `state_transition_supported`
   - explicit alignment eligibility and exclusion reason
4. Update transition and category logic in `src/echorm/anomaly/clagn.py` and `src/echorm/anomaly/candidates.py` so:
   - `transition_detected=true` requires both the existing metric condition and a changing-state supported pair
   - `anomaly_category=clagn_transition` is impossible for same-state or alignment-ineligible objects
   - same-state supported objects remain available as non-transition or precursor discovery context
5. Update downstream governance in `src/echorm/eval/discovery_snapshot.py` and `src/echorm/eval/first_pass.py` so:
   - promoted snapshots exclude alignment-ineligible objects
   - complete same-state objects may remain in promoted discovery context but cannot enter transition-led first-pass behavior through mislabeled transition fields
   - first-pass reporting remains explicit about supported transitions versus precursor-only candidates
6. Add tests that prove:
   - deterministic adjacent-pair selection and tie-breaking
   - same-state fallback behavior when no changing-state eligible pair exists
   - exclusion of alignment-ineligible objects from promoted snapshots
   - transition gating and category safety for same-state and incomplete objects
   - downstream first-pass compatibility with the repaired discovery payloads
7. Update project metadata and documentation checks so `0050` is tracked as a spec-plan-review package and remains part of the canonical repository-local governance surface.

## Expected File Changes

### Modified Files

- `ark/projectlist.md`
- `ark/playbooks/0050-discovery-transition-window-alignment-and-eligibility.md`
- `src/echorm/anomaly/candidates.py`
- `src/echorm/anomaly/clagn.py`
- `src/echorm/eval/discovery_snapshot.py`
- `src/echorm/eval/first_pass.py`
- `src/echorm/eval/literal_corpora.py`
- `src/echorm/eval/root_closeout.py`
- `tests/test_clagn_anomaly_discovery.py`
- `tests/test_discovery_snapshot.py`
- `tests/test_documentation_state.py`
- `tests/test_first_pass_review.py`
- `tests/test_literal_corpora.py`
- `tests/test_root_authority_closeout.py`

### Added Files

- `ark/plans/0050-discovery-transition-window-alignment-and-eligibility.md`

## Validation

- `python3 -m pytest tests/test_literal_corpora.py tests/test_clagn_anomaly_discovery.py tests/test_discovery_snapshot.py tests/test_first_pass_review.py tests/test_root_authority_closeout.py tests/test_documentation_state.py -q`
- `python3 -m ruff check src/echorm/eval/literal_corpora.py src/echorm/eval/root_closeout.py src/echorm/anomaly/clagn.py src/echorm/anomaly/candidates.py src/echorm/eval/discovery_snapshot.py src/echorm/eval/first_pass.py tests/test_literal_corpora.py tests/test_clagn_anomaly_discovery.py tests/test_discovery_snapshot.py tests/test_first_pass_review.py tests/test_root_authority_closeout.py tests/test_documentation_state.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Repository-local discovery objects carry one explicit selected adjacent pair or an explicit alignment-ineligible record.
- Pair-dependent discovery features and transition summaries are derived from the selected adjacent pair rather than first-state and last-state compression.
- Same-state supported objects remain explicit without being mislabeled as CLAGN transitions.
- Alignment-ineligible objects cannot enter promoted discovery snapshots.
- First-pass review remains compatible with the repaired discovery payloads and preserves hold-out governance, repository-local scope, and the real-data-rerun requirement.

## Dependencies

- `0019`
- `0035`
- `0043`
- `0048`
- `0049`
