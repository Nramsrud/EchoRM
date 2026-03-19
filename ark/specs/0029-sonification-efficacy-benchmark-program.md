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
- The package reports accuracy, time-to-decision, confidence-calibration error, inter-rater agreement, confusion summaries, and performance by training level.
- The efficacy benchmark summary shows audio-only accuracy at or above plot-only accuracy, combined-modality accuracy at or above plot-only accuracy, calibration error at or below 0.20, and inter-rater agreement at or above 0.60.

## Dependencies

- `0015`
- `0017`
- `0026`
- `0027`
- `0028`
