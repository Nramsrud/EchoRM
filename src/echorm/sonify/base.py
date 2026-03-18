"""Shared sonification types and configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MappingConfig:
    """Stable configuration for a mapping family."""

    mapping_family: str
    normalization_mode: str
    uncertainty_mode: str
    sample_rate_hz: int
    time_scale: float


@dataclass(frozen=True, slots=True)
class RenderInput:
    """Science inputs for one sonification render."""

    object_uid: str
    driver_channel: str
    response_channel: str
    driver_values: tuple[float, ...]
    response_values: tuple[float, ...]
    delay_steps: int
    line_width: float
    asymmetry: float
    strength: float


@dataclass(frozen=True, slots=True)
class SonificationPlan:
    """A deterministic event-plan representation of one sonification."""

    object_uid: str
    config: MappingConfig
    input_channels: tuple[str, ...]
    event_steps: tuple[dict[str, float], ...]
