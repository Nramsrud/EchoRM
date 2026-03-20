"""Release assembly helpers."""

from __future__ import annotations


def build_release_bundle(
    *,
    version: str,
    catalog_package: dict[str, object],
    benchmark_tables: tuple[str, ...],
    audio_products: tuple[str, ...],
    provenance_records: tuple[dict[str, object], ...],
    publication_artifacts: tuple[str, ...] = (),
    claims_scope: str = "benchmark",
) -> dict[str, object]:
    """Assemble a provenance-aware public release bundle."""
    return {
        "version": version,
        "claims_scope": claims_scope,
        "catalog_package": catalog_package,
        "benchmark_tables": benchmark_tables,
        "audio_products": audio_products,
        "provenance_records": provenance_records,
        "publication_artifacts": publication_artifacts,
        "artifact_inventory": (
            "code",
            "configuration",
            "manifests",
            "benchmark_tables",
            "audio_products",
            "provenance_records",
            "publication_artifacts",
        ),
    }


def build_release_index(bundle: dict[str, object]) -> str:
    """Build a concise public release index from a structured bundle."""
    version = str(bundle["version"])
    catalog_package = bundle["catalog_package"]
    benchmark_tables_object = bundle["benchmark_tables"]
    audio_products_object = bundle["audio_products"]
    provenance_records_object = bundle["provenance_records"]
    publication_artifacts_object = bundle.get("publication_artifacts", ())
    if not isinstance(catalog_package, dict):
        raise ValueError("catalog package must be a mapping")
    if not isinstance(benchmark_tables_object, tuple):
        raise ValueError("benchmark tables must be a tuple")
    if not isinstance(audio_products_object, tuple):
        raise ValueError("audio products must be a tuple")
    if not isinstance(provenance_records_object, tuple):
        raise ValueError("provenance records must be a tuple")
    if not isinstance(publication_artifacts_object, tuple):
        raise ValueError("publication artifacts must be a tuple")
    benchmark_tables = tuple(str(value) for value in benchmark_tables_object)
    audio_products = tuple(str(value) for value in audio_products_object)
    provenance_records = tuple(str(value) for value in provenance_records_object)
    publication_artifacts = tuple(
        str(value) for value in publication_artifacts_object
    )
    return (
        f"# Release {version}\n\n"
        f"- Catalog entries: {catalog_package['entry_count']}\n"
        f"- Benchmark scope: {bundle['claims_scope']}\n"
        f"- Benchmark tables: {len(benchmark_tables)}\n"
        f"- Audio products: {len(audio_products)}\n"
        f"- Provenance records: {len(provenance_records)}\n"
        f"- Publication artifacts: {len(publication_artifacts)}\n"
    )
