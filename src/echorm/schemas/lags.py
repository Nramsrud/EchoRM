"""Lag-result schema."""

from __future__ import annotations

from ._base import TableSchema

LAG_RESULT_SCHEMA = TableSchema(
    name="lags",
    required_columns=(
        "object_uid",
        "pair_id",
        "driver_channel",
        "response_channel",
        "method",
        "lag_median",
        "lag_lo",
        "lag_hi",
        "significance",
        "alias_score",
        "quality_score",
    ),
    provenance_columns=("posterior_path", "method_config_hash"),
)
