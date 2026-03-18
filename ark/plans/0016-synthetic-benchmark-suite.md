# 0016 Synthetic Benchmark Suite Plan

## Goal

Implement the synthetic truth tables that support method validation, sonification comparison, and later optimization work.

## Implementation Approach

Separate continuum generation, transfer-function application, contamination injection, and benchmark-record serialization so benchmark families remain explicit, reproducible, and immutable once fixed.

## Steps

1. Implement synthetic continuum generators for the required baseline and alternative variability models.
2. Implement transfer-function families and contamination or complexity injections for the benchmark scenarios.
3. Define the benchmark-family builders and serialize each realization into truth, method-output, audio, and score records.
4. Add tests that validate family coverage, truth-parameter preservation, and deterministic benchmark generation from fixed seeds.

## Expected File Changes

### New Files

- `src/echorm/simulate/continuum.py` - synthetic continuum generators
- `src/echorm/simulate/transfer.py` - transfer-function families
- `src/echorm/simulate/injections.py` - contamination and complexity injections
- `src/echorm/simulate/benchmarks.py` - benchmark-family builders
- `tests/test_synthetic_benchmarks.py` - benchmark-generation tests

### Modified Files

- `src/echorm/schemas/sonifications.py` - benchmark-output linkage if needed
- `src/echorm/schemas/lags.py` - benchmark-output linkage if needed

## Validation

- `python3 -m pytest tests/test_synthetic_benchmarks.py`
- `python3 -m mypy src tests`

## Exit Criteria

- All required benchmark families can be generated from tracked code.
- Truth parameters, derived outputs, and evaluation records remain linked.
- Tests protect deterministic generation and family coverage.

## Risks

| Risk | Mitigation |
|------|------------|
| Benchmark families drift into an unreviewable monolith | Separate generators, injections, and family builders into distinct modules |
| Truth parameters are lost once derived outputs are created | Store truth records as first-class outputs and assert their presence in tests |

## Dependencies

- `0005`
- `0010`
- `0014`
