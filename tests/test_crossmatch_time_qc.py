from __future__ import annotations

from echorm.calibrate.normalize import science_normalize, sonification_normalize
from echorm.calibrate.time import observed_frame_mjd, rest_frame_mjd
from echorm.crossmatch.models import SurveyIdentifier, resolve_identity
from echorm.eval.qc import assess_series_quality


def test_identity_resolution_preserves_aliases_and_reference_epoch() -> None:
    identity = resolve_identity(
        canonical_name="NGC 5548",
        aliases=("NGC 5548", "AGNWATCH-NGC5548"),
        survey_ids=(SurveyIdentifier(survey="agn_watch", local_id="AGNWATCH-NGC5548"),),
        reference_epoch_mjd=50000.0,
    )
    assert identity.object_uid == "ngc5548"
    assert identity.alias_group == "NGC 5548,AGNWATCH-NGC5548"
    assert identity.reference_epoch_mjd == 50000.0


def test_time_conversion_round_trips_between_frames() -> None:
    mjd_obs = 57010.0
    mjd_rest = rest_frame_mjd(mjd_obs, 0.5, reference_epoch_mjd=57000.0)
    assert observed_frame_mjd(mjd_rest, 0.5, reference_epoch_mjd=57000.0) == mjd_obs


def test_normalization_modes_preserve_transform_metadata() -> None:
    samples = ((1.0, 2.0), (2.0, 4.0), (3.0, 3.0))
    science = science_normalize(samples, reference_flux=2.0)
    sonification = sonification_normalize(samples)

    assert science[0].normalization_mode == "science"
    assert science[0].transform_hash == "science:2.000000"
    assert sonification[-1].normalization_mode == "sonification"
    assert sonification[0].normalized_flux == 0.0


def test_quality_assessment_reports_gaps_and_review_priority() -> None:
    assessment = assess_series_quality(
        mjd_obs=(1.0, 2.0, 12.0),
        quality_flags=("ok", "flagged", "ok"),
        line_coverage="Hbeta",
    )
    assert assessment.gap_flag is True
    assert assessment.review_priority == "high"
    assert assessment.quality_score < 1.0
