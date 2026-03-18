from __future__ import annotations

from echorm.schemas import (
    LAG_RESULT_SCHEMA,
    LINE_METRICS_SCHEMA,
    OBJECT_MANIFEST_SCHEMA,
    PHOTOMETRY_SCHEMA,
    SONIFICATION_SCHEMA,
    SPECTRAL_EPOCH_SCHEMA,
)


def test_all_schema_columns_are_unique() -> None:
    for schema in (
        OBJECT_MANIFEST_SCHEMA,
        PHOTOMETRY_SCHEMA,
        SPECTRAL_EPOCH_SCHEMA,
        LINE_METRICS_SCHEMA,
        LAG_RESULT_SCHEMA,
        SONIFICATION_SCHEMA,
    ):
        assert len(schema.all_columns) == len(set(schema.all_columns))


def test_photometry_schema_tracks_provenance_and_quality() -> None:
    assert PHOTOMETRY_SCHEMA.provenance_columns == (
        "source_release",
        "raw_row_hash",
        "normalization_reference",
        "transform_hash",
    )
    assert PHOTOMETRY_SCHEMA.quality_columns == (
        "quality_flag",
        "is_upper_limit",
        "gap_flag",
        "quality_score",
        "review_priority",
        "normalization_mode",
    )


def test_lag_schema_reports_missing_columns() -> None:
    missing = LAG_RESULT_SCHEMA.missing_columns(
        {"object_uid", "pair_id", "driver_channel"}
    )
    assert "lag_median" in missing
    assert "method_config_hash" in missing


def test_schema_projects_records_into_canonical_order() -> None:
    record = {
        "object_uid": "ngc5548",
        "survey": "agn_watch",
        "band": "5100A",
        "mjd_obs": 50000.0,
        "mjd_rest": 49700.0,
        "flux": 1.2,
        "flux_err": 0.1,
        "mag": 14.2,
        "mag_err": 0.05,
        "flux_unit": "mJy",
        "source_release": "agn_watch_legacy",
        "raw_row_hash": "abc123",
        "normalization_reference": "raw_flux",
        "transform_hash": "raw",
        "quality_flag": "ok",
        "is_upper_limit": False,
        "gap_flag": False,
        "quality_score": 1.0,
        "review_priority": "low",
        "normalization_mode": "raw",
    }
    ordered = PHOTOMETRY_SCHEMA.ordered_record(record)
    assert tuple(ordered) == PHOTOMETRY_SCHEMA.all_columns
    assert ordered["raw_row_hash"] == "abc123"
