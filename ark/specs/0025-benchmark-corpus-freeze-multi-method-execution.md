# 0025 Benchmark Corpus Freeze and Multi-Method Execution

## Summary

Freeze the gold and silver benchmark corpora, execute the core reverberation methods on real benchmark objects, and materialize null and failure diagnostics as tracked artifacts.

## Scope

- Define frozen gold and silver benchmark manifests with inclusion criteria, literature labels, strata, and exclusion reasons.
- Expand AGN Watch and SDSS-RM benchmark acquisition from bounded fixtures to the declared benchmark corpora.
- Run PyCCF, pyZDCF, JAVELIN, and PyROA on real benchmark objects with explicit runtime metadata, convergence diagnostics, and failure capture.
- Materialize shuffled-pair, misaligned-pair, and cadence-stress null outputs needed for later calibration and false-positive analysis.
- Emit method-level artifacts in forms consumable by later validation, review, and claims-audit packages.

## Non-Goals

- Close the gold or silver validation gate by itself.
- Produce the final population-level validation reports.
- Treat wrapper availability as sufficient evidence of benchmark execution.

## Global Constraints

- Benchmark manifests, labels, and splits must become immutable before downstream validation reporting.
- Method outputs must preserve provenance, configuration, diagnostics, and failure states explicitly.
- Null and stress cases must remain labeled as such and must not be merged into primary benchmark metrics without explicit handling.

## Acceptance Criteria

- Tracked commands can materialize frozen gold and silver benchmark manifests from committed code and declared source metadata.
- The repository can execute PyCCF, pyZDCF, JAVELIN, and PyROA across the benchmark corpus subset selected for the package and store method-level outputs and failures as tracked artifacts.
- Null and cadence-stress benchmark outputs are materialized in tracked artifacts with explicit labels and provenance.

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
