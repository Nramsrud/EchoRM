# 0038 Literal Root Authority Remediation Playbook

## Purpose

Define the remediation sequence required to close every adversarially identified gap between the current implementation and the literal requirements of the root authority documents.

## Scope

This playbook governs the work required after the adversarial review determined that the current implementation passes internal closeout artifacts without fully satisfying the root project plan or root agent specification. It covers real backend execution, literal corpus-scale acquisition, real-response benchmarking, literal optimizer orchestration, real-data discovery analysis, publication-grade release outputs, and a final conformance audit.

## Governing Rule

Acceptability is full satisfaction of the root authority documents in implementation, deliverables, and readiness. Proxy compliance does not count as completion.

The following are explicitly non-acceptable as evidence of root closeout:

- surrogate wrappers presented as backend completion
- pseudo-fits presented as spectral-backend completion
- fixture-slice corpora presented as full gold, silver, or discovery coverage
- derived proxy response series presented as real continuum or line-response measurements
- static candidate scoring presented as Ray Tune, Optuna, or Ax orchestration
- authored anomaly scores or fixed-threshold labels presented as discovery analysis
- count-only release summaries presented as methods paper, catalog paper, archive, or open-source release completion
- count-only or circular audits presented as root-authority compliance

## Adversarial Failure Classes

### F1. Backend Compliance Failure

The current repository names `pyPETaL`, `LITMUS`, `MICA2`, `EzTao`, `celerite2`, and `PyQSOFit` in tracked artifacts without executing literal third-party backend integrations on real tracked corpora.

### F2. Corpus Compliance Failure

The current repository freezes small committed fixtures and derived slices rather than the literal AGN Watch, SDSS-RM / SDSS-V RM, ZTF DR24+, and CLAGN corpora required by the root authority documents.

### F3. Response-Evidence Failure

The current repository derives proxy response series from reduced fixture inputs rather than executing the benchmark program on real measured continuum and line-response data products.

### F4. Optimization Compliance Failure

The current repository does not yet implement literal `Ray Tune`, `Optuna`, and `Ax` orchestration over the root objective surface with guarded mutation boundaries and auditable Pareto optimization.

### F5. Discovery Compliance Failure

The current repository ranks discovery candidates from authored fixture attributes rather than from validated pipeline outputs on frozen real hold-out corpora.

### F6. Release Compliance Failure

The current repository does not yet produce the methods-paper, catalog-paper, benchmark archive, audio archive, analyst workbench, and open-source release outputs required by the root authority documents.

### F7. Audit Compliance Failure

The current repository declares root closeout from a shallow artifact-count audit that does not test literal compliance against the root authority documents.

## Remediation Work Packages

### 0039 Real Backend and Spectral Backend Integration

Purpose:
- replace surrogate RM and spectral stand-ins with literal backend integrations

Required outcomes:
- execute `pyPETaL`, `LITMUS`, `MICA2`, `EzTao`, and `celerite2` as actual tracked backend integrations
- execute `PyQSOFit` as the main spectral-fitting backend on tracked spectra
- store backend versions, invocation parameters, runtime diagnostics, convergence diagnostics, warnings, and failure modes
- remove `surrogate_contract`, `tracked_wrapper`, `synthetic pseudo-fit`, and equivalent evidence labels from any artifact promoted as root-closeout evidence

### 0040 Full Corpus Acquisition, Raw Preservation, and Freeze

Purpose:
- acquire and freeze the literal root-scope corpora

Required outcomes:
- AGN Watch gold corpora stored with raw-download preservation, parser family records, and object manifests
- SDSS-RM / SDSS-V RM silver corpora stored with raw spectral epochs, normalized derivatives, line availability, literature lag labels, and exclusion reasons
- ZTF DR24+ and CLAGN discovery corpora stored with query provenance, release identifiers, raw responses, normalized tables, crossmatch keys, and immutable hold-out markers
- freeze reports with hashes, inclusion criteria, strata definitions, and scope counts tied directly to the root authority documents

### 0041 Real-Data Benchmark Execution and Validation Closure

Purpose:
- close the benchmark program on real measured continuum and line-response data

Required outcomes:
- method execution over real continuum and line-response measurements rather than derived proxy response series
- gold and silver benchmark outputs at literal corpus scope with literature-facing comparison tables
- null suites covering shuffled, reversed, misaligned, sparse, low-SNR, contaminated, and state-change controls as required by the authority plan
- benchmark deliverables required by the root phases, including the AGN Watch memo, SDSS-RM leaderboard, and mapping ablations

### 0042 Root Optimization Orchestration and Objective Completion

Purpose:
- implement the literal root optimization program

Required outcomes:
- tracked `Ray Tune`, `Optuna`, and `Ax` orchestration rather than backend-name simulation
- full root objective package, including lag accuracy, coverage, false-positive rate, agreement, change-point precision and recall, efficacy metrics, runtime, storage footprint, reproducibility, and interpretability penalties where the authority plan requires them
- Pareto-front outputs, experiment dashboards, benchmark guards, hold-out protections, and mutation-surface controls
- auditable keep/discard decisions for optimized mappings and analysis configurations

### 0043 Hold-Out Discovery and CLAGN Real-Data Analysis

Purpose:
- execute literal discovery and CLAGN analysis on the frozen hold-out pool

Required outcomes:
- anomaly ranking built from validated real pipeline outputs rather than authored fixture scores
- CLAGN transition and precursor analyses with aligned timelines and spectroscopic evidence
- candidate memos, ranked catalogs, follow-up priorities, and anomaly taxonomy assignment grounded in the validated benchmark behavior
- explicit separation between benchmark-calibrated parameters and untouched hold-out evidence

### 0044 Publication-Grade Release, Analyst Workbench, and Archive Assembly

Purpose:
- assemble the literal release and review outputs required by the root authority documents

Required outcomes:
- methods-paper artifact bundle and catalog-paper artifact bundle generated from tracked results
- open-source release bundle with code, configs, manifests, workflows, and reproducibility checklist
- benchmark archive and audio archive with provenance-complete manifests
- analyst workbench views exposing benchmark, discovery, optimization, and release evidence from structured tracked artifacts

### 0045 Literal Root Authority Conformance Audit and Final Readiness Gate

Purpose:
- replace the shallow closeout audit with literal conformance testing

Required outcomes:
- root-authority audit criteria mapped one-to-one to the required datasets, modules, methods, metrics, phases, deliverables, and guardrails from the authority documents
- explicit failing conditions for surrogate evidence, placeholder deliverables, missing raw-preservation records, missing release artifacts, or incomplete real-data execution
- final readiness decision based on literal evidence rather than artifact counts

## Sequencing Rules

1. `0039` and `0040` are prerequisites for any new claim of root-scope scientific completion.
2. `0041` must consume the frozen corpora from `0040` and the literal backend integrations from `0039`.
3. `0042` may optimize only against benchmark artifacts frozen under `0040` and validated under `0041`.
4. `0043` must use hold-out corpora frozen before optimization outputs are promoted and may not back-fit thresholds on discovery results.
5. `0044` must expose the outputs of `0041` through `0043` through the analyst workbench and release bundles without introducing hand-curated scientific claims.
6. `0045` closes the root authority documents only after literal evidence exists for every required dataset tier, method family, benchmark deliverable, discovery deliverable, release artifact, and guardrail.

## Acceptance Gate

The root authority documents are satisfied only when all of the following are true:

- every required RM backend and `PyQSOFit` execute as literal tracked integrations rather than surrogate stand-ins
- the gold, silver, and discovery corpora are frozen at literal root scope with raw-preservation, provenance, and hold-out governance
- benchmark outputs operate on real continuum and line-response measurements and reproduce the required root validation deliverables
- `Ray Tune`, `Optuna`, and `Ax` run as actual orchestrators over the full root objective package with protected benchmark and hold-out boundaries
- discovery and CLAGN outputs are derived from validated real-data analysis and produce ranked catalogs, timelines, and memos
- the analyst workbench, open-source release, methods-paper artifacts, catalog-paper artifacts, benchmark archive, and audio archive all exist as tracked deliverables
- the final root-authority audit tests literal compliance and rejects every proxy or placeholder form of evidence listed in this playbook

## Exit Condition

No implementation, benchmark result, release artifact, or readiness claim may be described as satisfying the root authority documents until `0045` passes on literal evidence.
