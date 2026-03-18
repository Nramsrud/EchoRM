# 0017 Validation and Blinded Efficacy

## Summary

Validate the pipeline on benchmark objects and run blinded plot-only, audio-only, and combined-modality efficacy testing.

## Scope

- Define staged validation on gold and silver benchmark sets.
- Define metric suites for lag recovery, interval calibration, false positives, disagreement, runtime, and success by regime.
- Define blinded efficacy tasks for lag comparison, contamination detection, state-change detection, and anomalous line-response detection.
- Define the required memos, tables, and benchmark leaderboards.

## Non-Goals

- Discovery ranking on the hold-out pool.
- Benchmark-driven optimization.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Benchmark validation must precede discovery claims and optimization.

## Acceptance Criteria

- Gold-benchmark outputs include literature comparison, line-fit diagnostics, and mapping-comparison memos.
- Silver-benchmark outputs include scalable recovery metrics, disagreement statistics, and runtime summaries.
- Blinded efficacy studies record accuracy, time-to-decision, confidence calibration, and performance by training level.

## Dependencies

- `0006`
- `0007`
- `0012`
- `0013`
- `0015`
- `0016`
