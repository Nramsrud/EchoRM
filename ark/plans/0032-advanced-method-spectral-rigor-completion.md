# 0032 Advanced Method and Spectral Rigor Completion Plan

## Goal

Implement advanced RM-method and spectral-rigor artifacts so the repository records the remaining root-scope inference and decomposition evidence in tracked outputs.

## Implementation Approach

Extend the existing benchmark-corpus and validation package machinery with advanced-method adapters, explicit spectral-fit families, and a dedicated closeout package rather than introducing a separate artifact model.

## Steps

1. Add tracked wrappers for `pyPETaL`, `LITMUS`, `MICA2`, `EzTao`, and `celerite2`, including deterministic diagnostics, runtime metadata, and evidence labels.
2. Add a `PyQSOFit`-style spectral-fit record and include it in benchmark object diagnostics alongside the existing continuum-fit variants.
3. Implement an advanced-rigor package that summarizes object coverage, method execution, convergence, agreement, and spectral-fit coverage.
4. Add tests that verify advanced-method serialization, spectral-fit completeness, and package-level threshold reporting.

## Expected File Changes

### New Files

- `src/echorm/rm/pypetal.py`
- `src/echorm/rm/litmus.py`
- `src/echorm/rm/mica2.py`
- `src/echorm/rm/eztao.py`
- `src/echorm/rm/celerite2.py`
- `src/echorm/spectra/pyqsofit.py`
- `tests/test_root_authority_closeout.py`

### Modified Files

- `src/echorm/eval/benchmark_corpus.py`
- `src/echorm/cli/benchmark.py`
- `workflows/Snakefile`
- `workflows/rules/common.smk`

## Validation

- `python3 -m pytest tests/test_root_authority_closeout.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Advanced-method and spectral-rigor artifacts are generated through tracked commands and workflows.
- Object-level diagnostics include the declared advanced methods and spectral-fit families.
- The package is consumable by the review surface and the root closeout audit.

## Risks

| Risk | Mitigation |
|------|------------|
| Advanced backends remain wrapper-grade rather than evidentiary | Record evidence labels and diagnostics explicitly rather than implying stronger execution than the artifact supports |
| Spectral fit variants drift from schema expectations | Reuse the existing line-metric schema and add tests for every fit family |

## Dependencies

- `0025`
- `0026`
- `0027`
- `0028`
