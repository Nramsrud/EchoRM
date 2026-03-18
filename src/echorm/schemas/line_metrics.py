"""Line-metric schema."""

from __future__ import annotations

from ._base import TableSchema

LINE_METRICS_SCHEMA = TableSchema(
    name="line_metrics",
    required_columns=(
        "object_uid",
        "epoch_uid",
        "line_name",
        "line_flux",
        "line_flux_err",
        "ew",
        "ew_err",
        "fwhm",
        "fwhm_err",
        "sigma_line",
        "sigma_line_err",
        "centroid",
        "centroid_err",
        "skew",
        "kurtosis",
        "blue_red_asymmetry",
        "fit_model_id",
        "continuum_variant",
        "calibration_confidence",
        "residual_rms",
    ),
)
