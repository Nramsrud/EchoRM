# 0027 Silver Benchmark Population Validation Plan

## Goal

Close the population-scale validation gap with a broad SDSS-RM benchmark package that reports quantitative performance, null behavior, and regime-specific outcomes.

## Implementation Approach

Build a silver validation package over the frozen silver corpus, benchmark-run outputs, and null controls, then emit population-level metrics, tables, and failure-mode reports from tracked artifacts.

## Steps

1. Select the broad published-lag silver population from the frozen manifest and define the regime breakdowns and thresholds to be reported.
2. Aggregate method-level and consensus benchmark outputs into population metrics, including lag recovery, coverage, disagreement, false-positive, and runtime summaries.
3. Incorporate null, shuffled-pair, and cadence-stress controls into the silver validation package with explicit reporting and threshold checks.
4. Build leaderboards, literature comparison tables, runtime summaries, and failure-mode summaries from the aggregated outputs.
5. Add tests that validate metric aggregation, regime labeling, null-control handling, threshold evaluation, and artifact completeness.

## Expected File Changes

### New Files

- silver validation aggregation and reporting modules under `src/echorm/eval/` and `src/echorm/reports/`
- tests covering metric aggregation, regime reporting, and null-control summaries

### Modified Files

- workflow and CLI surfaces for silver validation package materialization
- review-surface data loaders if needed for interim artifact compatibility

## Validation

- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`
- tracked silver validation package command over the selected SDSS-RM population

## Exit Criteria

- Population-level silver benchmark metrics are reproducible from tracked artifacts.
- Coverage, false-positive, and disagreement metrics satisfy the declared thresholds for the benchmark slice.
- Null and shuffled controls are reported explicitly with failure-mode visibility.
- The package emits a leaderboard, literature comparison table, runtime summary, and regime-specific summaries.

## Risks

| Risk | Mitigation |
|------|------------|
| Population reporting hides important regime failures | Require explicit stratification by line, redshift, cadence, and quality regime |
| Null controls are computed but not surfaced clearly | Treat null-control summaries as required top-level outputs rather than optional diagnostics |

## Dependencies

- `0012`
- `0013`
- `0017`
- `0025`
