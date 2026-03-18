
# Project Plan: AGN/Quasar Reverberation Sonification with Continuum + Line + Uncertainty Encoding
Version 1.0  
Prepared: 2026-03-16  
Target audience: research lead + AI coding / analysis agents

## 0. Purpose

Build a rigorously validated research codebase that uses **uncertainty-aware sonification** as a first-class analysis tool for **AGN/quasar reverberation mapping (RM)** and **changing-look AGN (CLAGN)** discovery. The project should start from well-studied, benchmarkable data where lags and spectral responses are already known, and only then move into an anomaly/discovery program.

This plan is intentionally optimized for an AI research/coding agent: it gives the scientific background, the datasets, the software stack, the code architecture, the evaluation metrics, the experiment loops, and the discovery strategy needed to become effective quickly.

---

## 1. Executive summary

### 1.1 Core thesis

Astronomy sonification is mature enough to support real analysis in 1D time series and spectra, but has not yet produced a **validated, uncertainty-aware pipeline for AGN continuum + emission-line reverberation**. The combination is unusually promising because RM is fundamentally about **correlated delays, echoes, line breathing, changing line profiles, and state transitions**—exactly the kinds of patterns the auditory system can detect well when the mappings are designed carefully. The astronomy sonification review by Zanella et al. identified nearly 100 sound-based astronomy projects and explicitly framed scientific discovery as one of the main motivations, but also emphasized current limitations and the need for more rigorous methods and broader adoption [R1]. Controlled testing with `astronify` showed that even simple sonification can help users identify high-SNR signals, but that training and improved mappings are required for subtler cases [R2, R3]. Trayford et al. then showed that listeners could recover physically meaningful information from galaxy spectral audifications, and argued that these methods can extend to datacubes [R5].

### 1.2 Why AGN/quasar reverberation is the right first target

Reverberation mapping is already defined around delayed response: continuum variations drive delayed broad-line and continuum reprocessing signals. RM is used across the AGN structure hierarchy, from the X-ray corona and accretion disc to the broad-line region (BLR) and dusty torus [R14]. SDSS-V/BHM RM is explicitly targeting a representative sample of **>1000 quasars** with optical broad-line coverage and lags expected from **days to years** [R7, R9]. The predecessor SDSS-RM data set already provides **11 years of photometric and 7 years of spectroscopic light curves for 849 broad-line quasars**, with published Hα/Hβ/Mg II/C IV lags [R8]. AGN Watch remains a gold-standard historical archive with public light curves and spectra [R6]. ZTF now provides public light curves through **DR24 (March 2018–October 2025)** and programmatic access through IRSA APIs and Parquet bulk products [R10, R11, R12].

### 1.3 Scientific opening

Continuum RM remains scientifically unsettled. Large ZTF-based analyses found that continuum-emission sizes inferred from inter-band lags are often larger than standard thin-disc predictions and can plausibly include a significant diffuse BLR continuum contribution [R15]. Lawther et al. showed that diffuse continuum contamination can elevate inter-band delays across the UV–optical regime and argued there may be no clean “disc-dominated” intervals in their NGC 5548 models [R16]. AGN STORM 2 for Mrk 817 similarly found that diffuse continuum plus broad-line emission can explain observed continuum lags, while direct X-ray illumination contributes only a small fraction [R17]. That means there is room for a method that is specifically designed to expose **echo structure, contamination, and regime changes**.

### 1.4 Research program in one sentence

Build a reproducible Python research platform that:
1. ingests and harmonizes AGN Watch, SDSS-RM / SDSS-V RM, and ZTF data,
2. fits continuum and line variability with multiple lag-inference methods,
3. converts continuum, line, and uncertainty structure into consistent sonifications,
4. validates those sonifications against known lags and synthetic benchmarks,
5. uses AI-driven experiment loops to optimize mappings and anomaly scoring, and
6. extends to CLAGN to search for **lag-state changes, decoupled line responses, and pre-transition signatures**.

### 1.5 What counts as success

Success should be staged:

- **Methods success**: the pipeline recovers known lags and uncertainty structure on AGN Watch / SDSS-RM, and sonification helps identify injected anomalies or known anomalous objects faster or more reliably than strong non-audio baselines.
- **Catalog success**: produce a ranked list of objects with statistically and aurally unusual lag/response behavior.
- **Science success**: identify at least one robust, interpretable subpopulation or object-level anomaly worth follow-up (e.g., state-dependent lag shifts, line-specific decoupling, diffuse-continuum-dominated cases, or CLAGN precursors).
- **Open-science success**: release code, benchmark datasets, mapping definitions, audio artifacts, and reproducible workflows.

---

## 2. Scientific background the agent must master

### 2.1 Sonification state of the art

The agent should understand the current astronomy sonification landscape before designing anything new:

- Zanella et al. review the field and identify nearly 100 astronomy sound projects, spanning research, education, public engagement, and accessibility; they also emphasize limitations and future directions [R1].
- Brown et al. provide the best direct evidence that astronomy sonification needs **efficacy testing**, not just aesthetics. Their controlled tests with `astronify` show that listeners can identify high-SNR signals with simple sonifications, but medium-SNR cases need better mappings and/or training [R2].
- `astronify` is useful as a baseline 1D sonification tool and also provides a light-curve simulator for synthetic data [R3].
- `STRAUSS` is a better foundation for the project’s custom sonification engine because it explicitly supports richer parameter mapping, flexible control, and even a spectral-audification example [R4].
- Trayford et al. show that spectral audification can preserve real physical information in galaxy spectra and argue that the same ideas can be extended to spatially resolved datacubes [R5].

**Implication for this project:** do not treat sonification as presentation. Treat it as a tunable representation whose usefulness must be validated quantitatively.

### 2.2 AGN/quasar reverberation background

The agent should internalize the RM problem structure:

- RM measures delayed responses of broad lines and reprocessed continuum relative to a variable continuum driver [R7, R14, R21].
- SDSS-V/BHM RM seeks representative, flux-limited quasar samples with Hα/Hβ, Mg II, and C IV coverage and days-to-years lag sensitivity [R7, R9].
- SDSS-RM already gives a large benchmark set of quasars with long photometric and spectroscopic baselines and published lag measurements [R8].
- Cross-correlation methods remain standard, but model-based approaches can better handle irregular sampling, correlated errors, and seasonal gaps [R21, R22, R23, R24, R25, R26].

### 2.3 Continuum RM and why it is scientifically interesting

The agent must understand that continuum lags are not simply “measure and fit a thin disc”:

- Reviews emphasize that continuum RM often finds wavelength-dependent lags larger than standard expectations and that this “accretion disc size problem” remains open [R14].
- The ZTF study by Guo et al. found significant inter-band lags in 94 type 1 AGN and inferred continuum-emission sizes larger than standard thin-disc predictions, with evidence for diffuse BLR continuum contamination [R15].
- Lawther et al. modeled diffuse continuum in NGC 5548 and argued it can contaminate the measured lag signal across the UV/optical, with no clean disc-dominated intervals in their models [R16].
- AGN STORM 2 on Mrk 817 again found that diffuse continuum plus broad lines can dominate the observed continuum delays [R17].

**Implication:** a good sonification system should be able to make it easy to hear when inter-band lags look like a clean monotonic disc sequence versus when they look contaminated, multi-component, or state-dependent.

### 2.4 Changing-look AGN (CLAGN) extension

The CLAGN extension is not a separate project; it is the high-value anomaly program built on the validated RM platform:

- Wang et al. (2025) found that CLAGNs in ZTF occupy a distinct variability regime and may represent a “critical state” where moderate accretion-rate fluctuations temporarily change spectral appearance rather than a simple Type 1 ↔ Type 2 switch [R18].
- DESI DR1 + SDSS DR16 CLAGN work compiled a large statistical catalog of **561 CL-AGNs**, confirmed a critical Eddington ratio around **~0.01**, found strong BEL–continuum change correlations, and identified peculiar long-decline states [R19].
- Komossa et al.’s review of AGN extremes is important because it broadens the anomaly taxonomy beyond CLAGN to include “frozen-look” behavior, deep fades, outbursts, semi-periodicity, and other extremes [R20].

**Implication:** the anomaly taxonomy should include not only classical turn-on/turn-off CLAGN, but also decoupled or frozen-response systems, slow declines, repeated state changes, and line-specific anomalies.

---

## 3. Project goals and hypotheses

### 3.1 Primary goals

**G1.** Build a rigorously tested research codebase for AGN/quasar sonification with explicit continuum, line, and uncertainty encoding.

**G2.** Validate the pipeline on AGN Watch and SDSS-RM using known lag-bearing systems and literature benchmarks.

**G3.** Build a scalable ZTF-assisted continuum-RM and anomaly-discovery layer.

**G4.** Extend the pipeline to CLAGN and adjacent AGN extremes.

**G5.** Use an AI-driven experiment loop to search mapping/model space more broadly than a human would typically attempt.

### 3.2 Hypotheses

**H1.** A well-designed sonification of multi-band continuum + line response + uncertainty will improve detection of injected RM anomalies relative to visual-only inspection baselines.

**H2.** Objects with substantial diffuse BLR continuum contamination will occupy identifiable clusters in either audio-embedding space or human/auditory ranking space.

**H3.** Some CLAGN or pre-CLAGN objects will show **state-dependent lag hierarchies or line-response changes** before or during spectral transitions.

**H4.** Multi-method consensus (PyCCF + pyZDCF + JAVELIN + PyROA + LITMUS + optional MICA2) will reduce false positives and make the anomaly catalog scientifically robust [R21, R22, R23, R24, R25, R26, R27].

**H5.** An “autoresearch”-style experiment loop with fixed benchmarks and multi-objective optimization can accelerate discovery of better sonification mappings and lag-analysis configurations [R33, R34, R35, R36, R37, R38, R39].

---

## 4. Scope and non-goals

### 4.1 In scope

- Optical / UV / IR AGN continuum and broad-line RM
- Public light curves and spectra from AGN Watch, SDSS-RM / SDSS-V RM, and ZTF
- Optional NEOWISE mid-IR extension for CLAGN follow-up [R46, R47]
- Validation on synthetic and literature-backed benchmark objects
- Sonification for discovery, not just outreach
- AI-assisted experiment design, code generation, hyperparameter search, and anomaly ranking

### 4.2 Out of scope in v1

- Full X-ray RM or torus RM as a core track
- A claim that sound alone is superior to standard RM methods
- Real-time telescope operations
- Generative music or aesthetic optimization as a primary goal
- Large-scale LSST integration in v1 (but the architecture should make this possible later)

---

## 5. Data strategy

## 5.1 Dataset tiers

Use a strict three-tier model:

### Tier A — Gold benchmark (small, interpretable, literature-rich)
Purpose: validation and debugging  
Primary source: **AGN Watch** [R6]

Characteristics:
- canonical nearby AGN with public light curves and spectra
- dense historical campaigns
- strong literature context
- ideal for hand-inspected, object-level validation

Recommended first objects:
- NGC 5548
- other AGN Watch targets with strong optical/UV campaigns

### Tier B — Silver benchmark (large, published lags, scalable)
Purpose: method comparison and automated evaluation  
Primary source: **SDSS-RM final data set** [R8]

Characteristics:
- 849 broad-line quasars
- long photometric + spectroscopic baselines
- published lag catalogs for Hα/Hβ/Mg II/C IV
- ideal for large-scale benchmark tables and failure-mode analysis

### Tier C — Discovery / anomaly pool
Purpose: scalable search and CLAGN extension  
Primary sources: **ZTF public data + literature / catalog CLAGN labels**, optionally NEOWISE and DESI/SDSS spectral labels [R10, R11, R12, R18, R19, R46, R47]

Characteristics:
- huge scale
- noisier and more heterogeneous
- less complete spectroscopic coverage
- ideal for anomaly ranking, preselection, and CLAGN follow-up

---

## 6. Data sources, access paths, and intended use

### 6.1 AGN Watch
Source: [R6]

Use:
- gold-standard validation
- debugging of line/continuum alignment
- testing diffuse-continuum and line-breathing representations

Acquisition:
- direct download from the AGN Watch website
- store raw files exactly as downloaded
- create object manifests with bibliographic metadata

Implementation notes:
- because AGN Watch is old and heterogeneous, write bespoke parsers per file format family
- preserve original metadata, comments, and units
- record any inferred metadata separately

### 6.2 SDSS-RM / SDSS-V RM
Sources: [R7, R8, R9, R13]

Use:
- main benchmark for lag recovery and line-response analysis
- core spectroscopic RM platform
- population-scale anomaly mining

Acquisition:
- use official published data products where available [R8]
- use `astroquery.sdss` and/or SDSS programmatic access for spectra and metadata [R13]
- maintain both raw FITS and normalized tabular derivative products

Implementation notes:
- separate “spectral-epoch data” from “derived line metrics”
- record redshift, line coverage, signal-to-noise, cadence statistics, and literature lag labels
- create a stable object-level manifest with source IDs, aliases, and line availability

### 6.3 ZTF
Sources: [R10, R11, R12]

Use:
- continuum-lag estimation
- long-baseline variability characterization
- CLAGN discovery and follow-up
- low-cost broad search over anomaly classes

Acquisition:
- use IRSA Lightcurve API for small/medium retrieval jobs [R12]
- use Parquet bulk downloads or cloud access for large sweeps [R11]
- keep release versions explicit (e.g., DR24) and hashed in manifests [R10]

Implementation notes:
- preserve ZTF object IDs and crossmatch keys
- cache query URLs and responses
- store raw IRSA tables and a normalized parquet format
- keep bad-catflags masks and query constraints explicit

### 6.4 Optional NEOWISE extension
Sources: [R46, R47]

Use:
- mid-IR follow-up in CLAGN or long-timescale response cases
- independent slow-echo channel for anomaly interpretation

Acquisition:
- use IRSA Time Series / catalog services [R47]
- for scale, use bulk parquet/catalog products [R47]
- record the six-month cadence structure and multi-epoch grouping [R46]

Implementation notes:
- do not include in v1 validation metrics
- use only after optical pipeline is stable

---

## 7. Research software stack

The stack should privilege **reproducibility, modularity, benchmarkability, and agent-friendliness**.

### 7.1 Core Python stack

Required:
- Python 3.11+
- `numpy`, `scipy`, `pandas` or `polars`
- `astropy`, `astroquery`
- `matplotlib`
- `pyarrow` / parquet
- `pytest`

### 7.2 RM and time-series packages

Use these as explicit wrappers rather than re-implementations:

- `PyCCF` for ICCF + FR/RSS uncertainty estimation [R22]
- `pyZDCF` for robust cross-correlation on sparse, unevenly sampled data [R23]
- `JAVELIN` for DRW-based direct lag fitting [R21]
- `PyROA` for simultaneous running-optimal-average modeling with MCMC uncertainties [R24]
- `pyPETaL` as an orchestration benchmark because it already combines PyCCF, pyZDCF, JAVELIN, PyROA, outlier rejection, detrending, and alias-mitigation weights [R25]
- `LITMUS` as the modern differentiable Bayesian lag framework and likely top-tier method for later-stage validation [R26]
- `MICA2` for transfer-function modeling and virtual RM cases [R27]
- `EzTao` for DRW/CARMA simulation and fitting [R28]
- `celerite2` for scalable 1D Gaussian-process regression with JAX/PyMC interfaces [R30]
- `astropy.timeseries.LombScargle` for unevenly sampled periodicity diagnostics and false-alarm checks [R31]

### 7.3 Spectral analysis

- `PyQSOFit` as the main quasar spectral fitting backend for continuum, Fe II, line decomposition, and uncertainty estimation [R29]

Implementation note:
- do not trust a single spectral decomposition. Record decomposition choices and fit variants as first-class metadata.

### 7.4 Sonification stack

- `STRAUSS` as the primary custom sonification engine [R4]
- `astronify` as a baseline/reference implementation and for synthetic-light-curve generation [R2, R3]
- lightweight audio utilities (`soundfile`, `scipy.signal`, `ffmpeg`) for rendering, normalization, and export

### 7.5 Workflow / reproducibility stack

- `Snakemake` for reproducible and scalable workflows [R42]
- `Hydra` for hierarchical config composition and multi-run sweeps [R43]
- `MLflow` for experiment tracking and artifact logging [R40]
- `DVC` for data + experiment versioning without polluting Git history [R41]

### 7.6 Optimization / autoresearch stack

- Karpathy-style `autoresearch` as the conceptual template: fixed benchmark, one editable code locus, short comparable experiments, keep/discard loop [R33]
- `Ray Tune` for scalable experiment execution and schedulers like PBT/ASHA, plus integrations with Ax and Optuna [R38]
- `Optuna` for multi-objective search [R37]
- `Ax` for Bayesian optimization of expensive objectives [R39]
- `DSPy` for declarative AI program composition [R34]
- `MIPROv2` when optimizing prompts/instructions/examples for agent behaviors [R35]
- `TextGrad` for feedback-driven optimization of compound AI systems [R36]

---

## 8. Repository architecture

Use a single monorepo with clean boundaries.

```text
agn-rm-sonify/
  README.md
  pyproject.toml
  environment/
    conda-lock.yml
    docker/
  configs/
    hydra/
    datasets/
    sonification/
    rm_methods/
    experiments/
  data/
    raw/
    interim/
    processed/
    external/
  manifests/
    objects.parquet
    datasets.yaml
  workflows/
    Snakefile
    rules/
  src/agnsonify/
    ingest/
    crossmatch/
    calibrate/
    spectra/
    photometry/
    rm/
    simulate/
    sonify/
    embeddings/
    anomaly/
    eval/
    reports/
    cli/
  tests/
    unit/
    integration/
    regression/
  notebooks/
    validation/
    exploratory/
  agents/
    program.md
    roles/
    prompts/
    evals/
  docs/
    project_plan/
    API/
    references/
```

### 8.1 Module responsibilities

**`ingest/`**  
Raw readers for AGN Watch, SDSS(-RM), ZTF, optional NEOWISE.

**`crossmatch/`**  
Object identity management, aliases, coordinate reconciliation, survey-to-survey joins.

**`calibrate/`**  
Flux/magnitude normalization, time standardization, spectral recalibration, masking.

**`spectra/`**  
Rest-frame conversion, continuum subtraction, line-window extraction, PyQSOFit wrappers, multi-epoch line metrics.

**`photometry/`**  
Light-curve cleaning, cadence summaries, detrending, outlier masking, interpolation prep.

**`rm/`**  
Wrappers and harmonized outputs for PyCCF, pyZDCF, JAVELIN, PyROA, LITMUS, MICA2.

**`simulate/`**  
Synthetic continuum + transfer-function + contamination + survey cadence generators.

**`sonify/`**  
All audio mappings and renderers.

**`embeddings/`**  
Feature extraction from audio and non-audio representations.

**`anomaly/`**  
Ranking, clustering, prioritization, catalog production.

**`eval/`**  
Metric definitions, synthetic benchmark scoring, ablations, calibration diagnostics.

**`reports/`**  
Tables, plots, HTML dashboards, audio galleries, paper figures.

**`cli/`**  
Reproducible command-line entry points for every stage.

---

## 9. Canonical data model

The most important architectural decision is to standardize *all* data into a small number of canonical schemas.

### 9.1 Object manifest

`objects.parquet`

Columns:
- `object_uid`
- `canonical_name`
- `ra_deg`, `dec_deg`
- `redshift`
- `survey_ids` (JSON)
- `line_coverage` (JSON)
- `is_clagn_label`
- `tier` (`gold` / `silver` / `discovery`)
- `literature_refs`
- `notes`

### 9.2 Photometry schema

`photometry.parquet`

Columns:
- `object_uid`
- `survey`
- `band`
- `mjd_obs`
- `mjd_rest`
- `flux`
- `flux_err`
- `mag`
- `mag_err`
- `flux_unit`
- `quality_flag`
- `is_upper_limit`
- `source_release`
- `raw_row_hash`

### 9.3 Spectral epoch schema

`spectra_index.parquet` plus raw FITS

Columns:
- `object_uid`
- `epoch_uid`
- `survey`
- `mjd_obs`
- `mjd_rest`
- `z`
- `spec_path`
- `wave_min`, `wave_max`
- `median_snr`
- `calibration_state`
- `quality_flag`

### 9.4 Derived line-metric schema

`line_metrics.parquet`

Columns:
- `object_uid`
- `epoch_uid`
- `line_name`
- `line_flux`
- `line_flux_err`
- `ew`
- `ew_err`
- `fwhm`
- `fwhm_err`
- `sigma_line`
- `sigma_line_err`
- `centroid`
- `centroid_err`
- `skew`
- `kurtosis`
- `blue_red_asymmetry`
- `fit_model_id`

### 9.5 Lag-result schema

`lags.parquet`

Columns:
- `object_uid`
- `pair_id`
- `driver_channel`
- `response_channel`
- `method`
- `lag_median`
- `lag_lo`
- `lag_hi`
- `significance`
- `alias_score`
- `quality_score`
- `posterior_path`
- `method_config_hash`

### 9.6 Sonification manifest

`sonifications.parquet`

Columns:
- `object_uid`
- `sonification_id`
- `mapping_family`
- `input_channels`
- `audio_path`
- `duration_sec`
- `time_scale`
- `normalization_mode`
- `uncertainty_mode`
- `mapping_config_hash`
- `provenance_hash`

---

## 10. Data ingestion, calibration, and normalization

This stage decides whether the downstream science is trustworthy.

### 10.1 Non-negotiable principles

1. **Never overwrite raw data.**
2. **Track every normalization decision as metadata.**
3. **Preserve both observed-frame and rest-frame times.**
4. **Preserve both raw fluxes and normalized/scaled versions.**
5. **Keep all masks and flags.**
6. **Do not audio-normalize away physically meaningful amplitude structure before storing a science-ready representation.**

### 10.2 Time handling

Implementation:
- store all times in MJD (observed)
- derive rest-frame time as `mjd_rest = (mjd_obs - t0) / (1 + z)` using a documented per-object `t0`
- keep observed-frame analyses as default for comparison with literature when the literature is in observed frame
- only compare lag populations in rest frame after explicit conversion

### 10.3 Photometric normalization

Maintain three parallel representations:

**R0 raw**  
native units exactly as supplied

**R1 science-normalized**  
converted to consistent flux density / relative flux units where possible

**R2 sonification-normalized**  
robustly standardized version used for audio mapping

Recommended transforms:
- robust median centering
- scale by MAD or robust percentile range
- optional de-trending channel (not replacement) for low-frequency structure
- never discard original amplitudes; store transforms explicitly

### 10.4 Spectral calibration and normalization

Per-epoch steps:
1. wavelength solution validation
2. Galactic extinction correction if applicable
3. redshift to rest frame
4. resample to a common grid only in derived products, never overwrite raw
5. narrow-line anchoring / [O III]-based relative flux recalibration where appropriate, especially for CLAGN spectral comparisons (informed by CLAGN practice in DESI work [R19])
6. produce multiple continuum-subtraction variants:
   - minimal local continuum
   - global pseudo-continuum
   - full PyQSOFit decomposition

### 10.5 Line extraction

For each relevant line:
- Hα
- Hβ
- Mg II
- C IV
- optional He II, Fe II complexes, continuum windows

Store:
- integrated flux
- EW
- centroid
- FWHM and line dispersion
- blue/red asymmetry
- residual diagnostics
- fit uncertainty
- data quality notes

### 10.6 Missing data and gaps

Do **not** silently interpolate for primary analysis. Instead:
- preserve the irregularly sampled truth
- create explicit interpolation products only for methods that require them
- flag long seasonal gaps
- expose gap structure to the sonification layer

### 10.7 QC rules

Implement a scoring system:
- cadence adequacy
- median S/N
- fraction masked
- line coverage quality
- line-fit stability
- agreement between lag methods
- alias risk

Each object/pair gets a `quality_score` and `review_priority`.

---

## 11. Reverberation inference stack

The project should never trust one lag method.

### 11.1 Baseline methods

**PyCCF** [R22]  
Use for:
- literature continuity
- quick baselines
- centroid/peak estimates
- FR/RSS uncertainty distributions

**pyZDCF** [R23]  
Use for:
- sparse or unevenly sampled pairs
- robustness checks against interpolation assumptions

**JAVELIN** [R21]  
Use for:
- direct light-curve fitting under DRW assumptions
- comparison to legacy continuum RM literature
- fast baseline model-based inference

**PyROA** [R24]  
Use for:
- multi-lightcurve simultaneous fits
- Bayesian uncertainties
- smooth latent driver models

### 11.2 Modern / advanced methods

**pyPETaL** [R25]  
Use as:
- meta-pipeline benchmark
- sanity-check reference implementation
- convenient baseline orchestration

**LITMUS** [R26]  
Use for:
- later-stage high-rigor lag recovery
- false-positive suppression
- model comparison / null-hypothesis testing
- seasonal alias disambiguation

**MICA2** [R27]  
Use for:
- transfer-function exploration
- multi-component response modeling
- cases with poor or partially missing drivers

**EzTao + celerite2** [R28, R30]  
Use for:
- DRW/CARMA simulations
- scalable GP baselines
- simulation-based benchmark generation

### 11.3 Recommended inference protocol

For each channel pair:
1. run PyCCF
2. run pyZDCF
3. run JAVELIN
4. run PyROA
5. if quality high or result anomalous, run LITMUS
6. if transfer-function complexity seems important, run MICA2
7. build a **consensus lag object** from all methods

Consensus rules:
- agreement cluster: methods consistent within uncertainty
- contested: multi-method disagreement or strong aliasing
- likely spurious: weak significance + alias-risk + poor QC
- candidate anomaly: high QC but method disagreement or unusual transfer-function / state dependence

### 11.4 Metrics recorded per method

- median lag
- credible/confidence intervals
- posterior width
- alias/ridge count
- significance / null score
- runtime
- convergence diagnostics
- agreement score vs other methods

---

## 12. Sonification design specification

This is the heart of the project. The mapping must be **stable, documented, and testable**.

### 12.1 Design principles

1. **Continuity:** the same astrophysical concept should map to the same auditory concept across the whole project.
2. **Local interpretability:** a user should be able to point to a sound event and explain what data feature it corresponds to.
3. **Uncertainty honesty:** uncertainty should never be hidden behind clean sounds.
4. **Comparability:** mappings should be normalized enough for cross-object listening, but not so aggressively that physically meaningful differences vanish.
5. **Plurality:** build several mapping families and evaluate them, rather than assuming a single “correct” sonification.

### 12.2 Canonical mapping family A — Echo ensemble

Best for RM intuition.

Channels:
- driving continuum bands = distinct instrument families / timbres
- line channels = delayed echo voices
- uncertainty = roughness / breathiness / stereo diffusion
- missing data = filtered silence / muted band-limited noise
- line width = spectral brightness or bandwidth
- line asymmetry = stereo offset or timbral asymmetry
- line strength = loudness envelope

Interpretation:
- a clean disc-like continuum sequence should sound like ordered band-to-band delay
- a BLR line response should sound like a later echo with different timbre
- diffuse continuum contamination should sound like extra smeared or duplicated echoes
- CLAGN transitions should sound like the disappearance, delay shift, or decoupling of response voices

### 12.3 Canonical mapping family B — Direct audification + overlays

Best for “hear the data” purists.

Mapping:
- preserve time order directly, with only global time compression
- map normalized flux to amplitude and/or instantaneous pitch
- overlay discrete audio cues for line metrics and uncertainty changes
- use this as the closest equivalent to waveform listening

### 12.4 Canonical mapping family C — Feature token stream

Best for AI + human anomaly review.

Mapping:
- detect events (flares, lag peaks, line-breathing episodes, asymmetry changes)
- encode events as short motifs/tokens
- use this for compressed scanning of large catalogs

### 12.5 Uncertainty encoding (required)

At least three uncertainty encodings should be implemented and benchmarked:

**U1 Roughness encoding**  
higher uncertainty -> noisier / rougher timbre

**U2 Jitter encoding**  
higher uncertainty -> slight pitch / onset instability

**U3 Diffusion encoding**  
higher uncertainty -> broader stereo spread / reverb-like blur

The mapping should be chosen empirically, not by taste.

### 12.6 Audio normalization policy

Store two audio products per sonification:

- **science WAV**: lossless, fixed loudness policy, stable dynamic range
- **presentation MP3/OGG**: optimized for listening convenience

Never tune the science WAV by ear after rendering.

### 12.7 Required output bundle per object

For every finalized object:
- main audio file
- isolated channel stems
- synchronized plot movie
- mapping legend
- JSON/YAML config
- provenance record linking back to raw data hashes

---

## 13. Simulation and benchmark generation

A discovery-oriented project needs synthetic truth tables.

### 13.1 Why simulation is mandatory

Simulation is required to answer:
- do we recover the correct lag?
- does uncertainty sound like uncertainty?
- does sonification help on specific anomaly classes?
- which mapping family is best under which data conditions?

### 13.2 Synthetic continuum models

Implement:
- DRW baseline via EzTao [R28]
- optional higher-order CARMA variants [R28]
- GP alternatives with celerite2 [R30]

### 13.3 Transfer-function families

Generate line / diffuse-continuum responses using:
- Gaussian
- top-hat
- gamma
- exponential

These are directly aligned with MICA2’s supported transfer-function families [R27].

### 13.4 Contamination / complexity injections

Inject:
- diffuse continuum contamination (motivated by Lawther et al. and AGN STORM 2) [R16, R17]
- state-dependent lag shifts
- line breathing (lag or width changes with luminosity)
- partial decoupling of line and continuum
- frozen-look behavior
- seasonal gaps
- calibration drifts
- outliers / spurious points
- cadence degradation to ZTF-like sampling

### 13.5 Benchmark families

Build at least five benchmark suites:

**B1 Clean RM**  
single continuum driver + single delayed line

**B2 Disc-like continuum hierarchy**  
multi-band continuum lags with monotonic wavelength sequence

**B3 Diffuse-continuum contaminated**  
disc-like sequence plus smeared BLR continuum contribution

**B4 State-change / CLAGN-like**  
lag or response law changes mid-stream

**B5 Failure cases**  
sparse cadence, seasonal aliasing, low S/N, bad calibration

### 13.6 Benchmark outputs

For every synthetic realization store:
- ground-truth parameters
- method outputs
- audio files
- metadata
- agent/human annotations
- evaluation scores

---

## 14. Validation and refinement program

Validation must happen in a strict order.

### 14.1 Stage V1 — software correctness

Goals:
- parsers read all datasets correctly
- unit tests pass
- reference outputs stable
- audio rendering deterministic

Deliverables:
- parser fixtures
- small synthetic tests
- reproducible hashes for benchmark outputs

### 14.2 Stage V2 — gold benchmark on AGN Watch

Goals:
- validate spectral parsing and line extraction
- reproduce known qualitative lag structure
- test diffuse-continuum and line-breathing hypotheses on canonical objects

Priority object:
- NGC 5548 first, because it is central to the diffuse-continuum discussion [R16, R14]

Required outputs:
- lag comparison table versus literature
- line-fit diagnostics
- audio set with multiple mapping families
- memo documenting which mappings make known features most audible

### 14.3 Stage V3 — silver benchmark on SDSS-RM

Goals:
- scalable lag recovery benchmarking
- consensus-method comparisons
- object-level quality control
- anomaly taxonomy development

Use published lag-bearing subsamples from SDSS-RM as the main benchmark target [R8].

Required metrics:
- lag recovery MAE against literature
- interval coverage / calibration
- false-positive rate on shuffled/null pairs
- disagreement rate between methods
- runtime per object / pair
- success by line, redshift, and cadence regime

### 14.4 Stage V4 — continuum RM benchmark on ZTF

Goals:
- test inter-band continuum lag recovery at scale
- compare against ZTF-based continuum-RM results [R15]
- develop continuum-only sonification mappings

Required metrics:
- recovery of known-like lag hierarchies in simulated and literature-inspired objects
- thin-disc-like vs contaminated classification performance
- stability under cadence degradation

### 14.5 Stage V5 — human + AI sonification efficacy testing

This is where the project becomes scientifically credible as sonification research.

Design:
- blinded tasks on synthetic and real objects
- participants or agents see:
  - plot-only
  - audio-only
  - plot+audio
- tasks:
  - identify which of two objects has larger lag
  - identify contaminated vs clean sequence
  - detect state change
  - identify anomalous line response

Metrics:
- accuracy
- time-to-decision
- agreement with ground truth
- calibration of confidence
- performance by training level

This stage is directly motivated by Brown et al.’s argument that astronomy sonification needs efficacy testing [R2].

---

## 15. Experimental program toward novel results

Once the validation stages succeed, move to discovery.

### 15.1 Discovery track D1 — continuum-lag outliers

Target:
- objects whose continuum lag hierarchy or size strongly departs from standard expectations

Scientific interest:
- diffuse continuum dominated systems
- unusual disc structure
- state-dependent lag changes

Key outputs:
- ranked outlier catalog
- audio galleries for top candidates
- comparison to literature expectations

### 15.2 Discovery track D2 — line-response anomalies

Target:
- objects where Hβ / Mg II / C IV behave differently than expected relative to continuum

Scientific interest:
- stratified BLR structure
- state-dependent line responsivity
- partial decoupling between continuum and line emission

Key outputs:
- per-line anomaly scores
- line-specific audio stems
- response asymmetry tables

### 15.3 Discovery track D3 — CLAGN precursor / transition signatures

Target:
- objects with changing spectroscopic state and unusual lag or variability behavior before, during, or after transition

Scientific interest:
- whether CLAGN transitions have measurable precursor signatures
- whether “frozen-look” or peculiar slow-decline objects occupy their own lag-response class [R18, R19, R20]

Key outputs:
- transition-aligned lag timelines
- pre/post-change sonification comparisons
- candidate precursor catalog

### 15.4 Discovery track D4 — extreme / peculiar objects

Taxonomy informed by Komossa et al. [R20] and CLAGN studies [R18, R19]:
- classical turn-on / turn-off CLAGN
- repeated state changers
- frozen-look / weak-response objects
- very large continuum-lag objects
- strong diffuse-continuum candidates
- peculiar long-decline systems
- line-width / lag decouplers

---

## 16. Candidate novelty claims to aim for

Do not aim first for a grand theory. Aim for publishable incremental findings such as:

1. **A validated uncertainty-aware sonification framework for RM**  
   This alone is likely publishable if benchmarked well.

2. **Evidence that one sonification mapping improves anomaly detection on known-like RM tasks**  
   Strong methods paper.

3. **A catalog of lag/response outliers in SDSS-RM or ZTF-linked AGN**  
   Good catalog paper.

4. **A subpopulation of CLAGN with distinct pre-transition or transition-time lag behavior**  
   High-value science paper if robust.

5. **Evidence for a “frozen-look” or weak-response class in public RM/CLAGN data**  
   Strong incremental discovery if carefully validated.

---

## 17. AI-agent operating model

The project should use a multi-agent structure, but with strict guardrails.

### 17.1 Agent roles

**A. Literature agent**  
Builds and updates a machine-readable bibliography and extracts key methods/claims.

**B. Data engineer agent**  
Writes and tests ingestion / normalization code.

**C. RM scientist agent**  
Implements lag methods, convergence checks, and consensus logic.

**D. Sonification scientist agent**  
Implements and evaluates mapping families.

**E. Evaluation agent**  
Runs synthetic benchmarks and produces leaderboard tables.

**F. Discovery agent**  
Ranks anomalies and drafts object memos.

**G. Report agent**  
Generates reproducible reports, plots, audio bundles, and paper drafts.

### 17.2 Guardrails

- gold benchmark objects must be immutable
- benchmark splits must be fixed before mapping optimization
- discovery objects must never tune the core objective
- all code patches must pass tests
- all anomaly claims require:
  1. multi-method support,
  2. QC threshold,
  3. provenance record,
  4. human review memo

---

## 18. Autoresearch / optimization framework

This is where Karpathy-style ideas are useful, but only if tightly controlled.

### 18.1 Conceptual template

Karpathy’s `autoresearch` is useful as a design pattern: small code surface, fixed time budget, clear metric, autonomous keep/discard loop, human control through `program.md` [R33]. The scientific analogue here is not “let an agent rewrite everything.” It is:

- define a fixed benchmark suite
- define allowed mutation surfaces
- define objective metrics
- let agents iterate on mappings / configs / model choices
- accept only experiments that improve benchmark performance or Pareto trade-offs

### 18.2 What the agents are allowed to change

Allowed mutation zones:
- `src/agnsonify/sonify/*`
- `src/agnsonify/anomaly/*`
- `configs/sonification/*`
- `configs/experiments/*`
- prompt/program files under `agents/`

Restricted mutation zones:
- raw data manifests
- benchmark labels
- test fixtures
- provenance machinery

### 18.3 Optimization objectives

Define a **multi-objective** score:

- `M1` lag recovery MAE on synthetic truth
- `M2` coverage calibration of lag intervals
- `M3` false-positive rate on null/shuffled pairs
- `M4` anomaly detection AUC / precision@k on held-out anomaly benchmarks
- `M5` human/agent discriminability on audio tasks
- `M6` compute cost / runtime
- `M7` interpretability penalty (hand-scored or rule-based)

Search should optimize the Pareto front, not a single scalar. Optuna supports multi-objective optimization [R37], Ax provides Bayesian optimization for adaptive experiments [R39], and Ray Tune can orchestrate large sweeps and integrates with Optuna/Ax/PBT/ASHA [R38].

### 18.4 Suggested search spaces

**Sonification search space**
- pitch range
- tempo / time compression
- uncertainty encoding mode
- line-width mapping
- stereo/spatialization mode
- loudness normalization policy
- event token thresholds

**RM modeling search space**
- detrending choice
- outlier rejection thresholds
- GP / DRW priors
- transfer-function family
- lag window
- consensus weighting

**Anomaly search space**
- embedding model family
- clustering threshold
- outlier score weighting
- literature-prior injection

### 18.5 LLM program optimization

Use:
- `DSPy` to structure agent modules and evaluation [R34]
- `MIPROv2` to tune agent instructions / few-shot examples where appropriate [R35]
- `TextGrad` only for bounded optimization of prompts or report templates, not for unreviewed scientific claims [R36]

## 19. Suggested model/representation learning layer

This layer is optional in v1, but likely high value in v2.

### 19.1 Simulation-based inference (SBI)

Li et al. (2024) show that deep-learning-based SBI can accelerate continuum RM inference by **10^3–10^5x** relative to traditional methods on simulated data [R32]. This is highly relevant for large-scale anomaly screening.

Recommendation:
- do **not** replace classical methods with SBI in v1
- use SBI as a fast proposal engine or prefilter
- only promote SBI outputs after calibration against benchmark sets

### 19.2 Audio embeddings

Recommended strategy:
- derive embeddings from rendered audio or channel stems
- compare to embeddings from raw light-curve/line-feature vectors
- use agreement between audio and non-audio embeddings as a confidence signal

Possible tasks:
- cluster contaminated vs clean simulated RM cases
- rank CLAGN transition types
- detect outlier motif families

### 19.3 Joint representation learning

Later-stage target:
- learn joint embeddings from:
  - light curves
  - line metrics
  - lag posteriors
  - audio
- use these for anomaly ranking and retrieval

---

## 20. Required outputs and deliverables

### 20.1 Per-object outputs

For every finalized analysis object:
- summary YAML/JSON
- cleaned photometry table
- derived line-metrics table
- lag-method comparison table
- one or more audio files
- synchronized figure/video
- human-readable memo

### 20.2 Catalog-level outputs

- benchmark leaderboard
- anomaly catalog
- CLAGN transition catalog
- sonification-mapping leaderboard
- literature comparison table

### 20.3 Publication-ready artifacts

- methods paper figures
- object case-study figures
- supplement with audio files
- open-source package docs
- reproducibility checklist

---

## 21. Evaluation metrics in detail

### 21.1 Science metrics

- lag recovery MAE / RMSE
- posterior coverage
- method agreement fraction
- alias rejection rate
- line-response stability
- change-point detection precision/recall
- CLAGN transition lead-time, where measurable

### 21.2 Sonification efficacy metrics

- anomaly detection accuracy from audio-only / plot-only / combined tasks
- time-to-correct identification
- inter-rater agreement
- transfer learning after brief training
- confusion matrix by anomaly type

### 21.3 Engineering metrics

- runtime per object
- GPU / CPU cost
- storage footprint
- reproducibility rate under reruns
- test coverage

### 21.4 Product metrics

- percentage of outputs with full provenance
- documentation completeness
- number of benchmarked mapping families
- number of objects passing all QC gates

---

## 22. Milestone roadmap

### Phase 0 — Foundation (2–3 weeks)
- assemble bibliography
- set up repo, CI, configs, DVC/MLflow/Snakemake/Hydra
- define schemas and manifests

### Phase 1 — Ingestion and normalization (3–5 weeks)
- AGN Watch parsers
- SDSS-RM readers
- ZTF IRSA API + bulk retrieval helpers
- raw → normalized pipeline

### Phase 2 — Classical RM baseline (3–5 weeks)
- PyCCF, pyZDCF, JAVELIN, PyROA wrappers
- lag-result schema
- null tests and basic benchmarks

### Phase 3 — Spectral decomposition + line metrics (3–5 weeks)
- PyQSOFit integration
- multi-epoch line extraction
- QC and fit diagnostics

### Phase 4 — Sonification engine v1 (3–4 weeks)
- implement mapping families A/B/C
- render audio bundles
- channel stem support
- uncertainty encodings

### Phase 5 — Synthetic benchmark suite (3–4 weeks)
- DRW/CARMA generators
- transfer-function injections
- contamination/state-change/failure benchmarks

### Phase 6 — Validation on AGN Watch + SDSS-RM (4–6 weeks)
- literature comparison
- benchmark leaderboard
- mapping ablations

### Phase 7 — AI/autoresearch loop (3–5 weeks)
- Ray/Optuna/Ax orchestration
- agent programs and benchmark controls
- benchmark-driven optimization

### Phase 8 — ZTF + CLAGN discovery extension (4–8 weeks)
- continuum RM scaling
- CLAGN labels and transition alignment
- anomaly catalog generation

### Phase 9 — Publication / release (ongoing)
- methods paper
- catalog paper
- code + docs release
- benchmark + audio archive

---

## 23. Risk register and mitigations

### Risk 1 — Sonification adds little beyond good plots
Mitigation:
- run real efficacy tests
- benchmark against strong visual baselines
- treat this as a scientific question, not an assumption

### Risk 2 — Too many false positives from lag methods
Mitigation:
- require multi-method consensus
- use null/shuffle controls
- use LITMUS and alias diagnostics [R26]

### Risk 3 — Spectral calibration artifacts mimic CLAGN behavior
Mitigation:
- explicit [O III]-anchored recalibration where applicable
- pseudo-photometry checks
- store calibration-state confidence

### Risk 4 — Agentic optimization overfits benchmarks
Mitigation:
- fixed held-out benchmark splits
- hidden test sets
- no direct mutation of benchmark labels

### Risk 5 — Codebase becomes too complex for agents
Mitigation:
- keep mutation surfaces small
- use modular repo
- adopt `program.md` and issue-driven workflows inspired by `autoresearch` [R33]

---

## 24. Recommended first concrete work package

If starting tomorrow, the highest-value first 6–8 week package is:

1. Repo setup with Snakemake + Hydra + DVC + MLflow.
2. AGN Watch ingestion for NGC 5548 plus one other object.
3. SDSS-RM ingestion for a small published-lag subset.
4. PyCCF + JAVELIN + PyROA wrappers.
5. Minimal `STRAUSS`-based “echo ensemble” sonification.
6. Synthetic clean-vs-contaminated benchmark generator.
7. Small blinded plot/audio/plot+audio evaluation.
8. Write the first internal memo:
   **“Can we hear diffuse-continuum-like contamination in benchmark RM data?”**

That package is small enough to ship, benchmark, and iterate.

---

## 25. Final recommendation

Treat the project as a **methods-first science platform**.

The likely best path to novel results is:
1. validate aggressively on AGN Watch and SDSS-RM,
2. use ZTF for scale and continuum variability context,
3. add CLAGN only after the benchmark pipeline is stable,
4. use agentic/autoresearch loops only against fixed metrics and immutable benchmarks,
5. aim first for a publishable methods result plus an anomaly catalog,
6. then push toward a science claim about **diffuse-continuum-dominated systems, lag-state changes, or CLAGN precursors**.

This is ambitious but realistic. The key is to insist on **benchmarkability, uncertainty honesty, and multi-method consensus** from the beginning.

---

## 26. Reference guide

[R1] Zanella et al., *Sonification and Sound Design for Astronomy Research, Education and Public Engagement* (2022 / Nature Astronomy review).  
https://arxiv.org/abs/2206.13536

[R2] Brown et al., *Evaluating the efficacy of sonification for signal detection in univariate, evenly sampled light curves using astronify* (2022).  
https://academic.oup.com/mnras/article/516/4/5674/6698731

[R3] `astronify` documentation.  
https://astronify.readthedocs.io/en/latest/

[R4] `STRAUSS` documentation.  
https://strauss.readthedocs.io/en/latest/

[R5] Trayford et al., *Inspecting spectra with sound: proof-of-concept & extension to datacubes* (2023).  
https://arxiv.org/abs/2306.10126

[R6] International AGN Watch archive.  
https://www.asc.ohio-state.edu/astronomy/agnwatch/

[R7] SDSS DR18 Black Hole Mapper Reverberation Mapping page.  
https://www.sdss.org/dr18/bhm/programs/rm/

[R8] Shen et al., *The Sloan Digital Sky Survey Reverberation Mapping Project: Key Results* (2024).  
https://ui.adsabs.harvard.edu/abs/2024ApJS..272...26S/abstract

[R9] *The Nineteenth Data Release of the Sloan Digital Sky Survey* (BHM overview including RM/AQMES).  
https://arxiv.org/html/2507.07093v1

[R10] ZTF public data release page.  
https://www.ztf.caltech.edu/ztf-public-releases.html

[R11] IRSA ZTF mission/services page.  
https://irsa.ipac.caltech.edu/Missions/ztf.html

[R12] IRSA ZTF Lightcurve API.  
https://irsa.ipac.caltech.edu/docs/program_interface/ztf_lightcurve_api.html

[R13] `astroquery.sdss` documentation.  
https://astroquery.readthedocs.io/en/latest/sdss/sdss.html

[R14] Cackett et al., *Reverberation mapping of active galactic nuclei: from X-ray corona to dusty torus* (2021 review).  
https://pmc.ncbi.nlm.nih.gov/articles/PMC8188568/

[R15] Guo, Barth & Wang, *AGN Continuum Reverberation Mapping Based on Zwicky Transient Facility Light Curves* (2022).  
https://arxiv.org/abs/2207.06432

[R16] Lawther et al., *Diffuse continuum delays in NGC 5548 / contamination of disc reverberation signatures* (2018).  
https://academic.oup.com/mnras/article/481/1/533/5076066

[R17] Netzer et al., *AGN STORM 2: X. The origin of the interband continuum delays in Mrk 817* (2024).  
https://arxiv.org/abs/2410.02652

[R18] Wang et al., *Systematic Analysis of Changing-look AGN Variability Using ZTF Light Curves* (2025).  
https://arxiv.org/abs/2511.10217

[R19] Guo et al., *Changing-look AGN from DESI DR1. II. Statistical Properties* (2024).  
https://arxiv.org/abs/2408.00402

[R20] Komossa et al., *The extremes of AGN variability* (2024 review).  
https://arxiv.org/abs/2408.00089

[R21] Zu, Kochanek & Peterson, *An Alternative Approach To Measuring Reverberation Lags in Active Galactic Nuclei* (JAVELIN paper).  
https://arxiv.org/abs/1008.0641

[R22] PyCCF code record.  
https://ui.adsabs.harvard.edu/abs/2018ascl.soft05032S/abstract

[R23] `pyZDCF` documentation.  
https://pyzdcf.readthedocs.io/en/latest/index.html

[R24] Donnan et al., *PyROA / Running Optimal Average for quasar time-delay analysis* (2021).  
https://research-repository.st-andrews.ac.uk/handle/10023/24192

[R25] `pyPETaL` repository and docs.  
https://github.com/Zstone19/pypetal

[R26] McDougall et al., *LITMUS: Bayesian Lag Recovery in Reverberation Mapping with Fast Differentiable Models* (2025).  
https://arxiv.org/abs/2505.09832

[R27] `MICA2` repository and docs.  
https://github.com/LiyrAstroph/MICA2

[R28] `EzTao` toolkit.  
https://github.com/ywx649999311/EzTao

[R29] `PyQSOFit` repository.  
https://github.com/legolason/PyQSOFit

[R30] `celerite2` documentation.  
https://celerite2.readthedocs.io/en/latest/

[R31] Astropy Lomb–Scargle docs.  
https://docs.astropy.org/en/latest/timeseries/lombscargle.html

[R32] Li et al., *Fast and Flexible Inference Framework for Continuum Reverberation Mapping using Simulation-based Inference with Deep Learning* (2024).  
https://arxiv.org/abs/2407.14621

[R33] Karpathy, `autoresearch` repository.  
https://github.com/karpathy/autoresearch

[R34] DSPy.  
https://dspy.ai/

[R35] DSPy `MIPROv2` optimizer.  
https://dspy.ai/api/optimizers/MIPROv2/

[R36] TextGrad paper.  
https://arxiv.org/abs/2406.07496

[R37] Optuna multi-objective optimization docs.  
https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/002_multi_objective.html

[R38] Ray Tune docs.  
https://docs.ray.io/en/latest/tune/index.html

[R39] Ax docs (Bayesian optimization).  
https://ax.dev/docs/intro-to-bo/

[R40] MLflow Tracking docs.  
https://mlflow.org/docs/latest/ml/tracking/

[R41] DVC experiment management docs.  
https://doc.dvc.org/user-guide/experiment-management

[R42] Snakemake docs.  
https://snakemake.readthedocs.io/en/stable/

[R43] Hydra docs.  
https://hydra.cc/docs/intro/

[R46] NEOWISE Single-exposure Source Database documentation.  
https://irsa.ipac.caltech.edu/data/WISE/docs/release/NEOWISE/expsup/sec2_1.html

[R47] IRSA WISE / NEOWISE mission and services page.  
https://irsa.ipac.caltech.edu/Missions/wise.html
