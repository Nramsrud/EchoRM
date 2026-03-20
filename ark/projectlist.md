# Project List

Numbered work packages, release groupings, and dependency ordering derived from the authority documents.

## Releases

```yaml
releases:
  - version: "v0.1.0"
    name: "Foundation and Standards"
    status: released
    summary: "Establish the public repository boundary, the repository skeleton, the workflow substrate, and the canonical schema layer."
    projects: ["0001", "0002", "0003", "0004", "0005"]
    notes: "All committed outputs must remain formal, concise, precise, and limited to essential content."
  - version: "v0.2.0"
    name: "Benchmark Core"
    status: active
    summary: "Deliver benchmark data access, calibration, inference, sonification, simulation, and validation on known lag-bearing systems."
    projects: ["0006", "0007", "0008", "0009", "0010", "0011", "0012", "0013", "0014", "0015", "0016", "0017", "0021", "0022", "0023", "0024", "0025", "0026", "0027", "0028", "0029", "0030"]
    notes: "Validation on benchmark objects gates all later discovery claims."
  - version: "v0.3.0"
    name: "Discovery, Optimization, and Scale-Out"
    status: planning
    summary: "Complete the root-scope scientific program beyond the benchmark gate: advanced real-data inference, optimization, discovery hold-out analysis, analyst review surfaces, and release preparation."
    projects: ["0018", "0019", "0031", "0032", "0033", "0034", "0035", "0036"]
    notes: "Discovery work remains downstream of fixed benchmark suites and immutable labels, and benchmark readiness remains a prerequisite."
  - version: "v1.0.0"
    name: "Open Science Release"
    status: planning
    summary: "Package methods, catalog outputs, and reproducible artifacts for external release."
    projects: ["0020", "0037"]
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
    status: committed
    priority: medium
    release: "v1.0.0"
    files:
      spec: ark/specs/0020-release-catalog-publication.md
      plan: ark/plans/0020-release-catalog-publication.md
      review: null
    dependencies: ["0017", "0018", "0019"]
    tags: [release, catalog, publications]
    notes: "Release only after validation, optimization, and discovery outputs are scientifically reviewed."
  - id: "0021"
    title: "Benchmark Readiness Hardening"
    summary: "Convert the benchmark scaffold into an executable readiness surface with structured run bundles, readiness reports, and reproducible review artifacts."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0021-benchmark-readiness-hardening.md
      plan: ark/plans/0021-benchmark-readiness-hardening.md
      review: null
    dependencies: ["0004", "0006", "0007", "0015", "0016", "0017"]
    tags: [benchmarks, validation, readiness, workflow]
    notes: "Benchmark readiness requires executable run bundles, explicit environment checks, and reviewable outputs."
  - id: "0022"
    title: "Benchmark Review Web Interface"
    summary: "Provide a read-only web interface for navigating benchmark runs, inspecting readiness state, and reviewing result quality."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0022-benchmark-review-web-interface.md
      plan: ark/plans/0022-benchmark-review-web-interface.md
      review: null
    dependencies: ["0021"]
    tags: [review, web, benchmarks, tailscale]
    notes: "Default network binding must use a detected Tailscale address, with localhost available only by explicit flag."
  - id: "0023"
    title: "First Benchmark Execution Package"
    summary: "Define and execute the first benchmark package with explicit scientific scope, evidence levels, fixture-backed real-data checks, and synthetic lag-recovery cases."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0023-first-benchmark-execution-package.md
      plan: ark/plans/0023-first-benchmark-execution-package.md
      review: null
    dependencies: ["0006", "0007", "0010", "0016", "0017", "0021", "0022"]
    tags: [benchmarks, validation, evidence, scientific-rigor]
    notes: "The first benchmark must distinguish real-fixture ingest fidelity from synthetic lag-recovery evidence and must not overstate scientific claims."
  - id: "0024"
    title: "Broad Benchmark Scientific Validation Gate Playbook"
    summary: "Define the staged gate from bounded first benchmark coverage to broad scientific validation across gold, silver, continuum-RM, and sonification-efficacy benchmarks."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/playbooks/0024-broad-benchmark-scientific-validation-gate.md
      plan: null
      review: null
    dependencies: ["0006", "0007", "0010", "0011", "0012", "0013", "0015", "0016", "0017", "0021", "0022", "0023"]
    tags: [validation, benchmarks, playbook, scientific-rigor]
    notes: "This playbook defines the evidence gates, required artifacts, and remaining implementation gaps before any broad scientific-validation claim is allowed."
  - id: "0025"
    title: "Benchmark Corpus Freeze and Multi-Method Execution"
    summary: "Freeze the gold and silver benchmark corpora, execute the core reverberation methods on real benchmark objects, and materialize null and failure diagnostics."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0025-benchmark-corpus-freeze-multi-method-execution.md
      plan: ark/plans/0025-benchmark-corpus-freeze-multi-method-execution.md
      review: null
    dependencies: ["0006", "0007", "0010", "0011", "0012", "0016", "0021", "0023", "0024"]
    tags: [validation, benchmarks, methods, manifests]
    notes: "This package establishes the frozen benchmark manifests and real benchmark method outputs required by all later broad-validation packages."
  - id: "0026"
    title: "Gold Benchmark Validation and Case Studies"
    summary: "Validate the literature-rich AGN Watch gold benchmark set with object-level lag comparison, line diagnostics, audio artifacts, and case-study memos."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0026-gold-benchmark-validation-case-studies.md
      plan: ark/plans/0026-gold-benchmark-validation-case-studies.md
      review: null
    dependencies: ["0013", "0015", "0017", "0025"]
    tags: [validation, gold, agn-watch, case-studies]
    notes: "Broad scientific validation requires more than one gold object with literature comparison, line-fit diagnostics, and mapping-comparison review."
  - id: "0027"
    title: "Silver Benchmark Population Validation"
    summary: "Validate a broad SDSS-RM published-lag benchmark population with population metrics, null controls, and regime-level reporting."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0027-silver-benchmark-population-validation.md
      plan: ark/plans/0027-silver-benchmark-population-validation.md
      review: null
    dependencies: ["0012", "0013", "0017", "0025"]
    tags: [validation, silver, sdss-rm, population]
    notes: "This package closes the population-scale validation gap with literature comparison, null controls, and regime-specific performance summaries."
  - id: "0028"
    title: "Continuum-RM Benchmark Expansion"
    summary: "Expand the continuum-RM benchmark program across hierarchy, contamination, state-change, and cadence-stability tasks with literature-inspired ZTF benchmark objects."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0028-continuum-rm-benchmark-expansion.md
      plan: ark/plans/0028-continuum-rm-benchmark-expansion.md
      review: null
    dependencies: ["0008", "0009", "0016", "0017", "0025"]
    tags: [validation, continuum-rm, ztf, contamination]
    notes: "This package establishes the broad continuum benchmark needed before contamination or disc-like claims are promoted."
  - id: "0029"
    title: "Sonification Efficacy Benchmark Program"
    summary: "Run the blinded plot-only, audio-only, and combined-modality efficacy benchmark program against strong visual baselines."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0029-sonification-efficacy-benchmark-program.md
      plan: ark/plans/0029-sonification-efficacy-benchmark-program.md
      review: null
    dependencies: ["0015", "0017", "0026", "0027", "0028"]
    tags: [validation, efficacy, sonification, blinded]
    notes: "Broad scientific validation requires a real blinded efficacy program rather than structural task scaffolding alone."
  - id: "0030"
    title: "Scientific Validation Review Surface and Claims Audit"
    summary: "Upgrade the review application for scientific analysis across validation packages and implement the cross-package claims audit that determines whether the broad-validation gate is satisfied."
    status: committed
    priority: high
    release: "v0.2.0"
    files:
      spec: ark/specs/0030-scientific-validation-review-surface-claims-audit.md
      plan: ark/plans/0030-scientific-validation-review-surface-claims-audit.md
      review: null
    dependencies: ["0022", "0026", "0027", "0028", "0029"]
    tags: [validation, review, web, claims-audit]
    notes: "The gate is not closed unless the tracked analysis surface and claims audit make the validation outputs inspectable and govern promotion correctly."
  - id: "0031"
    title: "Root Authority Closeout Playbook"
    summary: "Define the remaining sequence required to satisfy the full root project plan and root agent specification beyond the current benchmark-validation gate."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/playbooks/0031-root-authority-closeout-playbook.md
      plan: null
      review: null
    dependencies: ["0024", "0018", "0019", "0020"]
    tags: [playbook, roadmap, scientific-rigor, root-scope]
    notes: "This playbook treats the benchmark gate as a prerequisite and maps the remaining real-data, discovery, optimization, and release obligations."
  - id: "0032"
    title: "Advanced Method and Spectral Rigor Completion"
    summary: "Close the remaining real-data inference and spectral-analysis gaps required by the root authority documents, including advanced RM backends and PyQSOFit-backed decomposition."
    status: conceived
    priority: high
    release: "v0.3.0"
    files:
      spec: null
      plan: null
      review: null
    dependencies: ["0025", "0026", "0027", "0028"]
    tags: [rm, spectra, advanced-methods, real-data]
    notes: "This package is where pyPETaL, LITMUS, MICA2, EzTao, celerite2, and PyQSOFit move from declared scope into validated execution."
  - id: "0033"
    title: "Corpus Scale-Out and Discovery Hold-Out Freeze"
    summary: "Scale the benchmark and discovery corpora to the full root-scope manifests with explicit hold-out governance, strata, and provenance."
    status: conceived
    priority: high
    release: "v0.3.0"
    files:
      spec: null
      plan: null
      review: null
    dependencies: ["0006", "0007", "0008", "0009", "0025"]
    tags: [data, manifests, hold-out, discovery]
    notes: "This package freezes the broad silver population, the full gold set, and the discovery-pool manifests needed by later optimization and anomaly work."
  - id: "0034"
    title: "Benchmark-Governed Optimization and Agent Loop Completion"
    summary: "Implement the root-scope optimization layer with Ray Tune, Optuna, Ax, immutable benchmark guards, and auditable experiment outputs."
    status: conceived
    priority: high
    release: "v0.3.0"
    files:
      spec: null
      plan: null
      review: null
    dependencies: ["0018", "0032", "0033"]
    tags: [optimization, autoresearch, experiments, governance]
    notes: "This package upgrades the current optimization scaffold into the benchmark-driven experiment loop described by the authority plan."
  - id: "0035"
    title: "Discovery Hold-Out and CLAGN Scientific Analysis"
    summary: "Execute the root-scope discovery program on hold-out ZTF and CLAGN corpora with interpretable anomaly ranking, transition timelines, and candidate evidence bundles."
    status: conceived
    priority: high
    release: "v0.3.0"
    files:
      spec: null
      plan: null
      review: null
    dependencies: ["0019", "0032", "0033", "0034"]
    tags: [discovery, ztf, clagn, anomaly]
    notes: "This package closes the discovery claims gap with ranked catalogs, transition analyses, and follow-up prioritization backed by explicit evidence."
  - id: "0036"
    title: "Scientific Analyst Workbench and Discovery Review Surface"
    summary: "Extend the read-only review application into the analyst-facing workbench required for benchmark, discovery, and release-phase scientific review."
    status: conceived
    priority: medium
    release: "v0.3.0"
    files:
      spec: null
      plan: null
      review: null
    dependencies: ["0033", "0035"]
    tags: [review, web, discovery, analyst]
    notes: "The root program is not operationally complete until discovery and release outputs are inspectable through the tracked analysis surface."
  - id: "0037"
    title: "Public Release and Publication Closeout"
    summary: "Assemble the externally reviewable methods release, anomaly catalog, audio archive, and publication-facing artifacts required by the root authority plan."
    status: conceived
    priority: high
    release: "v1.0.0"
    files:
      spec: null
      plan: null
      review: null
    dependencies: ["0020", "0035", "0036"]
    tags: [release, catalog, publication, provenance]
    notes: "This package closes the root plan only after validated methods, discovery outputs, and review surfaces are integrated and provenance-complete."
```
## Authority Notes

- The root scientific plan and root agent spec remain the authority sources for scientific scope and decomposition decisions.
- All committed documentation must remain formal, concise, precise, and limited to essential content.
