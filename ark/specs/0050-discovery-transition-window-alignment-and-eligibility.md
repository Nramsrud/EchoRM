# 0050 Discovery Transition-Window Alignment and Eligibility

## Summary

Repair the repository-local discovery alignment layer so CLAGN transition evidence and promoted review candidates are anchored to one deterministic adjacent spectroscopic state pair with complete photometric support.

## Scope

- Replace the deprecated first-state and last-state midpoint rule with one selected adjacent state pair per repository-local discovery object.
- Define deterministic pair selection from the recorded state sequence using only spectroscopic adjacency and raw photometric support.
- Require every pair-dependent discovery feature to derive from the selected pair, including `split_mjd`, pre-state and post-state window summaries, `lag_outlier`, `line_response_outlier`, `sonification_outlier`, pre-state and post-state lag proxies, pre-state and post-state line fluxes, line-response ratios, and transition summaries.
- Record alignment provenance explicitly, including the full state sequence, the selected pair, the split position, band-support counts, completeness status, and any exclusion reason.
- Keep repository-local discovery, promoted snapshot, and first-pass outputs explicit about which objects are transition-eligible, precursor-only, or alignment-ineligible.

## Non-Goals

- Benchmark retuning.
- Hold-out score-threshold retuning.
- External scientific or publication claims.

## Global Constraints

- The selected alignment pair must come from adjacent spectroscopic epochs in the frozen hold-out state sequence. Non-adjacent first-state and last-state compression may not drive promoted discovery outputs.
- Pair selection may depend only on state-sequence order, photometric time span, and raw band-support counts. Anomaly scores, benchmark links, and manual-review outcomes may not affect pair choice.
- Transition eligibility requires the selected split midpoint to lie within the photometric span and to have at least one `g` row and one `r` row on each side of the split, because the current lag proxy depends on both bands.
- If one or more eligible adjacent changing-state pairs exist, the selected pair must maximize `min(pre_g, pre_r, post_g, post_r)`. Ties must be broken by earliest `split_mjd`.
- If no eligible adjacent changing-state pair exists but one or more eligible adjacent same-state pairs exist, the selected pair must maximize `min(pre_g, pre_r, post_g, post_r)`. Ties must be broken by earliest `split_mjd`. The object may remain in repository-local discovery outputs only as non-transition or precursor context and must carry `state_transition_supported=false`.
- If no eligible adjacent pair exists, the object remains hold-out corpus evidence but is alignment-ineligible and may not enter the promoted discovery snapshot or transition-led first-pass review.
- `transition_detected=true` and `anomaly_category=clagn_transition` require both an eligible adjacent changing-state pair and the existing metric-based transition condition.
- The full state sequence and the selected pair must remain explicit in repository-local outputs. Downstream packages may not infer transition alignment from floating raw-file paths or undocumented heuristics.

## Acceptance Criteria

- Repository-local discovery artifacts record the selected adjacent pair, state-sequence provenance, band-support counts, completeness status, and exclusion reason for every object.
- Objects with no eligible adjacent pair are explicit and are excluded from promoted discovery snapshots.
- Objects aligned only to same-state pairs are explicit and cannot be labeled or promoted as CLAGN transitions.
- Pair-dependent discovery features and score components are derived from the selected adjacent pair rather than from the first and last catalog epochs.
- Tests verify deterministic pair selection, exclusion of alignment-ineligible objects, same-state non-transition handling, and downstream compatibility with promoted discovery snapshots and first-pass review.

## Dependencies

- `0019`
- `0035`
- `0043`
- `0048`
- `0049`
