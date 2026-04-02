# 0050 Discovery Transition-Window Alignment and Eligibility Adversarial Review

## Inputs Reviewed

- `agn_quasar_reverberation_sonification_project_plan.md`
- `agn_quasar_reverberation_sonification_agent_spec.yaml`
- `ark/specs/0019-clagn-anomaly-discovery.md`
- `ark/specs/0035-discovery-holdout-clagn-scientific-analysis.md`
- `ark/specs/0043-holdout-discovery-clagn-real-data-analysis.md`
- `ark/specs/0048-benchmark-governed-first-pass-review.md`
- `ark/specs/0049-canonical-discovery-snapshot-promotion-freeze.md`
- `ark/specs/0050-discovery-transition-window-alignment-and-eligibility.md`
- `ark/plans/0050-discovery-transition-window-alignment-and-eligibility.md`
- `src/echorm/eval/literal_corpora.py`
- `src/echorm/eval/root_closeout.py`
- `src/echorm/anomaly/clagn.py`
- `src/echorm/anomaly/candidates.py`
- `src/echorm/eval/discovery_snapshot.py`
- `src/echorm/eval/first_pass.py`

## Alignment Findings

- Root-science alignment: satisfied. The spec restores transition-aligned pre-state and post-state analysis rather than inferring transitions from an uncovered first-state and last-state midpoint.
- Hold-out alignment: satisfied. The spec uses deterministic coverage and provenance rules only and does not tune discovery scores or thresholds on hold-out results.
- Benchmark-first alignment: satisfied. The spec preserves downstream dependence on the benchmark-governed discovery and first-pass surfaces.
- Provenance alignment: satisfied. The spec requires the full state sequence, the selected pair, and the exclusion reason to remain explicit in repository-local outputs.
- Claims-boundary alignment: satisfied. The spec preserves repository-local scope and does not weaken the manual-review or real-data-rerun requirements.

## Ambiguity Checks

- Pair-choice check: satisfied. The spec defines adjacent-pair selection, the support score, and the tie-break rule explicitly.
- Feature-alignment check: satisfied. The spec requires all pair-dependent features to derive from the same selected pair.
- Transition-label check: satisfied. The spec blocks `clagn_transition` labeling unless an eligible changing-state pair exists.
- Incomplete-data check: satisfied. The spec distinguishes alignment-ineligible objects from same-state precursor context and blocks both from transition-led promotion.
- Floating-heuristic check: satisfied. The spec prohibits undocumented first-state and last-state compression and does not allow downstream packages to reconstruct alignment implicitly.

## Blocking Findings

- None.

## Plan Coverage Findings

- Adjacent-pair coverage: satisfied. The plan assigns deterministic adjacent-pair enumeration and selection to the literal discovery loader where the current split rule originates.
- Feature-rebuild coverage: satisfied. The plan explicitly requires all pair-dependent discovery features and summaries to be recomputed from the selected pair rather than patched only at promotion time.
- Transition-gating coverage: satisfied. The plan updates both transition detection and candidate categorization so same-state and alignment-ineligible objects cannot be mislabeled as CLAGN transitions.
- Downstream-governance coverage: satisfied. The plan updates snapshot promotion and first-pass review so the repaired discovery contract is preserved after materialization.
- Validation coverage: satisfied. The plan names direct tests for pair selection, same-state fallback, alignment exclusion, transition gating, and downstream compatibility.
- Ambiguity check: satisfied. The plan leaves ownership of the selection rule, transition gate, and promotion behavior explicit and does not rely on undocumented fallback heuristics.

## Implementation Review Findings

- Alignment provenance: satisfied. The implementation now carries the full state sequence, selected adjacent pair, band-support counts, completeness status, and exclusion reasons through repository-local discovery outputs.
- Transition-label safety: satisfied. `transition_detected` and `clagn_transition` now require a supported changing-state pair, while same-state supported objects remain explicit as precursor-only context.
- Promotion safety: satisfied. Alignment-ineligible objects are excluded from promoted discovery snapshots, and first-pass review operates only on the promoted subset.
- Pair-derived feature alignment: satisfied. Pair-dependent lag, line-response, and summary fields are rebuilt from the selected adjacent pair rather than the deprecated first-state and last-state midpoint rule.
- Blocking implementation findings: none. The implemented behavior matches the `0050` spec and plan.
- Downstream observation: the repaired discovery contract can yield a first-pass review with zero primary-wave candidates under the unchanged `0048` rule. This is a consequence of the existing benchmark-governed thresholds, not a `0050` implementation defect or an ambiguity in the alignment contract.

## Review Outcome

The spec and plan close the current gap in the discovery contracts. They align the code path to the root scientific requirement for transition-aligned evidence, prevent one-sided pre-state and post-state inference from being promoted, and are sufficiently explicit to guide implementation without ambiguity.
