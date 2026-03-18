from __future__ import annotations

from echorm.reports.catalog import build_catalog_package
from echorm.reports.release import build_release_bundle, build_release_index


def test_release_bundle_is_complete_and_provenance_aware() -> None:
    catalog = build_catalog_package(
        release_version="v1.0.0",
        entries=(
            {
                "object_uid": "ztf-target-001",
                "anomaly_category": "clagn_transition",
                "rank_score": 0.8,
            },
        ),
    )
    bundle = build_release_bundle(
        version="v1.0.0",
        catalog_package=catalog,
        benchmark_tables=("benchmarks/clean.csv", "benchmarks/contaminated.csv"),
        audio_products=("audio/ngc5548-echo.wav",),
        provenance_records=(
            {"artifact": "catalog", "hash": "abc123"},
            {"artifact": "audio", "hash": "def456"},
        ),
    )

    assert bundle["artifact_inventory"] == (
        "code",
        "configuration",
        "manifests",
        "benchmark_tables",
        "audio_products",
        "provenance_records",
    )
    assert str(bundle["provenance_records"]).count("artifact") == 2


def test_release_index_matches_bundle_contents() -> None:
    catalog = build_catalog_package(
        release_version="v1.0.0",
        entries=({"object_uid": "ztf-target-001"},),
    )
    bundle = build_release_bundle(
        version="v1.0.0",
        catalog_package=catalog,
        benchmark_tables=("benchmarks/clean.csv",),
        audio_products=("audio/ngc5548-echo.wav", "audio/ngc5548-direct.wav"),
        provenance_records=({"artifact": "catalog", "hash": "abc123"},),
    )
    index = build_release_index(bundle)

    assert "# Release v1.0.0" in index
    assert "- Catalog entries: 1" in index
    assert "- Audio products: 2" in index
