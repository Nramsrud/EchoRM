"""Sonification schema."""

from __future__ import annotations

from ._base import TableSchema

SONIFICATION_SCHEMA = TableSchema(
    name="sonifications",
    required_columns=(
        "object_uid",
        "sonification_id",
        "mapping_family",
        "input_channels",
        "audio_path",
        "duration_sec",
        "time_scale",
        "normalization_mode",
        "uncertainty_mode",
    ),
    provenance_columns=("mapping_config_hash", "provenance_hash"),
)
