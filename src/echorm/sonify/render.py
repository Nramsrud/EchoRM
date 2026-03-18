"""Science-audio render helpers."""

from __future__ import annotations

from ..schemas import SONIFICATION_SCHEMA
from .base import SonificationPlan


def build_sonification_manifest(
    *,
    plan: SonificationPlan,
    sonification_id: str,
    audio_path: str,
) -> dict[str, object]:
    """Serialize a sonification plan into the canonical manifest schema."""
    config_hash = (
        f"{plan.config.mapping_family}|{plan.config.normalization_mode}|"
        f"{plan.config.uncertainty_mode}|{plan.config.sample_rate_hz}"
    )
    provenance_hash = (
        f"{plan.object_uid}:{len(plan.event_steps)}:{plan.config.time_scale}"
    )
    record = {
        "object_uid": plan.object_uid,
        "sonification_id": sonification_id,
        "mapping_family": plan.config.mapping_family,
        "input_channels": ",".join(plan.input_channels),
        "audio_path": audio_path,
        "duration_sec": len(plan.event_steps) / plan.config.sample_rate_hz,
        "time_scale": plan.config.time_scale,
        "normalization_mode": plan.config.normalization_mode,
        "uncertainty_mode": plan.config.uncertainty_mode,
        "mapping_config_hash": config_hash,
        "provenance_hash": provenance_hash,
    }
    return SONIFICATION_SCHEMA.ordered_record(record)
