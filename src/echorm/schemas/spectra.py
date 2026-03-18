"""Spectral-epoch schema."""

from __future__ import annotations

from ._base import TableSchema

SPECTRAL_EPOCH_SCHEMA = TableSchema(
    name="spectra_index",
    required_columns=(
        "object_uid",
        "epoch_uid",
        "survey",
        "mjd_obs",
        "mjd_rest",
        "z",
        "spec_path",
        "wave_min",
        "wave_max",
        "median_snr",
        "calibration_state",
    ),
    quality_columns=("quality_flag",),
)
