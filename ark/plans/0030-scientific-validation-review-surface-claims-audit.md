# 0030 Scientific Validation Review Surface and Claims Audit Plan

## Goal

Make the user-facing review tool sufficient for scientific analysis across the validation program and implement the gate audit that governs broad-validation claims.

## Implementation Approach

Extend the existing review surface from run-and-case inspection to validation-analysis workflows, then add a claims-audit layer that reads the tracked validation artifacts and records whether the broad scientific-validation gate is satisfied.

## Steps

1. Extend the review-artifact schemas and loaders to support gold, silver, continuum-RM, efficacy, null-suite, and rerun artifacts plus cross-package summaries.
2. Add package, cohort, object, method, rerun, and task-level pages and filters to the review application.
3. Add comparative views for literature tables, null-test outcomes, runtime summaries, failure summaries, exclusions, and linked audio artifacts.
4. Implement the claims-audit generator that evaluates the declared gate conditions and quantitative thresholds from tracked validation artifacts and writes a structured audit dossier.
5. Add tests that validate review-surface navigation, filtering, artifact linking, threshold visibility, and claims-audit evaluation.

## Expected File Changes

### New Files

- review-surface and claims-audit modules under `src/echorm/reports/` and `src/echorm/eval/`
- tests covering validation-package navigation and claims-audit outputs

### Modified Files

- existing review app, CLI, and benchmark artifact surfaces
- workflow and CLI paths for cross-package claims-audit generation

## Validation

- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`
- tracked review-surface launch command over the validation artifact root
- tracked claims-audit command over the generated validation packages

## Exit Criteria

- The review application supports scientific analysis across validation packages from tracked artifacts alone.
- A claims-audit artifact evaluates and records whether the broad-validation gate is satisfied under the declared quantitative thresholds.
- Limitations, exclusions, evidence levels, reproducibility status, and non-demonstrated capabilities remain visible in the review surface and audit outputs.

## Risks

| Risk | Mitigation |
|------|------------|
| The review surface becomes a second untracked interpretation layer | Load every displayed value directly from tracked validation artifacts and test the route outputs |
| Claims audit overstates readiness when inputs are incomplete | Record unmet gate conditions explicitly and default to non-promotion unless every requirement is satisfied |

## Dependencies

- `0022`
- `0026`
- `0027`
- `0028`
- `0029`
