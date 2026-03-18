from __future__ import annotations

from echorm.schemas import LINE_METRICS_SCHEMA
from echorm.spectra.continuum import (
    fit_full_decomposition,
    fit_local_continuum,
    fit_pseudo_continuum,
)
from echorm.spectra.lines import extract_line_metrics
from echorm.spectra.preprocess import preprocess_spectrum


def test_multiple_continuum_variants_remain_comparable() -> None:
    spectrum = preprocess_spectrum(
        wavelength_obs=(7200.0, 7220.0, 7240.0, 7260.0, 7280.0, 7300.0),
        flux=(1.0, 1.1, 1.8, 1.7, 1.1, 1.0),
        redshift=0.5,
        calibration_state="pipeline",
    )
    local_fit = fit_local_continuum(spectrum)
    pseudo_fit = fit_pseudo_continuum(spectrum)
    full_fit = fit_full_decomposition(spectrum)

    local_metrics = extract_line_metrics(
        object_uid="sdssrm-101",
        epoch_uid="sdssrm-101-e001",
        line_name="Hbeta",
        spectrum=spectrum,
        fit=local_fit,
        line_window=(4810.0, 4865.0),
    )
    pseudo_metrics = extract_line_metrics(
        object_uid="sdssrm-101",
        epoch_uid="sdssrm-101-e001",
        line_name="Hbeta",
        spectrum=spectrum,
        fit=pseudo_fit,
        line_window=(4810.0, 4865.0),
    )
    full_metrics = extract_line_metrics(
        object_uid="sdssrm-101",
        epoch_uid="sdssrm-101-e001",
        line_name="Hbeta",
        spectrum=spectrum,
        fit=full_fit,
        line_window=(4810.0, 4865.0),
    )

    assert LINE_METRICS_SCHEMA.validate_record(local_metrics) == ()
    assert local_metrics["continuum_variant"] == "local"
    assert pseudo_metrics["continuum_variant"] == "pseudo_continuum"
    assert full_metrics["continuum_variant"] == "full_decomposition"
    assert float(str(local_metrics["line_flux"])) > 0.0
    assert float(str(full_metrics["calibration_confidence"])) > 0.0
