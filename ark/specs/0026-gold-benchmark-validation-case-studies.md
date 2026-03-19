# 0026 Gold Benchmark Validation and Case Studies

## Summary

Validate the literature-rich AGN Watch gold benchmark set with object-level lag comparison, line diagnostics, mapping comparisons, and case-study artifacts.

## Scope

- Validate more than one canonical AGN Watch benchmark object against literature expectations.
- Produce object-level lag comparison tables, line-fit diagnostics, and mapping-comparison memos.
- Materialize multiple mapping-family audio artifacts tied to the same benchmark objects and diagnostics.
- Record object-level limitations, benchmark notes, and non-demonstrated capabilities directly in the validation artifacts.

## Non-Goals

- Population-scale SDSS-RM validation.
- Continuum-RM benchmark expansion on ZTF-like data.
- Close the broad-validation gate by gold evidence alone.

## Global Constraints

- Gold-benchmark outputs must remain object-level, literature-aware, and reviewable by case.
- Validation claims must distinguish qualitative literature continuity from quantitative benchmark performance explicitly.
- Mapping comparisons must remain tied to tracked diagnostics and benchmark objects rather than subjective free-form impressions alone.

## Acceptance Criteria

- More than one AGN Watch gold benchmark object is validated in tracked artifacts with literature comparison, method table, and line-fit diagnostics.
- The package records a mean absolute lag error at or below 3.0 days across the declared gold set and records rerun drift on the primary metrics.
- Each validated object has a mapping-comparison memo, linked audio artifacts across the selected mapping families, and an explicit claims-boundary panel.
- The gold validation package states demonstrated capability, limitations, residual uncertainties, and evidence level explicitly for each object and for the package as a whole.

## Dependencies

- `0013`
- `0015`
- `0017`
- `0025`
