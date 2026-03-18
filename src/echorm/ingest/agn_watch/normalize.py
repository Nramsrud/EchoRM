"""Canonical normalization for AGN Watch fixtures."""

from __future__ import annotations

from ...eval.qc import assess_series_quality
from ...schemas import (
    OBJECT_MANIFEST_SCHEMA,
    PHOTOMETRY_SCHEMA,
    SPECTRAL_EPOCH_SCHEMA,
)
from .manifests import RawSourceManifest
from .parsers import ParsedAgnWatchFile


def build_object_manifest(
    parsed: ParsedAgnWatchFile,
    *,
    line_coverage: str,
    literature_refs: str,
) -> dict[str, object]:
    """Build a canonical object-manifest record."""
    metadata = parsed.metadata
    record = {
        "object_uid": parsed.object_uid,
        "canonical_name": parsed.canonical_name,
        "ra_deg": float(metadata["ra_deg"]),
        "dec_deg": float(metadata["dec_deg"]),
        "redshift": float(metadata["redshift"]),
        "survey_ids": metadata["survey_id"],
        "alias_group": metadata["survey_id"],
        "reference_epoch_mjd": min(
            [row.mjd_obs for row in parsed.photometry_rows]
            or [epoch.mjd_obs for epoch in parsed.spectral_epochs]
        ),
        "line_coverage": line_coverage,
        "is_clagn_label": False,
        "tier": "gold",
        "literature_refs": literature_refs,
        "notes": "; ".join(parsed.comments),
    }
    return OBJECT_MANIFEST_SCHEMA.ordered_record(record)


def build_photometry_records(
    parsed: ParsedAgnWatchFile,
    manifest: RawSourceManifest,
) -> list[dict[str, object]]:
    """Build canonical photometry records for a parsed light curve."""
    band = parsed.metadata["band"]
    redshift = float(parsed.metadata["redshift"])
    unit = parsed.metadata["unit"]
    qc = assess_series_quality(
        mjd_obs=tuple(row.mjd_obs for row in parsed.photometry_rows),
        quality_flags=tuple(row.quality_flag for row in parsed.photometry_rows),
        line_coverage="Hbeta",
    )
    records: list[dict[str, object]] = []
    for index, row in enumerate(parsed.photometry_rows):
        record = {
            "object_uid": parsed.object_uid,
            "survey": "agn_watch",
            "band": band,
            "mjd_obs": row.mjd_obs,
            "mjd_rest": row.mjd_obs / (1.0 + redshift),
            "flux": row.flux,
            "flux_err": row.flux_err,
            "mag": -2.5,
            "mag_err": 0.0,
            "flux_unit": unit,
            "source_release": manifest.source_url,
            "raw_row_hash": f"{parsed.object_uid}:{index}",
            "normalization_reference": "raw_flux",
            "transform_hash": "raw",
            "quality_flag": row.quality_flag,
            "is_upper_limit": False,
            "gap_flag": qc.gap_flag,
            "quality_score": qc.quality_score,
            "review_priority": qc.review_priority,
            "normalization_mode": "raw",
        }
        records.append(PHOTOMETRY_SCHEMA.ordered_record(record))
    return records


def build_spectral_epoch_records(
    parsed: ParsedAgnWatchFile,
    manifest: RawSourceManifest,
) -> list[dict[str, object]]:
    """Build canonical spectral-epoch records for a parsed spectral index."""
    redshift = float(parsed.metadata["redshift"])
    records: list[dict[str, object]] = []
    for epoch in parsed.spectral_epochs:
        record = {
            "object_uid": parsed.object_uid,
            "epoch_uid": epoch.epoch_uid,
            "survey": "agn_watch",
            "mjd_obs": epoch.mjd_obs,
            "mjd_rest": epoch.mjd_obs / (1.0 + redshift),
            "z": redshift,
            "spec_path": epoch.spec_path,
            "wave_min": epoch.wave_min,
            "wave_max": epoch.wave_max,
            "median_snr": epoch.median_snr,
            "calibration_state": epoch.calibration_state,
            "quality_flag": manifest.source_url,
        }
        records.append(SPECTRAL_EPOCH_SCHEMA.ordered_record(record))
    return records
