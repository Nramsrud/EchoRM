# 0011 Model-Based Lag Wrappers Plan

## Goal

Implement the first model-based reverberation adapters around JAVELIN and PyROA with canonical lag-result outputs and preserved posterior evidence.

## Implementation Approach

Use thin adapters around each backend, preserve posterior and convergence artifacts explicitly, and serialize the comparable outputs into the canonical lag schema without discarding method-specific context.

## Steps

1. Add model-based reverberation adapters for JAVELIN and PyROA under the shared reverberation package.
2. Implement canonical serialization of lag summaries, uncertainty intervals, runtime metadata, and configuration hashes for both methods.
3. Add explicit capture of posterior locations, convergence diagnostics, and multi-light-curve context where the backend provides them.
4. Add synthetic or fixture-backed tests that verify adapter execution, canonical lag serialization, and preservation of posterior evidence.

## Expected File Changes

### New Files

- `src/echorm/rm/javelin.py` - JAVELIN adapter
- `src/echorm/rm/pyroa.py` - PyROA adapter
- `src/echorm/rm/posteriors.py` - posterior and convergence helpers
- `tests/test_model_based_lag_wrappers.py` - adapter and serialization tests

### Modified Files

- `src/echorm/rm/base.py` - shared method interfaces if needed
- `src/echorm/schemas/lags.py` - posterior and diagnostic fields if needed

## Validation

- `python3 -m pytest tests/test_model_based_lag_wrappers.py`
- `python3 -m mypy src tests`

## Exit Criteria

- JAVELIN and PyROA both emit canonical lag-result records.
- Posterior paths and convergence diagnostics remain accessible for downstream review.
- Tests cover both adapters and the serialization boundary.

## Risks

| Risk | Mitigation |
|------|------------|
| Posterior evidence becomes detached from canonical summaries | Store canonical summaries and posterior references together and assert both in tests |
| Backend-specific fit assumptions are hidden by the shared interface | Keep method configuration hashes and backend metadata explicit in the serialized output |

## Dependencies

- `0005`
- `0009`
