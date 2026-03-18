# 0009 Crossmatch, Time Standards, and Quality Control

## Summary

Define the shared crossmatch, calibration, time-standard, and quality-control layer across all surveys.

## Scope

- Define object identity reconciliation across surveys.
- Preserve both observed-frame and rest-frame time representations.
- Define raw, science-normalized, and sonification-normalized photometric representations.
- Define mask, gap, and quality-score policies for photometry and spectra.

## Non-Goals

- Reverberation inference.
- Spectral decomposition.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- No primary analysis may rely on silent interpolation or hidden normalization.

## Acceptance Criteria

- The project has a documented policy for object identity, aliases, time conversion, and per-object reference epochs.
- Raw, science-normalized, and sonification-normalized representations are defined without loss of provenance.
- Quality-control outputs include explicit scores, flags, gap indicators, and review-priority signals.

## Dependencies

- `0005`
- `0006`
- `0007`
- `0008`
