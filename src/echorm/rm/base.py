"""Shared reverberation-method interfaces."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TimeSeries:
    """A simple sampled time series."""

    channel: str
    mjd_obs: tuple[float, ...]
    values: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class LagRun:
    """Method-level lag result plus structured diagnostics."""

    object_uid: str
    pair_id: str
    driver_channel: str
    response_channel: str
    method: str
    lag_median: float
    lag_lo: float
    lag_hi: float
    significance: float
    alias_score: float
    quality_score: float
    diagnostics: dict[str, object]
    runtime_metadata: dict[str, object]


def build_pair_id(driver: TimeSeries, response: TimeSeries) -> str:
    """Build a stable channel-pair identifier."""
    return f"{driver.channel}->{response.channel}"
