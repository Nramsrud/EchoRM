# 0041 Real-Data Benchmark Execution and Validation Closure Plan

## Goal

Replace the proxy-response benchmark path with real measured continuum and line-response validation at root-closeout scope.

## Implementation Approach

Route the benchmark builders through the frozen corpus layer, build measured driver and response series from acquired data products, and tighten the validation packages and audits to reject proxy evidence.

## Steps

1. Build measured continuum and line-response extraction from the frozen corpora.
2. Update method execution, consensus, and null builders to consume measured series.
3. Regenerate gold and silver validation packages with literature-facing deliverables and mapping ablations.
4. Add tests that fail if benchmark artifacts report proxy-response evidence in root-closeout runs.

## Expected File Changes

### Modified Files

- `src/echorm/eval/benchmark_corpus.py`
- `src/echorm/eval/validation.py`
- `src/echorm/eval/broad_validation.py`
- `src/echorm/reports/*`
- `src/echorm/cli/benchmark.py`
- `workflows/Snakefile`
- `workflows/rules/common.smk`
- `tests/*`

## Validation

- `python3 -m pytest`
- `python3 -m mypy src tests`

## Exit Criteria

- Root-closeout benchmark artifacts run on measured data products and include the required validation deliverables.
- Proxy-response evidence blocks promotion.

## Dependencies

- `0012`
- `0017`
- `0039`
- `0040`
- `0038`
