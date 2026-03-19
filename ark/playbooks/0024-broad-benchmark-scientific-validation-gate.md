# 0024 Broad Benchmark Scientific Validation Gate

## Purpose

Define the staged gate from the bounded first benchmark package to broad scientific validation across AGN Watch, SDSS-RM, continuum-RM, and sonification-efficacy benchmarks.

## Why This Is A Playbook

This gate spans multiple remaining implementation slices rather than one code change. It requires dataset expansion, real backend execution, population-scale validation, benchmark governance, and blinded efficacy studies to converge before any broad scientific-validation claim is permitted.

## Current State

- The repository has executable readiness and review surfaces.
- The first benchmark package is scientifically bounded and explicit about evidence levels.
- Current evidence is limited to fixture-backed ingest checks and synthetic lag-recovery cases.
- The present validation metrics, leaderboards, memos, and efficacy tasks are structurally correct but not yet sufficient for broad benchmark claims.
- Model-based reverberation-method integrations are wrapper-level rather than demonstrated end-to-end benchmark executions.

## Gate Definition

Broad scientific validation is reached only when all of the following are true:

1. Gold-benchmark validation is demonstrated on a literature-rich AGN Watch object set with object-level diagnostic review.
2. Silver-benchmark validation is demonstrated on a large published-lag SDSS-RM benchmark set with population-scale metrics.
3. Continuum-RM benchmarking is demonstrated on literature-inspired or known-like ZTF benchmark objects with contamination and cadence-stability analysis.
4. Sonification efficacy is demonstrated against strong plot-only baselines on blinded benchmark tasks.
5. All validation claims are reproduced from tracked artifacts with frozen benchmark definitions, explicit provenance, and explicit limitations.

This gate is scoped to the declared benchmark program. It does not authorize claims about field deployment, full survey coverage, or discovery-pool performance beyond the benchmark slices and evidence levels materialized in tracked artifacts.

## Quantitative Gate Thresholds

- Gold package:
  - at least 2 gold objects
  - mean absolute lag error at or below 3.0 days across the package
  - 4 tracked methods executed for every gold object
  - rerun drift at or below 0.25 days on the declared primary metrics
- Silver package:
  - at least 4 silver objects
  - interval or posterior coverage at or above 0.75
  - null false-positive rate at or below 0.10
  - inter-method disagreement rate at or below 0.50
  - runtime recorded for every object and method record
- Continuum package:
  - at least 5 benchmark cases
  - contaminated-versus-clean classification accuracy at or above 0.75
  - cadence-stability score at or above 0.75
  - rerun classifications preserved within the declared tolerance
- Efficacy package:
  - audio-only accuracy at or above plot-only accuracy
  - combined-modality accuracy at or above plot-only accuracy
  - confidence-calibration error at or below 0.20
  - inter-rater agreement at or above 0.60
- Cross-package:
  - evidence level, scope, limitations, and non-demonstrated capability are present on every package
  - repeated reruns preserve package readiness and primary conclusions within declared tolerances

## Remaining Gaps

### G1. Benchmark Corpus Expansion

- Replace the current fixture-only gold and silver evidence with frozen benchmark manifests covering the full gold object set and a broad published-lag silver set.
- Define immutable benchmark splits, inclusion criteria, literature labels, and exclusion reasons.
- Record benchmark strata for line, cadence, redshift, signal-to-noise, contamination class, and known failure modes.

### G2. Real Method Execution

- Run PyCCF and pyZDCF on real benchmark light curves rather than only synthetic derived series.
- Complete end-to-end execution paths for JAVELIN and PyROA on benchmark objects with convergence diagnostics and failure capture.
- Add the next-tier comparison methods required by the authority plan when they become practical, especially pyPETaL and LITMUS.
- Materialize method-level posteriors, diagnostics, runtime metadata, and failure states in tracked artifacts.

### G3. Consensus and Null Calibration

- Benchmark consensus classification against real and null benchmark cases.
- Add shuffled-pair, misaligned-pair, and sparse-cadence null suites at benchmark scale.
- Calibrate agreement, alias, and false-positive thresholds against held benchmark outputs rather than heuristic constants alone.

### G4. Spectral and Line-Response Validation

- Execute multi-epoch spectral decomposition on the gold and silver benchmark sets.
- Emit line-fit diagnostics, calibration diagnostics, and line-response stability measures for benchmark objects.
- Compare recovered line metrics and qualitative response behavior against literature expectations on gold objects.

### G5. Gold Benchmark Validation

- Expand AGN Watch from the current bounded ingest checks to object-level validation on a literature-rich gold set.
- Required outputs:
  - lag comparison table versus literature
  - line-fit diagnostics
  - mapping-comparison memo
  - audio set with multiple mapping families
- NGC 5548 remains the first priority object, but the gate requires more than one canonical object.

### G6. Silver Benchmark Validation

- Expand from the current published-lag fixture subset to a broad SDSS-RM benchmark population.
- Required metrics:
  - lag recovery MAE and RMSE against literature
  - posterior or interval coverage
  - false-positive rate on null or shuffled pairs
  - disagreement rate between methods
  - runtime per object and pair
  - success by line, redshift, cadence, and quality regime
- Required artifacts:
  - benchmark leaderboard
  - literature comparison table
  - failure-mode summaries
  - object-level QC inventories

### G7. Continuum-RM Benchmarking

- Implement the disc-like, diffuse-continuum-contaminated, state-change, and failure-case suites at broader scale.
- Benchmark continuum-lag recovery on literature-inspired or known-like ZTF objects.
- Required metrics:
  - recovery of known-like lag hierarchies
  - thin-disc-like versus contaminated classification performance
  - cadence-degradation stability

### G8. Sonification Efficacy Validation

- Replace the current structural blinded-task scaffold with a real blinded benchmark program.
- Include plot-only, audio-only, and plot-plus-audio tasks.
- Benchmark against strong visual baselines, not against absence of review.
- Required metrics:
  - accuracy
  - time-to-decision
  - confidence calibration
  - inter-rater agreement
  - performance by training level
  - confusion matrix by anomaly type

### G9. Reproducibility and Claims Governance

- Freeze benchmark manifests, labels, and splits before broad validation reporting.
- Store reproducibility hashes, environment metadata, and rerun outcomes for every validation package.
- Require every published validation artifact to state scope, evidence level, limitations, and non-demonstrated capabilities directly.

### G10. Review Application Upgrade For Scientific Analysis

- Expand the review application from run-and-case inspection to benchmark-analysis workflows over gold, silver, continuum-RM, and efficacy packages.
- Add benchmark-package navigation by suite, object, line, method, mapping family, contamination class, cadence regime, and validation status.
- Add comparative views for method agreement, literature comparison, null-test outcomes, failure modes, and rerun stability.
- Add cohort tables and filtering for population-scale silver benchmark analysis, including regime breakdowns and sortable metric columns.
- Add object-level review pages that combine lag outputs, consensus status, line-fit diagnostics, benchmark notes, and linked audio artifacts.
- Add explicit claims-boundary panels that show demonstrated capability, limitations, non-demonstrated capability, and evidence level for each package and object.
- Add efficacy-review views for plot-only, audio-only, and plot-plus-audio outcomes, including confusion summaries and timing metrics.
- Preserve the read-only contract and ensure every displayed value is loaded from tracked artifact files rather than hidden process state.

## Required Validation Packages

The gate should be executed as the following sequence:

1. Gold benchmark execution package
2. Silver benchmark execution package
3. Continuum-RM benchmark execution package
4. Sonification efficacy execution package
5. Cross-package scientific review and claims audit

Each package should have its own numbered spec and implementation plan. None should claim to close the gate independently.

The review application should receive matching implementation slices alongside these packages so each package becomes inspectable through the same tracked analysis surface rather than through ad hoc local inspection.

## Required Tracked Artifacts

- Frozen benchmark manifests for gold, silver, and continuum-RM suites
- Method-level outputs, posteriors, diagnostics, and null-test results
- Gold and silver validation leaderboards
- Literature comparison tables
- Mapping-comparison memos
- Audio bundles with provenance and parameter manifests
- Efficacy task packages, responses, and scored summaries
- Cross-package claims dossier stating demonstrated capability, non-demonstrated capability, and residual risks
- Review-application indexes and object-level analysis views over the generated validation artifacts

## Review Application Requirements

The user-facing review surface must be sufficient for scientific analysis, not only for artifact presence checks.

Minimum required capabilities:

- run index covering readiness, first benchmark, gold, silver, continuum-RM, and efficacy packages
- package-level summaries with explicit scope, evidence level, warnings, and claims boundaries
- object-level drill-down for benchmark objects and task-level drill-down for efficacy studies
- sortable and filterable cohort tables for silver benchmark populations
- direct comparison views across methods, mapping families, and reruns
- direct links to literature comparison tables, diagnostics, audio artifacts, and null-test outputs
- visibility into failure cases, exclusions, and benchmark-strata membership

The gate is not satisfied if the validation artifacts exist but cannot be navigated, inspected, and compared efficiently through the tracked review interface.

## Minimum Acceptance Standard For The Gate

The broad scientific-validation gate is satisfied only if all of the following are present in tracked artifacts:

- More than one gold benchmark object is validated against literature expectations.
- A broad SDSS-RM published-lag benchmark population is evaluated with population metrics and regime breakdowns.
- Continuum-RM benchmark performance is measured on contamination and cadence-stability tasks.
- Sonification efficacy is benchmarked against plot-only baselines on blinded tasks.
- Repeated reruns preserve benchmark classifications and summary conclusions within predeclared tolerances.
- The quantitative thresholds in this playbook are satisfied and recorded by the claims audit.

## Non-Promotable Evidence

The following do not justify a broad scientific-validation claim on their own:

- readiness bundles
- fixture-backed ingest checks
- synthetic-only lag recovery
- wrapper-level support for model-based methods without benchmark execution
- unblinded audio demos
- leaderboard summaries without literature comparisons or null controls

## Exit Condition

After this gate is satisfied, the repository may describe the benchmark program as scientifically ready within the declared benchmark scope and broadly scientifically validated within that scope. Discovery and optimization claims remain downstream of that gate and must still treat the discovery pool as hold-out.
