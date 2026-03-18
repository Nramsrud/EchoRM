"""Public-product acquisition helpers for SDSS-RM fixtures."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AcquisitionPlan:
    """Pinned acquisition metadata for a published-lag subset."""

    release_id: str
    catalog_url: str
    raw_root: str
    object_uids: tuple[str, ...]


def load_public_subset(path: Path) -> dict[str, object]:
    """Load a frozen published-lag subset payload."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("SDSS-RM subset payload must be a mapping")
    return {str(key): value for key, value in payload.items()}


def build_acquisition_plan(
    *,
    release_id: str,
    catalog_url: str,
    raw_root: str,
    object_uids: tuple[str, ...],
) -> AcquisitionPlan:
    """Create a pinned acquisition plan."""
    return AcquisitionPlan(
        release_id=release_id,
        catalog_url=catalog_url,
        raw_root=raw_root,
        object_uids=object_uids,
    )
