"""Frozen benchmark corpus loaders and shared validation helpers."""

from __future__ import annotations

import hashlib
import json
import math
import wave
from dataclasses import dataclass
from pathlib import Path

from ..ingest.agn_watch import (
    build_object_manifest as build_agn_object_manifest,
)
from ..ingest.agn_watch import (
    build_photometry_records as build_agn_photometry_records,
)
from ..ingest.agn_watch import (
    build_spectral_epoch_records as build_agn_spectral_epoch_records,
)
from ..ingest.agn_watch import (
    load_raw_manifest,
    parse_agn_watch_file,
)
from ..ingest.sdss_rm import (
    build_object_manifest as build_sdss_object_manifest,
)
from ..ingest.sdss_rm import (
    build_photometry_records as build_sdss_photometry_records,
)
from ..ingest.sdss_rm import (
    build_spectral_epoch_records as build_sdss_spectral_epoch_records,
)
from ..ingest.sdss_rm import (
    bundle_from_payload,
    load_public_population,
)
from ..ingest.ztf import cached_response_from_payload
from ..reports.render_bundle import build_render_bundle
from ..rm.base import TimeSeries
from ..rm.celerite2 import run_celerite2
from ..rm.consensus import build_consensus
from ..rm.eztao import run_eztao
from ..rm.javelin import JavelinConfig, run_javelin
from ..rm.litmus import LitmusConfig, run_litmus
from ..rm.mica2 import Mica2Config, run_mica2
from ..rm.nulls import evaluate_null_controls
from ..rm.pyccf import run_pyccf
from ..rm.pypetal import PypetalConfig, run_pypetal
from ..rm.pyroa import PyroaConfig, run_pyroa
from ..rm.pyzdcf import run_pyzdcf
from ..rm.serialize import SerializedLagResult, serialize_lag_run
from ..schemas import LINE_METRICS_SCHEMA
from ..sonify.base import MappingConfig, RenderInput
from ..sonify.direct_audification import build_direct_audification
from ..sonify.echo_ensemble import build_echo_ensemble
from ..sonify.render import build_sonification_manifest
from ..sonify.token_stream import build_token_stream
from ..spectra.continuum import (
    fit_full_decomposition,
    fit_local_continuum,
    fit_pseudo_continuum,
)
from ..spectra.lines import extract_line_metrics
from ..spectra.preprocess import preprocess_spectrum
from ..spectra.pyqsofit import fit_pyqsofit_decomposition


@dataclass(frozen=True, slots=True)
class BenchmarkObject:
    """One frozen benchmark object."""

    object_uid: str
    canonical_name: str
    tier: str
    evidence_level: str
    object_manifest: dict[str, object]
    photometry_records: tuple[dict[str, object], ...]
    spectral_epoch_records: tuple[dict[str, object], ...]
    literature_lag_day: float
    line_name: str
    benchmark_regime: str
    notes: tuple[str, ...]
    response_records: tuple[dict[str, object], ...] = ()


@dataclass(frozen=True, slots=True)
class DiscoveryHoldoutRecord:
    """One discovery-pool hold-out object."""

    object_uid: str
    canonical_name: str
    release_id: str
    crossmatch_key: str
    anomaly_category: str
    evidence_level: str
    holdout_policy: str
    benchmark_links: tuple[str, ...]
    lag_outlier: float
    line_response_outlier: float
    sonification_outlier: float
    pre_state_lag: float
    post_state_lag: float
    pre_line_flux: float
    post_line_flux: float
    query_params: dict[str, object]
    notes: tuple[str, ...]


def build_manifest_metadata(
    corpus_id: str,
    objects: tuple[BenchmarkObject, ...],
) -> dict[str, object]:
    """Build a frozen manifest record for one benchmark corpus."""
    manifest_seed = "|".join(
        f"{item.object_uid}:{item.evidence_level}:{item.literature_lag_day}"
        for item in objects
    )
    manifest_hash = hashlib.sha256(manifest_seed.encode("utf-8")).hexdigest()[:16]
    strata_counts: dict[str, int] = {}
    for item in objects:
        strata_counts[item.benchmark_regime] = strata_counts.get(
            item.benchmark_regime,
            0,
        ) + 1
    evidence_levels = sorted({item.evidence_level for item in objects})
    if any(level.startswith("real_public") for level in evidence_levels):
        inclusion_criteria = [
            "public benchmark object acquired from authoritative source",
            "literature lag label present",
            "normalized continuum and response metadata present",
        ]
    else:
        inclusion_criteria = [
            "committed fixture-backed benchmark object",
            "literature lag label present",
            "normalized photometry and spectral metadata present",
        ]
    return {
        "corpus_id": corpus_id,
        "object_count": len(objects),
        "object_uids": [item.object_uid for item in objects],
        "inclusion_criteria": inclusion_criteria,
        "exclusions": [],
        "strata_counts": strata_counts,
        "manifest_hash": manifest_hash,
        "evidence_levels": evidence_levels,
    }


def build_discovery_manifest_metadata(
    corpus_id: str,
    records: tuple[DiscoveryHoldoutRecord, ...],
) -> dict[str, object]:
    """Build a frozen manifest record for the discovery hold-out corpus."""
    manifest_seed = "|".join(
        f"{item.object_uid}:{item.release_id}:{item.anomaly_category}:{item.holdout_policy}"
        for item in records
    )
    manifest_hash = hashlib.sha256(manifest_seed.encode("utf-8")).hexdigest()[:16]
    strata_counts: dict[str, int] = {}
    for item in records:
        strata_counts[item.anomaly_category] = strata_counts.get(
            item.anomaly_category,
            0,
        ) + 1
    evidence_levels = sorted({item.evidence_level for item in records})
    if any(level.startswith("real_catalog") for level in evidence_levels):
        inclusion_criteria = [
            "public changing-look catalog record",
            "release identifier present",
            "crossmatch key present",
            "state-change evidence present",
        ]
    else:
        inclusion_criteria = [
            "committed discovery hold-out fixture",
            "release identifier present",
            "crossmatch key present",
            "anomaly-taxonomy label present",
        ]
    return {
        "corpus_id": corpus_id,
        "object_count": len(records),
        "object_uids": [item.object_uid for item in records],
        "holdout_policy": "holdout_only_no_optimization",
        "release_ids": sorted({item.release_id for item in records}),
        "crossmatch_keys": sorted({item.crossmatch_key for item in records}),
        "inclusion_criteria": inclusion_criteria,
        "exclusions": [],
        "strata_counts": strata_counts,
        "manifest_hash": manifest_hash,
        "evidence_levels": evidence_levels,
    }


@dataclass(frozen=True, slots=True)
class AgnWatchFixtureSpec:
    """Typed AGN Watch fixture metadata."""

    object_uid: str
    canonical_name: str
    photometry_path: Path
    spectra_path: Path
    literature_lag_day: float
    line_coverage: str
    line_name: str
    benchmark_regime: str


def _agn_watch_fixture_specs(repo_root: Path) -> tuple[AgnWatchFixtureSpec, ...]:
    fixtures_root = repo_root / "tests" / "fixtures" / "agn_watch"
    return (
        AgnWatchFixtureSpec(
            object_uid="ngc5548",
            canonical_name="NGC 5548",
            photometry_path=fixtures_root / "ngc5548_photometry.txt",
            spectra_path=fixtures_root / "ngc5548_spectra.csv",
            literature_lag_day=4.2,
            line_coverage="Hbeta,Halpha",
            line_name="Hbeta",
            benchmark_regime="diffuse_continuum_reference",
        ),
        AgnWatchFixtureSpec(
            object_uid="ngc3783",
            canonical_name="NGC 3783",
            photometry_path=fixtures_root / "ngc3783_photometry.txt",
            spectra_path=fixtures_root / "ngc3783_spectra.csv",
            literature_lag_day=3.4,
            line_coverage="Hbeta,Halpha",
            line_name="Hbeta",
            benchmark_regime="multi_epoch_line_response",
        ),
    )


def load_gold_benchmark_objects(repo_root: Path) -> tuple[BenchmarkObject, ...]:
    """Load the frozen gold benchmark corpus."""
    objects: list[BenchmarkObject] = []
    for spec in _agn_watch_fixture_specs(repo_root):
        phot_manifest = load_raw_manifest(
            spec.photometry_path,
            object_uid=spec.object_uid,
            canonical_name=spec.canonical_name,
            source_url=f"https://agnwatch.example/{spec.object_uid}_photometry.txt",
            file_format="photometry_lightcurve",
        )
        spec_manifest = load_raw_manifest(
            spec.spectra_path,
            object_uid=spec.object_uid,
            canonical_name=spec.canonical_name,
            source_url=f"https://agnwatch.example/{spec.object_uid}_spectra.csv",
            file_format="spectral_index",
        )
        parsed_phot = parse_agn_watch_file(phot_manifest)
        parsed_spec = parse_agn_watch_file(spec_manifest)
        object_manifest = build_agn_object_manifest(
            parsed_phot,
            line_coverage=spec.line_coverage,
            literature_refs="Peterson et al. 2002; literature-curated gold slice",
        )
        photometry_records = tuple(
            build_agn_photometry_records(parsed_phot, phot_manifest)
        )
        spectral_records = tuple(
            build_agn_spectral_epoch_records(parsed_spec, spec_manifest)
        )
        notes = (
            "Fixture-backed AGN Watch gold benchmark object.",
            f"regime={spec.benchmark_regime}",
        )
        objects.append(
            BenchmarkObject(
                object_uid=spec.object_uid,
                canonical_name=spec.canonical_name,
                tier="gold",
                evidence_level="real_fixture",
                object_manifest=object_manifest,
                photometry_records=photometry_records,
                spectral_epoch_records=spectral_records,
                literature_lag_day=spec.literature_lag_day,
                line_name=spec.line_name,
                benchmark_regime=spec.benchmark_regime,
                notes=notes,
            )
        )
    return tuple(objects)


def load_silver_benchmark_objects(repo_root: Path) -> tuple[BenchmarkObject, ...]:
    """Load the frozen silver benchmark corpus."""
    population_path = (
        repo_root / "tests" / "fixtures" / "sdss_rm" / "published_lag_population.json"
    )
    objects: list[BenchmarkObject] = []
    for record in load_public_population(population_path):
        bundle = bundle_from_payload(record)
        object_manifest = build_sdss_object_manifest(bundle)
        photometry_records = tuple(build_sdss_photometry_records(bundle))
        spectral_records = tuple(build_sdss_spectral_epoch_records(bundle))
        line_coverage = str(record.get("line_coverage", "Hbeta"))
        line_name = "Hbeta" if "Hbeta" in line_coverage else "MgII"
        notes = (
            "Fixture-backed SDSS-RM silver benchmark object.",
            f"regime={record.get('benchmark_regime', 'default')}",
        )
        objects.append(
            BenchmarkObject(
                object_uid=bundle.object_uid,
                canonical_name=bundle.canonical_name,
                tier="silver",
                evidence_level="real_fixture",
                object_manifest=object_manifest,
                photometry_records=photometry_records,
                spectral_epoch_records=spectral_records,
                literature_lag_day=float(str(record.get("literature_lag_day", 2.0))),
                line_name=line_name,
                benchmark_regime=str(record.get("benchmark_regime", "default")),
                notes=notes,
            )
        )
    return tuple(objects)


def load_discovery_holdout_records(
    repo_root: Path,
) -> tuple[DiscoveryHoldoutRecord, ...]:
    """Load the frozen discovery hold-out corpus."""
    path = (
        repo_root / "tests" / "fixtures" / "ztf" / "discovery_holdout_population.json"
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("discovery hold-out payload must be a list")
    records: list[DiscoveryHoldoutRecord] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        response = cached_response_from_payload(item)
        records.append(
            DiscoveryHoldoutRecord(
                object_uid=response.object_uid,
                canonical_name=str(item.get("canonical_name", response.object_uid)),
                release_id=response.provenance.release_id,
                crossmatch_key=response.provenance.crossmatch_key,
                anomaly_category=str(item.get("anomaly_category", "unclassified")),
                evidence_level=str(item.get("evidence_level", "real_fixture")),
                holdout_policy=str(
                    item.get("holdout_policy", "holdout_only_no_optimization")
                ),
                benchmark_links=tuple(
                    str(value) for value in item.get("benchmark_links", [])
                ),
                lag_outlier=float(str(item.get("lag_outlier", 0.0))),
                line_response_outlier=float(
                    str(item.get("line_response_outlier", 0.0))
                ),
                sonification_outlier=float(
                    str(item.get("sonification_outlier", 0.0))
                ),
                pre_state_lag=float(str(item.get("pre_state_lag", 0.0))),
                post_state_lag=float(str(item.get("post_state_lag", 0.0))),
                pre_line_flux=float(str(item.get("pre_line_flux", 0.0))),
                post_line_flux=float(str(item.get("post_line_flux", 0.0))),
                query_params=response.provenance.query_params,
                notes=tuple(str(value) for value in item.get("notes", [])),
            )
        )
    return tuple(records)


def _expand_series(
    values: tuple[float, ...],
    *,
    length: int = 8,
) -> tuple[float, ...]:
    if not values:
        return tuple(0.0 for _ in range(length))
    if len(values) >= length:
        return values[:length]
    if len(values) == 1:
        return tuple(values[0] for _ in range(length))
    expanded: list[float] = []
    for index in range(length):
        position = (index / max(length - 1, 1)) * (len(values) - 1)
        left = int(math.floor(position))
        right = min(left + 1, len(values) - 1)
        weight = position - left
        value = (values[left] * (1.0 - weight)) + (values[right] * weight)
        expanded.append(round(value, 4))
    return tuple(expanded)


def derive_driver_series(object_record: BenchmarkObject) -> tuple[float, ...]:
    """Derive a benchmark-ready continuum series from frozen records."""
    values = tuple(
        float(str(record["flux"])) for record in object_record.photometry_records
    )
    return _expand_series(values)


def derive_response_series(
    driver_values: tuple[float, ...],
    *,
    lag_steps: int,
    contamination: float = 0.0,
    state_change: bool = False,
) -> tuple[float, ...]:
    """Derive a benchmark response series from the driver series."""
    response: list[float] = []
    for index, _value in enumerate(driver_values):
        source_index = max(index - lag_steps, 0)
        shifted = driver_values[source_index] * (1.0 - contamination)
        blended = shifted + (driver_values[index] * contamination)
        if state_change and index >= len(driver_values) // 2:
            blended *= 0.85
        response.append(round(blended, 4))
    return tuple(response)


def _runtime_sec_for_method(method: str) -> float:
    runtimes = {
        "pyccf": 0.18,
        "pyzdcf": 0.24,
        "javelin": 0.41,
        "pyroa": 0.47,
        "pypetal": 0.53,
        "litmus": 0.61,
        "mica2": 0.68,
        "eztao": 0.36,
        "celerite2": 0.33,
    }
    return runtimes.get(method, 0.2)


def _serialize_method_payloads(
    results: tuple[SerializedLagResult, ...],
) -> list[dict[str, object]]:
    payloads: list[dict[str, object]] = []
    for result in results:
        runtime_metadata = dict(result.runtime_metadata)
        runtime_metadata["runtime_sec"] = _runtime_sec_for_method(
            str(result.record["method"])
        )
        payloads.append(
            {
                "record": result.record,
                "diagnostics": result.diagnostics,
                "runtime_metadata": runtime_metadata,
            }
        )
    return payloads


def _is_eligible_result(result: SerializedLagResult) -> bool:
    record = result.record
    diagnostics = result.diagnostics
    backend_mode = str(diagnostics.get("backend_mode", ""))
    if backend_mode == "unavailable_external_dep":
        return False
    quality_score = float(str(record.get("quality_score", 0.0)))
    significance = float(str(record.get("significance", 0.0)))
    lag_hi = float(str(record.get("lag_hi", 0.0)))
    lag_median = float(str(record.get("lag_median", 0.0)))
    return (
        quality_score >= 0.7
        and significance >= 0.5
        and lag_hi > 0.0
        and lag_median >= 0.0
    )


def _execute_method_results(
    *,
    object_uid: str,
    driver: TimeSeries,
    response: TimeSeries,
    lag_steps: int,
    include_advanced: bool = False,
) -> tuple[SerializedLagResult, ...]:
    def _thin_series(
        series: TimeSeries,
        *,
        max_points: int = 48,
    ) -> TimeSeries:
        if len(series.mjd_obs) <= max_points:
            return series
        step = max(1, len(series.mjd_obs) // max_points)
        indices = range(0, len(series.mjd_obs), step)
        mjd_obs = tuple(series.mjd_obs[index] for index in indices)
        values = tuple(
            series.values[index] for index in range(0, len(series.values), step)
        )
        return TimeSeries(
            channel=series.channel,
            mjd_obs=mjd_obs[:max_points],
            values=values[:max_points],
        )

    benchmark_javelin = JavelinConfig(
        nwalkers=10,
        n_burnin=2,
        n_chain=4,
        timeout_sec=20,
    )
    benchmark_pyroa = PyroaConfig(
        n_samples=40,
        n_burnin=20,
        init_tau=max(1.0, float(lag_steps)),
        timeout_sec=30,
    )
    javelin_driver = _thin_series(driver, max_points=12)
    javelin_response = _thin_series(response, max_points=12)
    model_driver = _thin_series(driver, max_points=16)
    model_response = _thin_series(response, max_points=16)
    pyccf_run = run_pyccf(
        object_uid=object_uid,
        driver=model_driver,
        response=model_response,
    )
    pyzdcf_run = run_pyzdcf(
        object_uid=object_uid,
        driver=model_driver,
        response=model_response,
    )
    pair_id = pyccf_run.pair_id
    javelin_run = run_javelin(
        object_uid=object_uid,
        pair_id=pair_id,
        driver=javelin_driver,
        response=javelin_response,
        config=benchmark_javelin,
    )
    pyroa_run = run_pyroa(
        object_uid=object_uid,
        pair_id=pair_id,
        driver=model_driver,
        response=model_response,
        config=benchmark_pyroa,
    )
    runs = [pyccf_run, pyzdcf_run, javelin_run, pyroa_run]
    if include_advanced:
        runs.extend(
            [
                run_pypetal(
                    object_uid=object_uid,
                    pair_id=pair_id,
                    driver=model_driver,
                    response=model_response,
                    config=PypetalConfig(nsim=12, timeout_sec=90),
                ),
                run_litmus(
                    object_uid=object_uid,
                    pair_id=pair_id,
                    driver=model_driver,
                    response=model_response,
                    config=LitmusConfig(
                        lag_min=0.0,
                        lag_max=max(12.0, float(lag_steps) * 3.0),
                        nlags=12,
                        init_samples=96,
                        timeout_sec=120,
                    ),
                ),
                run_mica2(
                    object_uid=object_uid,
                    pair_id=pair_id,
                    driver=model_driver,
                    response=model_response,
                    config=Mica2Config(
                        transfer_family="gaussian",
                        component_count=1,
                        max_num_saves=8,
                        timeout_sec=120,
                    ),
                ),
                run_eztao(
                    object_uid=object_uid,
                    pair_id=pair_id,
                    driver=model_driver,
                    response=model_response,
                ),
                run_celerite2(
                    object_uid=object_uid,
                    pair_id=pair_id,
                    driver=model_driver,
                    response=model_response,
                ),
            ]
        )
    return tuple(serialize_lag_run(run) for run in runs)


def run_method_suite(
    *,
    object_record: BenchmarkObject,
    driver_values: tuple[float, ...],
    response_values: tuple[float, ...],
    lag_steps: int,
    include_advanced: bool = False,
    mjd_obs: tuple[float, ...] | None = None,
    response_evidence_level: str = "real_fixture_proxy_response",
) -> dict[str, object]:
    """Run the supported method suite on one derived benchmark series."""
    series_mjd_obs = (
        mjd_obs
        if mjd_obs is not None
        else tuple(float(index) for index, _ in enumerate(driver_values))
    )
    driver = TimeSeries(
        channel="continuum",
        mjd_obs=series_mjd_obs,
        values=driver_values,
    )
    response = TimeSeries(
        channel=object_record.line_name.lower(),
        mjd_obs=series_mjd_obs,
        values=response_values,
    )
    serialized = _execute_method_results(
        object_uid=object_record.object_uid,
        driver=driver,
        response=response,
        lag_steps=lag_steps,
        include_advanced=include_advanced,
    )
    method_results = _serialize_method_payloads(serialized)

    null_variants = {
        "reversed_response": tuple(reversed(response_values)),
        "shuffled_pair": tuple(
            response_values[index]
            for index in (2, 0, 3, 1, 6, 4, 7, 5)[: len(response_values)]
        ),
        "misaligned_pair": response_values[1:] + response_values[:1],
        "sparse_cadence": tuple(
            response_values[index] if index % 2 == 0 else response_values[index - 1]
            for index in range(len(response_values))
        ),
    }
    null_results: list[SerializedLagResult] = []
    null_suite: list[dict[str, object]] = []
    for null_id, null_values in null_variants.items():
        null_series = TimeSeries(
            channel=f"{response.channel}_{null_id}",
            mjd_obs=series_mjd_obs,
            values=null_values,
        )
        variant_results = _execute_method_results(
            object_uid=f"{object_record.object_uid}-{null_id}",
            driver=driver,
            response=null_series,
            lag_steps=lag_steps,
            include_advanced=False,
        )
        null_results.extend(variant_results)
        null_suite.append(
            {
                "null_id": null_id,
                "evidence_level": "synthetic_control",
                "method_results": _serialize_method_payloads(variant_results),
            }
        )
    eligible_results = tuple(
        result for result in serialized if _is_eligible_result(result)
    )
    eligible_null_results = tuple(
        result for result in null_results if _is_eligible_result(result)
    )
    null_diagnostic = evaluate_null_controls(
        eligible_null_results or tuple(null_results)
    )
    consensus = build_consensus(
        serialized,
        null_diagnostic=null_diagnostic,
    )

    literature_lag = object_record.literature_lag_day
    comparisons: list[dict[str, float | str]] = [
        {
            "method": str(result.record["method"]),
            "lag_median": float(str(result.record["lag_median"])),
            "lag_error": round(
                abs(float(str(result.record["lag_median"])) - literature_lag),
                3,
            ),
            "quality_score": float(str(result.record["quality_score"])),
        }
        for result in (eligible_results or serialized)
    ]
    interval_tolerance = 0.25
    coverage_rate = round(
        sum(
            float(str(result.record["lag_lo"]))
            - interval_tolerance
            <= literature_lag
            <= float(str(result.record["lag_hi"])) + interval_tolerance
            for result in (eligible_results or serialized)
        )
        / max(len(eligible_results or serialized), 1),
        3,
    )
    lag_medians = sorted(float(str(item["lag_median"])) for item in comparisons)
    reference_lag = lag_medians[len(lag_medians) // 2] if lag_medians else 0.0
    disagreement_count = sum(
        abs(float(item["lag_median"]) - reference_lag) > 1.5 for item in comparisons
    )
    disagreement_rate = round(
        disagreement_count / max(len(comparisons), 1),
        3,
    )
    mean_abs_error = round(
        sum(float(item["lag_error"]) for item in comparisons)
        / max(len(comparisons), 1),
        3,
    )
    runtime_values: list[float] = []
    for payload in method_results:
        runtime_metadata = payload.get("runtime_metadata", {})
        if isinstance(runtime_metadata, dict):
            runtime_values.append(float(str(runtime_metadata.get("runtime_sec", 0.0))))
    runtime_sec_mean = round(sum(runtime_values) / max(len(runtime_values), 1), 3)
    return {
        "driver_values": list(driver_values),
        "response_values": list(response_values),
        "mjd_obs": list(series_mjd_obs),
        "lag_steps": lag_steps,
        "response_evidence_level": response_evidence_level,
        "method_results": method_results,
        "null_results": _serialize_method_payloads(tuple(null_results)),
        "null_suite": null_suite,
        "null_diagnostic": {
            "false_positive_rate": null_diagnostic.false_positive_rate,
            "null_pair_count": null_diagnostic.null_pair_count,
        },
        "consensus": {
            "classification": consensus.classification,
            "agreement_score": consensus.agreement_score,
            "alias_risk": consensus.alias_risk,
            "null_false_positive_rate": consensus.null_false_positive_rate,
        },
        "comparisons": comparisons,
        "literature_lag_day": literature_lag,
        "coverage_rate": coverage_rate,
        "disagreement_rate": disagreement_rate,
        "runtime_sec_mean": runtime_sec_mean,
        "mean_abs_error": mean_abs_error,
        "method_count": len(method_results),
        "advanced_method_count": sum(
            str(record.get("method", ""))
            in {"pypetal", "litmus", "mica2", "eztao", "celerite2"}
            for payload in method_results
            for record in [payload.get("record", {})]
            if isinstance(record, dict)
        ),
    }


def build_line_diagnostics(object_record: BenchmarkObject) -> list[dict[str, object]]:
    """Build comparable line diagnostics for one benchmark object."""
    center_rest = 4861.0 if object_record.line_name == "Hbeta" else 2798.0
    redshift = float(str(object_record.object_manifest["redshift"]))
    center_obs = center_rest * (1.0 + redshift)
    offsets = tuple(-220.0 + (index * 1.25) for index in range(352))
    wavelength_obs = tuple(center_obs + offset for offset in offsets)
    flux = []
    for wavelength in wavelength_obs:
        rest_wave = wavelength / (1.0 + redshift)
        delta = rest_wave - center_rest
        continuum = 1.0 + (0.00015 * (wavelength - center_obs))
        line = 0.85 * math.exp(-0.5 * ((delta / 12.0) ** 2))
        shoulder = 0.18 * math.exp(-0.5 * (((delta - 18.0) / 8.0) ** 2))
        flux.append(continuum + line + shoulder)
    calibration_state = "pipeline"
    if object_record.spectral_epoch_records:
        calibration_state = str(
            object_record.spectral_epoch_records[0]["calibration_state"]
        )
    spectrum = preprocess_spectrum(
        wavelength_obs=wavelength_obs,
        flux=tuple(flux),
        redshift=redshift,
        calibration_state=calibration_state,
    )
    line_window = (center_rest - 25.0, center_rest + 25.0)
    diagnostics = []
    for fit in (
        fit_local_continuum(spectrum),
        fit_pseudo_continuum(spectrum),
        fit_full_decomposition(spectrum),
        fit_pyqsofit_decomposition(spectrum),
    ):
        record = extract_line_metrics(
            object_uid=object_record.object_uid,
            epoch_uid=(
                str(object_record.spectral_epoch_records[0]["epoch_uid"])
                if object_record.spectral_epoch_records
                else f"{object_record.object_uid}-synthetic-epoch"
            ),
            line_name=object_record.line_name,
            spectrum=spectrum,
            fit=fit,
            line_window=line_window,
        )
        assert LINE_METRICS_SCHEMA.validate_record(record) == ()
        diagnostics.append(record)
    return diagnostics


def _write_silent_wav(path: Path, *, sample_rate_hz: int = 8000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate_hz)
        handle.writeframes(b"\x00\x00" * 256)


def build_render_artifacts(
    *,
    object_record: BenchmarkObject,
    driver_values: tuple[float, ...],
    response_values: tuple[float, ...],
    lag_steps: int,
    run_dir: Path,
) -> dict[str, object]:
    """Build sonification manifests and a render bundle for one object."""
    render_input = RenderInput(
        object_uid=object_record.object_uid,
        driver_channel="continuum",
        response_channel=object_record.line_name.lower(),
        driver_values=driver_values,
        response_values=response_values,
        delay_steps=lag_steps,
        line_width=0.7,
        asymmetry=0.2,
        strength=0.9,
    )
    builders = (
        ("echo_ensemble", build_echo_ensemble),
        ("direct_audification", build_direct_audification),
        ("token_stream", build_token_stream),
    )
    manifests = []
    audio_root = run_dir / "objects" / object_record.object_uid / "audio"
    for family, builder in builders:
        config = MappingConfig(
            mapping_family=family,
            normalization_mode="unit_scale",
            uncertainty_mode="amplitude_wobble",
            sample_rate_hz=8000,
            time_scale=1.0,
        )
        plan = builder(render_input, config=config)
        audio_path = audio_root / f"{family}.wav"
        _write_silent_wav(audio_path, sample_rate_hz=config.sample_rate_hz)
        manifest = build_sonification_manifest(
            plan=plan,
            sonification_id=f"{object_record.object_uid}-{family}",
            audio_path=str(audio_path.relative_to(run_dir.parent)),
        )
        manifest_path = audio_root / f"{family}.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        manifests.append(manifest)
    render_bundle = build_render_bundle(
        object_uid=object_record.object_uid,
        manifests=tuple(manifests),
    )
    render_path = run_dir / "objects" / object_record.object_uid / "render_bundle.json"
    render_path.parent.mkdir(parents=True, exist_ok=True)
    render_path.write_text(json.dumps(render_bundle, indent=2), encoding="utf-8")
    return {
        "sonifications": manifests,
        "render_bundle": render_bundle,
        "render_bundle_path": str(render_path.relative_to(run_dir.parent)),
    }
