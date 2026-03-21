from __future__ import annotations

import pytest

from echorm.eval.benchmark_corpus import BenchmarkObject
from echorm.eval.literal_corpora import build_interpolated_series, build_measured_series


def _benchmark_object() -> BenchmarkObject:
    object_manifest = {
        "object_uid": "test-object",
        "canonical_name": "Test Object",
        "redshift": 0.01,
    }
    photometry_records = (
        {
            "mjd_obs": 1.00,
            "flux": 10.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 2.00,
            "flux": 20.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 3.00,
            "flux": 30.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 4.00,
            "flux": 40.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 5.00,
            "flux": 50.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 6.00,
            "flux": 60.0,
            "normalization_mode": "raw",
        },
    )
    response_records = (
        {
            "mjd_obs": 1.08,
            "flux": 100.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 2.04,
            "flux": 110.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 3.11,
            "flux": 120.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 4.07,
            "flux": 130.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 5.02,
            "flux": 140.0,
            "normalization_mode": "raw",
        },
        {
            "mjd_obs": 6.04,
            "flux": 150.0,
            "normalization_mode": "raw",
        },
    )
    return BenchmarkObject(
        object_uid="test-object",
        canonical_name="Test Object",
        tier="gold",
        evidence_level="test",
        object_manifest=object_manifest,
        photometry_records=photometry_records,
        response_records=response_records,
        spectral_epoch_records=(),
        literature_lag_day=2.0,
        line_name="Hbeta",
        benchmark_regime="test",
        notes=(),
    )


def test_build_measured_series_matches_nearest_response_points() -> None:
    pair = build_measured_series(_benchmark_object())

    assert pair.response_evidence_level == "real_measured_response"
    assert pair.mjd_obs == (1.04, 2.02, 3.055, 4.035, 5.01, 6.02)
    assert pair.driver_values == (10.0, 20.0, 30.0, 40.0, 50.0, 60.0)
    assert pair.response_values == (100.0, 110.0, 120.0, 130.0, 140.0, 150.0)


def test_build_interpolated_series_interpolates_onto_continuum_cadence() -> None:
    pair = build_interpolated_series(_benchmark_object())

    assert pair.response_evidence_level == "real_interpolated_response"
    assert pair.mjd_obs == (2.0, 3.0, 4.0, 5.0, 6.0)
    assert pair.driver_values == (20.0, 30.0, 40.0, 50.0, 60.0)
    assert pair.response_values == pytest.approx(
        (
            109.58333333333333,
            118.97196261682244,
            129.27083333333334,
            139.78947368421052,
            149.60784313725492,
        )
    )
