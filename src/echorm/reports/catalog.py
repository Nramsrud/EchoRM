"""Catalog package builders."""

from __future__ import annotations


def build_catalog_package(
    *,
    release_version: str,
    entries: tuple[dict[str, object], ...],
) -> dict[str, object]:
    """Build a public catalog package."""
    return {
        "release_version": release_version,
        "entries": entries,
        "entry_count": len(entries),
    }
