# 0046 Adversarial Root Authority Gap-Closure Plan

## Purpose

Define the strict remediation plan required after the latest adversarial review determined that the current implementation remains materially short of literal root-authority compliance.

## Scope

This playbook governs the remaining work required to satisfy the root project plan and root agent specification in implementation, deliverables, and readiness. It applies to the active remediation sequence under `0039` through `0045` and tightens their acceptance criteria where the current implementation still permits proxy, partial, or placeholder evidence.

## Governing Rule

Acceptability is literal satisfaction of the root authority documents. A package is incomplete if it satisfies only a repository-local check while failing the scientific intent, data scope, or deliverable definition stated in the root project plan or root agent specification.

The following are explicitly non-acceptable as completion evidence:

- published-light-curve subsets presented as full SDSS-RM or ZTF raw-ingest compliance
- catalog rows presented as discovery-pool light-curve or transition-analysis compliance
- synthetic spectra or placeholder epochs presented as spectral-rigor completion
- silent or placeholder audio assets presented as scientific sonification outputs
- scalarized toy search over hand-authored candidates presented as literal root optimization
- placeholder markdown summaries presented as methods papers, catalog papers, figures, archives, or release bundles
- audits based primarily on counts, file existence, or internally asserted evidence labels

## Controlling Findings and Required Response

### F1. Corpus and Raw-Preservation Compliance Failure

Observed gap:
- the implementation does not yet preserve and operate on the full raw SDSS-RM and ZTF products required by the root authority documents

Required response:
- `0040` must acquire official SDSS-RM and ZTF source products at the raw layer, preserve them exactly as downloaded, and materialize the required normalized derivatives in parallel rather than in place
- `0040` must store release identifiers, query provenance, raw hashes, exclusion reasons, and immutable freeze manifests for gold, silver, and discovery tiers
- `0045` must fail if AGN Watch, SDSS-RM, or ZTF raw-preservation records are incomplete

Acceptance evidence:
- tracked raw-product manifests for AGN Watch, SDSS-RM, and ZTF
- tracked normalized derivative manifests linked one-to-one back to raw hashes
- corpus freeze reports with scope counts and exclusion reasons aligned to the root plan

### F2. Spectral-Rigor Compliance Failure

Observed gap:
- the implementation does not yet derive spectral diagnostics from real spectral epochs at the literal scope required by the root authority documents

Required response:
- `0039` and `0041` must operate on real spectral epochs, not synthetic or stand-in spectra
- `0039` must record observed-frame and rest-frame representations, continuum variants, calibration state, and real `PyQSOFit` decomposition products
- `0041` must produce real line-metric tables from tracked spectral epochs across the required line set where coverage exists

Acceptance evidence:
- tracked spectral-epoch records for silver and gold corpora where the authority plan requires them
- tracked real `PyQSOFit` outputs and alternative continuum-subtraction outputs
- line-metric tables and calibration diagnostics derived from those real spectral epochs

### F3. Scientific Sonification Output Failure

Observed gap:
- the current audio layer does not yet produce the literal science outputs required by the root authority documents

Required response:
- `0041` must render real science audio from real benchmark objects with explicit uncertainty encodings
- `0044` must assemble the required per-object sonification bundle: science WAV, presentation audio, isolated stems, synchronized figure or movie, mapping legend, config, and provenance record
- `0044` must expose these assets through the analyst workbench and release archive

Acceptance evidence:
- non-placeholder audio artifacts linked to tracked inputs and render configs
- benchmarked uncertainty encodings across the required mapping families
- per-object release bundles containing the literal sonification outputs required by the root plan

### F4. Discovery and CLAGN Compliance Failure

Observed gap:
- discovery ranking and CLAGN analysis do not yet derive from validated real pipeline outputs on real hold-out data

Required response:
- `0043` must execute discovery on frozen real hold-out light curves and spectral evidence rather than catalog-row deltas alone
- `0043` must produce continuum-lag outlier outputs, line-response anomaly outputs, CLAGN transition timelines, pre/post sonification comparisons, and candidate precursor records
- `0043` must preserve the hold-out boundary explicitly and record any benchmark-calibrated thresholds separately from discovery evidence

Acceptance evidence:
- ranked anomaly catalog with provenance to validated real-data outputs
- CLAGN transition and precursor artifacts with explicit temporal alignment
- candidate memos tied to measured hold-out evidence rather than authored or inferred fixture labels

### F5. Optimization Compliance Failure

Observed gap:
- the optimization layer does not yet implement the literal root objective surface or a real Pareto program

Required response:
- `0042` must run `Ray Tune`, `Optuna`, and `Ax` over real mutable surfaces and recorded experiments rather than over a tiny fixed candidate list
- `0042` must implement the full objective set required by the root plan, including held-out anomaly precision metrics and audio-task discriminability
- `0042` must record Pareto-front outputs, experiment dashboards, mutation guards, benchmark protections, and keep-discard decisions

Acceptance evidence:
- tracked experiment outputs from all three orchestrators over real search spaces
- explicit objective records for all required root metrics
- Pareto-front artifacts and mutation-guard records

### F6. Publication and Release Compliance Failure

Observed gap:
- the release surface remains a placeholder summary rather than a publication-grade deliverable set

Required response:
- `0044` must produce the literal catalog-level outputs required by the root plan, including benchmark leaderboard, anomaly catalog, CLAGN transition catalog, sonification-mapping leaderboard, and literature comparison table
- `0044` must produce publication-ready artifact bundles, not placeholder markdown stubs
- `0044` must produce the benchmark archive, audio archive, open-source package documentation, and analyst workbench evidence views

Acceptance evidence:
- structured release artifacts for every required catalog and leaderboard
- methods-paper and catalog-paper artifact bundles with figures and supporting tables
- benchmark and audio archive manifests with provenance-complete inventories

### F7. Final Audit Compliance Failure

Observed gap:
- the current root-authority audit remains too shallow to prove literal compliance

Required response:
- `0045` must map each audit condition directly to a required root-authority dataset, method family, metric family, deliverable family, and governance rule
- `0045` must inspect content, not only presence or counts
- `0045` must fail on placeholder audio, synthetic spectra used as scientific evidence, missing SDSS/ZTF raw preservation, missing catalog-level outputs, or incomplete objective implementation

Acceptance evidence:
- a conformance audit whose checks can be traced one-to-one back to root-authority clauses
- explicit failure conditions for every currently observed ambiguity class

## Package Tightening Instructions

### 0039 Real Backend and Spectral Backend Integration

Tighten to require:
- literal execution records for all declared RM backends and `PyQSOFit`
- real-data examples for each backend family
- failure-mode and fallback reporting that does not count as completion

### 0040 Full Corpus Acquisition, Raw Preservation, and Freeze

Tighten to require:
- official raw-source preservation for AGN Watch, SDSS-RM, and ZTF
- explicit rest-frame and normalization metadata
- freeze manifests that enumerate included and excluded scope

### 0041 Real-Data Benchmark Execution and Validation Closure

Tighten to require:
- benchmark execution on real measured continuum and line-response data
- real spectral products and line-metric outputs
- literal sonification deliverables and benchmark-facing validation artifacts

### 0042 Root Optimization Orchestration and Objective Completion

Tighten to require:
- real optimizer search spaces
- full root objective implementation
- Pareto outputs and guarded experiment controls

### 0043 Hold-Out Discovery and CLAGN Real-Data Analysis

Tighten to require:
- validated hold-out ranking inputs
- transition and precursor outputs
- real discovery evidence bundles and galleries

### 0044 Publication-Grade Release, Analyst Workbench, and Archive Assembly

Tighten to require:
- publication-grade content bundles
- literal archive inventories
- analyst workbench support for benchmark, optimization, discovery, and release review

### 0045 Literal Root Authority Conformance Audit and Final Readiness Gate

Tighten to require:
- one-to-one clause coverage against the root authority documents
- content inspection rather than count-only checks
- automatic rejection of every placeholder-evidence class listed in this playbook

## Sequencing

1. Tighten `0039` through `0045` before any new closeout claim is made.
2. Complete `0040` before promoting any SDSS-RM or ZTF scientific readiness claim.
3. Complete the real spectral and sonification obligations in `0039` and `0041` before any claim of root-scope validation closure.
4. Complete `0042` before discovery outputs are interpreted as benchmark-governed rather than exploratory.
5. Complete `0043` before any CLAGN or anomaly claim is promoted as root-authority compliant.
6. Complete `0044` before any claim of publication or release readiness.
7. Run `0045` only after all prior evidence exists in tracked artifacts.

## Acceptance Gate

The root authority documents are satisfied only when all of the following are true:

- AGN Watch, SDSS-RM, and ZTF raw products are preserved exactly as required and linked to normalized derivatives
- real spectral-epoch processing and real `PyQSOFit` decomposition outputs exist at the required benchmark scope
- real sonification assets, uncertainty encodings, and per-object audio bundles exist as literal scientific outputs
- benchmark validation uses real measured continuum and line-response series at the declared literal scope
- discovery and CLAGN outputs derive from validated hold-out pipeline products rather than catalog-only or fixture-authored proxies
- `Ray Tune`, `Optuna`, and `Ax` execute the literal optimization program over the full root objective package
- publication-grade leaderboards, catalogs, archives, analyst workbench views, and paper-artifact bundles exist in tracked form
- the final conformance audit verifies all of the above directly and rejects placeholder evidence

## Exit Condition

No implementation, deliverable, benchmark result, release artifact, or readiness statement may be described as satisfying the root authority documents until the tightened `0039` through `0045` sequence is complete and `0045` passes on literal evidence.
