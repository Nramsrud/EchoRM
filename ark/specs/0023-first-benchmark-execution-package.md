# 0023 First Benchmark Execution Package

## Summary

Define and execute the first benchmark package with explicit scientific scope, evidence levels, fixture-backed real-data checks, and synthetic lag-recovery cases.

## Scope

- Define the first benchmark package as a bounded scientific artifact rather than a generic readiness report.
- Include fixture-backed real-data ingestion and provenance checks for the initial AGN Watch and SDSS-RM benchmark objects.
- Include synthetic lag-recovery cases that exercise the current reverberation-method and validation surfaces.
- Record benchmark scope, evidence levels, limitations, and claims boundaries in machine-readable and human-readable outputs.
- Materialize the benchmark package through tracked command-line and workflow entry points compatible with the review web interface.

## Non-Goals

- Claim full scientific validation on large real-survey benchmark sets.
- Replace the first benchmark package with discovery-scale evaluation.
- Hide fixture-backed or synthetic evidence behind generalized “benchmark passed” language.

## Global Constraints

- Every benchmark case must declare its evidence level explicitly as real-fixture, synthetic, or derived.
- Benchmark outputs must distinguish ingestion-fidelity checks from lag-recovery checks and must not merge them into one opaque score.
- Any scientific claim made from the benchmark package must remain bounded by the underlying evidence level and benchmark coverage.

## Acceptance Criteria

- One tracked command can materialize a first benchmark package with explicit case taxonomy, metrics, evidence levels, and limitations.
- The package contains real-fixture benchmark cases for the initial AGN Watch and SDSS-RM objects and synthetic lag-recovery cases for the current reverberation surfaces.
- The benchmark summary states what is demonstrated, what is not yet demonstrated, and which next scientific gaps remain before broader benchmark claims.

## Dependencies

- `0006`
- `0007`
- `0010`
- `0016`
- `0017`
- `0021`
- `0022`
