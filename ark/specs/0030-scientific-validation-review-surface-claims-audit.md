# 0030 Scientific Validation Review Surface and Claims Audit

## Summary

Upgrade the review application for scientific analysis across validation packages and implement the cross-package claims audit that determines whether the broad-validation gate is satisfied.

## Scope

- Extend the review surface to navigate gold, silver, continuum-RM, and efficacy validation packages in addition to readiness and first-benchmark runs.
- Add package, cohort, object, method, mapping-family, rerun, and task-level review views required for scientific analysis.
- Expose literature comparison tables, null-test outputs, failure summaries, exclusions, claims boundaries, and linked audio artifacts from tracked files.
- Implement the cross-package claims audit that evaluates whether the declared broad-validation gate criteria are satisfied by tracked artifacts.

## Non-Goals

- Replace package-level validation work with UI-only summaries.
- Introduce write access, artifact mutation, or hidden in-memory interpretation logic.
- Promote broad scientific-validation claims without the underlying tracked evidence.

## Global Constraints

- The review application must remain read-only and derive all analysis views from tracked artifact files.
- Claims-audit logic must evaluate explicit gate criteria and record unmet conditions directly.
- The review surface must make limitations, exclusions, evidence levels, and non-demonstrated capabilities visible rather than implicit.

## Acceptance Criteria

- The review application can navigate and compare validation packages, cohorts, objects, methods, null suites, reruns, and efficacy tasks from tracked artifacts.
- The service exposes the literature comparisons, null-test outputs, runtime summaries, failure summaries, exclusions, and claims-boundary panels needed for scientific review.
- A tracked claims-audit artifact evaluates the quantitative thresholds and qualitative gate conditions in the playbook against the generated validation packages and records whether promotion is allowed.
- The claims audit defaults to non-promotion when any required threshold, evidence label, or reproducibility condition is missing.

## Dependencies

- `0022`
- `0026`
- `0027`
- `0028`
- `0029`
