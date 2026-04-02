"""Benchmark-governed first-pass review package assembly."""

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
from .readiness import ToolStatus, VerificationCheck, _write_json, detect_tool_statuses

PRIMARY_WAVE_TRANSITION_SUPPORTED_REQUIRED = True
PRIMARY_WAVE_TRANSITION_DETECTED_REQUIRED = True

PRIMARY_WAVE_RULE: JSONDict = {
    "state_transition_supported": PRIMARY_WAVE_TRANSITION_SUPPORTED_REQUIRED,
    "transition_detected": PRIMARY_WAVE_TRANSITION_DETECTED_REQUIRED,
}

BENCHMARK_LINK_TO_ANCHORS: dict[str, tuple[str, ...]] = {
    "gold_validation": ("gold-ngc5548", "gold-ngc3783"),
    "silver_validation": ("silver-population",),
    "continuum_validation": ("continuum-behavior",),
    "efficacy_benchmark": ("efficacy-interpretability",),
    "root_authority_audit": ("root-authority-gate",),
}

REVIEW_PRIORITY_ORDER = {
    "high": 0,
    "medium": 1,
    "low": 2,
}


def _load_required_run(artifact_root: Path, run_id: str) -> JSONDict:
    path = artifact_root / run_id / "index.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{run_id} payload must be a mapping")
    return payload


def _bool_value(
    payload: Mapping[str, object],
    key: str,
    default: bool = False,
) -> bool:
    value = payload.get(key, default)
    return value if isinstance(value, bool) else default


def _find_dict_item(
    records: list[JSONDict],
    key: str,
    target: str,
) -> JSONDict:
    for record in records:
        if str(record.get(key, "")) == target:
            return record
    raise ValueError(f"missing record for {key}={target}")


def _anchor_summary(anchor: Mapping[str, object]) -> str:
    metrics = _mapping_value(anchor, "metrics")
    metric_lines = "\n".join(
        f"- {key}: {value}" for key, value in sorted(metrics.items())
    ) or "- none"
    limitations = "\n".join(
        f"- {item}" for item in _string_list(anchor, "limitations")
    ) or "- none"
    return (
        f"# Anchor {anchor['anchor_id']}\n\n"
        f"- Label: {anchor['label']}\n"
        f"- Kind: {anchor['anchor_kind']}\n"
        f"- Source run: {anchor['source_run']}\n"
        f"- Role: {anchor['role']}\n"
        f"- Evidence level: {anchor['evidence_level']}\n\n"
        "## Metrics\n\n"
        f"{metric_lines}\n\n"
        "## Limitations\n\n"
        f"{limitations}\n"
    )


def _candidate_summary(candidate: Mapping[str, object]) -> str:
    benchmark_links = ", ".join(_string_list(candidate, "benchmark_links")) or "none"
    anchor_links = ", ".join(_string_list(candidate, "benchmark_anchor_ids")) or "none"
    limitations = "\n".join(
        f"- {item}" for item in _string_list(candidate, "limitations")
    ) or "- none"
    score_components = _mapping_value(candidate, "score_components")
    score_lines = "\n".join(
        f"- {key}: {value}" for key, value in sorted(score_components.items())
    ) or "- none"
    return (
        f"# Candidate {candidate['object_uid']}\n\n"
        f"- Canonical name: {candidate['canonical_name']}\n"
        f"- Review wave: {candidate['review_wave']}\n"
        f"- Review order: {candidate['review_order']}\n"
        f"- Disposition: {candidate['disposition']}\n"
        f"- Next action: {candidate['next_action']}\n"
        f"- Real-data rerun required: {candidate['real_data_rerun_required']}\n"
        f"- Evidence level: {candidate['evidence_level']}\n"
        f"- Transition alignment status: {candidate['transition_alignment_status']}\n"
        f"- State transition supported: {candidate['state_transition_supported']}\n"
        f"- Benchmark links: {benchmark_links}\n"
        f"- Benchmark anchor ids: {anchor_links}\n"
        f"- Reason: {candidate['reason']}\n\n"
        "## Score Components\n\n"
        f"{score_lines}\n\n"
        "## Limitations\n\n"
        f"{limitations}\n"
    )


def _report_candidate_line(candidate: Mapping[str, object]) -> str:
    benchmark_links = ", ".join(_string_list(candidate, "benchmark_links"))
    return (
        f"- {candidate['canonical_name']} ({candidate['object_uid']}): "
        f"{candidate['review_wave']}, {candidate['disposition']}, "
        f"{candidate['next_action']}; "
        f"rank={_float_value(candidate, 'rank_score'):.3f}; "
        f"lag_state_change={_float_value(candidate, 'lag_state_change'):.3f}; "
        "line_response_ratio="
        f"{_float_value(candidate, 'line_response_ratio'):.3f}; "
        f"alignment_status={candidate['transition_alignment_status']}; "
        f"benchmark_links={benchmark_links}; "
        f"reason={candidate['reason']}"
    )


def _review_report(
    *,
    payload: Mapping[str, object],
    anchors: list[JSONDict],
    candidates: list[JSONDict],
    primary_ids: tuple[str, ...],
    deferred_ids: tuple[str, ...],
) -> str:
    summary = _mapping_value(payload, "summary")
    promoted_snapshot = _mapping_value(payload, "promoted_snapshot")
    anchor_lines = "\n".join(
        (
            f"- {anchor['label']} ({anchor['source_run']}): {anchor['role']}; "
            f"metrics={_mapping_value(anchor, 'metrics')}"
        )
        for anchor in anchors
    )
    candidate_lines = "\n".join(
        _report_candidate_line(candidate) for candidate in candidates
    ) or "- none"
    limitations = "\n".join(
        f"- {item}" for item in _string_list(payload, "limitations")
    )
    return (
        f"# First-Pass Review {payload['run_id']}\n\n"
        "## Summary\n\n"
        f"- Readiness: {payload['readiness']}\n"
        f"- Anchor count: {summary['anchor_count']}\n"
        f"- Candidate count: {summary['candidate_count']}\n"
        f"- Primary wave count: {summary['primary_wave_count']}\n"
        f"- Deferred wave count: {summary['deferred_wave_count']}\n"
        f"- Real-data rerun required count: "
        f"{summary['real_data_rerun_required_count']}\n"
        f"- Promoted snapshot id: {promoted_snapshot['promoted_snapshot_id']}\n"
        "- Promoted inventory digest: "
        f"{promoted_snapshot['candidate_inventory_digest']}\n"
        f"- Promoted order digest: {promoted_snapshot['candidate_order_digest']}\n\n"
        "## Strategy\n\n"
        "- Anchor calibration precedes hold-out interpretation.\n"
        "- Discovery snapshot promotion excludes candidates without complete "
        "pre/post state-window coverage.\n"
        "- Same-state aligned candidates remain explicit as precursor-only context "
        "and cannot satisfy the transition-led wave rule.\n"
        "- Primary wave is restricted to promoted candidates with supported "
        "changing-state evidence and recorded transition detection.\n"
        "- Review order is deterministic and uses tracked review priority, rank "
        "score, benchmark links, and object identifier fields.\n"
        "- Every candidate remains under a real-data rerun requirement before "
        "broader scientific interpretation.\n\n"
        "## Anchors\n\n"
        f"{anchor_lines}\n\n"
        "## Primary Wave\n\n"
        + ("\n".join(f"- {item}" for item in primary_ids) or "- none")
        + "\n\n## Deferred Wave\n\n"
        + ("\n".join(f"- {item}" for item in deferred_ids) or "- none")
        + "\n\n## Candidate Records\n\n"
        + candidate_lines
        + "\n\n## Limitations\n\n"
        + limitations
        + "\n"
    )


def _build_anchor_records(
    *,
    gold_payload: Mapping[str, object],
    silver_payload: Mapping[str, object],
    continuum_payload: Mapping[str, object],
    efficacy_payload: Mapping[str, object],
    audit_payload: Mapping[str, object],
) -> list[JSONDict]:
    gold_objects = _dict_list(gold_payload, "objects")
    ngc5548 = _find_dict_item(gold_objects, "object_uid", "ngc5548")
    ngc3783 = _find_dict_item(gold_objects, "object_uid", "ngc3783")
    silver_summary = _mapping_value(silver_payload, "summary")
    continuum_summary = _mapping_value(continuum_payload, "summary")
    efficacy_summary = _mapping_value(efficacy_payload, "summary")
    audit_summary = _mapping_value(audit_payload, "summary")
    return [
        {
            "anchor_id": "gold-ngc5548",
            "anchor_kind": "benchmark_object",
            "label": str(ngc5548["canonical_name"]),
            "source_run": "gold_validation",
            "source_path": "gold_validation/objects/ngc5548/index.json",
            "role": str(ngc5548["benchmark_regime"]),
            "evidence_level": str(ngc5548["evidence_level"]),
            "metrics": {
                "literature_lag_day": _float_value(ngc5548, "literature_lag_day"),
                "coverage_rate": _float_value(ngc5548, "coverage_rate"),
                "primary_metric": _float_value(ngc5548, "primary_metric"),
            },
            "limitations": _string_list(gold_payload, "limitations"),
        },
        {
            "anchor_id": "gold-ngc3783",
            "anchor_kind": "benchmark_object",
            "label": str(ngc3783["canonical_name"]),
            "source_run": "gold_validation",
            "source_path": "gold_validation/objects/ngc3783/index.json",
            "role": str(ngc3783["benchmark_regime"]),
            "evidence_level": str(ngc3783["evidence_level"]),
            "metrics": {
                "literature_lag_day": _float_value(ngc3783, "literature_lag_day"),
                "coverage_rate": _float_value(ngc3783, "coverage_rate"),
                "primary_metric": _float_value(ngc3783, "primary_metric"),
            },
            "limitations": _string_list(gold_payload, "limitations"),
        },
        {
            "anchor_id": "silver-population",
            "anchor_kind": "validation_summary",
            "label": "Silver Population Gate",
            "source_run": "silver_validation",
            "source_path": "silver_validation/index.json",
            "role": "population_consistency_reference",
            "evidence_level": "repository_local_package",
            "metrics": {
                "population_count": int(str(silver_summary.get("population_count", 0))),
                "coverage_rate": _float_value(silver_summary, "coverage_rate"),
                "false_positive_rate": _float_value(
                    silver_summary, "false_positive_rate"
                ),
                "disagreement_rate": _float_value(
                    silver_summary, "disagreement_rate"
                ),
            },
            "limitations": _string_list(silver_payload, "limitations"),
        },
        {
            "anchor_id": "continuum-behavior",
            "anchor_kind": "validation_summary",
            "label": "Continuum Behavior Gate",
            "source_run": "continuum_validation",
            "source_path": "continuum_validation/index.json",
            "role": "state_change_and_contamination_reference",
            "evidence_level": "repository_local_package",
            "metrics": {
                "classification_accuracy": _float_value(
                    continuum_summary, "classification_accuracy"
                ),
                "cadence_stability_score": _float_value(
                    continuum_summary, "cadence_stability_score"
                ),
                "warning_count": int(str(continuum_summary.get("warning_count", 0))),
            },
            "limitations": _string_list(continuum_payload, "limitations"),
        },
        {
            "anchor_id": "efficacy-interpretability",
            "anchor_kind": "validation_summary",
            "label": "Efficacy Interpretability Gate",
            "source_run": "efficacy_benchmark",
            "source_path": "efficacy_benchmark/index.json",
            "role": "audio_interpretability_reference",
            "evidence_level": "repository_local_package",
            "metrics": {
                "audio_only_accuracy": _float_value(
                    efficacy_summary, "audio_only_accuracy"
                ),
                "plot_only_accuracy": _float_value(
                    efficacy_summary, "plot_only_accuracy"
                ),
                "plot_audio_accuracy": _float_value(
                    efficacy_summary, "plot_audio_accuracy"
                ),
            },
            "limitations": _string_list(efficacy_payload, "limitations"),
        },
        {
            "anchor_id": "root-authority-gate",
            "anchor_kind": "audit_summary",
            "label": "Root Authority Gate",
            "source_run": "root_authority_audit",
            "source_path": "root_authority_audit/index.json",
            "role": "repository_local_claims_boundary",
            "evidence_level": "repository_local_package",
            "metrics": {
                "condition_count": int(str(audit_summary.get("condition_count", 0))),
                "conditions_passed": int(
                    str(audit_summary.get("conditions_passed", 0))
                ),
                "promotion_allowed": _bool_value(
                    audit_summary, "promotion_allowed", False
                ),
            },
            "limitations": _string_list(audit_payload, "limitations"),
        },
    ]


def _primary_wave_reason(candidate: Mapping[str, object]) -> str:
    return (
        "Candidate satisfies the transition-supported primary-wave rule and "
        "should receive manual review before a real-data rerun."
    )


def _deferred_reason(
    *,
    state_transition_supported: bool,
    transition_alignment_status: str,
    transition_detected: bool,
) -> str:
    if not state_transition_supported:
        return (
            "Deferred because the promoted evidence records a precursor-only "
            f"alignment status ({transition_alignment_status}) rather than a "
            "supported changing-state pair."
        )
    if not transition_detected:
        return (
            "Deferred because the tracked fixture-bounded evidence does not record "
            "a transition detection."
        )
    return "Deferred because the candidate does not satisfy the declared rule set."


def _review_priority_rank(value: str) -> int:
    return REVIEW_PRIORITY_ORDER.get(value, len(REVIEW_PRIORITY_ORDER))


def _state_transition_supported(
    *,
    candidate: Mapping[str, object],
    transition: Mapping[str, object],
    dataset_completeness: Mapping[str, object],
    transition_detected: bool,
) -> bool:
    transition_value = transition.get("state_transition_supported")
    if isinstance(transition_value, bool):
        return transition_value
    completeness_value = dataset_completeness.get("state_transition_supported")
    if isinstance(completeness_value, bool):
        return completeness_value

    # Historical fixture artifacts may predate explicit transition-support fields.
    return transition_detected and str(candidate.get("anomaly_category", "")) == (
        "clagn_transition"
    )


def _promoted_candidate_ids(promoted_snapshot: Mapping[str, object]) -> tuple[str, ...]:
    return tuple(_string_list(promoted_snapshot, "candidate_order"))


def _filter_discovery_candidates(
    discovery_payload: Mapping[str, object],
    *,
    promoted_snapshot: Mapping[str, object],
) -> list[JSONDict]:
    promoted_ids = set(_promoted_candidate_ids(promoted_snapshot))
    if not promoted_ids:
        return []
    return [
        candidate
        for candidate in _dict_list(discovery_payload, "candidates")
        if str(candidate.get("object_uid", "")) in promoted_ids
    ]


def _build_candidate_reviews(
    discovery_candidates: list[JSONDict],
    *,
    source_run_id: str,
) -> list[JSONDict]:
    reviews: list[JSONDict] = []
    for candidate in discovery_candidates:
        evidence_bundle = _mapping_value(candidate, "evidence_bundle")
        transition = _mapping_value(candidate, "transition")
        dataset_completeness = _mapping_value(candidate, "dataset_completeness")
        benchmark_links = _string_list(evidence_bundle, "benchmark_links")
        anchor_ids = sorted(
            {
                anchor_id
                for link in benchmark_links
                for anchor_id in BENCHMARK_LINK_TO_ANCHORS.get(link, ())
            }
        )
        rank_score = _float_value(candidate, "rank_score")
        lag_state_change = _float_value(evidence_bundle, "lag_state_change")
        line_response_ratio = _float_value(evidence_bundle, "line_response_ratio")
        transition_detected = _bool_value(transition, "transition_detected")
        state_transition_supported = _state_transition_supported(
            candidate=candidate,
            transition=transition,
            dataset_completeness=dataset_completeness,
            transition_detected=transition_detected,
        )
        transition_alignment_status = str(
            transition.get(
                "alignment_status",
                dataset_completeness.get("state_window_alignment", "unknown"),
            )
        )
        primary_wave = state_transition_supported and transition_detected
        reviews.append(
            {
                "object_uid": str(candidate["object_uid"]),
                "canonical_name": str(candidate["canonical_name"]),
                "anomaly_category": str(candidate["anomaly_category"]),
                "review_priority": str(candidate["review_priority"]),
                "method_support_count": int(
                    str(candidate.get("method_support_count", 0))
                ),
                "review_wave": "primary" if primary_wave else "deferred",
                "disposition": "review_now" if primary_wave else "defer",
                "next_action": (
                    "manual_review_then_real_data_rerun"
                    if primary_wave
                    else "complete_primary_wave_then_real_data_rerun"
                ),
                "real_data_rerun_required": True,
                "reason": (
                    _primary_wave_reason(candidate)
                    if primary_wave
                    else _deferred_reason(
                        state_transition_supported=state_transition_supported,
                        transition_alignment_status=transition_alignment_status,
                        transition_detected=transition_detected,
                    )
                ),
                "rank_score": rank_score,
                "benchmark_links": benchmark_links,
                "benchmark_anchor_ids": anchor_ids,
                "evidence_level": str(
                    evidence_bundle.get(
                        "evidence_level",
                        transition.get("evidence_level", "unknown"),
                    )
                ),
                "limitations": _string_list(candidate, "limitations"),
                "score_components": {
                    str(key): value
                    for key, value in _mapping_value(
                        evidence_bundle, "score_components"
                    ).items()
                },
                "lag_state_change": lag_state_change,
                "line_response_ratio": line_response_ratio,
                "transition_detected": transition_detected,
                "state_transition_supported": state_transition_supported,
                "transition_alignment_status": transition_alignment_status,
                "source_paths": {
                    "candidate_index": (
                        f"{source_run_id}/candidates/{candidate['object_uid']}/index.json"
                    ),
                    "candidate_memo": str(candidate.get("memo_path", "")),
                },
            }
        )
    reviews.sort(
        key=lambda item: (
            0 if str(item["review_wave"]) == "primary" else 1,
            _review_priority_rank(str(item["review_priority"])),
            -_float_value(item, "rank_score"),
            tuple(sorted(_string_list(item, "benchmark_links"))),
            str(item["object_uid"]),
        )
    )
    for order, review in enumerate(reviews, start=1):
        review["review_order"] = order
    return reviews


def materialize_first_pass_review_package(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_id: str = "first_pass_review",
    profile: str = "first_pass_review",
    snapshot_run_id: str = "discovery_snapshot",
    verification: tuple[VerificationCheck, ...] | None = None,
    tools: tuple[ToolStatus, ...] | None = None,
) -> Path:
    """Materialize the benchmark-governed first-pass review package."""
    verification_records: tuple[VerificationCheck, ...] = verification or ()
    tool_records: tuple[ToolStatus, ...] = tools or detect_tool_statuses()
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    gold_payload = _load_required_run(artifact_root, "gold_validation")
    silver_payload = _load_required_run(artifact_root, "silver_validation")
    continuum_payload = _load_required_run(artifact_root, "continuum_validation")
    efficacy_payload = _load_required_run(artifact_root, "efficacy_benchmark")
    audit_payload = _load_required_run(artifact_root, "root_authority_audit")
    promoted_snapshot = validate_promoted_discovery_snapshot(
        artifact_root=artifact_root,
        snapshot_run_id=snapshot_run_id,
    )
    source_run_id = str(promoted_snapshot["source_run_id"])
    discovery_payload = _load_required_run(artifact_root, source_run_id)

    anchors = _build_anchor_records(
        gold_payload=gold_payload,
        silver_payload=silver_payload,
        continuum_payload=continuum_payload,
        efficacy_payload=efficacy_payload,
        audit_payload=audit_payload,
    )
    candidates = _build_candidate_reviews(
        _filter_discovery_candidates(
            discovery_payload,
            promoted_snapshot=promoted_snapshot,
        ),
        source_run_id=source_run_id,
    )
    primary_ids = tuple(
        str(candidate["object_uid"])
        for candidate in candidates
        if str(candidate["review_wave"]) == "primary"
    )
    deferred_ids = tuple(
        str(candidate["object_uid"])
        for candidate in candidates
        if str(candidate["review_wave"]) == "deferred"
    )
    payload = _package_header(
        run_id=run_id,
        profile=profile,
        package_type="first_pass_review",
        benchmark_scope=(
            "Repository-local first-pass review over tracked benchmark, discovery, "
            "and audit artifacts."
        ),
        readiness="ready_with_warnings" if candidates else "degraded",
        verification=verification_records,
        tools=tool_records,
        summary={
            "anchor_count": len(anchors),
            "candidate_count": len(candidates),
            "primary_wave_count": len(primary_ids),
            "deferred_wave_count": len(deferred_ids),
            "real_data_rerun_required_count": sum(
                bool(candidate["real_data_rerun_required"]) for candidate in candidates
            ),
        },
        demonstrated=(
            "The repository records a deterministic first-pass review sequence from "
            "tracked benchmark and discovery artifacts.",
            "Every candidate retains evidence level, benchmark links, and explicit "
            "next actions.",
        ),
        not_demonstrated=(
            "The package does not convert fixture-bounded hold-out evidence into "
            "broader scientific claims.",
            "The package does not replace real-data reruns or external review.",
        ),
        limitations=(
            "Current discovery inputs remain fixture-bounded and repository-local.",
            "Only candidates present in the promoted discovery snapshot are "
            "reviewed.",
            "Wave assignment is a governance aid for review order rather than a "
            "recalibration of discovery scoring.",
            "Findings apply to the supplied artifact root and can change when a "
            "different discovery-analysis run is materialized.",
        ),
        warnings=tuple(
            warning
            for warning in (
                "fixture_bounded_holdout_evidence",
                "real_data_rerun_required_for_all_candidates",
                "no_complete_promoted_candidates" if not candidates else "",
            )
            if warning
        ),
        artifact_root=artifact_root,
    )
    payload["anchors"] = anchors
    payload["candidates"] = candidates
    payload["promoted_snapshot"] = {
        "snapshot_run_id": snapshot_run_id,
        "promoted_snapshot_id": str(promoted_snapshot["promoted_snapshot_id"]),
        "source_run_id": str(promoted_snapshot["source_run_id"]),
        "source_path": str(promoted_snapshot["source_path"]),
        "source_reference": str(promoted_snapshot["source_reference"]),
        "candidate_inventory_digest": str(
            promoted_snapshot["candidate_inventory_digest"]
        ),
        "candidate_order_digest": str(promoted_snapshot["candidate_order_digest"]),
    }
    payload["strategy"] = {
        "anchor_phase": {
            "phase_id": "anchor_calibration",
            "anchor_ids": [str(anchor["anchor_id"]) for anchor in anchors],
        },
        "promoted_snapshot_id": str(promoted_snapshot["promoted_snapshot_id"]),
        "primary_wave_rule": dict(PRIMARY_WAVE_RULE),
        "deferred_wave_rule": "all remaining tracked candidates",
        "ordering_fields": [
            "review_priority",
            "rank_score",
            "benchmark_links",
            "object_uid",
        ],
        "primary_wave_candidate_ids": list(primary_ids),
        "deferred_wave_candidate_ids": list(deferred_ids),
        "universal_requirements": [
            "manual scientific review",
            "real-data rerun before broader scientific interpretation",
        ],
    }

    anchor_dir = run_dir / "anchors"
    anchor_dir.mkdir(parents=True, exist_ok=True)
    for anchor in anchors:
        item_dir = anchor_dir / str(anchor["anchor_id"])
        item_dir.mkdir(parents=True, exist_ok=True)
        _write_json(item_dir / "index.json", anchor)
        _write_markdown(item_dir / "summary.md", _anchor_summary(anchor))

    candidate_dir = run_dir / "candidates"
    candidate_dir.mkdir(parents=True, exist_ok=True)
    for candidate in candidates:
        item_dir = candidate_dir / str(candidate["object_uid"])
        item_dir.mkdir(parents=True, exist_ok=True)
        candidate["memo_path"] = (
            f"{run_id}/candidates/{candidate['object_uid']}/memo.md"
        )
        _write_json(item_dir / "index.json", candidate)
        summary = _candidate_summary(candidate)
        _write_markdown(item_dir / "summary.md", summary)
        _write_markdown(item_dir / "memo.md", summary)

    report = _review_report(
        payload=payload,
        anchors=anchors,
        candidates=candidates,
        primary_ids=primary_ids,
        deferred_ids=deferred_ids,
    )
    payload["report_path"] = f"{run_id}/report.md"
    _write_json(run_dir / "index.json", payload)
    _write_markdown(run_dir / "summary.md", _package_dossier(payload))
    _write_markdown(run_dir / "dossier.md", _package_dossier(payload))
    _write_markdown(run_dir / "report.md", report)
    _update_root_index(
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        package_type="first_pass_review",
        readiness=str(payload["readiness"]),
        count=len(candidates),
    )
    return run_dir / "index.json"
