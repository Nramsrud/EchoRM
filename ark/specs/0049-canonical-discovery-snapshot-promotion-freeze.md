# 0049 Canonical Discovery Snapshot Promotion and Freeze

## Summary

Freeze and promote one repository-local `discovery_analysis` snapshot as the canonical input for first-pass review and downstream scientific interpretation.

## Scope

- Define a promoted discovery-snapshot record with the promoted run identifier, artifact path, repository revision or equivalent source reference, corpus reference, candidate inventory, candidate-order digest, and source package references.
- Require first-pass review and any downstream scientific analysis package to declare the promoted snapshot identifier and digest they analyze.
- Define divergence checks that compare newly materialized discovery outputs against the promoted snapshot and block reuse of prior findings when the candidate inventory changes.
- Preserve evidence levels, hold-out governance, benchmark links, limitations, and the real-data-rerun requirement on every promoted candidate record.

## Non-Goals

- New discovery scoring, threshold tuning, or objective tuning.
- Promotion of any candidate to a broader scientific claim.
- External-release or publication readiness.

## Global Constraints

- Exactly one promoted repository-local discovery snapshot may be canonical at a time.
- The canonical snapshot must be identified by an explicit promotion record and digest rather than by a floating artifact path or a `latest` label.
- Promotion must remain downstream of the frozen hold-out corpus and may not weaken hold-out governance.
- A change in candidate count, candidate identifiers, candidate order, evidence level, benchmark links, or corpus reference invalidates prior first-pass findings until the snapshot is explicitly re-promoted and the first pass is rerun.
- Promotion does not remove the requirement for manual review or real-data reruns before broader scientific interpretation.
- The promoted snapshot must remain explicit that it is repository-local and not equivalent to full-survey discovery closure.

## Acceptance Criteria

- A tracked promotion artifact records the canonical discovery snapshot identifier, artifact path, repository revision or equivalent source reference, corpus reference, candidate inventory, candidate-order digest, and package references.
- First-pass review artifacts declare the promoted discovery snapshot identifier and digest they analyze.
- Divergence checks fail when a newly materialized discovery snapshot differs from the promoted candidate inventory or its declared references.
- Tests verify that prior first-pass findings cannot be reused after an unpromoted discovery-snapshot change.
- Documentation states that scientific findings apply only to the promoted repository-local discovery snapshot.

## Dependencies

- `0040`
- `0043`
- `0045`
- `0048`
