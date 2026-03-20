# 0031 Root Authority Closeout Playbook

## Purpose

Define the remaining sequence required to satisfy the full root project plan and root agent specification after completion of the benchmark-validation gate.

## Scope

This playbook addresses the gap between benchmark-scope scientific readiness and full root-scope program completion. It covers advanced real-data inference, corpus scale-out, benchmark-governed optimization, hold-out discovery analysis, analyst-facing review surfaces, and externally reviewable release artifacts.

## Current State

- The benchmark-validation gate defined by `0024` through `0030` is satisfied within its declared scope.
- The repository has reproducible benchmark bundles, scientific review artifacts, and a read-only benchmark review surface.
- The current optimization, discovery, and release modules exist but remain scaffold-grade relative to the root authority documents.
- The repository does not yet satisfy the full root plan across advanced RM backends, full corpus coverage, discovery hold-out workflows, or publication-grade release outputs.

## Root-Scope Gaps

### G1. Advanced Real-Data Inference Is Incomplete

- The root authority documents require end-to-end support for `pyPETaL`, `LITMUS`, `MICA2`, `EzTao`, and `celerite2` in addition to the current core methods.
- The recommended inference protocol requires selective high-rigor execution of `LITMUS` and `MICA2` on high-quality or anomalous cases.
- Runtime, convergence, posterior, alias, and agreement diagnostics must exist for these backends on tracked real-data objects.

### G2. Spectral Decomposition Has Not Reached Root Rigor

- The root plan names `PyQSOFit` as the main spectral fitting backend.
- Multiple continuum-subtraction variants, calibration choices, and fit-model identifiers must remain first-class metadata rather than implicit implementation details.
- Gold and silver objects need literature-facing line-response and calibration diagnostics at broader scale than the present benchmark slice.

### G3. Corpus Coverage And Hold-Out Governance Are Not Yet Complete

- The root plan calls for a full gold object set, a broad published-lag silver benchmark, and a discovery-hold-out pool built from ZTF and CLAGN labels.
- Immutable inclusion criteria, benchmark strata, exclusion reasons, and hold-out boundaries must be frozen and tracked before optimization or anomaly ranking expands.
- Discovery-pool manifests, query provenance, and release pinning must be explicit at corpus scale.

### G4. Optimization Has Not Reached Root-Plan Form

- The current optimization layer does not yet implement the declared `Ray Tune`, `Optuna`, and `Ax` orchestration pattern.
- Pareto-style optimization objectives, benchmark-driven retain/discard logic, and protected mutation surfaces must be encoded in tracked workflows and artifacts.
- Agent-program optimization remains incomplete relative to the benchmark-governed autoresearch model in the root plan.

### G5. Discovery And CLAGN Analysis Are Not Scientifically Closed

- The root plan requires interpretable anomaly ranking over continuum-lag outliers, line-response anomalies, CLAGN transitions, and extreme-object taxonomies.
- Hold-out discovery results must include ranked catalogs, transition-aligned timelines, object memos, and evidence bundles backed by validated methods.
- Audio and non-audio representations should contribute explicit evidence; opaque aggregate scores are insufficient.

### G6. Analyst-Facing Review Is Benchmark-Centric Rather Than Program-Wide

- The current review surface is sufficient for benchmark analysis but not yet for full discovery and release review.
- Root-scope completion requires navigation across benchmark, discovery, catalog, and release artifacts through one read-only analysis surface.
- Review pages must expose hold-out governance, candidate evidence, anomaly taxonomies, release provenance, and publication-boundary claims.

### G7. Release And Publication Outputs Are Not Yet Externally Defensible

- The root plan requires methods-release artifacts, anomaly catalogs, audio archives, reproducibility checklists, and publication-facing figures and tables.
- Release assembly must be generated from validated structured artifacts rather than hand-curated summaries.
- Public release claims must remain traceable to benchmark evidence, discovery review, and frozen provenance records.

## Closeout Sequence

The full root program should be closed through the following work packages.

### 0032 Advanced Method and Spectral Rigor Completion

Purpose:
- finish advanced RM-method execution and high-rigor spectral decomposition on tracked real-data corpora

Required outcomes:
- validated wrappers and execution paths for `pyPETaL`, `LITMUS`, `MICA2`, `EzTao`, and `celerite2`
- `PyQSOFit`-backed spectral decomposition with retained fit variants and calibration metadata
- tracked diagnostics for runtime, convergence, alias structure, posterior width, and transfer-function complexity
- promotion of benchmark and anomaly conclusions only after the required advanced-method checks pass where the root protocol demands them

### 0033 Corpus Scale-Out and Discovery Hold-Out Freeze

Purpose:
- freeze the full root-scope benchmark and discovery corpora with explicit provenance and hold-out governance

Required outcomes:
- full gold manifest beyond the current minimal case-study set
- broad silver manifest with literature labels, regimes, strata, exclusions, and release pinning
- discovery-hold-out manifests for ZTF and CLAGN corpora with query provenance, crossmatch keys, and explicit no-optimization boundaries
- tracked hashes and freeze reports for all root-scope corpora

### 0034 Benchmark-Governed Optimization and Agent Loop Completion

Purpose:
- upgrade the current optimization scaffold into the root-plan autoresearch system

Required outcomes:
- tracked `Ray Tune`, `Optuna`, and `Ax` orchestration
- immutable benchmark guards covering labels, manifests, hold-out boundaries, and prohibited mutation zones
- Pareto-style objective packages over science, sonification, and engineering metrics
- auditable experiment outputs, retention rules, and rerun-stability checks for optimized mappings and configurations

### 0035 Discovery Hold-Out and CLAGN Scientific Analysis

Purpose:
- execute the root discovery program on the frozen hold-out pool

Required outcomes:
- ranked continuum-lag outlier catalog
- ranked line-response anomaly catalog
- CLAGN transition and precursor analyses with aligned timelines
- candidate memos with anomaly taxonomies, evidence bundles, and follow-up prioritization
- explicit linkage between validated benchmark behavior and discovery scoring logic

### 0036 Scientific Analyst Workbench and Discovery Review Surface

Purpose:
- extend the review surface into the analyst workbench required for program-wide scientific review

Required outcomes:
- package, object, candidate, cohort, and release navigation across benchmark, discovery, and publication artifacts
- sortable and filterable candidate tables with anomaly categories, confidence, method support, and review status
- object-level pages combining lag outputs, spectra diagnostics, sonification products, transition evidence, and provenance
- release-facing views that expose claims boundaries, limitations, and provenance completeness directly from structured artifacts

### 0037 Public Release and Publication Closeout

Purpose:
- assemble the externally reviewable release required by the root plan

Required outcomes:
- methods-release bundle with code, configuration, manifests, benchmark tables, and provenance records
- anomaly catalog release with candidate inventories, evidence summaries, and review status
- audio archive with science-ready provenance manifests
- publication-facing figures, tables, and reproducibility checklist generated from tracked artifacts

## Sequencing Rules

1. `0024` through `0030` remain a prerequisite and may not be weakened.
2. `0032` and `0033` must complete before discovery-scale scoring or optimization outputs are promoted.
3. `0034` must optimize only against frozen benchmark artifacts and may never tune directly on discovery-hold-out data.
4. `0035` may use optimized mappings or configurations only after their benchmark-governed evidence is recorded.
5. `0036` must receive matching implementation slices alongside `0035` and `0037` so new claims remain inspectable.
6. `0037` closes the root program only after validated methods, discovery outputs, and review surfaces are integrated.

## Root Closeout Gate

The full root project plan and root agent specification are satisfied only when all of the following are true:

- the benchmark-validation gate remains passing within its declared scope
- advanced RM methods and `PyQSOFit`-backed spectral workflows run on tracked real-data corpora with stored diagnostics
- frozen full-scope gold, silver, and discovery manifests exist with explicit provenance and hold-out governance
- benchmark-governed optimization runs through tracked orchestration with protected mutation surfaces and auditable objectives
- hold-out discovery analysis produces ranked anomaly and CLAGN outputs with interpretable evidence bundles
- the read-only analyst workbench exposes benchmark, discovery, and release artifacts through tracked structured files
- the release bundle includes externally reviewable methods, catalogs, audio products, provenance records, and publication-facing artifacts

## Non-Gate Items

- Simulation-based inference and joint representation learning remain optional accelerants rather than root-v1 closeout gates.
- Audio and feature embeddings may be used in discovery ranking when their provenance and validation are explicit, but the root closeout does not require a full joint-embedding platform.
- Optional NEOWISE follow-up remains secondary to the optical pipeline and does not block root-v1 completion.

## Exit Condition

The root authority documents are operationally satisfied only after `0032` through `0037` are implemented, validated, and integrated without weakening the benchmark-governed scientific-rigor rules established by the earlier packages.
