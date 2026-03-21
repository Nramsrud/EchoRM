# 0047 Literal Root Authority Final Conformance Remediation

## Purpose

Define the final remediation required after the latest adversarial review found that the implementation still does not literally satisfy the root project plan and root agent specification.

## Scope

This playbook governs the remaining work needed to close the current adversarial findings in:

- data-model conformance
- corpus scope and raw-preservation scope
- continuum real-data validation
- Pareto optimization semantics
- discovery and CLAGN scientific outputs
- publication-grade release deliverables

It applies to the active remediation chain under `0039` through `0045` and supersedes any interpretation that treats the current passing repository-local audit as sufficient evidence of literal root-authority compliance.

## Governing Rule

Acceptability is full satisfaction of the root authority documents in implementation, deliverables, and readiness. Repository-local passing tests, internal audits, or artifact counts do not qualify as completion if the scientific intent or literal deliverable definition remains unmet.

The following are explicitly non-acceptable as completion evidence:

- `mjd_rest` values computed without the documented per-object `t0`
- raw-only photometry records presented as compliance with the required `R0` / `R1` / `R2` parallel representations
- curated slices presented as full SDSS-RM, SDSS-V, or ZTF corpus compliance
- synthetic or literature-inspired continuum packages presented as full real-data continuum validation
- scalarized optimization presented as Pareto optimization
- heuristic catalog-transition scoring presented as literal discovery-track compliance
- markdown drafts or inventory notes presented as publication-grade deliverables

## Controlling Findings and Required Response

### F1. Time and Normalization Conformance Failure

Observed gap:
- the implementation does not yet satisfy the root data-model requirements for rest-frame time handling and parallel normalization

Required response:
- `0040` must define and persist a documented per-object `t0`
- `0040` and `0041` must materialize `R0` raw, `R1` science-normalized, and `R2` sonification-normalized products in tracked form
- `0045` must fail if any root-closeout evidence uses a rest-frame conversion that omits `t0` or if the parallel representation set is incomplete

Acceptance evidence:
- object manifests that record `t0`
- tracked `R0`, `R1`, and `R2` products linked one-to-one by provenance
- audit checks that validate the conversion and representation rules directly

### F2. Corpus Scope and Raw-Product Conformance Failure

Observed gap:
- the implementation still operates on curated slices where the root authority documents require broader SDSS-RM and ZTF scope with explicit raw-product preservation

Required response:
- `0040` must acquire and freeze the declared SDSS-RM and ZTF source scope using official access paths
- `0040` must preserve raw source products and normalized derivative products in parallel
- `0045` must fail if silver or discovery compliance is asserted from curated slices without explicit authority-approved scope labels

Acceptance evidence:
- freeze manifests with scope counts, exclusions, release identifiers, and raw hashes
- raw-product manifests for SDSS-RM and ZTF linked to normalized derivatives
- scope labels in release artifacts that distinguish subset evidence from full-scope evidence

### F3. Continuum Real-Data Validation Failure

Observed gap:
- the continuum package remains synthetic or literature-inspired where the root authority documents require real-data continuum validation as part of the scientific program

Required response:
- `0041` must add real-data continuum benchmark cases sourced from tracked public data
- `0041` must separate synthetic support tasks from real-data validation tasks in both artifacts and readiness claims
- `0045` must fail if a continuum readiness claim depends materially on synthetic-only evidence

Acceptance evidence:
- tracked real-data continuum benchmark cases
- literature comparison outputs tied to those real cases
- explicit evidence labels that prevent synthetic support cases from being promoted as full validation

### F4. Pareto Optimization Conformance Failure

Observed gap:
- the optimization layer still collapses the root objective program into a scalar objective

Required response:
- `0042` must implement the literal `M1` through `M7` objective family
- `0042` must produce Pareto-front artifacts rather than ranking candidates solely by a scalar aggregate
- `0045` must fail if any optimizer backend promotes a single scalar as the controlling optimization target for root-closeout readiness

Acceptance evidence:
- tracked objective records for each required metric family
- Pareto-front artifacts from `Ray Tune`, `Optuna`, and `Ax`
- experiment summaries that preserve trade-offs rather than scalar collapse

### F5. Discovery and CLAGN Output Failure

Observed gap:
- the discovery layer still derives anomaly ranking from heuristic hold-out summary signals rather than from the full line-aware discovery products required by the root authority documents

Required response:
- `0043` must produce per-line anomaly scores, response asymmetry tables, transition-aligned lag timelines, pre/post sonification comparisons, and precursor outputs
- `0043` must tie discovery evidence to validated pipeline products rather than to summary deltas alone
- `0045` must fail if discovery compliance is asserted without those line-aware outputs

Acceptance evidence:
- ranked anomaly outputs with per-line evidence
- CLAGN transition bundles with temporal alignment and pre/post evidence surfaces
- precursor catalog entries with provenance to validated hold-out analysis products

### F6. Publication and Release Deliverable Failure

Observed gap:
- release outputs remain drafts or summaries where the root authority documents require publication-grade artifacts

Required response:
- `0044` must replace draft markdown stubs with literal methods-paper, catalog-paper, figure, table, and archive bundles
- `0044` must materialize the catalog-level outputs and publication-facing assets required by the root plan
- `0045` must fail if publication readiness is asserted from placeholder or summary-only deliverables

Acceptance evidence:
- publication-grade methods bundle
- publication-grade catalog bundle
- catalog-level tables, figures, and archive manifests in tracked form

## Sequencing

1. Close `F1` and `F2` before promoting any new root-closeout readiness claim.
2. Close `F3` before presenting continuum validation as root-authority compliant.
3. Close `F4` before using optimization outputs to justify discovery or release readiness.
4. Close `F5` before asserting CLAGN or anomaly-track compliance.
5. Close `F6` before asserting publication or release readiness.
6. Re-run `0045` only after `F1` through `F6` are materially closed in tracked artifacts.

## Acceptance Gate

The current adversarial findings are closed only when all of the following are true:

- root-closeout data products use the documented time model and persisted parallel normalization representations
- SDSS-RM and ZTF scope claims are backed by raw-product and freeze manifests at the required scope
- continuum validation includes tracked real-data benchmark cases
- optimization outputs preserve literal Pareto trade-offs across the required metric family
- discovery and CLAGN outputs include the line-aware and transition-aware scientific products required by the root plan
- release and publication artifacts are content-complete rather than placeholder summaries
- `0045` verifies each of the above directly and rejects any residual proxy or placeholder evidence

## Exit Condition

No readiness statement may describe the repository as satisfying the root authority documents until this playbook is complete and the final conformance audit passes on literal evidence.
