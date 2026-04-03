# 0052 Reviewed Primary-Wave Real-Data Rerun Package

## Summary

Materialize a repository-local rerun package for manually advanced primary-wave discovery candidates, recomputing their live ZTF-backed discovery evidence and comparing the rerun outputs to the promoted snapshot that selected them.

## Scope

- Consume the promoted discovery snapshot, the current first-pass review package, and the local primary-wave manual review artifact.
- Restrict rerun execution to candidates explicitly marked `advance` in the manual review artifact.
- Recompute discovery candidate bundles for those candidates from repository-local raw photometry and catalog-transition inputs.
- Record candidate-level comparisons between rerun outputs and the promoted discovery snapshot, including transition status, alignment status, support counts, score components, and metric deltas.
- Preserve rerun provenance, evidence level, claims boundary, and the manual-review rationale that authorized each rerun.

## Non-Goals

- New discovery threshold tuning.
- Promotion of rerun outputs to external scientific claims.
- Replacing benchmark governance, manual review, or later real-data interpretation steps.

## Global Constraints

- The rerun package must remain repository-local and explicitly downstream of the promoted discovery snapshot and the manual review artifact.
- Only candidates listed in `recommended_rerun_candidates` from the manual review artifact may be rerun.
- The rerun package may recompute discovery evidence only from the existing hold-out discovery inputs and the same repaired transition-alignment contract; it may not change scoring logic or first-pass governance.
- The package must keep the baseline promoted candidate payload and the rerun candidate payload separate and compare them explicitly rather than overwriting the promoted snapshot.
- If a rerun candidate falls back to offline photometry or loses transition support, the package must record that state explicitly and may not silently treat the rerun as equivalent to the promoted snapshot.
- Every rerun record must remain under the repository-local claims boundary and preserve the requirement for broader scientific interpretation to follow dedicated rerun review.

## Acceptance Criteria

- A tracked command materializes a rerun package for the manually advanced candidate subset.
- Every rerun candidate record includes the manual-review disposition, the baseline promoted payload and the rerun candidate payload, and a structured comparison.
- The package summary records how many reviewed candidates were rerun, how many preserved transition support, and how many degraded or changed status.
- Tests verify shortlist enforcement, comparison completeness, and claims-boundary preservation.

## Dependencies

- `0035`
- `0043`
- `0048`
- `0049`
- `0050`
- `0051`
