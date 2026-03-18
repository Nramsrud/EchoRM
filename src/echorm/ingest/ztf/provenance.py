"""Release and query provenance objects for ZTF responses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ZtfQueryProvenance:
    """Query and release metadata for one cached ZTF response."""

    release_id: str
    query_params: dict[str, object]
    bad_flag_policy: str
    crossmatch_key: str


@dataclass(frozen=True, slots=True)
class ZtfObservation:
    """One observation row from a cached ZTF response."""

    mjd_obs: float
    band: str
    flux: float
    flux_err: float
    mag: float
    mag_err: float
    catflags: int


@dataclass(frozen=True, slots=True)
class ZtfCachedResponse:
    """A cached raw response plus pinned provenance."""

    object_uid: str
    provenance: ZtfQueryProvenance
    rows: tuple[ZtfObservation, ...]


def cached_response_from_payload(payload: dict[str, object]) -> ZtfCachedResponse:
    """Build a cached-response object from a frozen payload."""
    query_params = payload["query_params"]
    rows = payload["rows"]
    if not isinstance(query_params, dict):
        raise ValueError("query_params payload must be a mapping")
    if not isinstance(rows, list):
        raise ValueError("rows payload must be a list")
    provenance = ZtfQueryProvenance(
        release_id=str(payload["release_id"]),
        query_params={str(key): value for key, value in query_params.items()},
        bad_flag_policy=str(payload["bad_flag_policy"]),
        crossmatch_key=str(payload["crossmatch_key"]),
    )
    observations = tuple(
        ZtfObservation(
            mjd_obs=float(row["mjd_obs"]),
            band=str(row["band"]),
            flux=float(row["flux"]),
            flux_err=float(row["flux_err"]),
            mag=float(row["mag"]),
            mag_err=float(row["mag_err"]),
            catflags=int(row["catflags"]),
        )
        for row in rows
        if isinstance(row, dict)
    )
    return ZtfCachedResponse(
        object_uid=str(payload["object_uid"]),
        provenance=provenance,
        rows=observations,
    )
