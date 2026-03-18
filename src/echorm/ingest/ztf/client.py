"""API and bulk-access interfaces for ZTF."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetrievalPlan:
    """Pinned retrieval metadata for one ZTF access path."""

    mode: str
    release_id: str
    target_id: str
    query: dict[str, object]
    crossmatch_key: str


def build_api_plan(
    *,
    release_id: str,
    target_id: str,
    ra_deg: float,
    dec_deg: float,
    radius_arcsec: float,
    bad_flag_policy: str,
    crossmatch_key: str,
) -> RetrievalPlan:
    """Build a pinned interactive API retrieval plan."""
    return RetrievalPlan(
        mode="api",
        release_id=release_id,
        target_id=target_id,
        query={
            "ra_deg": ra_deg,
            "dec_deg": dec_deg,
            "radius_arcsec": radius_arcsec,
            "bad_flag_policy": bad_flag_policy,
        },
        crossmatch_key=crossmatch_key,
    )


def build_bulk_plan(
    *,
    release_id: str,
    target_id: str,
    parquet_uri: str,
    filters: dict[str, object],
    crossmatch_key: str,
) -> RetrievalPlan:
    """Build a pinned bulk-scale retrieval plan."""
    return RetrievalPlan(
        mode="bulk",
        release_id=release_id,
        target_id=target_id,
        query={"parquet_uri": parquet_uri, "filters": filters},
        crossmatch_key=crossmatch_key,
    )
