# 0044 Publication-Grade Release, Analyst Workbench, and Archive Assembly Plan

## Goal

Maintain a repository-local release-closeout package and analyst workbench that expose tracked outputs without overstating publication status.

## Implementation Approach

Extend the release and review builders so they assemble structured repository-local bundles and expose them through the analyst workbench directly from benchmark, optimization, discovery, and audit artifacts.

## Steps

1. Keep methods, catalog, archive, and open-source release outputs materialized through one repository-local package.
2. Extend the analyst workbench with optimization, discovery, release, and conformance views.
3. Preserve provenance manifests, inventories, and source-package references across release outputs.
4. Add tests that fail when required release or review deliverables become incomplete or untraceable.

## Expected File Changes

### Modified Files

- `src/echorm/reports/release.py`
- `src/echorm/reports/review_app.py`
- `src/echorm/eval/root_closeout.py`
- `src/echorm/cli/benchmark.py`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Release-closeout artifacts remain reviewable, provenance-complete, and explicit about their repository-local claims boundary.
- The analyst workbench can navigate those outputs without ambiguity.

## Dependencies

- `0020`
- `0036`
- `0037`
- `0041`
- `0042`
- `0043`
- `0038`
