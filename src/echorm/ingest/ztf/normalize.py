"""Canonical photometry normalization for cached ZTF responses."""

from __future__ import annotations

from ...schemas import PHOTOMETRY_SCHEMA
from .provenance import ZtfCachedResponse


def build_photometry_records(response: ZtfCachedResponse) -> list[dict[str, object]]:
    """Build canonical photometry records from a cached response."""
    records: list[dict[str, object]] = []
    for index, row in enumerate(response.rows):
        record = {
            "object_uid": response.object_uid,
            "survey": "ztf",
            "band": row.band,
            "mjd_obs": row.mjd_obs,
            "mjd_rest": row.mjd_obs,
            "flux": row.flux,
            "flux_err": row.flux_err,
            "mag": row.mag,
            "mag_err": row.mag_err,
            "flux_unit": "ztf_native",
            "source_release": response.provenance.release_id,
            "raw_row_hash": f"{response.object_uid}:{index}",
            "quality_flag": f"catflags={row.catflags}",
            "is_upper_limit": False,
        }
        records.append(PHOTOMETRY_SCHEMA.ordered_record(record))
    return records
