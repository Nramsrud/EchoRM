"""Canonical lag-result builders."""

from __future__ import annotations

from dataclasses import dataclass

from ..schemas import LAG_RESULT_SCHEMA
from .base import LagRun


@dataclass(frozen=True, slots=True)
class SerializedLagResult:
    """Canonical lag record plus structured diagnostics."""

    record: dict[str, object]
    diagnostics: dict[str, object]
    runtime_metadata: dict[str, object]


def serialize_lag_run(run: LagRun) -> SerializedLagResult:
    """Serialize a method-level lag result into the canonical lag schema."""
    config_object = run.runtime_metadata.get("config", {})
    if not isinstance(config_object, dict):
        raise ValueError("lag runtime metadata must expose a configuration mapping")
    posterior_path = run.diagnostics.get("posterior_path", "")
    config_hash = "|".join(
        f"{key}={value}" for key, value in sorted(config_object.items())
    )
    record = LAG_RESULT_SCHEMA.ordered_record(
        {
            "object_uid": run.object_uid,
            "pair_id": run.pair_id,
            "driver_channel": run.driver_channel,
            "response_channel": run.response_channel,
            "method": run.method,
            "lag_median": run.lag_median,
            "lag_lo": run.lag_lo,
            "lag_hi": run.lag_hi,
            "significance": run.significance,
            "alias_score": run.alias_score,
            "quality_score": run.quality_score,
            "posterior_path": str(posterior_path),
            "method_config_hash": config_hash,
        }
    )
    return SerializedLagResult(
        record=record,
        diagnostics=run.diagnostics,
        runtime_metadata=run.runtime_metadata,
    )
