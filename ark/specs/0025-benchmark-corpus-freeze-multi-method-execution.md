# 0025 Benchmark Corpus Freeze and Multi-Method Execution

## Summary

Freeze the gold and silver benchmark corpora, execute the core reverberation methods on real benchmark objects, and materialize null and failure diagnostics as tracked artifacts.

## Scope

- Define frozen gold and silver benchmark manifests with inclusion criteria, literature labels, strata, and exclusion reasons.
- Expand AGN Watch and SDSS-RM benchmark acquisition from bounded fixtures to the declared benchmark corpora.
- Run PyCCF, pyZDCF, JAVELIN, and PyROA on real benchmark objects with explicit runtime metadata, convergence diagnostics, and failure capture.
- Materialize shuffled-pair, misaligned-pair, and cadence-stress null outputs needed for later calibration and false-positive analysis.
- Emit method-level artifacts in forms consumable by later validation, review, and claims-audit packages.
- Label every driver and response series explicitly as real fixture response, real-fixture proxy response, literature-inspired response, or synthetic control; proxy responses must never be reported as direct real-series evidence.

## Non-Goals

- Close the gold or silver validation gate by itself.
- Produce the final population-level validation reports.
- Treat wrapper availability as sufficient evidence of benchmark execution.

## Global Constraints

- Benchmark manifests, labels, and splits must become immutable before downstream validation reporting.
- Method outputs must preserve provenance, configuration, diagnostics, and failure states explicitly.
- Null and stress cases must remain labeled as such and must not be merged into primary benchmark metrics without explicit handling.

## Acceptance Criteria

- Tracked commands materialize frozen gold and silver benchmark manifests with inclusion criteria, exclusion reasons, strata counts, evidence labels, and manifest hashes.
- The repository executes PyCCF, pyZDCF, JAVELIN, and PyROA across the selected benchmark corpus slice and stores method-level outputs, runtime metadata, convergence diagnostics, and explicit failure records as tracked artifacts.
- Every benchmark object records whether its response path is direct fixture response or proxy response, and no proxy response is labeled as direct real-series evidence.
- Null outputs include shuffled-pair, misaligned-pair, reversed-response, and sparse-cadence variants with explicit labels and provenance.
- Repeated materialization preserves manifest hashes and package-level benchmark counts exactly.

## Dependencies

- `0006`
- `0007`
- `0010`
- `0011`
- `0012`
- `0016`
- `0021`
- `0023`
- `0024`
