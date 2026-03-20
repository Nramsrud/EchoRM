# 0039 Real Backend and Spectral Backend Integration

## Summary

Replace surrogate RM and spectral stand-ins with literal third-party backend integrations and explicit execution diagnostics.

## Scope

- Integrate `pyPETaL`, `LITMUS`, `MICA2`, `EzTao`, `celerite2`, and `PyQSOFit` from their real upstream implementations or documented invocation surfaces.
- Preserve backend versions, invocation arguments, runtime, warnings, convergence diagnostics, and failure states in tracked artifacts.
- Fail closed when a declared backend is unavailable rather than silently substituting surrogate evidence.
- Keep benchmark and discovery artifacts explicit about which backends executed successfully on which objects.

## Non-Goals

- Corpus acquisition.
- Discovery ranking.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Root-closeout evidence may not use `surrogate_contract`, `tracked_wrapper`, pseudo-fit labels, or equivalent fallback claims.
- Backend integration must preserve provenance and non-success states explicitly.

## Acceptance Criteria

- Every required advanced backend executes through a literal integration path or produces an explicit failing artifact that blocks promotion.
- `PyQSOFit` operates as the main spectral-fit backend for tracked spectra in the root-closeout path.
- Backend records include versions, parameters, runtime, diagnostics, warnings, and artifact paths.
- Tests verify that root-closeout packages fail if a required backend is absent or replaced by a surrogate label.

## Dependencies

- `0011`
- `0013`
- `0032`
- `0038`
