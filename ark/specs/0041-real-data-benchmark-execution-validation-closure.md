# 0041 Real-Data Benchmark Execution and Validation Closure

## Summary

Execute the validation program on real measured continuum and line-response data from the frozen corpora and close the proxy-response benchmark gap.

## Scope

- Run the required RM methods on real continuum and line-response measurements rather than derived proxy response series.
- Produce the gold and silver validation deliverables required by the root phases, including literature-facing comparison tables.
- Expand null and failure diagnostics to the controls named in the authority plan.
- Record benchmark evidence levels, limitations, and non-demonstrated capability boundaries explicitly.

## Non-Goals

- Discovery hold-out ranking.
- Publication release packaging.

## Global Constraints

- Real-data validation claims must remain bounded by the measured channels and corpora actually executed.
- Null and failure diagnostics must remain explicit and reproducible.
- Root-closeout promotion may not rely on proxy response evidence.

## Acceptance Criteria

- Gold and silver benchmark packages run on real measured series from the frozen corpora.
- Validation outputs include AGN Watch memo, SDSS-RM leaderboard, and mapping-ablation artifacts.
- Null suites cover shuffled, reversed, misaligned, sparse, low-SNR, contaminated, and state-change controls.
- Tests verify that root-closeout validation fails when proxy response evidence is present.

## Dependencies

- `0012`
- `0017`
- `0039`
- `0040`
- `0038`
