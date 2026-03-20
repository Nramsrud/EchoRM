# 0046 Adversarial Root Authority Gap-Closure Plan

## Goal

Execute one final remediation pass that closes every remaining adversarial finding and leaves the repository in a state of literal root-authority compliance.

## Governing Rule

Completion is allowed only when the implementation, deliverables, benchmarks, and final readiness gate satisfy the root project plan and root agent specification without proxy, placeholder, or count-only substitutions.

## Scope

This plan governs the final execution of `0039` through `0045`. It is the controlling implementation plan for the last required pass to root-authority closure.

## Workstreams

### W1. Raw Data and Corpus Closure

Packages:
- `0040`

Objective:
- replace partial and subset corpus compliance with literal raw-preservation and freeze compliance for AGN Watch, SDSS-RM, and ZTF

Required implementation:
1. Preserve AGN Watch raw files exactly as downloaded, including comments, units, and parser-family metadata.
2. Acquire SDSS-RM source products at the raw layer, preserve raw spectral and tabular products, and generate normalized derivatives in parallel.
3. Acquire ZTF raw light-curve products and query-response records with explicit release identifiers, query provenance, masks, and crossmatch keys.
4. Materialize freeze manifests for gold, silver, and discovery tiers with inclusion criteria, exclusion reasons, strata counts, release versions, and raw hashes.
5. Extend the audit surface so SDSS-RM and ZTF raw preservation are checked alongside AGN Watch.

Acceptance criteria:
- raw-preservation manifests exist for AGN Watch, SDSS-RM, and ZTF
- normalized derivative manifests point back to raw hashes one-to-one
- freeze manifests record literal scope, exclusions, and release provenance
- no root-closeout artifact depends on fixture-slice corpus evidence

### W2. Spectral and Backend Closure

Packages:
- `0039`
- `0041`

Objective:
- replace synthetic spectral evidence and partial backend closure with literal real-data backend and spectral execution

Required implementation:
1. Execute `pyPETaL`, `LITMUS`, `MICA2`, `EzTao`, `celerite2`, and `PyQSOFit` on real tracked data products rather than on synthetic or proxy substitutes.
2. Materialize real spectral-epoch records for gold and silver objects where coverage exists.
3. Preserve observed-frame and rest-frame products, calibration state, continuum variants, and real line-metric tables.
4. Remove any spectral diagnostic path that fabricates synthetic benchmark spectra for root-authority evidence.
5. Add failure reporting that remains visible but does not count toward completion.

Acceptance criteria:
- real spectral epochs are present where the root plan requires them
- `PyQSOFit` and alternative continuum variants operate on real spectra
- advanced RM backend outputs record literal execution evidence on real tracked corpora
- root-closeout spectral outputs no longer depend on synthetic placeholder spectra

### W3. Real Benchmark and Sonification Closure

Packages:
- `0041`

Objective:
- close the benchmark program on real measured continuum and line-response series and materialize literal sonification outputs

Required implementation:
1. Run benchmark execution on real measured continuum and response series across gold and silver scope.
2. Expand null controls to the literal root benchmark set, including shuffled, reversed, misaligned, sparse, contaminated, state-change, and low-SNR variants.
3. Generate the required benchmark-facing artifacts: AGN Watch memo, SDSS-RM leaderboard, literature comparison tables, and mapping ablations.
4. Replace placeholder audio rendering with real science WAVs, presentation audio, stems, synchronized figure or movie outputs, mapping legends, and provenance-linked configs.
5. Benchmark the required uncertainty encodings across the declared mapping families.

Acceptance criteria:
- gold and silver benchmark outputs use real measured continuum and response series
- benchmark dossiers include the required literature-facing deliverables
- sonification outputs are non-placeholder and provenance-complete
- required mapping families and uncertainty encodings are benchmarked explicitly

### W4. Optimization Closure

Packages:
- `0042`

Objective:
- implement the literal root optimization program and remove toy-search behavior

Required implementation:
1. Define real mutable search spaces over mapping and analysis parameters rather than fixed hand-authored candidate lists.
2. Implement the full root objective package, including lag MAE, interval coverage, null false-positive rate, held-out anomaly precision or AUC, audio-task discriminability, runtime, and interpretability penalties.
3. Run `Ray Tune`, `Optuna`, and `Ax` as actual orchestrators over those search spaces.
4. Materialize Pareto-front outputs, experiment dashboards, keep-discard decisions, mutation guards, and benchmark protections.
5. Prove that discovery hold-out evidence remains isolated from optimization targets.

Acceptance criteria:
- all three optimizer backends run over real search spaces
- all root objectives are materialized explicitly in tracked experiment outputs
- Pareto-front artifacts exist and are reviewable
- mutation guards and hold-out protections are auditable

### W5. Discovery and CLAGN Closure

Packages:
- `0043`

Objective:
- replace catalog-row and proxy discovery evidence with validated hold-out scientific analysis

Required implementation:
1. Run discovery on frozen real hold-out light-curve and spectral evidence.
2. Generate continuum-lag outlier outputs, line-response anomaly outputs, CLAGN transition timelines, and precursor analyses.
3. Produce ranked anomaly catalogs, candidate precursor catalogs, top-candidate audio galleries, and follow-up memos grounded in validated real-data outputs.
4. Preserve explicit separation between benchmark-calibrated parameters and untouched hold-out evidence.

Acceptance criteria:
- ranked discovery outputs are derived from validated hold-out pipeline products
- CLAGN transition artifacts include explicit temporal alignment and evidence surfaces
- discovery deliverables include the literal root outputs rather than proxy summaries

### W6. Publication, Archive, and Workbench Closure

Packages:
- `0044`

Objective:
- assemble the literal root-plan release and review outputs

Required implementation:
1. Materialize benchmark leaderboard, anomaly catalog, CLAGN transition catalog, sonification-mapping leaderboard, and literature comparison table.
2. Produce publication-grade methods and catalog artifact bundles with figures, case-study surfaces, and supporting tables.
3. Assemble benchmark and audio archives with provenance-complete manifests and inventories.
4. Extend the analyst workbench to support benchmark, optimization, discovery, release, and final-audit inspection.
5. Ensure per-object release bundles include cleaned photometry, line metrics, lag comparison, audio assets, synchronized figure or movie, mapping legend, config, and memo.

Acceptance criteria:
- all catalog-level outputs required by the root plan exist in tracked form
- publication bundles are content-complete rather than placeholder markdown
- benchmark and audio archives are inventory-complete and provenance-complete
- analyst workbench exposes the literal release evidence directly

### W7. Final Conformance Audit

Packages:
- `0045`

Objective:
- make the final root-authority gate content-based, literal, and adversarially robust

Required implementation:
1. Build a requirement matrix that maps root-authority clauses to concrete checks.
2. Replace count-only conditions with content inspections over datasets, outputs, and evidence labels.
3. Add explicit fail conditions for:
   - missing SDSS-RM or ZTF raw preservation
   - synthetic spectral evidence used as root-closeout evidence
   - placeholder or silent audio outputs
   - toy optimization surfaces
   - missing catalog-level outputs or publication bundles
   - discovery evidence derived from proxy or authored scores
4. Surface the final gate in the workflow, release bundle, and analyst workbench.

Acceptance criteria:
- every audit clause maps back to a root-authority requirement
- the audit fails on every ambiguity class listed in `0046`
- readiness is promoted only when literal evidence passes

## Sequencing

1. Complete `W1` before promoting any new corpus or raw-data compliance claim.
2. Complete `W2` before promoting any spectral-rigor or advanced-backend claim.
3. Complete `W3` before promoting any root-scope benchmark or sonification claim.
4. Complete `W4` before promoting any benchmark-governed optimization claim.
5. Complete `W5` before promoting any discovery or CLAGN scientific claim.
6. Complete `W6` before promoting any release or publication readiness claim.
7. Run `W7` only after `W1` through `W6` have materialized their tracked evidence.

## Verification

Repository gates:
- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`
- `snakemake --snakefile workflows/Snakefile --dry-run`

Remediation checkpoints:
1. Corpus freeze verification over AGN Watch, SDSS-RM, and ZTF raw-preservation records
2. Spectral verification over real spectral epochs and real `PyQSOFit` products
3. Benchmark verification over real measured continuum and response series
4. Sonification verification over real rendered audio assets and bundle completeness
5. Optimization verification over literal objectives and Pareto outputs
6. Discovery verification over validated hold-out outputs and CLAGN transition products
7. Release verification over catalogs, archives, publication bundles, and analyst workbench routes
8. Final conformance verification through `0045`

## Exit Criteria

This remediation pass is complete only when all of the following are true:

- `0039` through `0045` satisfy the tightened obligations from [0046](/home/echorm/Developer/EchoRM/ark/playbooks/0046-adversarial-root-authority-gap-closure-plan.md)
- all repository quality gates pass
- all benchmark and release deliverables required by the root authority documents exist in tracked form
- the final `0045` gate passes on literal evidence
- no remaining readiness statement depends on proxy, placeholder, synthetic stand-in, or count-only evidence

## Dependencies

- `0039`
- `0040`
- `0041`
- `0042`
- `0043`
- `0044`
- `0045`
