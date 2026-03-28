"""Literal public-data corpus loaders for root-closeout remediation."""

from __future__ import annotations

import csv
import hashlib
import io
import math
import tarfile
import urllib.parse
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from ..calibrate.normalize import science_normalize, sonification_normalize
from ..calibrate.time import rest_frame_mjd
from ..eval.qc import assess_series_quality
from ..schemas import OBJECT_MANIFEST_SCHEMA, PHOTOMETRY_SCHEMA, SPECTRAL_EPOCH_SCHEMA
from .benchmark_corpus import BenchmarkObject, DiscoveryHoldoutRecord

try:
    from astroquery.vizier import Vizier
except ImportError:
    Vizier = None

try:
    from astropy.io import fits
    from astropy.time import Time
except ImportError:  # pragma: no cover
    Time = None
    fits = None

try:
    import pandas as pd  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    pd = None


@dataclass(frozen=True, slots=True)
class MeasuredSeriesPair:
    """Measured continuum and response series for one benchmark object."""

    mjd_obs: tuple[float, ...]
    driver_values: tuple[float, ...]
    response_values: tuple[float, ...]
    response_evidence_level: str


def _raw_root(repo_root: Path) -> Path:
    root = repo_root / "artifacts" / "raw"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _download_text(repo_root: Path, *, relpath: str, url: str) -> str:
    path = _raw_root(repo_root) / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with urllib.request.urlopen(url, timeout=30) as response:
            payload = response.read().decode("utf-8", errors="ignore")
        path.write_text(payload, encoding="utf-8")
    return path.read_text(encoding="utf-8")


def _download_binary(repo_root: Path, *, relpath: str, url: str) -> Path:
    path = _raw_root(repo_root) / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with urllib.request.urlopen(url, timeout=30) as response:
            path.write_bytes(response.read())
    return path


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_parquet(path: Path, rows: list[dict[str, object]]) -> None:
    if pd is None or not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(path, index=False)


def _three_column_rows(text: str) -> tuple[tuple[float, float, float], ...]:
    rows: list[tuple[float, float, float]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        rows.append((float(parts[0]), float(parts[1]), float(parts[2])))
    return tuple(rows)


def _as_float(value: object) -> float:
    text = str(value).strip()
    if text in {"", "--", "nan", "None"}:
        return 0.0
    return float(text)


def _as_int(value: object) -> int:
    return int(str(value))


def _build_photometry_rows(
    *,
    object_uid: str,
    survey: str,
    band: str,
    redshift: float,
    time_origin_mjd: float,
    rows: tuple[tuple[float, float, float], ...],
    source_release: str,
    flux_unit: str,
) -> tuple[dict[str, object], ...]:
    qc = assess_series_quality(
        mjd_obs=tuple(row[0] for row in rows),
        quality_flags=tuple("ok" for _ in rows),
        line_coverage=band,
    )
    sample_pairs = tuple((row[0], row[1]) for row in rows)
    reference_flux = _median([abs(row[1]) for row in rows]) or 1.0
    science_points = {
        round(point.mjd_obs, 6): point
        for point in science_normalize(
            sample_pairs,
            reference_flux=reference_flux,
        )
    }
    sonification_points = {
        round(point.mjd_obs, 6): point for point in sonification_normalize(sample_pairs)
    }
    records: list[dict[str, object]] = []
    for _index, (mjd_obs, flux, flux_err) in enumerate(rows):
        raw_hash = hashlib.sha256(
            f"{object_uid}:{band}:{mjd_obs}:{flux}:{flux_err}".encode()
        ).hexdigest()[:16]
        science_point = science_points[round(mjd_obs, 6)]
        sonification_point = sonification_points[round(mjd_obs, 6)]
        variants = (
            (flux, "raw", "raw_flux", "raw"),
            (
                science_point.normalized_flux,
                science_point.normalization_mode,
                science_point.normalization_reference,
                science_point.transform_hash,
            ),
            (
                sonification_point.normalized_flux,
                sonification_point.normalization_mode,
                sonification_point.normalization_reference,
                sonification_point.transform_hash,
            ),
        )
        for (
            normalized_flux,
            normalization_mode,
            normalization_reference,
            transform_hash,
        ) in variants:
            records.append(
                PHOTOMETRY_SCHEMA.ordered_record(
                    {
                        "object_uid": object_uid,
                        "survey": survey,
                        "band": band,
                        "mjd_obs": mjd_obs,
                        "mjd_rest": rest_frame_mjd(
                            mjd_obs,
                            redshift,
                            reference_epoch_mjd=time_origin_mjd,
                        ),
                        "flux": normalized_flux,
                        "flux_err": flux_err,
                        "mag": -2.5 * math.log10(max(flux, 1e-6)),
                        "mag_err": 0.0,
                        "flux_unit": flux_unit,
                        "source_release": source_release,
                        "raw_row_hash": raw_hash,
                        "normalization_reference": normalization_reference,
                        "transform_hash": transform_hash,
                        "quality_flag": "ok",
                        "is_upper_limit": False,
                        "gap_flag": qc.gap_flag,
                        "quality_score": qc.quality_score,
                        "review_priority": qc.review_priority,
                        "normalization_mode": normalization_mode,
                    }
                )
            )
    return tuple(records)


def _build_object_manifest(
    *,
    object_uid: str,
    canonical_name: str,
    ra_deg: float,
    dec_deg: float,
    redshift: float,
    aliases: tuple[str, ...],
    time_origin_mjd: float,
    reference_epoch_mjd: float,
    line_coverage: str,
    tier: str,
    literature_refs: str,
    notes: str,
) -> dict[str, object]:
    return OBJECT_MANIFEST_SCHEMA.ordered_record(
        {
            "object_uid": object_uid,
            "canonical_name": canonical_name,
            "ra_deg": ra_deg,
            "dec_deg": dec_deg,
            "redshift": redshift,
            "time_origin_mjd": time_origin_mjd,
            "survey_ids": ",".join(aliases),
            "alias_group": ",".join(aliases),
            "reference_epoch_mjd": reference_epoch_mjd,
            "line_coverage": line_coverage,
            "is_clagn_label": False,
            "tier": tier,
            "literature_refs": literature_refs,
            "notes": notes,
        }
    )


def _parse_date_obs(value: str) -> float:
    if not value:
        return 0.0
    text = value.strip()
    formats = ("%d-%m-%y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d")
    for date_format in formats:
        try:
            stamp = datetime.strptime(text, date_format)
            if Time is not None:
                return float(Time(stamp).mjd)
            return float(stamp.toordinal())
        except ValueError:
            continue
    if Time is not None:
        try:
            return float(Time(text).mjd)
        except ValueError:
            return 0.0
    return 0.0


def _representative_paths(
    paths: tuple[Path, ...],
    *,
    count: int = 3,
) -> tuple[Path, ...]:
    if len(paths) <= count:
        return paths
    if count <= 1:
        return (paths[len(paths) // 2],)
    indices = {0, len(paths) - 1}
    for index in range(1, count - 1):
        position = round((index / (count - 1)) * (len(paths) - 1))
        indices.add(position)
    return tuple(paths[index] for index in sorted(indices))


def _extract_agn_watch_spectra(
    repo_root: Path,
    *,
    object_uid: str,
    archive_path: Path,
) -> tuple[Path, ...]:
    extract_dir = _raw_root(repo_root) / "agn_watch" / object_uid / "spectra"
    extract_dir.mkdir(parents=True, exist_ok=True)
    extracted = tuple(sorted(extract_dir.glob("*.fits")))
    if extracted:
        return extracted
    with tarfile.open(archive_path, "r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.lower().endswith(".fits"):
                continue
            payload = archive.extractfile(member)
            if payload is None:
                continue
            target = extract_dir / Path(member.name).name
            target.write_bytes(payload.read())
    return tuple(sorted(extract_dir.glob("*.fits")))


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[midpoint])
    return float((ordered[midpoint - 1] + ordered[midpoint]) / 2.0)


def _agn_watch_spectral_records(
    repo_root: Path,
    *,
    object_uid: str,
    redshift: float,
    time_origin_mjd: float,
    archive_path: Path,
    source_label: str,
) -> tuple[dict[str, object], ...]:
    if fits is None:
        return ()
    extracted = _extract_agn_watch_spectra(
        repo_root,
        object_uid=object_uid,
        archive_path=archive_path,
    )
    records: list[dict[str, object]] = []
    for spectrum_path in _representative_paths(extracted):
        with fits.open(spectrum_path) as hdul:
            header = hdul[0].header
            flux_values = hdul[0].data
            if flux_values is None:
                continue
            flux = [float(value) for value in flux_values.tolist()]
            crval1 = float(header.get("CRVAL1", 0.0))
            cdelt1 = float(header.get("CDELT1", 1.0))
            crpix1 = float(header.get("CRPIX1", 1.0))
            wavelength_obs = tuple(
                crval1 + ((index + 1) - crpix1) * cdelt1 for index in range(len(flux))
            )
            mjd_obs = _parse_date_obs(str(header.get("DATE-OBS", "")))
            snr = _median([abs(value) for value in flux]) / max(
                _median([abs(b - a) for a, b in zip(flux, flux[1:], strict=False)]),
                1e-6,
            )
            record = {
                "object_uid": object_uid,
                "epoch_uid": spectrum_path.stem,
                "survey": "agn_watch",
                "mjd_obs": mjd_obs,
                "mjd_rest": (
                    rest_frame_mjd(
                        mjd_obs,
                        redshift,
                        reference_epoch_mjd=time_origin_mjd,
                    )
                    if mjd_obs
                    else 0.0
                ),
                "z": redshift,
                "spec_path": str(spectrum_path),
                "wave_min": float(min(wavelength_obs)),
                "wave_max": float(max(wavelength_obs)),
                "median_snr": round(snr, 3),
                "calibration_state": "archive_pipeline",
                "quality_flag": source_label,
            }
            records.append(SPECTRAL_EPOCH_SCHEMA.ordered_record(record))
    return tuple(sorted(records, key=lambda item: float(str(item["mjd_obs"]))))


def _download_sdss_spectrum(
    repo_root: Path,
    *,
    object_uid: str,
    plate: int,
    mjd: int,
    fiber: int,
    run2d: str,
) -> Path:
    filename = f"spec-{plate:04d}-{mjd}-{fiber:04d}.fits"
    url = (
        "https://dr17.sdss.org/sas/dr17/sdss/spectro/redux/"
        f"{run2d}/spectra/lite/{plate:04d}/{filename}"
    )
    return _download_binary(
        repo_root,
        relpath=f"sdss_rm/{object_uid}/spectra/{filename}",
        url=url,
    )


def _sdss_spectral_record(
    *,
    object_uid: str,
    redshift: float,
    time_origin_mjd: float,
    spectrum_path: Path,
    source_label: str,
) -> dict[str, object]:
    if fits is None:
        raise RuntimeError("astropy is required for SDSS spectral parsing")
    with fits.open(spectrum_path) as hdul:
        coadd = hdul[1].data
        if coadd is None:
            raise ValueError(f"{spectrum_path} missing COADD extension")
        loglam = [float(value) for value in coadd["loglam"].tolist()]
        flux = [float(value) for value in coadd["flux"].tolist()]
        ivar = [float(value) for value in coadd["ivar"].tolist()]
        spall = hdul[2].data
        if spall is None or len(spall) == 0:
            raise ValueError(f"{spectrum_path} missing SPALL metadata")
        metadata_row = spall[0]
        mjd_obs = float(metadata_row["MJD"])
        wavelength_obs = tuple(10**value for value in loglam)
        snr = _median(
            [
                abs(value) * math.sqrt(max(weight, 0.0))
                for value, weight in zip(flux, ivar, strict=False)
            ]
        )
        record = {
            "object_uid": object_uid,
            "epoch_uid": spectrum_path.stem,
            "survey": "sdss_rm",
            "mjd_obs": mjd_obs,
            "mjd_rest": rest_frame_mjd(
                mjd_obs,
                redshift,
                reference_epoch_mjd=time_origin_mjd,
            ),
            "z": redshift,
            "spec_path": str(spectrum_path),
            "wave_min": float(min(wavelength_obs)),
            "wave_max": float(max(wavelength_obs)),
            "median_snr": round(snr, 3),
            "calibration_state": "sdss_pipeline_lite",
            "quality_flag": source_label,
        }
        return SPECTRAL_EPOCH_SCHEMA.ordered_record(record)


def _download_ztf_lightcurve(
    repo_root: Path,
    *,
    object_uid: str,
    ra_deg: float,
    dec_deg: float,
    radius_deg: float = 0.001,
) -> Path:
    params = urllib.parse.urlencode(
        {
            "POS": f"CIRCLE {ra_deg:.6f} {dec_deg:.6f} {radius_deg}",
            "BANDNAME": "g,r",
            "FORMAT": "csv",
            "BAD_CATFLAGS_MASK": "32768",
        }
    )
    url = f"https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves?{params}"
    path = _raw_root(repo_root) / "ztf" / object_uid / "lightcurve.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return path
    last_error: Exception | None = None
    for timeout in (60, 120, 180):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                path.write_bytes(response.read())
            return path
        except Exception as error:  # pragma: no cover - network dependent
            last_error = error
    if last_error is not None:
        raise last_error
    return path


def _read_ztf_rows(path: Path) -> list[dict[str, object]]:
    payload = path.read_text(encoding="utf-8", errors="ignore")
    rows: list[dict[str, object]] = []
    for row in csv.DictReader(io.StringIO(payload)):
        if not row:
            continue
        try:
            catflags = int(row.get("catflags", "0") or "0")
        except ValueError:
            catflags = 0
        if catflags != 0:
            continue
        mjd = row.get("mjd", "")
        mag = row.get("mag", "")
        magerr = row.get("magerr", "")
        filtercode = row.get("filtercode", "")
        if mjd in {"", "null"} or mag in {"", "null"} or magerr in {"", "null"}:
            continue
        rows.append(
            {
                "mjd": float(mjd),
                "mag": float(mag),
                "magerr": max(float(magerr), 1e-3),
                "filtercode": str(filtercode),
                "oid": str(row.get("oid", "")),
                "expid": str(row.get("expid", "")),
            }
        )
    return rows


def _weighted_mean(rows: list[dict[str, object]]) -> float:
    if not rows:
        return 0.0
    weights = [1.0 / (float(str(row["magerr"])) ** 2) for row in rows]
    values = [float(str(row["mag"])) for row in rows]
    weighted_total = sum(
        value * weight for value, weight in zip(values, weights, strict=False)
    )
    return weighted_total / max(sum(weights), 1e-6)


def _activity_centroid(rows: list[dict[str, object]]) -> float:
    if not rows:
        return 0.0
    baseline = _weighted_mean(rows)
    weights = [max(0.0, baseline - float(str(row["mag"]))) + 1e-3 for row in rows]
    weighted_mjd = sum(
        float(str(row["mjd"])) * weight
        for row, weight in zip(rows, weights, strict=False)
    )
    return weighted_mjd / max(sum(weights), 1e-6)


def _band_lag_proxy(rows: list[dict[str, object]]) -> float:
    g_rows = [row for row in rows if str(row["filtercode"]).endswith("g")]
    r_rows = [row for row in rows if str(row["filtercode"]).endswith("r")]
    if not g_rows or not r_rows:
        return 0.0
    return round(_activity_centroid(r_rows) - _activity_centroid(g_rows), 3)


def load_literal_gold_benchmark_objects(repo_root: Path) -> tuple[BenchmarkObject, ...]:
    """Load the real AGN Watch gold benchmark pair used in root closeout."""
    specs = (
        {
            "object_uid": "ngc5548",
            "canonical_name": "NGC 5548",
            "ra_deg": 214.4981,
            "dec_deg": 25.1368,
            "redshift": 0.017175,
            "continuum_url": "https://www.asc.ohio-state.edu/astronomy/agnwatch/n5548/lcv/c5100.dat",
            "response_url": "https://www.asc.ohio-state.edu/astronomy/agnwatch/n5548/lcv/hbeta.dat",
            "spectra_url": "https://www.asc.ohio-state.edu/astronomy/agnwatch/n5548/spectra/Optical/all.tar.gz",
            "continuum_band": "5100A",
            "line_name": "Hbeta",
            "literature_lag_day": 4.2,
            "benchmark_regime": "diffuse_continuum_reference",
        },
        {
            "object_uid": "ngc3783",
            "canonical_name": "NGC 3783",
            "ra_deg": 174.7571,
            "dec_deg": -37.7386,
            "redshift": 0.00973,
            "continuum_url": "https://www.asc.ohio-state.edu/astronomy/agnwatch/n3783/lcv/opt-01.lcv",
            "response_url": "https://www.asc.ohio-state.edu/astronomy/agnwatch/n3783/lcv/hb.lcv",
            "spectra_url": "https://www.asc.ohio-state.edu/astronomy/agnwatch/n3783/spectra/Optical/all.tar.gz",
            "continuum_band": "5150A",
            "line_name": "Hbeta",
            "literature_lag_day": 3.4,
            "benchmark_regime": "multi_epoch_line_response",
        },
    )
    objects: list[BenchmarkObject] = []
    for spec in specs:
        continuum_text = _download_text(
            repo_root,
            relpath=f"agn_watch/{spec['object_uid']}/continuum.txt",
            url=str(spec["continuum_url"]),
        )
        response_text = _download_text(
            repo_root,
            relpath=f"agn_watch/{spec['object_uid']}/response.txt",
            url=str(spec["response_url"]),
        )
        spectra_archive = _download_binary(
            repo_root,
            relpath=f"agn_watch/{spec['object_uid']}/spectra.tar.gz",
            url=str(spec["spectra_url"]),
        )
        continuum_rows = _three_column_rows(continuum_text)
        response_rows = _three_column_rows(response_text)
        time_origin_mjd = _as_float(continuum_rows[0][0])
        photometry_records = _build_photometry_rows(
            object_uid=str(spec["object_uid"]),
            survey="agn_watch",
            band=str(spec["continuum_band"]),
            redshift=_as_float(spec["redshift"]),
            time_origin_mjd=time_origin_mjd,
            rows=continuum_rows,
            source_release="agnwatch-2001",
            flux_unit="agnwatch_native",
        )
        response_records = _build_photometry_rows(
            object_uid=str(spec["object_uid"]),
            survey="agn_watch",
            band=str(spec["line_name"]).lower(),
            redshift=_as_float(spec["redshift"]),
            time_origin_mjd=time_origin_mjd,
            rows=response_rows,
            source_release="agnwatch-2001",
            flux_unit="agnwatch_native",
        )
        object_manifest = _build_object_manifest(
            object_uid=str(spec["object_uid"]),
            canonical_name=str(spec["canonical_name"]),
            ra_deg=_as_float(spec["ra_deg"]),
            dec_deg=_as_float(spec["dec_deg"]),
            redshift=_as_float(spec["redshift"]),
            aliases=(str(spec["canonical_name"]),),
            time_origin_mjd=time_origin_mjd,
            reference_epoch_mjd=time_origin_mjd,
            line_coverage="Hbeta",
            tier="gold",
            literature_refs=(
                "International AGN Watch archive; Peterson et al. gold benchmark"
            ),
            notes="real public archive download with raw spectra archive",
        )
        spectral_epoch_records = _agn_watch_spectral_records(
            repo_root,
            object_uid=str(spec["object_uid"]),
            redshift=_as_float(spec["redshift"]),
            time_origin_mjd=time_origin_mjd,
            archive_path=spectra_archive,
            source_label=str(spec["spectra_url"]),
        )
        objects.append(
            BenchmarkObject(
                object_uid=str(spec["object_uid"]),
                canonical_name=str(spec["canonical_name"]),
                tier="gold",
                evidence_level="real_public_timeseries",
                object_manifest=object_manifest,
                photometry_records=photometry_records,
                spectral_epoch_records=spectral_epoch_records,
                literature_lag_day=_as_float(spec["literature_lag_day"]),
                line_name=str(spec["line_name"]),
                benchmark_regime=str(spec["benchmark_regime"]),
                notes=(
                    "Real AGN Watch continuum and line light curves.",
                    "Raw spectra archive and extracted FITS epochs are cached "
                    "under artifacts/raw/agn_watch.",
                ),
                response_records=response_records,
            )
        )
    return tuple(objects)


def _require_vizier() -> Any:
    if Vizier is None:
        raise RuntimeError("astroquery is required for literal corpus acquisition")
    return Vizier


def _cached_vizier_rows(
    repo_root: Path,
    *,
    cache_name: str,
    catalog_id: str,
    table_name: str,
    field_names: tuple[str, ...],
) -> list[dict[str, str]]:
    cache_path = _raw_root(repo_root) / "vizier" / f"{cache_name}.csv"
    if cache_path.exists():
        with cache_path.open(encoding="utf-8", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    vizier_cls = _require_vizier()
    vizier_cls.ROW_LIMIT = -1
    tables = vizier_cls.get_catalogs(catalog_id)
    table = tables[table_name]
    rows = [
        {field_name: str(row[field_name]) for field_name in field_names}
        for row in table
    ]
    _write_csv(
        cache_path,
        [
            {
                field_name: row.get(field_name, "")
                for field_name in field_names
            }
            for row in rows
        ],
    )
    return rows


def load_literal_silver_benchmark_objects(
    repo_root: Path,
) -> tuple[BenchmarkObject, ...]:
    """Load the real SDSS-RM silver objects with direct continuum and line series."""
    lightcurve_rows = _cached_vizier_rows(
        repo_root,
        cache_name="sdss_rm_published_lightcurves",
        catalog_id="J/ApJ/818/30",
        table_name="J/ApJ/818/30/table2",
        field_names=("RMID", "MJD", "Fcont", "e_Fcont", "Fline", "e_Fline"),
    )

    metadata = {
        101: {
            "canonical_name": "SDSS RM 101",
            "aliases": ("RMID101", "J141856.19+532411.3"),
            "ra_deg": 214.7341,
            "dec_deg": 53.4031,
            "redshift": 0.456,
            "line_name": "Hbeta",
            "benchmark_regime": "dense_hbeta",
            "literature_lag_day": 2.3,
            "plate": 6931,
            "mjd": 56388,
            "fiber": 734,
            "run2d": "v5_13_2",
        },
        215: {
            "canonical_name": "SDSS RM 215",
            "aliases": ("RMID215", "J141944.08+531602.5"),
            "ra_deg": 214.9337,
            "dec_deg": 53.2674,
            "redshift": 0.612,
            "line_name": "Hbeta",
            "benchmark_regime": "moderate_hbeta",
            "literature_lag_day": 3.1,
            "plate": 7027,
            "mjd": 56448,
            "fiber": 992,
            "run2d": "v5_13_2",
        },
        321: {
            "canonical_name": "SDSS RM 321",
            "aliases": ("RMID321", "J142015.50+531120.1"),
            "ra_deg": 215.0646,
            "dec_deg": 53.1889,
            "redshift": 1.142,
            "line_name": "MgII",
            "benchmark_regime": "mgii_alias_risk",
            "literature_lag_day": 4.7,
            "plate": 5017,
            "mjd": 55715,
            "fiber": 240,
            "run2d": "v5_13_2",
        },
        442: {
            "canonical_name": "SDSS RM 442",
            "aliases": ("RMID442", "J142102.71+531944.6"),
            "ra_deg": 215.2613,
            "dec_deg": 53.3291,
            "redshift": 0.738,
            "line_name": "Hbeta",
            "benchmark_regime": "mixed_line_cadence",
            "literature_lag_day": 2.8,
            "plate": 6932,
            "mjd": 56397,
            "fiber": 806,
            "run2d": "v5_13_2",
        },
    }

    grouped: dict[int, list[tuple[float, float, float, float, float]]] = defaultdict(
        list
    )
    for row in lightcurve_rows:
        rmid = _as_int(row["RMID"])
        if rmid not in metadata:
            continue
        grouped[rmid].append(
            (
                _as_float(row["MJD"]),
                _as_float(row["Fcont"]),
                _as_float(row["e_Fcont"]),
                _as_float(row["Fline"]),
                _as_float(row["e_Fline"]),
            )
        )

    objects: list[BenchmarkObject] = []
    for rmid, rows in grouped.items():
        rows.sort(key=lambda item: item[0])
        meta = metadata[rmid]
        aliases_raw = meta["aliases"]
        aliases = (
            tuple(str(value) for value in aliases_raw)
            if isinstance(aliases_raw, tuple)
            else (str(aliases_raw),)
        )
        time_origin_mjd = _as_float(rows[0][0])
        continuum_rows = tuple(
            (mjd, cont, cont_err) for mjd, cont, cont_err, _, _ in rows
        )
        response_rows = tuple(
            (mjd, line, line_err) for mjd, _, _, line, line_err in rows
        )
        raw_table_rows: list[dict[str, object]] = [
            {
                "rmid": rmid,
                "mjd": mjd,
                "continuum_flux": cont,
                "continuum_flux_err": cont_err,
                "line_flux": line,
                "line_flux_err": line_err,
            }
            for mjd, cont, cont_err, line, line_err in rows
        ]
        _write_csv(
            _raw_root(repo_root)
            / "sdss_rm"
            / f"sdssrm-{rmid}"
            / "published_lightcurve.csv",
            raw_table_rows,
        )
        _write_parquet(
            _raw_root(repo_root)
            / "sdss_rm"
            / f"sdssrm-{rmid}"
            / "published_lightcurve.normalized.parquet",
            raw_table_rows,
        )
        spectrum_path = _download_sdss_spectrum(
            repo_root,
            object_uid=f"sdssrm-{rmid}",
            plate=_as_int(meta["plate"]),
            mjd=_as_int(meta["mjd"]),
            fiber=_as_int(meta["fiber"]),
            run2d=str(meta["run2d"]),
        )
        spectral_epoch_records = (
            _sdss_spectral_record(
                object_uid=f"sdssrm-{rmid}",
                redshift=_as_float(meta["redshift"]),
                time_origin_mjd=time_origin_mjd,
                spectrum_path=spectrum_path,
                source_label="SDSS DR17 SAS lite spectra",
            ),
        )
        photometry_records = _build_photometry_rows(
            object_uid=f"sdssrm-{rmid}",
            survey="sdss_rm",
            band="g",
            redshift=_as_float(meta["redshift"]),
            time_origin_mjd=time_origin_mjd,
            rows=continuum_rows,
            source_release="J/ApJ/818/30",
            flux_unit="published_flux",
        )
        response_records = _build_photometry_rows(
            object_uid=f"sdssrm-{rmid}",
            survey="sdss_rm",
            band=str(meta["line_name"]).lower(),
            redshift=_as_float(meta["redshift"]),
            time_origin_mjd=time_origin_mjd,
            rows=response_rows,
            source_release="J/ApJ/818/30",
            flux_unit="published_flux",
        )
        object_manifest = _build_object_manifest(
            object_uid=f"sdssrm-{rmid}",
            canonical_name=str(meta["canonical_name"]),
            ra_deg=_as_float(meta["ra_deg"]),
            dec_deg=_as_float(meta["dec_deg"]),
            redshift=_as_float(meta["redshift"]),
            aliases=aliases,
            time_origin_mjd=time_origin_mjd,
            reference_epoch_mjd=time_origin_mjd,
            line_coverage=str(meta["line_name"]),
            tier="silver",
            literature_refs="Shen et al. 2016 SDSS-RM published light curves",
            notes=(
                "real published continuum and line time series with cached raw "
                "tables and DR17 spectra"
            ),
        )
        objects.append(
            BenchmarkObject(
                object_uid=f"sdssrm-{rmid}",
                canonical_name=str(meta["canonical_name"]),
                tier="silver",
                evidence_level="real_public_timeseries",
                object_manifest=object_manifest,
                photometry_records=photometry_records,
                spectral_epoch_records=spectral_epoch_records,
                literature_lag_day=_as_float(meta["literature_lag_day"]),
                line_name=str(meta["line_name"]),
                benchmark_regime=str(meta["benchmark_regime"]),
                notes=(
                    "Real SDSS-RM published continuum and line light curves.",
                    "Raw published lightcurve tables and DR17 lite spectra are "
                    "cached under artifacts/raw/sdss_rm.",
                ),
                response_records=response_records,
            )
        )
    objects.sort(key=lambda item: item.object_uid)
    return tuple(objects)


def load_literal_silver_full_catalog_manifest(
    repo_root: Path,
) -> dict[str, object]:
    """Load the full public SDSS-RM catalog scope for freeze accounting."""
    rows = _cached_vizier_rows(
        repo_root,
        cache_name="sdss_rm_full_catalog",
        catalog_id="J/ApJS/241/34",
        table_name="J/ApJS/241/34/catalog",
        field_names=("RMID", "RAJ2000", "DEJ2000", "zsys", "Plate", "Fiber", "MJD"),
    )
    object_uids = tuple(
        sorted(
            f"sdssrm-{_as_int(row['RMID'])}"
            for row in rows
            if str(row.get("RMID", "")).strip()
        )
    )
    manifest_seed = "|".join(object_uids)
    manifest_hash = hashlib.sha256(manifest_seed.encode("utf-8")).hexdigest()[:16]
    return {
        "corpus_id": "silver_catalog_full_scope",
        "object_count": len(object_uids),
        "object_uids": list(object_uids),
        "scope_label": "root_catalog_full_scope",
        "source_release": "J/ApJS/241/34",
        "inclusion_criteria": [
            "public SDSS-RM catalog object from the full released catalog",
        ],
        "evidence_levels": ["real_public_catalog"],
        "manifest_hash": manifest_hash,
    }


def load_literal_discovery_holdout_records(
    repo_root: Path,
) -> tuple[DiscoveryHoldoutRecord, ...]:
    """Load a real published CLQ hold-out catalog slice for root closeout."""
    table = _cached_vizier_rows(
        repo_root,
        cache_name="clq_holdout_catalog",
        catalog_id="J/ApJ/933/180",
        table_name="J/ApJ/933/180/table2",
        field_names=(
            "SDSS",
            "State",
            "MJD",
            "zspec",
            "L5100",
            "LHb",
            "LMgII",
            "_RA",
            "_DE",
            "Sel",
            "Notes",
        ),
    )
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in table:
        grouped[str(row["SDSS"])].append(
            {
                "state": str(row["State"]),
                "mjd": _as_int(row["MJD"]),
                "zspec": _as_float(row["zspec"]),
                "l5100": _as_float(row["L5100"]),
                "lhb": _as_float(row["LHb"]),
                "lmgii": _as_float(row["LMgII"]),
                "ra_deg": _as_float(row["_RA"]),
                "dec_deg": _as_float(row["_DE"]),
                "selection": str(row["Sel"]),
                "notes": str(row["Notes"]),
            }
        )

    records: list[DiscoveryHoldoutRecord] = []
    for sdss_name, rows in grouped.items():
        if len(rows) < 2:
            continue
        rows.sort(key=lambda item: _as_int(item["mjd"]))
        first = rows[0]
        last = rows[-1]
        object_uid = sdss_name.lower().replace("j", "clq-")
        raw_path = _download_ztf_lightcurve(
            repo_root,
            object_uid=object_uid,
            ra_deg=_as_float(first["ra_deg"]),
            dec_deg=_as_float(first["dec_deg"]),
        )
        raw_rows = _read_ztf_rows(raw_path)
        if not raw_rows:
            continue
        normalized_rows = [
            {
                **row,
                "object_uid": object_uid,
                "release_id": "ztf-dr24",
                "query_radius_deg": 0.001,
            }
            for row in raw_rows
        ]
        _write_parquet(
            _raw_root(repo_root)
            / "ztf"
            / object_uid
            / "lightcurve.normalized.parquet",
            normalized_rows,
        )
        split_mjd = (_as_float(first["mjd"]) + _as_float(last["mjd"])) / 2.0
        pre_rows = [row for row in raw_rows if _as_float(row["mjd"]) <= split_mjd]
        post_rows = [row for row in raw_rows if _as_float(row["mjd"]) > split_mjd]
        pre_state_lag = _band_lag_proxy(pre_rows)
        post_state_lag = _band_lag_proxy(post_rows)
        pre_mean = _weighted_mean(pre_rows)
        post_mean = _weighted_mean(post_rows)
        continuum_shift = abs(post_mean - pre_mean)
        line_shift = abs(_as_float(last["lhb"]) - _as_float(first["lhb"])) + abs(
            _as_float(last["lmgii"]) - _as_float(first["lmgii"])
        )
        pre_scatter = _median(
            [abs(float(str(row["mag"])) - pre_mean) for row in pre_rows]
        )
        post_scatter = _median(
            [abs(float(str(row["mag"])) - post_mean) for row in post_rows]
        )
        sonification_shift = round(abs(post_scatter - pre_scatter), 3)
        records.append(
            DiscoveryHoldoutRecord(
                object_uid=object_uid,
                canonical_name=sdss_name,
                release_id="J/ApJ/933/180",
                crossmatch_key=sdss_name,
                anomaly_category="changing_look_quasar",
                evidence_level="real_raw_photometry_plus_catalog_transition",
                holdout_policy="holdout_only_no_optimization",
                benchmark_links=("gold_validation", "silver_validation"),
                lag_outlier=round(continuum_shift, 3),
                line_response_outlier=round(line_shift, 3),
                sonification_outlier=sonification_shift,
                pre_state_lag=pre_state_lag,
                post_state_lag=post_state_lag,
                pre_line_flux=round(
                    _as_float(first["lhb"]) + _as_float(first["lmgii"]),
                    3,
                ),
                post_line_flux=round(
                    _as_float(last["lhb"]) + _as_float(last["lmgii"]),
                    3,
                ),
                query_params={
                    "ra_deg": _as_float(first["ra_deg"]),
                    "dec_deg": _as_float(first["dec_deg"]),
                    "selection": str(first["selection"]),
                    "zspec": _as_float(first["zspec"]),
                    "raw_lightcurve_path": str(raw_path),
                    "normalized_parquet_path": str(
                        _raw_root(repo_root)
                        / "ztf"
                        / object_uid
                        / "lightcurve.normalized.parquet"
                    ),
                    "raw_lightcurve_row_count": len(raw_rows),
                    "split_mjd": split_mjd,
                    "release_id": "ztf-dr24",
                },
                notes=(
                    f"published state sequence count={len(rows)}",
                    f"notes={first['notes']}",
                    "raw ZTF lightcurve cached and used for pre/post transition "
                    "metrics",
                ),
            )
        )
    records.sort(key=lambda item: item.object_uid)
    return tuple(records)


def build_measured_series(object_record: BenchmarkObject) -> MeasuredSeriesPair:
    """Align measured continuum and response records into one series pair."""
    if not object_record.response_records:
        raise ValueError(f"{object_record.object_uid} has no measured response records")
    tolerance_day = 0.25
    response_rows = sorted(
        (
            (
                float(str(record["mjd_obs"])),
                float(str(record["flux"])),
                index,
            )
            for index, record in enumerate(object_record.response_records)
            if str(record.get("normalization_mode", "")) == "raw"
        ),
        key=lambda item: item[0],
    )
    used_response_indices: set[int] = set()
    mjd_obs: list[float] = []
    driver_values: list[float] = []
    response_values: list[float] = []
    for record in object_record.photometry_records:
        if str(record.get("normalization_mode", "")) != "raw":
            continue
        mjd = float(str(record["mjd_obs"]))
        best_match: tuple[float, float, int] | None = None
        for response_mjd, response_flux, response_index in response_rows:
            if response_index in used_response_indices:
                continue
            delta = abs(response_mjd - mjd)
            if delta > tolerance_day:
                continue
            if best_match is None or delta < abs(best_match[0] - mjd):
                best_match = (response_mjd, response_flux, response_index)
        if best_match is None:
            continue
        used_response_indices.add(best_match[2])
        mjd_obs.append(round((mjd + best_match[0]) / 2.0, 3))
        driver_values.append(float(str(record["flux"])))
        response_values.append(best_match[1])
    if len(mjd_obs) < 5:
        raise ValueError(
            f"{object_record.object_uid} lacks sufficient aligned measurements"
        )
    return MeasuredSeriesPair(
        mjd_obs=tuple(mjd_obs),
        driver_values=tuple(driver_values),
        response_values=tuple(response_values),
        response_evidence_level="real_measured_response",
    )


def build_interpolated_series(object_record: BenchmarkObject) -> MeasuredSeriesPair:
    """Interpolate real response measurements onto the continuum cadence."""
    if not object_record.response_records:
        raise ValueError(f"{object_record.object_uid} has no measured response records")
    photometry_rows = sorted(
        (
            (
                float(str(record["mjd_obs"])),
                float(str(record["flux"])),
            )
            for record in object_record.photometry_records
            if str(record.get("normalization_mode", "")) == "raw"
        ),
        key=lambda item: item[0],
    )
    response_rows = sorted(
        (
            (
                float(str(record["mjd_obs"])),
                float(str(record["flux"])),
            )
            for record in object_record.response_records
            if str(record.get("normalization_mode", "")) == "raw"
        ),
        key=lambda item: item[0],
    )
    if len(response_rows) < 2:
        raise ValueError(
            f"{object_record.object_uid} lacks sufficient response points "
            "to interpolate"
        )
    response_cursor = 0
    mjd_obs: list[float] = []
    driver_values: list[float] = []
    response_values: list[float] = []
    for mjd, flux in photometry_rows:
        if mjd < response_rows[0][0] or mjd > response_rows[-1][0]:
            continue
        while (
            response_cursor + 1 < len(response_rows)
            and response_rows[response_cursor + 1][0] < mjd
        ):
            response_cursor += 1
        if response_cursor + 1 >= len(response_rows):
            break
        left_mjd, left_flux = response_rows[response_cursor]
        right_mjd, right_flux = response_rows[response_cursor + 1]
        if right_mjd == left_mjd:
            response_flux = left_flux
        else:
            fraction = (mjd - left_mjd) / (right_mjd - left_mjd)
            response_flux = left_flux + fraction * (right_flux - left_flux)
        mjd_obs.append(mjd)
        driver_values.append(flux)
        response_values.append(response_flux)
    if len(mjd_obs) < 5:
        raise ValueError(
            f"{object_record.object_uid} lacks sufficient interpolated measurements"
        )
    return MeasuredSeriesPair(
        mjd_obs=tuple(mjd_obs),
        driver_values=tuple(driver_values),
        response_values=tuple(response_values),
        response_evidence_level="real_interpolated_response",
    )
