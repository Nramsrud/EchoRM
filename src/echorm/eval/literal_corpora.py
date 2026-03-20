"""Literal public-data corpus loaders for root-closeout remediation."""

from __future__ import annotations

import hashlib
import math
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..eval.qc import assess_series_quality
from ..schemas import OBJECT_MANIFEST_SCHEMA, PHOTOMETRY_SCHEMA
from .benchmark_corpus import BenchmarkObject, DiscoveryHoldoutRecord

try:
    from astroquery.vizier import Vizier  # type: ignore[import-untyped]
except ImportError:
    Vizier = None


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
    rows: tuple[tuple[float, float, float], ...],
    source_release: str,
    flux_unit: str,
) -> tuple[dict[str, object], ...]:
    qc = assess_series_quality(
        mjd_obs=tuple(row[0] for row in rows),
        quality_flags=tuple("ok" for _ in rows),
        line_coverage=band,
    )
    records: list[dict[str, object]] = []
    for _index, (mjd_obs, flux, flux_err) in enumerate(rows):
        raw_hash = hashlib.sha256(
            f"{object_uid}:{band}:{mjd_obs}:{flux}:{flux_err}".encode()
        ).hexdigest()[:16]
        records.append(
            PHOTOMETRY_SCHEMA.ordered_record(
                {
                    "object_uid": object_uid,
                    "survey": survey,
                    "band": band,
                    "mjd_obs": mjd_obs,
                    "mjd_rest": mjd_obs / (1.0 + redshift),
                    "flux": flux,
                    "flux_err": flux_err,
                    "mag": -2.5 * math.log10(max(flux, 1e-6)),
                    "mag_err": 0.0,
                    "flux_unit": flux_unit,
                    "source_release": source_release,
                    "raw_row_hash": raw_hash,
                    "normalization_reference": "raw_flux",
                    "transform_hash": "raw",
                    "quality_flag": "ok",
                    "is_upper_limit": False,
                    "gap_flag": qc.gap_flag,
                    "quality_score": qc.quality_score,
                    "review_priority": qc.review_priority,
                    "normalization_mode": "raw",
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
        _download_binary(
            repo_root,
            relpath=f"agn_watch/{spec['object_uid']}/spectra.tar.gz",
            url=str(spec["spectra_url"]),
        )
        continuum_rows = _three_column_rows(continuum_text)
        response_rows = _three_column_rows(response_text)
        photometry_records = _build_photometry_rows(
            object_uid=str(spec["object_uid"]),
            survey="agn_watch",
            band=str(spec["continuum_band"]),
            redshift=_as_float(spec["redshift"]),
            rows=continuum_rows,
            source_release="agnwatch-2001",
            flux_unit="agnwatch_native",
        )
        response_records = _build_photometry_rows(
            object_uid=str(spec["object_uid"]),
            survey="agn_watch",
            band=str(spec["line_name"]).lower(),
            redshift=_as_float(spec["redshift"]),
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
            reference_epoch_mjd=_as_float(continuum_rows[0][0]),
            line_coverage="Hbeta",
            tier="gold",
            literature_refs=(
                "International AGN Watch archive; "
                "Peterson et al. gold benchmark"
            ),
            notes="real public archive download",
        )
        objects.append(
            BenchmarkObject(
                object_uid=str(spec["object_uid"]),
                canonical_name=str(spec["canonical_name"]),
                tier="gold",
                evidence_level="real_public_timeseries",
                object_manifest=object_manifest,
                photometry_records=photometry_records,
                spectral_epoch_records=(),
                literature_lag_day=_as_float(spec["literature_lag_day"]),
                line_name=str(spec["line_name"]),
                benchmark_regime=str(spec["benchmark_regime"]),
                notes=(
                    "Real AGN Watch continuum and line light curves.",
                    "Raw spectra archive cached under artifacts/raw/agn_watch.",
                ),
                response_records=response_records,
            )
        )
    return tuple(objects)


def _require_vizier() -> Any:
    if Vizier is None:
        raise RuntimeError("astroquery is required for literal corpus acquisition")
    return Vizier


def load_literal_silver_benchmark_objects(
    repo_root: Path,
) -> tuple[BenchmarkObject, ...]:
    """Load the real SDSS-RM silver objects with direct continuum and line series."""
    vizier_cls = _require_vizier()
    vizier_cls.ROW_LIMIT = -1
    tables = vizier_cls.get_catalogs("J/ApJ/818/30")
    lightcurve_table = tables["J/ApJ/818/30/table2"]

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
        },
    }

    grouped: dict[int, list[tuple[float, float, float, float, float]]] = (
        defaultdict(list)
    )
    for row in lightcurve_table:
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
        continuum_rows = tuple(
            (mjd, cont, cont_err) for mjd, cont, cont_err, _, _ in rows
        )
        response_rows = tuple(
            (mjd, line, line_err) for mjd, _, _, line, line_err in rows
        )
        photometry_records = _build_photometry_rows(
            object_uid=f"sdssrm-{rmid}",
            survey="sdss_rm",
            band="g",
            redshift=_as_float(meta["redshift"]),
            rows=continuum_rows,
            source_release="J/ApJ/818/30",
            flux_unit="published_flux",
        )
        response_records = _build_photometry_rows(
            object_uid=f"sdssrm-{rmid}",
            survey="sdss_rm",
            band=str(meta["line_name"]).lower(),
            redshift=_as_float(meta["redshift"]),
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
            reference_epoch_mjd=_as_float(rows[0][0]),
            line_coverage=str(meta["line_name"]),
            tier="silver",
            literature_refs="Shen et al. 2016 SDSS-RM published light curves",
            notes="real published continuum and line time series",
        )
        objects.append(
            BenchmarkObject(
                object_uid=f"sdssrm-{rmid}",
                canonical_name=str(meta["canonical_name"]),
                tier="silver",
                evidence_level="real_public_timeseries",
                object_manifest=object_manifest,
                photometry_records=photometry_records,
                spectral_epoch_records=(),
                literature_lag_day=_as_float(meta["literature_lag_day"]),
                line_name=str(meta["line_name"]),
                benchmark_regime=str(meta["benchmark_regime"]),
                notes=(
                    "Real SDSS-RM published continuum and line light curves.",
                    "Metadata remains bounded to RMIDs with "
                    "trusted local cross-identification.",
                ),
                response_records=response_records,
            )
        )
    objects.sort(key=lambda item: item.object_uid)
    return tuple(objects)


def load_literal_discovery_holdout_records(
    repo_root: Path,
) -> tuple[DiscoveryHoldoutRecord, ...]:
    """Load a real published CLQ hold-out catalog slice for root closeout."""
    del repo_root
    vizier_cls = _require_vizier()
    vizier_cls.ROW_LIMIT = -1
    table = vizier_cls.get_catalogs("J/ApJ/933/180")["J/ApJ/933/180/table2"]
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
        continuum_shift = abs(_as_float(last["l5100"]) - _as_float(first["l5100"]))
        line_shift = abs(_as_float(last["lhb"]) - _as_float(first["lhb"])) + abs(
            _as_float(last["lmgii"]) - _as_float(first["lmgii"])
        )
        sonification_shift = round((continuum_shift + line_shift) / 2.0, 3)
        records.append(
            DiscoveryHoldoutRecord(
                object_uid=sdss_name.lower().replace("j", "clq-"),
                canonical_name=sdss_name,
                release_id="J/ApJ/933/180",
                crossmatch_key=sdss_name,
                anomaly_category="changing_look_quasar",
                evidence_level="real_catalog_state_change",
                holdout_policy="holdout_only_no_optimization",
                benchmark_links=("gold_validation", "silver_validation"),
                lag_outlier=round(continuum_shift, 3),
                line_response_outlier=round(line_shift, 3),
                sonification_outlier=sonification_shift,
                pre_state_lag=0.0,
                post_state_lag=0.0,
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
                },
                notes=(
                    f"published state sequence count={len(rows)}",
                    f"notes={first['notes']}",
                ),
            )
        )
    records.sort(key=lambda item: item.object_uid)
    return tuple(records)


def build_measured_series(object_record: BenchmarkObject) -> MeasuredSeriesPair:
    """Align measured continuum and response records into one series pair."""
    if not object_record.response_records:
        raise ValueError(f"{object_record.object_uid} has no measured response records")
    response_by_mjd = {
        round(float(str(record["mjd_obs"])), 3): float(str(record["flux"]))
        for record in object_record.response_records
    }
    mjd_obs: list[float] = []
    driver_values: list[float] = []
    response_values: list[float] = []
    for record in object_record.photometry_records:
        mjd = round(float(str(record["mjd_obs"])), 3)
        if mjd not in response_by_mjd:
            continue
        mjd_obs.append(mjd)
        driver_values.append(float(str(record["flux"])))
        response_values.append(response_by_mjd[mjd])
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
