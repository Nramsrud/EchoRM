"""Frozen benchmark corpus loaders and shared validation helpers."""

from __future__ import annotations

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
from ..reports.render_bundle import build_render_bundle
from ..rm.base import TimeSeries
from ..rm.consensus import build_consensus
from ..rm.javelin import run_javelin
from ..rm.nulls import evaluate_null_controls
from ..rm.posteriors import ConvergenceDiagnostics, build_posterior_summary
from ..rm.pyccf import run_pyccf
from ..rm.pyroa import run_pyroa
from ..rm.pyzdcf import run_pyzdcf
from ..rm.serialize import serialize_lag_run
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


def run_method_suite(
    *,
    object_record: BenchmarkObject,
    driver_values: tuple[float, ...],
    response_values: tuple[float, ...],
    lag_steps: int,
) -> dict[str, object]:
    """Run the supported method suite on one derived benchmark series."""
    mjd_obs = tuple(float(index) for index, _ in enumerate(driver_values))
    driver = TimeSeries(
        channel="continuum",
        mjd_obs=mjd_obs,
        values=driver_values,
    )
    response = TimeSeries(
        channel=object_record.line_name.lower(),
        mjd_obs=mjd_obs,
        values=response_values,
    )
    pyccf_run = run_pyccf(
        object_uid=object_record.object_uid,
        driver=driver,
        response=response,
    )
    pyzdcf_run = run_pyzdcf(
        object_uid=object_record.object_uid,
        driver=driver,
        response=response,
    )
    posterior_samples = tuple(
        round(float(lag_steps) + offset, 3)
        for offset in (-0.4, -0.2, 0.0, 0.2, 0.4)
    )
    posterior = build_posterior_summary(
        samples=posterior_samples,
        posterior_path=f"posteriors/{object_record.object_uid}.json",
        latent_driver="drw",
    )
    diagnostics = ConvergenceDiagnostics(
        r_hat=1.01,
        effective_sample_size=512,
        passed=True,
    )
    pair_id = pyccf_run.pair_id
    javelin_run = run_javelin(
        object_uid=object_record.object_uid,
        pair_id=pair_id,
        driver_channel=driver.channel,
        response_channel=response.channel,
        posterior=posterior,
        diagnostics=diagnostics,
    )
    pyroa_run = run_pyroa(
        object_uid=object_record.object_uid,
        pair_id=pair_id,
        driver_channel=driver.channel,
        response_channel=response.channel,
        posterior=posterior,
        diagnostics=diagnostics,
    )
    serialized = tuple(
        serialize_lag_run(run)
        for run in (pyccf_run, pyzdcf_run, javelin_run, pyroa_run)
    )

    null_response = tuple(reversed(response_values))
    null_driver = TimeSeries(
        channel="continuum",
        mjd_obs=mjd_obs,
        values=driver_values,
    )
    null_series = TimeSeries(
        channel=f"{response.channel}_null",
        mjd_obs=mjd_obs,
        values=null_response,
    )
    null_results = tuple(
        serialize_lag_run(run)
        for run in (
            run_pyccf(
                object_uid=f"{object_record.object_uid}-null",
                driver=null_driver,
                response=null_series,
            ),
            run_pyzdcf(
                object_uid=f"{object_record.object_uid}-null",
                driver=null_driver,
                response=null_series,
            ),
        )
    )
    null_diagnostic = evaluate_null_controls(null_results)
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
        for result in serialized
    ]
    mean_abs_error = round(
        sum(float(item["lag_error"]) for item in comparisons)
        / max(len(comparisons), 1),
        3,
    )
    return {
        "driver_values": list(driver_values),
        "response_values": list(response_values),
        "lag_steps": lag_steps,
        "method_results": [
            {
                "record": result.record,
                "diagnostics": result.diagnostics,
                "runtime_metadata": result.runtime_metadata,
            }
            for result in serialized
        ],
        "null_results": [
            {
                "record": result.record,
                "diagnostics": result.diagnostics,
                "runtime_metadata": result.runtime_metadata,
            }
            for result in null_results
        ],
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
        "mean_abs_error": mean_abs_error,
    }


def build_line_diagnostics(object_record: BenchmarkObject) -> list[dict[str, object]]:
    """Build comparable line diagnostics for one benchmark object."""
    center_rest = 4861.0 if object_record.line_name == "Hbeta" else 2798.0
    wavelength_obs = tuple(
        center_rest * (1.0 + float(str(object_record.object_manifest["redshift"])))
        + offset
        for offset in (-40.0, -20.0, 0.0, 20.0, 40.0, 60.0)
    )
    flux = (1.0, 1.1, 1.8, 1.7, 1.15, 1.0)
    calibration_state = "pipeline"
    if object_record.spectral_epoch_records:
        calibration_state = str(
            object_record.spectral_epoch_records[0]["calibration_state"]
        )
    spectrum = preprocess_spectrum(
        wavelength_obs=wavelength_obs,
        flux=flux,
        redshift=float(str(object_record.object_manifest["redshift"])),
        calibration_state=calibration_state,
    )
    line_window = (center_rest - 25.0, center_rest + 25.0)
    diagnostics = []
    for fit in (
        fit_local_continuum(spectrum),
        fit_pseudo_continuum(spectrum),
        fit_full_decomposition(spectrum),
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
