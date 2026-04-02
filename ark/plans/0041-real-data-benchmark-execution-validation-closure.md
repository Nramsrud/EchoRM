# 0041 Real-Data Benchmark Execution and Validation Closure Plan

## Goal

Maintain repository-local benchmark validation packages whose scope, evidence levels, and limitations remain explicit in every generated output.

## Implementation Approach

Route validation builders through shared package helpers, preserve literature and rerun summaries, and keep evidence labels explicit across gold, silver, and continuum outputs.

## Steps

1. Keep gold, silver, and continuum package builders aligned to one evidence-labeling and limitations policy.
2. Preserve literature tables, reruns, warnings, and method records in the generated packages.
3. Ensure continuum support tasks remain visibly separated by evidence level.
4. Add tests that fail when validation outputs omit package boundaries or silently drop warnings and limitations.

## Expected File Changes

### Modified Files

- `src/echorm/eval/broad_validation.py`
- `src/echorm/eval/benchmark_corpus.py`
- `src/echorm/cli/benchmark.py`
- `src/echorm/reports/review_app.py`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Benchmark validation artifacts remain reviewable, reproducible, and explicit about their repository-local evidence boundaries.
- Package summaries remain usable by the review surface and claims audits without ambiguity.

## Dependencies

- `0012`
- `0017`
- `0039`
- `0040`
- `0038`
