"""Observed-frame and rest-frame time conversion helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReferenceEpoch:
    """Reference epoch metadata for one object."""

    object_uid: str
    mjd_obs: float
    redshift: float


def rest_frame_mjd(
    mjd_obs: float,
    redshift: float,
    *,
    reference_epoch_mjd: float = 0.0,
) -> float:
    """Convert observed-frame MJD into rest-frame MJD."""
    delta = mjd_obs - reference_epoch_mjd
    return reference_epoch_mjd + delta / (1.0 + redshift)


def observed_frame_mjd(
    mjd_rest: float,
    redshift: float,
    *,
    reference_epoch_mjd: float = 0.0,
) -> float:
    """Convert rest-frame MJD back into observed-frame MJD."""
    delta = mjd_rest - reference_epoch_mjd
    return reference_epoch_mjd + delta * (1.0 + redshift)
