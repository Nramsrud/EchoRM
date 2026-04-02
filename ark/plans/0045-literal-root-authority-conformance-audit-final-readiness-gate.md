# 0045 Literal Root Authority Conformance Audit and Final Readiness Gate Plan

## Goal

Replace the shallow root closeout audit with a literal conformance gate tied directly to the root authority documents.

## Implementation Approach

Enumerate root requirements, attach them to artifact and workflow checks, emit explicit fail states for every downgrade class identified by adversarial review, and surface the gate through the analyst workbench and release bundle.

## Steps

1. Define the root-authority requirement matrix over datasets, methods, metrics, phases, deliverables, and guardrails.
2. Implement strict audit checks and explicit downgrade detection for surrogate, proxy, placeholder, and count-only evidence.
3. Integrate the final audit into workflow outputs, release bundles, and review pages.
4. Add tests that prove the audit rejects each adversarial failure class.

## Expected File Changes

### Modified Files

- `src/echorm/eval/root_closeout.py`
- `src/echorm/reports/review_app.py`
- `src/echorm/reports/release.py`
- `src/echorm/cli/benchmark.py`
- `workflows/Snakefile`
- `workflows/rules/common.smk`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- The final audit fails on every downgrade class identified in the remediation playbook.
- Root-closeout readiness is determined only by literal conformance evidence.

## Dependencies

- `0041`
- `0042`
- `0043`
- `0044`
- `0038`
