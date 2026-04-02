# 0051 Transition-Supported First-Pass Governance Correction

## Summary

Correct the repository-local first-pass review rule so primary-wave admission follows repaired transition-support evidence rather than direction-specific hold-out heuristics that are not benchmark-justified.

## Scope

- Redefine primary-wave admission for promoted discovery candidates using explicit transition-support fields from the repaired discovery contract.
- Keep same-state precursor context and transition-negative candidates explicit in the deferred wave with bounded rationale.
- Preserve signed lag-change and line-response fields as reported interpretation evidence without using them as hard first-pass exclusion rules.
- Keep benchmark links, review priority, and rank score available for deterministic review ordering within the bounded repository-local review surface.

## Non-Goals

- Hold-out threshold retuning.
- Discovery score retuning.
- External scientific or publication claims.

## Global Constraints

- This package applies only to the repository-local `first_pass_review` surface built from a promoted discovery snapshot.
- Primary-wave admission must include every promoted candidate with `state_transition_supported=true` and `transition_detected=true`.
- Same-state supported candidates with `state_transition_supported=false` may remain in the promoted snapshot as precursor context but must remain deferred.
- Alignment-eligible candidates with `transition_detected=false` must remain deferred.
- `lag_state_change` and `line_response_ratio` must remain explicit in candidate records and reports as signed or directional interpretation fields, but they may not be used as hard primary-wave admission or exclusion criteria unless a later benchmark-governed spec establishes direction-specific benchmark support for that use.
- Primary-wave and deferred-wave ordering must be deterministic and derived only from tracked `review_priority`, `rank_score`, `benchmark_links`, and `object_uid` fields.
- Every candidate must remain under manual scientific review and a real-data-rerun requirement before broader scientific interpretation.
- The package must remain explicit that discovery evidence is repository-local and bounded by the promoted snapshot, benchmark labels, and limitations.

## Acceptance Criteria

- A rerun of `first_pass_review` places every promoted supported transition in the primary wave and keeps precursor-only or transition-negative cases deferred.
- Candidate records and the report preserve signed lag-change and line-response fields while no longer treating them as hard first-pass admission thresholds.
- Review ordering remains deterministic and traceable to tracked fields.
- The emitted package continues to state repository-local scope, benchmark linkage, manual-review requirements, and the real-data-rerun boundary explicitly.
- Tests verify transition-supported admission, precursor-only deferral, transition-negative deferral, deterministic ordering, and preservation of the claims boundary.

## Dependencies

- `0035`
- `0043`
- `0048`
- `0049`
- `0050`
