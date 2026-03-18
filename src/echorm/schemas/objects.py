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
        "survey_ids",
        "line_coverage",
        "is_clagn_label",
        "tier",
        "literature_refs",
        "notes",
    ),
)
