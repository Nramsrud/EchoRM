"""Canonical photometry normalization for cached ZTF responses."""

from __future__ import annotations

from ...calibrate.time import rest_frame_mjd
from ...eval.qc import assess_series_quality
from ...schemas import PHOTOMETRY_SCHEMA
from .provenance import ZtfCachedResponse


def build_photometry_records(response: ZtfCachedResponse) -> list[dict[str, object]]:
    """Build canonical photometry records from a cached response."""
    time_origin_mjd = min(row.mjd_obs for row in response.rows)
    qc = assess_series_quality(
        mjd_obs=tuple(row.mjd_obs for row in response.rows),
        quality_flags=tuple(
            "ok" if row.catflags == 0 else "flagged" for row in response.rows
        ),
        line_coverage="continuum_only",
    )
    records: list[dict[str, object]] = []
    for index, row in enumerate(response.rows):
        record = {
            "object_uid": response.object_uid,
            "survey": "ztf",
            "band": row.band,
            "mjd_obs": row.mjd_obs,
            "mjd_rest": rest_frame_mjd(
                row.mjd_obs,
                0.0,
                reference_epoch_mjd=time_origin_mjd,
            ),
            "flux": row.flux,
            "flux_err": row.flux_err,
            "mag": row.mag,
            "mag_err": row.mag_err,
            "flux_unit": "ztf_native",
            "source_release": response.provenance.release_id,
            "raw_row_hash": f"{response.object_uid}:{index}",
            "normalization_reference": "raw_flux",
            "transform_hash": "raw",
            "quality_flag": f"catflags={row.catflags}",
            "is_upper_limit": False,
            "gap_flag": qc.gap_flag,
            "quality_score": qc.quality_score,
            "review_priority": qc.review_priority,
            "normalization_mode": "raw",
        }
        records.append(PHOTOMETRY_SCHEMA.ordered_record(record))
    return records
