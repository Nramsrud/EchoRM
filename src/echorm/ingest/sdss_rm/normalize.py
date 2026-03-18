"""Canonical normalization for SDSS-RM published-lag fixtures."""

from __future__ import annotations

from ...eval.qc import assess_series_quality
from ...schemas import OBJECT_MANIFEST_SCHEMA, PHOTOMETRY_SCHEMA, SPECTRAL_EPOCH_SCHEMA
from .manifests import SdssRmObjectBundle


def build_object_manifest(bundle: SdssRmObjectBundle) -> dict[str, object]:
    """Build a canonical object-manifest record."""
    record = {
        "object_uid": bundle.object_uid,
        "canonical_name": bundle.canonical_name,
        "ra_deg": bundle.ra_deg,
        "dec_deg": bundle.dec_deg,
        "redshift": bundle.redshift,
        "survey_ids": ",".join(bundle.aliases),
        "alias_group": ",".join(bundle.aliases),
        "reference_epoch_mjd": min(epoch.mjd_obs for epoch in bundle.epochs),
        "line_coverage": bundle.line_coverage,
        "is_clagn_label": False,
        "tier": "silver",
        "literature_refs": bundle.literature_label,
        "notes": f"release={bundle.release_id}",
    }
    return OBJECT_MANIFEST_SCHEMA.ordered_record(record)


def build_spectral_epoch_records(bundle: SdssRmObjectBundle) -> list[dict[str, object]]:
    """Build canonical spectral-epoch records."""
    records: list[dict[str, object]] = []
    for epoch in bundle.epochs:
        record = {
            "object_uid": bundle.object_uid,
            "epoch_uid": epoch.epoch_uid,
            "survey": "sdss_rm",
            "mjd_obs": epoch.mjd_obs,
            "mjd_rest": epoch.mjd_obs / (1.0 + bundle.redshift),
            "z": bundle.redshift,
            "spec_path": epoch.raw_spec_path,
            "wave_min": epoch.wave_min,
            "wave_max": epoch.wave_max,
            "median_snr": epoch.median_snr,
            "calibration_state": epoch.calibration_state,
            "quality_flag": bundle.release_id,
        }
        records.append(SPECTRAL_EPOCH_SCHEMA.ordered_record(record))
    return records


def build_photometry_records(bundle: SdssRmObjectBundle) -> list[dict[str, object]]:
    """Build canonical continuum photometry records."""
    qc = assess_series_quality(
        mjd_obs=tuple(epoch.mjd_obs for epoch in bundle.epochs),
        quality_flags=tuple("ok" for _ in bundle.epochs),
        line_coverage=bundle.line_coverage,
    )
    records: list[dict[str, object]] = []
    for index, epoch in enumerate(bundle.epochs):
        record = {
            "object_uid": bundle.object_uid,
            "survey": "sdss_rm",
            "band": epoch.continuum_band,
            "mjd_obs": epoch.mjd_obs,
            "mjd_rest": epoch.mjd_obs / (1.0 + bundle.redshift),
            "flux": epoch.continuum_flux,
            "flux_err": epoch.continuum_flux_err,
            "mag": -2.5,
            "mag_err": 0.0,
            "flux_unit": "1e-17 erg s^-1 cm^-2 A^-1",
            "source_release": bundle.release_id,
            "raw_row_hash": f"{bundle.object_uid}:{index}",
            "normalization_reference": "raw_flux",
            "transform_hash": "raw",
            "quality_flag": "published_lag_subset",
            "is_upper_limit": False,
            "gap_flag": qc.gap_flag,
            "quality_score": qc.quality_score,
            "review_priority": qc.review_priority,
            "normalization_mode": "raw",
        }
        records.append(PHOTOMETRY_SCHEMA.ordered_record(record))
    return records
