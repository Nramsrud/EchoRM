from __future__ import annotations

from echorm.eval.efficacy import package_blinded_task, score_blinded_task
from echorm.eval.validation import validate_benchmark
from echorm.reports.leaderboards import (
    build_efficacy_leaderboard,
    build_validation_leaderboard,
)
from echorm.reports.memos import build_mapping_comparison_memo
from echorm.simulate.benchmarks import build_benchmark_family


def test_validation_metrics_capture_lag_error_and_interval_calibration() -> None:
    realization = build_benchmark_family(family="clean", seed=3)
    result = validate_benchmark(
        realization=realization,
        recovered_lag=2.1,
        interval=(1.8, 2.3),
        runtime_sec=4.2,
    )

    assert result.family == "clean"
    assert result.lag_error == 0.1
    assert result.interval_contains_truth is True


def test_blinded_task_framework_supports_all_required_modes() -> None:
    audio = package_blinded_task(
        task_id="task-audio",
        mode="audio_only",
        artifacts=("audio/ngc5548.wav",),
        answer_key="lag_detected",
    )
    plot = package_blinded_task(
        task_id="task-plot",
        mode="plot_only",
        artifacts=("reports/ngc5548/timeline.svg",),
        answer_key="lag_detected",
    )
    combined = package_blinded_task(
        task_id="task-combined",
        mode="plot_audio",
        artifacts=("audio/ngc5548.wav", "reports/ngc5548/timeline.svg"),
        answer_key="lag_detected",
    )

    audio_result = score_blinded_task(
        audio,
        prediction="lag_detected",
        decision_time_sec=12.0,
        confidence=0.7,
    )
    plot_result = score_blinded_task(
        plot,
        prediction="lag_detected",
        decision_time_sec=10.0,
        confidence=0.8,
    )
    combined_result = score_blinded_task(
        combined,
        prediction="lag_detected",
        decision_time_sec=8.0,
        confidence=0.9,
    )

    leaderboard = build_efficacy_leaderboard(
        (audio_result, plot_result, combined_result)
    )
    assert [entry["mode"] for entry in leaderboard] == [
        "plot_audio",
        "plot_only",
        "audio_only",
    ]


def test_reports_emit_leaderboards_and_comparison_memos() -> None:
    realization = build_benchmark_family(family="state_change", seed=5)
    validation = validate_benchmark(
        realization=realization,
        recovered_lag=2.0,
        interval=(1.5, 2.5),
        runtime_sec=5.0,
    )
    leaderboard = build_validation_leaderboard((validation,))
    memo = build_mapping_comparison_memo(
        family="echo_ensemble",
        validation=validation,
        efficacy_summary="plot_audio outperformed single-modality review.",
    )

    assert leaderboard[0]["rank"] == 1
    assert "Lag error: 0.000" in memo
