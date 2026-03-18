# Project List

Numbered work packages, release groupings, and dependency ordering derived from the authority documents.

## Releases

```yaml
releases:
  - version: "v0.1.0"
    name: "Foundation and Standards"
    status: active
    summary: "Establish the public repository boundary, the repository skeleton, the workflow substrate, and the canonical schema layer."
    projects: ["0001", "0002", "0003", "0004", "0005"]
    notes: "All committed outputs must remain formal, concise, precise, and limited to essential content."
  - version: "v0.2.0"
    name: "Benchmark Core"
    status: planning
    summary: "Deliver benchmark data access, calibration, inference, sonification, simulation, and validation on known lag-bearing systems."
    projects: ["0006", "0007", "0008", "0009", "0010", "0011", "0012", "0013", "0014", "0015", "0016", "0017"]
    notes: "Validation on benchmark objects gates all later discovery claims."
  - version: "v0.3.0"
    name: "Discovery and Optimization"
    status: planning
    summary: "Extend the validated pipeline into benchmark-driven optimization and CLAGN-oriented anomaly discovery."
    projects: ["0018", "0019"]
    notes: "Discovery work remains downstream of fixed benchmark suites and immutable labels."
  - version: "v1.0.0"
    name: "Open Science Release"
    status: planning
    summary: "Package methods, catalog outputs, and reproducible artifacts for external release."
    projects: ["0020"]
    notes: "Do not mark released until validation, discovery, and release artifacts are integrated."
```

## Projects

```yaml
projects:
  - id: "0001"
    title: "Foundation Baseline"
    summary: "Establish the minimal public repository baseline, the Python verification scaffold, and the first numbered work structure."
    status: committed
    priority: high
    release: "v0.1.0"
    files:
      spec: ark/specs/0001-foundation-bootstrap.md
      plan: ark/plans/0001-foundation-bootstrap.md
      review: null
    dependencies: []
    tags: [foundation, public-docs, python]
    notes: "This work provides the baseline from which the decomposed program begins."
  - id: "0002"
    title: "Public Repository Boundary and Documentation Standard"
    summary: "Define the publication boundary and the required editorial standard for all committed documentation."
    status: committed
    priority: high
    release: "v0.1.0"
    files:
      spec: ark/specs/0002-public-repository-boundary.md
      plan: ark/plans/0002-public-repository-boundary.md
      review: null
    dependencies: ["0001"]
    tags: [governance, documentation]
    notes: "This package applies to every later committed artifact."
  - id: "0003"
    title: "Research Platform Skeleton"
    summary: "Define the repository topology, package layout, and top-level interfaces required by the scientific plan."
    status: committed
    priority: high
    release: "v0.1.0"
    files:
      spec: ark/specs/0003-research-platform-skeleton.md
      plan: ark/plans/0003-research-platform-skeleton.md
      review: null
    dependencies: ["0002"]
    tags: [foundation, architecture]
    notes: "Keep each module boundary narrow and scientifically legible."
  - id: "0004"
    title: "Workflow and Experiment Stack"
    summary: "Define the workflow, configuration, data-versioning, and experiment-tracking substrate."
    status: committed
    priority: high
    release: "v0.1.0"
    files:
      spec: ark/specs/0004-workflow-experiment-stack.md
      plan: ark/plans/0004-workflow-experiment-stack.md
      review: null
    dependencies: ["0002", "0003"]
    tags: [workflow, reproducibility, experiments]
    notes: "Separate tracked metadata from large generated state."
  - id: "0005"
    title: "Canonical Schemas and Manifest Layer"
    summary: "Define the canonical schemas and manifests that standardize objects, photometry, spectra, lags, and sonifications."
    status: committed
    priority: high
    release: "v0.1.0"
    files:
      spec: ark/specs/0005-canonical-schemas-manifests.md
      plan: ark/plans/0005-canonical-schemas-manifests.md
      review: null
    dependencies: ["0002", "0003"]
    tags: [schemas, manifests, interfaces]
    notes: "All downstream code should target these schemas rather than survey-specific formats."
  - id: "0006"
    title: "AGN Watch Gold Ingestion"
    summary: "Ingest the gold benchmark archive with raw preservation, object manifests, and canonical tables."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0006-agn-watch-gold-ingestion.md
      plan: ark/plans/0006-agn-watch-gold-ingestion.md
      review: null
    dependencies: ["0004", "0005"]
    tags: [ingest, agn-watch, gold]
    notes: "Begin with NGC 5548 and one additional well-characterized object."
  - id: "0007"
    title: "SDSS-RM Silver Ingestion"
    summary: "Ingest the scalable published-lag benchmark set with raw spectra, object manifests, and canonical tables."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0007-sdss-rm-silver-ingestion.md
      plan: ark/plans/0007-sdss-rm-silver-ingestion.md
      review: null
    dependencies: ["0004", "0005"]
    tags: [ingest, sdss-rm, silver]
    notes: "Separate raw spectra, spectral epochs, and derived line products."
  - id: "0008"
    title: "ZTF Access Layer"
    summary: "Define the public-light-curve access layer for the discovery pool, with release pinning and query provenance."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0008-ztf-access-layer.md
      plan: ark/plans/0008-ztf-access-layer.md
      review: null
    dependencies: ["0004", "0005"]
    tags: [ingest, ztf, discovery]
    notes: "Keep release identifiers, query constraints, and flags explicit."
  - id: "0009"
    title: "Crossmatch, Time Standards, and Quality Control"
    summary: "Define the shared calibration, time-standard, and quality-control layer across all surveys."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0009-crossmatch-time-qc.md
      plan: ark/plans/0009-crossmatch-time-qc.md
      review: null
    dependencies: ["0005", "0006", "0007", "0008"]
    tags: [crossmatch, calibration, qc]
    notes: "Preserve observed-frame and rest-frame time, masks, flags, and explicit quality scores."
  - id: "0010"
    title: "Classical Lag Wrappers"
    summary: "Implement the classical cross-correlation lag methods and the method-level lag-result interface."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0010-classical-lag-wrappers.md
      plan: ark/plans/0010-classical-lag-wrappers.md
      review: null
    dependencies: ["0005", "0009"]
    tags: [rm, pyccf, pyzdcf]
    notes: "Provide literature-continuity baselines and uneven-sampling cross-checks."
  - id: "0011"
    title: "Model-Based Lag Wrappers"
    summary: "Implement the initial model-based lag methods and the required convergence and uncertainty diagnostics."
    status: committed
    priority: medium
    release: "v0.2.0"
    files:
      spec: ark/specs/0011-model-based-lag-wrappers.md
      plan: ark/plans/0011-model-based-lag-wrappers.md
      review: null
    dependencies: ["0005", "0009"]
    tags: [rm, javelin, pyroa]
    notes: "Start with JAVELIN and PyROA before later-stage advanced methods."
  - id: "0012"
    title: "Consensus Lags and Null Diagnostics"
    summary: "Build the consensus lag object, agreement taxonomy, alias diagnostics, and null controls."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0012-consensus-lags-null-diagnostics.md
      plan: ark/plans/0012-consensus-lags-null-diagnostics.md
      review: null
    dependencies: ["0010", "0011"]
    tags: [rm, consensus, diagnostics]
    notes: "This package determines whether a lag is agreed, contested, spurious, or anomalous."
  - id: "0013"
    title: "Spectral Decomposition and Line Metrics"
    summary: "Implement multi-epoch spectral decomposition, line extraction, and fit diagnostics."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0013-spectral-decomposition-line-metrics.md
      plan: ark/plans/0013-spectral-decomposition-line-metrics.md
      review: null
    dependencies: ["0005", "0007", "0009"]
    tags: [spectra, line-metrics, diagnostics]
    notes: "Retain multiple continuum-subtraction variants and calibration confidence metadata."
  - id: "0014"
    title: "Sonification Core and Echo Ensemble"
    summary: "Implement the stable sonification contract, uncertainty encoding policy, and the first echo-ensemble mapping family."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0014-sonification-core-echo-ensemble.md
      plan: ark/plans/0014-sonification-core-echo-ensemble.md
      review: null
    dependencies: ["0005", "0012", "0013"]
    tags: [sonification, audio, uncertainty]
    notes: "This package establishes the science-audio contract before comparative mapping work expands."
  - id: "0015"
    title: "Comparative Mapping Families and Render Bundles"
    summary: "Add the direct-audification and token-stream families plus the required render and provenance bundles."
    status: committed
    priority: medium
    release: "v0.2.0"
    files:
      spec: ark/specs/0015-comparative-mapping-families.md
      plan: ark/plans/0015-comparative-mapping-families.md
      review: null
    dependencies: ["0014"]
    tags: [sonification, rendering, provenance]
    notes: "Comparability across mapping families is required for later efficacy testing."
  - id: "0016"
    title: "Synthetic Benchmark Suite"
    summary: "Implement the synthetic truth tables for clean, contaminated, state-change, and failure-case benchmarks."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0016-synthetic-benchmark-suite.md
      plan: ark/plans/0016-synthetic-benchmark-suite.md
      review: null
    dependencies: ["0005", "0010", "0014"]
    tags: [simulation, benchmarks, truth]
    notes: "Benchmark labels become fixed inputs to all later optimization and validation work."
  - id: "0017"
    title: "Validation and Blinded Efficacy"
    summary: "Validate the pipeline on benchmark objects and run blinded plot/audio/plot+audio efficacy testing."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0017-validation-blinded-efficacy.md
      plan: ark/plans/0017-validation-blinded-efficacy.md
      review: null
    dependencies: ["0006", "0007", "0012", "0013", "0015", "0016"]
    tags: [validation, efficacy, leaderboards]
    notes: "Benchmark validation is the gate for all later discovery and release claims."
  - id: "0018"
    title: "Optimization Infrastructure"
    summary: "Define the benchmark-driven optimization layer for experiments, mappings, and controlled agent programs."
    status: committed
    priority: medium
    release: "v0.3.0"
    files:
      spec: ark/specs/0018-optimization-infrastructure.md
      plan: ark/plans/0018-optimization-infrastructure.md
      review: null
    dependencies: ["0004", "0016", "0017"]
    tags: [optimization, orchestration, experiments]
    notes: "Optimization must remain downstream of fixed benchmarks and explicit objective metrics."
  - id: "0019"
    title: "CLAGN and Anomaly Discovery Extension"
    summary: "Extend the validated pipeline into ZTF-scale anomaly ranking, CLAGN transition analysis, and follow-up prioritization."
    status: committed
    priority: medium
    release: "v0.3.0"
    files:
      spec: ark/specs/0019-clagn-anomaly-discovery.md
      plan: ark/plans/0019-clagn-anomaly-discovery.md
      review: null
    dependencies: ["0008", "0012", "0015", "0017"]
    tags: [clagn, anomaly, discovery]
    notes: "Treat the discovery pool as hold-out; do not optimize directly on it."
  - id: "0020"
    title: "Release, Catalog, and Publication Artifacts"
    summary: "Package the validated methods, catalogs, audio bundles, and publication-ready outputs for external release."
    status: planned
    priority: medium
    release: "v1.0.0"
    files:
      spec: ark/specs/0020-release-catalog-publication.md
      plan: ark/plans/0020-release-catalog-publication.md
      review: null
    dependencies: ["0017", "0018", "0019"]
    tags: [release, catalog, publications]
    notes: "Release only after validation, optimization, and discovery outputs are scientifically reviewed."
```
## Authority Notes

- The root scientific plan and root agent spec remain the authority sources for scientific scope and decomposition decisions.
- All committed documentation must remain formal, concise, precise, and limited to essential content.
