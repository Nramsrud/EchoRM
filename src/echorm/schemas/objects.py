"""Object-manifest schema."""

from __future__ import annotations

from ._base import TableSchema

OBJECT_MANIFEST_SCHEMA = TableSchema(
    name="objects",
    required_columns=(
        "object_uid",
        "canonical_name",
        "ra_deg",
        "dec_deg",
        "redshift",
        "time_origin_mjd",
        "survey_ids",
        "alias_group",
        "reference_epoch_mjd",
        "line_coverage",
        "is_clagn_label",
        "tier",
        "literature_refs",
        "notes",
    ),
)
