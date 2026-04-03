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
    status: released
    summary: "Deliver benchmark data access, calibration, inference, sonification, simulation, and validation on known lag-bearing systems."
    projects: ["0006", "0007", "0008", "0009", "0010", "0011", "0012", "0013", "0014", "0015", "0016", "0017", "0021", "0022", "0023", "0024", "0025", "0026", "0027", "0028", "0029", "0030"]
    notes: "Benchmark validation and review surfaces are integrated on main and remain the gate for all later discovery claims."
  - version: "v0.3.0"
    name: "Discovery, Optimization, and Scale-Out"
    status: active
    summary: "Integrate the repository-local root-closeout surface beyond the benchmark gate: advanced rigor, corpus governance, optimization, discovery analysis, analyst review, and release packaging."
    projects: ["0018", "0019", "0031", "0032", "0033", "0034", "0035", "0036", "0038", "0039", "0040", "0041", "0042", "0043", "0046", "0047", "0048", "0049", "0050", "0051", "0052"]
    notes: "The root-closeout package surface is integrated on main. Current readiness, discovery, release, and first-pass review outputs remain repository-local and bounded by the evidence labels, limitations, hold-out rules, and any promoted discovery-snapshot freeze recorded in their generated packages."
  - version: "v1.0.0"
    name: "Open Science Release"
    status: planning
    summary: "Package methods, catalog outputs, and reproducible artifacts for external release after explicit review of the generated release bundle."
    projects: ["0020", "0037", "0044", "0045"]
    notes: "Repository-local release-closeout and audit bundles exist on main. External release status remains planning until the generated bundle is reviewed within its declared claims boundary."
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
    summary: "Record the root-scope package sequence that extends the benchmark gate into advanced rigor, corpus governance, optimization, discovery, review, and release."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/playbooks/0031-root-authority-closeout-playbook.md
      plan: null
      review: null
    dependencies: ["0024", "0018", "0019", "0020"]
    tags: [playbook, roadmap, scientific-rigor, root-scope]
    notes: "This playbook records the root-scope package sequence now integrated on main. Repository-local readiness remains bounded by generated package evidence labels and limitations."
  - id: "0032"
    title: "Advanced Method and Spectral Rigor Completion"
    summary: "Close the remaining real-data inference and spectral-analysis gaps required by the root authority documents, including advanced RM backends and PyQSOFit-backed decomposition."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0032-advanced-method-spectral-rigor-completion.md
      plan: ark/plans/0032-advanced-method-spectral-rigor-completion.md
      review: null
    dependencies: ["0025", "0026", "0027", "0028"]
    tags: [rm, spectra, advanced-methods, real-data]
    notes: "Implemented on main through the repository-local advanced_rigor package. Interpret outputs only through their recorded evidence labels, diagnostics, and limitations."
  - id: "0033"
    title: "Corpus Scale-Out and Discovery Hold-Out Freeze"
    summary: "Scale the benchmark and discovery corpora to the full root-scope manifests with explicit hold-out governance, strata, and provenance."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0033-corpus-scaleout-discovery-holdout-freeze.md
      plan: ark/plans/0033-corpus-scaleout-discovery-holdout-freeze.md
      review: null
    dependencies: ["0006", "0007", "0008", "0009", "0025"]
    tags: [data, manifests, hold-out, discovery]
    notes: "Implemented on main through the repository-local corpus_scaleout package. Discovery manifests remain hold-out governed and explicitly evidence-labeled."
  - id: "0034"
    title: "Benchmark-Governed Optimization and Agent Loop Completion"
    summary: "Implement the root-scope optimization layer with Ray Tune, Optuna, Ax, immutable benchmark guards, and auditable experiment outputs."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0034-benchmark-governed-optimization-agent-loop-completion.md
      plan: ark/plans/0034-benchmark-governed-optimization-agent-loop-completion.md
      review: null
    dependencies: ["0018", "0032", "0033"]
    tags: [optimization, autoresearch, experiments, governance]
    notes: "Implemented on main through the repository-local optimization_closeout package. Optimization remains benchmark-governed and may not tune on hold-out data."
  - id: "0035"
    title: "Discovery Hold-Out and CLAGN Scientific Analysis"
    summary: "Execute the root-scope discovery program on hold-out ZTF and CLAGN corpora with interpretable anomaly ranking, transition timelines, and candidate evidence bundles."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0035-discovery-holdout-clagn-scientific-analysis.md
      plan: ark/plans/0035-discovery-holdout-clagn-scientific-analysis.md
      review: null
    dependencies: ["0019", "0032", "0033", "0034"]
    tags: [discovery, ztf, clagn, anomaly]
    notes: "Implemented on main through the repository-local discovery_analysis package. Candidate bundles remain evidence-labeled and require manual review."
  - id: "0036"
    title: "Scientific Analyst Workbench and Discovery Review Surface"
    summary: "Extend the read-only review application into the analyst-facing workbench required for benchmark, discovery, and release-phase scientific review."
    status: committed
    priority: medium
    release: "v0.3.0"
    files:
      spec: ark/specs/0036-scientific-analyst-workbench-discovery-review-surface.md
      plan: ark/plans/0036-scientific-analyst-workbench-discovery-review-surface.md
      review: null
    dependencies: ["0033", "0035"]
    tags: [review, web, discovery, analyst]
    notes: "Implemented on main through the review surface and release-closeout routes. The interface exposes repository-local artifacts and does not broaden their claims boundary."
  - id: "0037"
    title: "Public Release and Publication Closeout"
    summary: "Assemble the externally reviewable methods release, anomaly catalog, audio archive, and publication-facing artifacts required by the root authority plan."
    status: committed
    priority: high
    release: "v1.0.0"
    files:
      spec: ark/specs/0037-public-release-publication-closeout.md
      plan: ark/plans/0037-public-release-publication-closeout.md
      review: null
    dependencies: ["0020", "0035", "0036"]
    tags: [release, catalog, publication, provenance]
    notes: "Implemented on main through the repository-local release_closeout package. External publication readiness still requires explicit review of generated content."
  - id: "0038"
    title: "Literal Root Authority Remediation Playbook"
    summary: "Preserve the adversarial claims-boundary rubric used to prevent repository-local readiness from being overstated as literal full-scope closure."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/playbooks/0038-literal-root-authority-remediation-playbook.md
      plan: null
      review: null
    dependencies: ["0031", "0032", "0033", "0034", "0035", "0036", "0037"]
    tags: [playbook, remediation, root-authority, scientific-rigor]
    notes: "This playbook is retained as the adversarial claims-boundary record for repository-local root-closeout outputs."
  - id: "0039"
    title: "Real Backend and Spectral Backend Integration"
    summary: "Integrate structured advanced-backend and spectral-fit execution surfaces for the repository-local advanced-rigor package."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0039-real-backend-spectral-backend-integration.md
      plan: ark/plans/0039-real-backend-spectral-backend-integration.md
      review: null
    dependencies: ["0038", "0011", "0013", "0032"]
    tags: [rm, spectra, backends, real-data]
    notes: "Implemented on main through the repository-local advanced_rigor package. Backend and spectral records remain bounded by their tracked diagnostics and limitations."
  - id: "0040"
    title: "Full Corpus Acquisition, Raw Preservation, and Freeze"
    summary: "Freeze the repository-local gold, silver, and discovery corpora with explicit hashes, inclusion criteria, release identifiers, and hold-out governance."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0040-full-corpus-acquisition-raw-preservation-freeze.md
      plan: ark/plans/0040-full-corpus-acquisition-raw-preservation-freeze.md
      review: null
    dependencies: ["0038", "0006", "0007", "0008", "0009", "0033"]
    tags: [data, manifests, provenance, freeze]
    notes: "Implemented on main through repository-local corpus manifests. Current discovery scope remains the tracked hold-out slice recorded in generated artifacts."
  - id: "0041"
    title: "Real-Data Benchmark Execution and Validation Closure"
    summary: "Materialize benchmark validation packages over the tracked benchmark corpus with explicit literature comparisons, null controls, reruns, and evidence boundaries."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0041-real-data-benchmark-execution-validation-closure.md
      plan: ark/plans/0041-real-data-benchmark-execution-validation-closure.md
      review: null
    dependencies: ["0038", "0039", "0040", "0012", "0017"]
    tags: [validation, benchmarks, real-data, response]
    notes: "Implemented on main through repository-local gold, silver, continuum, and advanced-rigor packages. Evidence labels remain binding on interpretation."
  - id: "0042"
    title: "Root Optimization Orchestration and Objective Completion"
    summary: "Materialize benchmark-governed optimization through Ray Tune, Optuna, and Ax within the repository-local optimization closeout package."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0042-root-optimization-orchestration-objective-completion.md
      plan: ark/plans/0042-root-optimization-orchestration-objective-completion.md
      review: null
    dependencies: ["0038", "0040", "0041", "0018", "0034"]
    tags: [optimization, ray, optuna, ax, objectives]
    notes: "Implemented on main through repository-local optimization_closeout materialization with Ray Tune, Optuna, and Ax. Hold-out boundaries remain binding."
  - id: "0043"
    title: "Hold-Out Discovery and CLAGN Real-Data Analysis"
    summary: "Materialize repository-local hold-out candidate bundles and CLAGN transition analyses from tracked discovery inputs with explicit evidence bundles."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0043-holdout-discovery-clagn-real-data-analysis.md
      plan: ark/plans/0043-holdout-discovery-clagn-real-data-analysis.md
      review: null
    dependencies: ["0038", "0040", "0041", "0042", "0019", "0035"]
    tags: [discovery, clagn, hold-out, anomaly]
    notes: "Implemented on main through repository-local discovery_analysis materialization. Candidate records remain bounded by their evidence bundles and limitations."
  - id: "0044"
    title: "Publication-Grade Release, Analyst Workbench, and Archive Assembly"
    summary: "Assemble repository-local release and analyst-review bundles from tracked benchmark, optimization, discovery, and audit artifacts."
    status: committed
    priority: high
    release: "v1.0.0"
    files:
      spec: ark/specs/0044-publication-grade-release-analyst-workbench-archive-assembly.md
      plan: ark/plans/0044-publication-grade-release-analyst-workbench-archive-assembly.md
      review: null
    dependencies: ["0038", "0041", "0042", "0043", "0020", "0036", "0037"]
    tags: [release, publication, review, archive]
    notes: "Implemented on main through repository-local release_closeout materialization and review routes. Presence of the bundle does not by itself mark external release readiness."
  - id: "0045"
    title: "Literal Root Authority Conformance Audit and Final Readiness Gate"
    summary: "Materialize the repository-local root-authority audit over the integrated closeout packages and preserve its claims boundary explicitly."
    status: committed
    priority: high
    release: "v1.0.0"
    files:
      spec: ark/specs/0045-literal-root-authority-conformance-audit-final-readiness-gate.md
      plan: ark/plans/0045-literal-root-authority-conformance-audit-final-readiness-gate.md
      review: null
    dependencies: ["0038", "0041", "0042", "0043", "0044"]
    tags: [audit, conformance, readiness, governance]
    notes: "Implemented on main through repository-local root_authority_audit materialization. The audit governs tracked-artifact readiness and preserves limitations and non-demonstrated capabilities."
  - id: "0046"
    title: "Adversarial Root Authority Gap-Closure Plan"
    summary: "Record the adversarial checks that must be applied whenever the codebase or documentation summarizes root-scope readiness."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/playbooks/0046-adversarial-root-authority-gap-closure-plan.md
      plan: ark/plans/0046-adversarial-root-authority-gap-closure-plan.md
      review: null
    dependencies: ["0038", "0039", "0040", "0041", "0042", "0043", "0044", "0045"]
    tags: [playbook, remediation, adversarial-review, root-authority]
    notes: "This playbook is retained as the adversarial checklist used to review overclaims against the repository-local root-closeout surface."
  - id: "0047"
    title: "Literal Root Authority Final Conformance Remediation"
    summary: "Preserve the final repository-local claims-boundary rules after the adversarial remediation sequence was integrated on main."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/playbooks/0047-literal-root-authority-final-conformance-remediation.md
      plan: ark/plans/0047-literal-root-authority-final-conformance-remediation.md
      review: null
    dependencies: ["0046", "0039", "0040", "0041", "0042", "0043", "0044", "0045"]
    tags: [playbook, remediation, adversarial-review, root-authority, conformance]
    notes: "This remediation record is retained for final claims-boundary review. It no longer serves as a branch-only status note."
  - id: "0048"
    title: "Benchmark-Governed First-Pass Review"
    summary: "Materialize a repository-local first-pass review package that defines benchmark anchors, candidate waves, and bounded dispositions for the current hold-out pool."
    status: committed
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0048-benchmark-governed-first-pass-review.md
      plan: ark/plans/0048-benchmark-governed-first-pass-review.md
      review: ark/playbooks/0048-benchmark-governed-first-pass-review.md
    dependencies: ["0026", "0027", "0028", "0029", "0043", "0045"]
    tags: [analysis, discovery, governance, review, hold-out]
    notes: "Implemented through repository-local first_pass_review materialization. The package preserves the fixture-bounded claims boundary and the requirement for real-data reruns."
  - id: "0049"
    title: "Canonical Discovery Snapshot Promotion and Freeze"
    summary: "Freeze and promote one repository-local discovery-analysis snapshot as the canonical input for first-pass review and downstream scientific interpretation."
    status: active
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0049-canonical-discovery-snapshot-promotion-freeze.md
      plan: ark/plans/0049-canonical-discovery-snapshot-promotion-freeze.md
      review: ark/playbooks/0049-canonical-discovery-snapshot-promotion-freeze.md
    dependencies: ["0040", "0043", "0045", "0048"]
    tags: [discovery, governance, provenance, freeze, analysis]
    notes: "This package closes the artifact-root ambiguity exposed by the first pass by requiring one promoted canonical discovery snapshot before downstream scientific interpretation is reused."
  - id: "0050"
    title: "Discovery Transition-Window Alignment and Eligibility"
    summary: "Repair repository-local discovery alignment so CLAGN transition evidence is anchored to one deterministic adjacent state pair with complete photometric support."
    status: active
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0050-discovery-transition-window-alignment-and-eligibility.md
      plan: ark/plans/0050-discovery-transition-window-alignment-and-eligibility.md
      review: ark/playbooks/0050-discovery-transition-window-alignment-and-eligibility.md
    dependencies: ["0019", "0035", "0043", "0048", "0049"]
    tags: [discovery, alignment, clagn, hold-out, provenance]
    notes: "This package closes the state-alignment gap exposed by the canonical first pass by replacing first-state and last-state midpoint selection with deterministic adjacent-pair eligibility."
  - id: "0051"
    title: "Transition-Supported First-Pass Governance Correction"
    summary: "Correct repository-local first-pass review so primary-wave admission follows repaired transition-support evidence rather than direction-specific hold-out heuristics."
    status: active
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0051-transition-supported-first-pass-governance-correction.md
      plan: ark/plans/0051-transition-supported-first-pass-governance-correction.md
      review: ark/playbooks/0051-transition-supported-first-pass-governance-correction.md
    dependencies: ["0035", "0043", "0048", "0049", "0050"]
    tags: [governance, discovery, review, clagn, scientific-rigor]
    notes: "This package narrows first-pass wave assignment to the repaired transition-support contract while preserving repository-local scope, manual review, and real-data-rerun requirements."
  - id: "0052"
    title: "Reviewed Primary-Wave Real-Data Rerun Package"
    summary: "Materialize a repository-local rerun package for manually advanced primary-wave candidates with explicit baseline-versus-rerun comparisons."
    status: active
    priority: high
    release: "v0.3.0"
    files:
      spec: ark/specs/0052-reviewed-primary-wave-real-data-rerun-package.md
      plan: ark/plans/0052-reviewed-primary-wave-real-data-rerun-package.md
      review: ark/playbooks/0052-reviewed-primary-wave-real-data-rerun-package.md
    dependencies: ["0035", "0043", "0048", "0049", "0050", "0051"]
    tags: [rerun, discovery, review, provenance, scientific-rigor]
    notes: "This package freezes the reviewed rerun shortlist and compares rerun candidate bundles back to the promoted snapshot without weakening the repository-local claims boundary."
```
## Authority Notes

- The root scientific plan and root agent spec remain the authority sources for scientific scope and decomposition decisions.
- All committed documentation must remain formal, concise, precise, and limited to essential content.
