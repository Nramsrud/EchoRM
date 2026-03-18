"""Object and release metadata helpers for SDSS-RM."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SdssRmEpochAsset:
    """One raw spectral epoch and its attached continuum measurement."""

    epoch_uid: str
    mjd_obs: float
    wave_min: float
    wave_max: float
    median_snr: float
    calibration_state: str
    raw_spec_path: str
    continuum_band: str
    continuum_flux: float
    continuum_flux_err: float


@dataclass(frozen=True, slots=True)
class SdssRmObjectBundle:
    """Published-lag object metadata plus raw epoch assets."""

    release_id: str
    literature_label: str
    object_uid: str
    canonical_name: str
    aliases: tuple[str, ...]
    redshift: float
    ra_deg: float
    dec_deg: float
    line_coverage: str
    epochs: tuple[SdssRmEpochAsset, ...]


def bundle_from_payload(payload: dict[str, object]) -> SdssRmObjectBundle:
    """Build a typed object bundle from a frozen payload."""
    epoch_payloads = payload["epochs"]
    if not isinstance(epoch_payloads, list):
        raise ValueError("epochs payload must be a list")
    epochs = tuple(
        SdssRmEpochAsset(
            epoch_uid=str(epoch["epoch_uid"]),
            mjd_obs=float(epoch["mjd_obs"]),
            wave_min=float(epoch["wave_min"]),
            wave_max=float(epoch["wave_max"]),
            median_snr=float(epoch["median_snr"]),
            calibration_state=str(epoch["calibration_state"]),
            raw_spec_path=str(epoch["raw_spec_path"]),
            continuum_band=str(epoch["continuum_band"]),
            continuum_flux=float(epoch["continuum_flux"]),
            continuum_flux_err=float(epoch["continuum_flux_err"]),
        )
        for epoch in epoch_payloads
        if isinstance(epoch, dict)
    )
    aliases = payload["aliases"]
    if not isinstance(aliases, list):
        raise ValueError("aliases payload must be a list")
    return SdssRmObjectBundle(
        release_id=str(payload["release_id"]),
        literature_label=str(payload["literature_label"]),
        object_uid=str(payload["object_uid"]),
        canonical_name=str(payload["canonical_name"]),
        aliases=tuple(str(alias) for alias in aliases),
        redshift=float(str(payload["redshift"])),
        ra_deg=float(str(payload["ra_deg"])),
        dec_deg=float(str(payload["dec_deg"])),
        line_coverage=str(payload["line_coverage"]),
        epochs=epochs,
    )
