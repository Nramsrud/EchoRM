"""Photometry schema."""

from __future__ import annotations

from ._base import TableSchema

PHOTOMETRY_SCHEMA = TableSchema(
    name="photometry",
    required_columns=(
        "object_uid",
        "survey",
        "band",
        "mjd_obs",
        "mjd_rest",
        "flux",
        "flux_err",
        "mag",
        "mag_err",
        "flux_unit",
    ),
    provenance_columns=(
        "source_release",
        "raw_row_hash",
        "normalization_reference",
        "transform_hash",
    ),
    quality_columns=(
        "quality_flag",
        "is_upper_limit",
        "gap_flag",
        "quality_score",
        "review_priority",
        "normalization_mode",
    ),
)
