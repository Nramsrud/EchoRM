# 0039 Real Backend and Spectral Backend Integration

## Summary

Integrate structured advanced-backend and spectral-fit execution surfaces for the repository-local advanced-rigor package.

## Scope

- Materialize advanced method records for `pyPETaL`, `LITMUS`, `MICA2`, `EzTao`, `celerite2`, and `PyQSOFit`-backed spectral fit families within tracked advanced-rigor artifacts.
- Preserve backend versions, invocation arguments, runtime, warnings, diagnostics, and explicit evidence labels in tracked artifacts.
- Expose non-success states and limitations without silently dropping them from the repository-local package surface.
- Keep benchmark, discovery, and audit artifacts explicit about which advanced records are present for which tracked objects.

## Non-Goals

- Corpus acquisition.
- Discovery ranking.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Repository-local advanced-rigor claims remain bounded by tracked benchmark slices and recorded evidence levels.
- Backend integration must preserve provenance and non-success states explicitly.

## Acceptance Criteria

- The advanced-rigor package records advanced method entries and spectral-fit families for the tracked object set.
- `PyQSOFit`-backed spectral fit records remain visible in the repository-local advanced-rigor surface.
- Backend records include versions, parameters, runtime, diagnostics, warnings, and artifact paths or explicit limitations.
- Tests verify package completeness, explicit limitations, and review-surface compatibility.

## Dependencies

- `0011`
- `0013`
- `0032`
- `0038`
