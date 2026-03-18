# 0003 Research Platform Skeleton Plan

## Goal

Create the repository topology and module skeleton required for the research platform without yet implementing scientific logic.

## Implementation Approach

Use the existing `echorm` package as the canonical namespace, then add the full module tree, top-level directories, and minimal import-safe entry points so later work packages can land in stable locations.

## Steps

1. Confirm `src/echorm/` as the canonical source namespace and map the scientific-plan module taxonomy into that package.
2. Create the top-level directories for configuration, manifests, workflows, notebooks, and public references, keeping generated-artifact locations separate.
3. Add import-safe module markers and minimal interface stubs under `src/echorm/` for ingest, crossmatch, calibrate, spectra, photometry, reverberation inference, simulation, sonification, embeddings, anomaly analysis, evaluation, reporting, and CLI entry points.
4. Add structure tests that verify the required directories and import surfaces exist and can be imported without side effects.

## Expected File Changes

### New Files

- `src/echorm/ingest/__init__.py` - ingest package marker
- `src/echorm/crossmatch/__init__.py` - crossmatch package marker
- `src/echorm/calibrate/__init__.py` - calibration package marker
- `src/echorm/spectra/__init__.py` - spectra package marker
- `src/echorm/photometry/__init__.py` - photometry package marker
- `src/echorm/rm/__init__.py` - reverberation package marker
- `src/echorm/simulate/__init__.py` - simulation package marker
- `src/echorm/sonify/__init__.py` - sonification package marker
- `src/echorm/embeddings/__init__.py` - embeddings package marker
- `src/echorm/anomaly/__init__.py` - anomaly package marker
- `src/echorm/eval/__init__.py` - evaluation package marker
- `src/echorm/reports/__init__.py` - reporting package marker
- `src/echorm/cli/__init__.py` - CLI package marker
- `tests/test_repository_skeleton.py` - structure and import checks

### Modified Files

- `README.md` - top-level structure summary if needed
- `pyproject.toml` - package discovery or entry-point updates if needed

## Validation

- `python3 -m pytest tests/test_repository_skeleton.py`
- `python3 -m mypy src tests`

## Exit Criteria

- The repository topology exists in a stable, documented form.
- The full source-module skeleton is importable under `src/echorm/`.
- Later work packages have stable locations for configuration, manifests, workflows, and module code.

## Risks

| Risk | Mitigation |
|------|------------|
| Early skeleton choices force avoidable churn later | Keep the first pass structural and minimal; defer scientific logic to later specs |
| Module stubs acquire accidental runtime behavior | Restrict initial files to markers, interfaces, and side-effect-free imports |

## Dependencies

- `0002`
