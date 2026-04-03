"""Reviewed primary-wave rerun package assembly."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

from .broad_validation import (
    JSONDict,
    _dict_list,
    _float_value,
    _mapping_value,
    _package_dossier,
    _package_header,
    _string_list,
    _update_root_index,
    _write_markdown,
)
from .discovery_snapshot import validate_promoted_discovery_snapshot
from .literal_corpora import load_literal_discovery_holdout_records
from .readiness import ToolStatus, VerificationCheck, _write_json, detect_tool_statuses
from .root_closeout import materialize_discovery_candidate_bundle


def _load_required_run(artifact_root: Path, run_id: str) -> JSONDict:
    path = artifact_root / run_id / "index.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{run_id} payload must be a mapping")
    return payload


def _load_mapping_path(path: Path) -> JSONDict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} payload must be a mapping")
    return payload


def _resolve_manual_review_path(artifact_root: Path, manual_review_path: Path) -> Path:
    if manual_review_path.is_absolute():
        return manual_review_path
    return artifact_root / manual_review_path


def _bool_value(
    payload: Mapping[str, object],
    key: str,
    default: bool = False,
) -> bool:
    value = payload.get(key, default)
    return value if isinstance(value, bool) else default


def _candidate_ids(
    first_pass_payload: Mapping[str, object],
    *,
    review_wave: str | None = None,
) -> tuple[str, ...]:
    candidates = _dict_list(first_pass_payload, "candidates")
    return tuple(
        str(candidate.get("object_uid", ""))
        for candidate in candidates
        if review_wave is None or str(candidate.get("review_wave", "")) == review_wave
    )


def _manual_review_candidates(
    manual_review_payload: Mapping[str, object],
) -> list[JSONDict]:
    return _dict_list(manual_review_payload, "primary_wave_reviewed")


def _manual_review_map(
    manual_review_payload: Mapping[str, object],
) -> dict[str, JSONDict]:
    return {
        str(candidate.get("object_uid", "")): candidate
        for candidate in _manual_review_candidates(manual_review_payload)
    }


def _recommended_rerun_candidates(
    *,
    first_pass_payload: Mapping[str, object],
    manual_review_payload: Mapping[str, object],
) -> tuple[str, ...]:
    primary_ids = set(_candidate_ids(first_pass_payload, review_wave="primary"))
    recommended = tuple(
        _string_list(manual_review_payload, "recommended_rerun_candidates")
    )
    invalid = [
        object_uid for object_uid in recommended if object_uid not in primary_ids
    ]
    if invalid:
        raise ValueError(
            "manual review recommended_rerun_candidates must be a subset of the "
            f"first-pass primary wave: {', '.join(invalid)}"
        )
    return recommended


def _baseline_candidate_map(
    discovery_payload: Mapping[str, object],
    *,
    promoted_snapshot: Mapping[str, object],
) -> dict[str, JSONDict]:
    promoted_ids = set(_string_list(promoted_snapshot, "candidate_order"))
    return {
        str(candidate.get("object_uid", "")): candidate
        for candidate in _dict_list(discovery_payload, "candidates")
        if str(candidate.get("object_uid", "")) in promoted_ids
    }


def _transition_payload(
    candidate_payload: Mapping[str, object],
) -> Mapping[str, object]:
    return _mapping_value(candidate_payload, "transition")


def _dataset_payload(candidate_payload: Mapping[str, object]) -> Mapping[str, object]:
    return _mapping_value(candidate_payload, "dataset_completeness")


def _state_transition_supported(candidate_payload: Mapping[str, object]) -> bool:
    transition = _transition_payload(candidate_payload)
    if "state_transition_supported" in transition:
        return _bool_value(transition, "state_transition_supported")
    return _bool_value(
        _dataset_payload(candidate_payload), "state_transition_supported"
    )


def _transition_detected(candidate_payload: Mapping[str, object]) -> bool:
    return _bool_value(_transition_payload(candidate_payload), "transition_detected")


def _alignment_status(candidate_payload: Mapping[str, object]) -> str:
    transition = _transition_payload(candidate_payload)
    if "alignment_status" in transition:
        return str(transition.get("alignment_status", ""))
    return str(_dataset_payload(candidate_payload).get("state_window_alignment", ""))


def _support_score(candidate_payload: Mapping[str, object]) -> int:
    return int(
        str(_dataset_payload(candidate_payload).get("state_window_support_score", 0))
    )


def _row_count(candidate_payload: Mapping[str, object], key: str) -> int:
    return int(str(_dataset_payload(candidate_payload).get(key, 0)))


def _raw_lightcurve_source(candidate_payload: Mapping[str, object]) -> str:
    return str(_dataset_payload(candidate_payload).get("raw_lightcurve_source", ""))


def _evidence_level(candidate_payload: Mapping[str, object]) -> str:
    evidence_bundle = _mapping_value(candidate_payload, "evidence_bundle")
    value = evidence_bundle.get("evidence_level")
    if isinstance(value, str) and value:
        return value
    return str(_transition_payload(candidate_payload).get("evidence_level", ""))


def _comparison_status(
    *,
    baseline_payload: Mapping[str, object],
    rerun_payload: Mapping[str, object],
) -> str:
    if _state_transition_supported(
        baseline_payload
    ) and not _state_transition_supported(rerun_payload):
        return "degraded_transition_support"
    if _transition_detected(baseline_payload) and not _transition_detected(
        rerun_payload
    ):
        return "transition_not_reproduced"
    if _raw_lightcurve_source(rerun_payload) != _raw_lightcurve_source(
        baseline_payload
    ):
        return "raw_lightcurve_source_changed"
    if str(rerun_payload.get("anomaly_category", "")) != str(
        baseline_payload.get("anomaly_category", "")
    ):
        return "anomaly_category_changed"
    if _alignment_status(rerun_payload) != _alignment_status(baseline_payload):
        return "alignment_status_changed"
    if _evidence_level(rerun_payload) != _evidence_level(baseline_payload):
        return "evidence_level_changed"
    return "preserved"


def _build_comparison(
    *,
    baseline_payload: Mapping[str, object],
    rerun_payload: Mapping[str, object],
) -> JSONDict:
    status = _comparison_status(
        baseline_payload=baseline_payload,
        rerun_payload=rerun_payload,
    )
    baseline_rank = _float_value(baseline_payload, "rank_score")
    rerun_rank = _float_value(rerun_payload, "rank_score")
    baseline_transition = _transition_payload(baseline_payload)
    rerun_transition = _transition_payload(rerun_payload)
    return {
        "status": status,
        "transition_support_preserved": (
            _state_transition_supported(baseline_payload)
            and _state_transition_supported(rerun_payload)
        ),
        "transition_detected_preserved": (
            _transition_detected(baseline_payload)
            and _transition_detected(rerun_payload)
        ),
        "anomaly_category_changed": str(rerun_payload.get("anomaly_category", ""))
        != str(baseline_payload.get("anomaly_category", "")),
        "alignment_status_changed": _alignment_status(rerun_payload)
        != _alignment_status(baseline_payload),
        "evidence_level_changed": _evidence_level(rerun_payload)
        != _evidence_level(baseline_payload),
        "raw_lightcurve_source_changed": _raw_lightcurve_source(rerun_payload)
        != _raw_lightcurve_source(baseline_payload),
        "offline_fallback_present": _raw_lightcurve_source(rerun_payload)
        == "offline_ci_fallback",
        "baseline_transition_detected": _transition_detected(baseline_payload),
        "rerun_transition_detected": _transition_detected(rerun_payload),
        "baseline_state_transition_supported": _state_transition_supported(
            baseline_payload
        ),
        "rerun_state_transition_supported": _state_transition_supported(rerun_payload),
        "baseline_alignment_status": _alignment_status(baseline_payload),
        "rerun_alignment_status": _alignment_status(rerun_payload),
        "baseline_evidence_level": _evidence_level(baseline_payload),
        "rerun_evidence_level": _evidence_level(rerun_payload),
        "baseline_anomaly_category": str(baseline_payload.get("anomaly_category", "")),
        "rerun_anomaly_category": str(rerun_payload.get("anomaly_category", "")),
        "baseline_rank_score": baseline_rank,
        "rerun_rank_score": rerun_rank,
        "rank_score_delta": round(rerun_rank - baseline_rank, 3),
        "baseline_lag_state_change": _float_value(
            baseline_transition,
            "lag_state_change",
        ),
        "rerun_lag_state_change": _float_value(rerun_transition, "lag_state_change"),
        "lag_state_change_delta": round(
            _float_value(rerun_transition, "lag_state_change")
            - _float_value(baseline_transition, "lag_state_change"),
            3,
        ),
        "baseline_line_response_ratio": _float_value(
            baseline_transition,
            "line_response_ratio",
        ),
        "rerun_line_response_ratio": _float_value(
            rerun_transition,
            "line_response_ratio",
        ),
        "line_response_ratio_delta": round(
            _float_value(rerun_transition, "line_response_ratio")
            - _float_value(baseline_transition, "line_response_ratio"),
            3,
        ),
        "baseline_support_score": _support_score(baseline_payload),
        "rerun_support_score": _support_score(rerun_payload),
        "support_score_delta": _support_score(rerun_payload)
        - _support_score(baseline_payload),
        "baseline_pre_window_row_count": _row_count(
            baseline_payload,
            "pre_window_row_count",
        ),
        "rerun_pre_window_row_count": _row_count(rerun_payload, "pre_window_row_count"),
        "pre_window_row_count_delta": _row_count(
            rerun_payload,
            "pre_window_row_count",
        )
        - _row_count(baseline_payload, "pre_window_row_count"),
        "baseline_post_window_row_count": _row_count(
            baseline_payload,
            "post_window_row_count",
        ),
        "rerun_post_window_row_count": _row_count(
            rerun_payload,
            "post_window_row_count",
        ),
        "post_window_row_count_delta": _row_count(
            rerun_payload,
            "post_window_row_count",
        )
        - _row_count(baseline_payload, "post_window_row_count"),
        "baseline_raw_lightcurve_source": _raw_lightcurve_source(baseline_payload),
        "rerun_raw_lightcurve_source": _raw_lightcurve_source(rerun_payload),
    }


def _candidate_summary(candidate: Mapping[str, object]) -> str:
    comparison = _mapping_value(candidate, "comparison")
    manual_review = _mapping_value(candidate, "manual_review")
    return (
        f"# Primary-Wave Rerun Candidate {candidate['object_uid']}\n\n"
        f"- Canonical name: {candidate['canonical_name']}\n"
        f"- Manual-review disposition: {manual_review['disposition']}\n"
        f"- Manual-review reason: {manual_review['reason']}\n"
        f"- Manual-review key caveat: {manual_review.get('key_caveat', '')}\n"
        f"- Comparison status: {comparison['status']}\n"
        "- Transition support preserved: "
        f"{comparison['transition_support_preserved']}\n"
        f"- Transition detection preserved: "
        f"{comparison['transition_detected_preserved']}\n"
        f"- Offline fallback present: {comparison['offline_fallback_present']}\n"
        f"- Next action: {candidate['next_action']}\n\n"
        "## Comparison\n\n"
        f"- Baseline anomaly category: {comparison['baseline_anomaly_category']}\n"
        f"- Rerun anomaly category: {comparison['rerun_anomaly_category']}\n"
        f"- Baseline rank score: {comparison['baseline_rank_score']}\n"
        f"- Rerun rank score: {comparison['rerun_rank_score']}\n"
        f"- Rank score delta: {comparison['rank_score_delta']}\n"
        f"- Baseline lag state change: {comparison['baseline_lag_state_change']}\n"
        f"- Rerun lag state change: {comparison['rerun_lag_state_change']}\n"
        f"- Lag state change delta: {comparison['lag_state_change_delta']}\n"
        "- Baseline line-response ratio: "
        f"{comparison['baseline_line_response_ratio']}\n"
        f"- Rerun line-response ratio: {comparison['rerun_line_response_ratio']}\n"
        f"- Line-response ratio delta: {comparison['line_response_ratio_delta']}\n"
        f"- Baseline support score: {comparison['baseline_support_score']}\n"
        f"- Rerun support score: {comparison['rerun_support_score']}\n"
        f"- Support score delta: {comparison['support_score_delta']}\n"
    )


def _report_candidate_line(candidate: Mapping[str, object]) -> str:
    comparison = _mapping_value(candidate, "comparison")
    return (
        f"- {candidate['canonical_name']} ({candidate['object_uid']}): "
        f"status={comparison['status']}; "
        f"transition_support_preserved={comparison['transition_support_preserved']}; "
        f"transition_detected_preserved={comparison['transition_detected_preserved']}; "
        f"rank_delta={comparison['rank_score_delta']}; "
        f"support_delta={comparison['support_score_delta']}; "
        f"raw_lightcurve_source={comparison['rerun_raw_lightcurve_source']}"
    )


def _rerun_report(payload: Mapping[str, object], candidates: list[JSONDict]) -> str:
    summary = _mapping_value(payload, "summary")
    promoted_snapshot = _mapping_value(payload, "promoted_snapshot")
    first_pass_review = _mapping_value(payload, "first_pass_review")
    manual_review = _mapping_value(payload, "manual_review_artifact")
    candidate_lines = "\n".join(
        _report_candidate_line(candidate) for candidate in candidates
    )
    limitations = (
        "\n".join(f"- {item}" for item in _string_list(payload, "limitations"))
        or "- none"
    )
    return (
        f"# Primary-Wave Rerun {payload['run_id']}\n\n"
        "## Summary\n\n"
        f"- Readiness: {payload['readiness']}\n"
        f"- Promoted snapshot id: {promoted_snapshot['promoted_snapshot_id']}\n"
        f"- First-pass run id: {first_pass_review['run_id']}\n"
        f"- Manual-review artifact: {manual_review['path']}\n"
        f"- Reviewed candidate count: {summary['reviewed_candidate_count']}\n"
        "- Recommended rerun candidate count: "
        f"{summary['recommended_rerun_candidate_count']}\n"
        f"- Rerun candidate count: {summary['rerun_candidate_count']}\n"
        "- Transition support preserved count: "
        f"{summary['transition_support_preserved_count']}\n"
        "- Transition detected preserved count: "
        f"{summary['transition_detected_preserved_count']}\n"
        f"- Degraded candidate count: {summary['degraded_candidate_count']}\n"
        f"- Offline fallback count: {summary['offline_fallback_count']}\n\n"
        "## Strategy\n\n"
        "- Only candidates explicitly advanced by manual review are rerun.\n"
        "- The promoted baseline payload is preserved and compared against the "
        "rerun payload rather than overwritten.\n"
        "- Rerun results remain repository-local and still require dedicated "
        "scientific interpretation before broader claims.\n\n"
        "## Candidate Records\n\n"
        f"{candidate_lines or '- none'}\n\n"
        "## Limitations\n\n"
        f"{limitations}\n"
    )


def materialize_primary_wave_rerun_package(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_id: str = "primary_wave_rerun",
    profile: str = "primary_wave_rerun",
    snapshot_run_id: str = "discovery_snapshot",
    first_pass_run_id: str = "first_pass_review",
    manual_review_path: Path = Path("primary_wave_manual_review/index.json"),
    verification: tuple[VerificationCheck, ...] | None = None,
    tools: tuple[ToolStatus, ...] | None = None,
) -> Path:
    """Materialize a rerun package for reviewed primary-wave candidates."""
    verification_records: tuple[VerificationCheck, ...] = verification or ()
    tool_records: tuple[ToolStatus, ...] = tools or detect_tool_statuses()
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    promoted_snapshot = validate_promoted_discovery_snapshot(
        artifact_root=artifact_root,
        snapshot_run_id=snapshot_run_id,
    )
    discovery_payload = _load_required_run(
        artifact_root,
        str(promoted_snapshot["source_run_id"]),
    )
    first_pass_payload = _load_required_run(artifact_root, first_pass_run_id)
    resolved_manual_review_path = _resolve_manual_review_path(
        artifact_root,
        manual_review_path,
    )
    manual_review_payload = _load_mapping_path(resolved_manual_review_path)
    if str(manual_review_payload.get("promoted_snapshot_id", "")) != str(
        promoted_snapshot["promoted_snapshot_id"]
    ):
        raise ValueError(
            "manual review artifact must match the promoted discovery snapshot"
        )
    first_pass_snapshot = _mapping_value(first_pass_payload, "promoted_snapshot")
    if str(first_pass_snapshot.get("promoted_snapshot_id", "")) != str(
        promoted_snapshot["promoted_snapshot_id"]
    ):
        raise ValueError("first-pass review must match the promoted discovery snapshot")

    recommended_ids = _recommended_rerun_candidates(
        first_pass_payload=first_pass_payload,
        manual_review_payload=manual_review_payload,
    )
    review_map = _manual_review_map(manual_review_payload)
    missing_review_records = [
        object_uid for object_uid in recommended_ids if object_uid not in review_map
    ]
    if missing_review_records:
        raise ValueError(
            "manual review is missing primary-wave review records for: "
            f"{', '.join(missing_review_records)}"
        )
    non_advanced_recommendations = [
        object_uid
        for object_uid in recommended_ids
        if str(review_map[object_uid].get("disposition", "")) != "advance"
    ]
    if non_advanced_recommendations:
        raise ValueError(
            "manual review recommended_rerun_candidates must all be explicitly "
            f"marked advance: {', '.join(non_advanced_recommendations)}"
        )

    baseline_candidates = _baseline_candidate_map(
        discovery_payload,
        promoted_snapshot=promoted_snapshot,
    )
    missing_baselines = [
        object_uid
        for object_uid in recommended_ids
        if object_uid not in baseline_candidates
    ]
    if missing_baselines:
        raise ValueError(
            "promoted discovery snapshot baseline is missing candidate payloads for: "
            f"{', '.join(missing_baselines)}"
        )

    rerun_records = load_literal_discovery_holdout_records(
        repo_root,
        selected_object_uids=recommended_ids,
    )
    rerun_record_map = {record.object_uid: record for record in rerun_records}
    missing_rerun_records = [
        object_uid
        for object_uid in recommended_ids
        if object_uid not in rerun_record_map
    ]
    if missing_rerun_records:
        raise ValueError(
            "literal discovery rerun inputs are missing reviewed candidates: "
            f"{', '.join(missing_rerun_records)}"
        )

    candidates: list[JSONDict] = []
    degraded_candidate_count = 0
    transition_support_preserved_count = 0
    transition_detected_preserved_count = 0
    offline_fallback_count = 0
    for object_uid in recommended_ids:
        baseline_payload = baseline_candidates[object_uid]
        rerun_payload = materialize_discovery_candidate_bundle(
            record=rerun_record_map[object_uid],
            run_id=run_id,
            run_dir=run_dir,
        )
        comparison = _build_comparison(
            baseline_payload=baseline_payload,
            rerun_payload=rerun_payload,
        )
        if str(comparison["status"]) != "preserved":
            degraded_candidate_count += 1
        if bool(comparison["transition_support_preserved"]):
            transition_support_preserved_count += 1
        if bool(comparison["transition_detected_preserved"]):
            transition_detected_preserved_count += 1
        if bool(comparison["offline_fallback_present"]):
            offline_fallback_count += 1
        candidate_record: JSONDict = {
            "object_uid": object_uid,
            "canonical_name": str(rerun_payload.get("canonical_name", object_uid)),
            "manual_review": review_map[object_uid],
            "baseline_promoted_payload": baseline_payload,
            "rerun_candidate_payload": rerun_payload,
            "comparison": comparison,
            "next_action": "rerun_interpretation_review_before_broader_claims",
            "claims_boundary": {
                "claims_scope": "repository_local_reviewed_rerun",
                "broader_scientific_interpretation_requires_follow_on_review": True,
                "publication_claims_not_demonstrated": True,
            },
        }
        candidate_dir = run_dir / "candidates" / object_uid
        _write_json(candidate_dir / "index.json", candidate_record)
        summary = _candidate_summary(candidate_record)
        _write_markdown(candidate_dir / "summary.md", summary)
        _write_markdown(candidate_dir / "memo.md", summary)
        candidates.append(candidate_record)

    manual_review_path_text = (
        str(resolved_manual_review_path.relative_to(artifact_root))
        if resolved_manual_review_path.is_relative_to(artifact_root)
        else str(resolved_manual_review_path)
    )
    payload = _package_header(
        run_id=run_id,
        profile=profile,
        package_type="primary_wave_rerun",
        benchmark_scope=(
            "Repository-local rerun package for manually advanced discovery "
            "primary-wave candidates."
        ),
        readiness="ready_with_warnings" if candidates else "degraded",
        verification=verification_records,
        tools=tool_records,
        summary={
            "reviewed_candidate_count": int(
                str(manual_review_payload.get("reviewed_candidate_count", 0))
            ),
            "recommended_rerun_candidate_count": len(recommended_ids),
            "rerun_candidate_count": len(candidates),
            "transition_support_preserved_count": transition_support_preserved_count,
            "transition_detected_preserved_count": transition_detected_preserved_count,
            "degraded_candidate_count": degraded_candidate_count,
            "offline_fallback_count": offline_fallback_count,
        },
        demonstrated=(
            "Reviewed primary-wave candidates can be rerun from repository-local "
            "discovery inputs and compared to the promoted snapshot baseline.",
        ),
        not_demonstrated=(
            "Rerun outputs do not by themselves establish broader scientific claims "
            "or publication readiness.",
        ),
        limitations=(
            "Rerun results remain repository-local and require dedicated "
            "scientific interpretation.",
            "The rerun package is restricted to candidates already advanced by the "
            "manual primary-wave review artifact.",
        ),
        warnings=tuple(
            warning
            for warning in (
                "repository_local_rerun_review_required",
                (
                    "rerun_status_changes_present"
                    if degraded_candidate_count > 0
                    else ""
                ),
                (
                    "offline_photometry_fallback_present"
                    if offline_fallback_count > 0
                    else ""
                ),
            )
            if warning
        ),
        artifact_root=artifact_root,
    )
    payload["promoted_snapshot"] = {
        "snapshot_run_id": snapshot_run_id,
        "promoted_snapshot_id": str(promoted_snapshot["promoted_snapshot_id"]),
        "source_run_id": str(promoted_snapshot["source_run_id"]),
        "candidate_inventory_digest": str(
            promoted_snapshot["candidate_inventory_digest"]
        ),
        "candidate_order_digest": str(promoted_snapshot["candidate_order_digest"]),
    }
    payload["first_pass_review"] = {
        "run_id": first_pass_run_id,
        "path": f"{first_pass_run_id}/index.json",
        "primary_wave_candidate_ids": list(
            _candidate_ids(first_pass_payload, review_wave="primary")
        ),
    }
    payload["manual_review_artifact"] = {
        "path": manual_review_path_text,
        "promoted_snapshot_id": str(manual_review_payload["promoted_snapshot_id"]),
        "reviewed_candidate_count": int(
            str(manual_review_payload.get("reviewed_candidate_count", 0))
        ),
        "recommended_rerun_candidates": list(recommended_ids),
    }
    payload["claims_boundary"] = {
        "claims_scope": "repository_local_reviewed_rerun",
        "broader_scientific_interpretation_requires_follow_on_review": True,
        "publication_claims_not_demonstrated": True,
    }
    payload["candidates"] = candidates
    payload["report_path"] = f"{run_id}/report.md"
    report = _rerun_report(payload, candidates)
    _write_json(run_dir / "index.json", payload)
    _write_markdown(run_dir / "summary.md", _package_dossier(payload))
    _write_markdown(run_dir / "dossier.md", _package_dossier(payload))
    _write_markdown(run_dir / "report.md", report)
    _update_root_index(
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        package_type="primary_wave_rerun",
        readiness=str(payload["readiness"]),
        count=len(candidates),
    )
    return run_dir / "index.json"
