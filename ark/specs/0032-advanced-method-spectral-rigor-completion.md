# 0032 Advanced Method and Spectral Rigor Completion

## Summary

Close the remaining real-data inference and spectral-analysis gaps required by the root authority documents, including advanced RM backends and `PyQSOFit`-style decomposition metadata.

## Scope

- Add tracked wrappers and execution records for `pyPETaL`, `LITMUS`, `MICA2`, `EzTao`, and `celerite2`.
- Extend benchmark object artifacts with advanced-method diagnostics, transfer-function context, and runtime metadata.
- Add `PyQSOFit`-style spectral decomposition records alongside the existing continuum-fit variants.
- Materialize a package-level artifact that states scope, evidence level, limitations, and advanced-method outcomes directly.

## Non-Goals

- Discovery ranking on hold-out corpora.
- Public release packaging.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Advanced-method conclusions must remain bounded by the evidence materialized in tracked artifacts.
- Spectral decomposition variants, calibration choices, and fit identities must remain explicit metadata rather than hidden implementation state.

## Acceptance Criteria

- Every tracked benchmark object has advanced-method records with runtime, convergence, agreement, and evidence metadata.
- The spectral artifact set includes local, pseudo-continuum, full-decomposition, and `PyQSOFit`-style records with fit-model identifiers.
- Package outputs distinguish direct benchmark evidence from model-assisted or proxy evidence explicitly.
- The package is integrated into the workflow, review surface, and root closeout audit.

## Dependencies

- `0025`
- `0026`
- `0027`
- `0028`
