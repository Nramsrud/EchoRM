# 0010 Classical Lag Wrappers Plan

## Goal

Implement the first reverberation-method adapters around PyCCF and pyZDCF with canonical lag-result outputs.

## Implementation Approach

Wrap each method in a thin adapter that preserves method-specific evidence, then normalize outputs into the canonical lag schema without hiding uncertainty or sparse-sampling diagnostics.

## Steps

1. Create reverberation-method interfaces and adapter classes for PyCCF and pyZDCF under the shared reverberation package.
2. Map method outputs, uncertainty ranges, significance values, and runtime metadata into the canonical lag-result contract.
3. Preserve method-specific diagnostics such as FR/RSS outputs and sparse-sampling evidence in structured metadata rather than flattened summaries alone.
4. Add unit tests that run on synthetic or fixture-backed channel pairs and verify canonical lag-result construction.

## Expected File Changes

### New Files

- `src/echorm/rm/base.py` - shared reverberation-method interfaces
- `src/echorm/rm/pyccf.py` - PyCCF adapter
- `src/echorm/rm/pyzdcf.py` - pyZDCF adapter
- `src/echorm/rm/serialize.py` - canonical lag-result builders
- `tests/test_classical_lag_wrappers.py` - adapter and serialization tests

### Modified Files

- `src/echorm/schemas/lags.py` - adapter-facing helpers if needed

## Validation

- `python3 -m pytest tests/test_classical_lag_wrappers.py`
- `python3 -m mypy src tests`

## Exit Criteria

- PyCCF and pyZDCF both emit canonical lag-result records.
- Method-specific uncertainty and sparse-sampling evidence remain preserved.
- Synthetic or fixture-backed tests cover both adapters and their serialization path.

## Risks

| Risk | Mitigation |
|------|------------|
| Adapters become wrappers in name only and start re-implementing method logic | Keep the adapter boundary thin and preserve native method outputs wherever possible |
| Canonical serialization erases diagnostics needed later for consensus work | Store method-specific evidence in structured metadata and assert its presence in tests |

## Dependencies

- `0005`
- `0009`
