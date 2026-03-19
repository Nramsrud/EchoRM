# 0029 Sonification Efficacy Benchmark Program

## Summary

Run the blinded plot-only, audio-only, and combined-modality efficacy benchmark program against strong visual baselines.

## Scope

- Replace the current structural blinded-task scaffold with a real benchmark program over tracked validation artifacts.
- Include plot-only, audio-only, and plot-plus-audio task modes.
- Score accuracy, time-to-decision, confidence calibration, inter-rater agreement, and performance by training level.
- Materialize task packages, scored responses, cohort summaries, and confusion summaries as tracked artifacts.

## Non-Goals

- Discovery-pool evaluation.
- Unblinded audio demonstrations presented as efficacy evidence.
- Treat combined-modality performance as sufficient without comparison to plot-only baselines.

## Global Constraints

- Efficacy tasks must remain blinded with task identity separated from answer keys.
- Benchmark objects and task labels must be frozen before scoring and summary generation.
- Efficacy claims must remain bounded by the participant or agent cohort represented in the tracked artifacts.

## Acceptance Criteria

- The repository can materialize blinded efficacy task packages and scored responses for plot-only, audio-only, and plot-plus-audio modes.
- The package reports accuracy, time-to-decision, confidence calibration, inter-rater agreement, and performance by training level.
- The efficacy benchmark summary compares audio-only and combined-modality performance against strong plot-only baselines explicitly.

## Dependencies

- `0015`
- `0017`
- `0026`
- `0027`
- `0028`
