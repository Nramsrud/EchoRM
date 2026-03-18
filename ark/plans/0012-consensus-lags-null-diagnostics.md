# 0012 Consensus Lags and Null Diagnostics Plan

## Goal

Build the consensus lag object, agreement taxonomy, alias diagnostics, and null-control framework that sit above individual reverberation methods.

## Implementation Approach

Aggregate method-level lag records through an evidence-preserving consensus layer, pair that with explicit null controls and alias diagnostics, and classify outcomes into the project’s agreement taxonomy.

## Steps

1. Define the consensus lag object and its method-level evidence inputs.
2. Implement agreement, contest, spurious-result, and candidate-anomaly classification rules using canonical lag outputs from the method adapters.
3. Add null-pair and shuffled-control execution helpers plus alias-risk metrics that can be run alongside the consensus logic.
4. Add tests that exercise agreement, disagreement, alias-risk, and null-control scenarios on representative synthetic lag records.

## Expected File Changes

### New Files

- `src/echorm/rm/consensus.py` - consensus lag object and classification logic
- `src/echorm/rm/nulls.py` - null-control and shuffled-pair helpers
- `src/echorm/rm/aliasing.py` - alias-risk calculations
- `tests/test_consensus_lags.py` - consensus and diagnostics tests

### Modified Files

- `src/echorm/schemas/lags.py` - consensus-facing helpers if needed

## Validation

- `python3 -m pytest tests/test_consensus_lags.py`
- `python3 -m mypy src tests`

## Exit Criteria

- Consensus outputs preserve the underlying method evidence.
- Agreement classes and null-control outcomes are explicit and test-covered.
- Alias diagnostics are available for later validation and anomaly review.

## Risks

| Risk | Mitigation |
|------|------------|
| Consensus logic oversimplifies method disagreement | Preserve method-level inputs in the consensus object and test contested scenarios explicitly |
| Null controls drift from the real scoring pathway | Run null diagnostics through the same serialization and scoring surfaces used for real pairs |

## Dependencies

- `0010`
- `0011`
