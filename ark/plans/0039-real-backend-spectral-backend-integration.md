# 0039 Real Backend and Spectral Backend Integration Plan

## Goal

Implement literal backend execution for the advanced RM and spectral stack and remove surrogate evidence from root-closeout artifacts.

## Implementation Approach

Add a real backend registry, package-specific adapters, structured dependency detection, and explicit failure reporting. Route the root-closeout path through these integrations rather than through the current posterior-wrapping stand-ins.

## Steps

1. Add backend descriptors, availability checks, and version capture for `pyPETaL`, `LITMUS`, `MICA2`, `EzTao`, `celerite2`, and `PyQSOFit`.
2. Replace surrogate RM adapters with integrations that invoke the real backend or emit blocking unavailability diagnostics.
3. Replace the pseudo-fit spectral path with `PyQSOFit` execution and structured fit outputs.
4. Update package builders, workflows, and tests so root-closeout promotion fails when any required backend is unavailable or downgraded.

## Expected File Changes

### Modified Files

- `src/echorm/rm/*.py`
- `src/echorm/spectra/pyqsofit.py`
- `src/echorm/eval/benchmark_corpus.py`
- `src/echorm/eval/root_closeout.py`
- `src/echorm/cli/benchmark.py`
- `workflows/Snakefile`
- `workflows/rules/common.smk`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Root-closeout artifacts contain literal backend execution metadata and no surrogate evidence labels.
- Missing backends block promotion explicitly.

## Dependencies

- `0011`
- `0013`
- `0032`
- `0038`
