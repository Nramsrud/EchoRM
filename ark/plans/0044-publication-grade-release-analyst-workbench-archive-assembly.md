# 0044 Publication-Grade Release, Analyst Workbench, and Archive Assembly Plan

## Goal

Replace placeholder release summaries with the literal release, archive, and analyst-review deliverables required by the root authority documents.

## Implementation Approach

Extend the release and review builders so they assemble publication-grade bundles and expose them through the analyst workbench directly from structured benchmark, optimization, and discovery artifacts.

## Steps

1. Build structured methods-paper, catalog-paper, benchmark-archive, audio-archive, and open-source release bundles.
2. Extend the analyst workbench with optimization, discovery, release, and conformance views.
3. Add provenance manifests, hashes, and reproducibility checklists to every release bundle.
4. Add tests that fail when any required release or review deliverable is missing or placeholder-only.

## Expected File Changes

### Modified Files

- `src/echorm/reports/release.py`
- `src/echorm/reports/catalog.py`
- `src/echorm/reports/review_app.py`
- `src/echorm/eval/root_closeout.py`
- `src/echorm/cli/benchmark.py`
- `workflows/Snakefile`
- `workflows/rules/common.smk`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Root-closeout release artifacts are publication-grade, provenance-complete, and reviewable through the analyst workbench.
- Placeholder-only release evidence no longer passes the root-closeout path.

## Dependencies

- `0020`
- `0036`
- `0037`
- `0041`
- `0042`
- `0043`
- `0038`
