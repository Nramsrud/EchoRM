"""Raw-source manifest helpers for AGN Watch fixtures."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RawSourceManifest:
    """Immutable metadata for one preserved AGN Watch source file."""

    object_uid: str
    canonical_name: str
    source_path: Path
    source_url: str
    file_format: str
    raw_text: str


def load_raw_manifest(
    path: Path,
    *,
    object_uid: str,
    canonical_name: str,
    source_url: str,
    file_format: str,
) -> RawSourceManifest:
    """Load raw-source text without mutation."""
    return RawSourceManifest(
        object_uid=object_uid,
        canonical_name=canonical_name,
        source_path=path,
        source_url=source_url,
        file_format=file_format,
        raw_text=path.read_text(encoding="utf-8"),
    )
