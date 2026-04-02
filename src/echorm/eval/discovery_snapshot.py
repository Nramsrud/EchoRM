"""Canonical discovery snapshot promotion helpers."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections.abc import Mapping
from pathlib import Path

from .broad_validation import (
    JSONDict,
    _dict_list,
    _mapping_value,
    _package_dossier,
    _package_header,
    _string_list,
    _update_root_index,
    _write_markdown,
)
from .readiness import ToolStatus, VerificationCheck, _write_json


def _load_required_run(artifact_root: Path, run_id: str) -> JSONDict:
    path = artifact_root / run_id / "index.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{run_id} payload must be a mapping")
    return payload


def _hash_payload(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]


def _repo_source_reference(repo_root: Path) -> str:
    try:
        completed = subprocess.run(
            ("git", "rev-parse", "HEAD"),
            check=True,
            capture_output=True,
            cwd=repo_root,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return f"unavailable:{repo_root}"
    return completed.stdout.strip() or f"unavailable:{repo_root}"


def _candidate_inventory(
    discovery_payload: Mapping[str, object],
) -> list[JSONDict]:
    inventory: list[JSONDict] = []
    for candidate in _dict_list(discovery_payload, "candidates"):
        evidence_bundle = _mapping_value(candidate, "evidence_bundle")
        inventory.append(
            {
                "object_uid": str(candidate.get("object_uid", "")),
                "canonical_name": str(candidate.get("canonical_name", "")),
                "anomaly_category": str(candidate.get("anomaly_category", "")),
                "rank_score": candidate.get("rank_score", 0.0),
                "review_priority": str(candidate.get("review_priority", "")),
                "evidence_level": str(evidence_bundle.get("evidence_level", "")),
                "benchmark_links": _string_list(evidence_bundle, "benchmark_links"),
            }
        )
    return inventory


def build_promoted_snapshot_reference(
    discovery_payload: Mapping[str, object],
) -> JSONDict:
    """Build the canonical candidate inventory and digests for a discovery run."""
    inventory = _candidate_inventory(discovery_payload)
    order = [str(item["object_uid"]) for item in inventory]
    return {
        "candidate_count": len(inventory),
        "candidate_inventory": inventory,
        "candidate_inventory_digest": _hash_payload(inventory),
        "candidate_order": order,
        "candidate_order_digest": _hash_payload(order),
    }


def _corpus_reference(corpus_payload: Mapping[str, object], run_id: str) -> JSONDict:
    discovery_manifest = _mapping_value(corpus_payload, "discovery_manifest")
    return {
        "run_id": run_id,
        "path": f"{run_id}/index.json",
        "corpus_id": str(discovery_manifest.get("corpus_id", "")),
        "manifest_hash": str(discovery_manifest.get("manifest_hash", "")),
        "holdout_policy": str(discovery_manifest.get("holdout_policy", "")),
        "release_ids": _string_list(discovery_manifest, "release_ids"),
        "object_uids": _string_list(discovery_manifest, "object_uids"),
    }


def _package_references(
    *,
    discovery_run_id: str,
    corpus_run_id: str,
) -> list[JSONDict]:
    return [
        {
            "run_id": discovery_run_id,
            "path": f"{discovery_run_id}/index.json",
            "package_type": "discovery_analysis",
        },
        {
            "run_id": corpus_run_id,
            "path": f"{corpus_run_id}/index.json",
            "package_type": "corpus_scaleout",
        },
    ]


def _snapshot_summary(reference: Mapping[str, object]) -> str:
    return (
        f"# Discovery Snapshot {reference['promoted_snapshot_id']}\n\n"
        f"- Source run: {reference['source_run_id']}\n"
        f"- Source path: {reference['source_path']}\n"
        f"- Source reference: {reference['source_reference']}\n"
        f"- Candidate count: {reference['candidate_count']}\n"
        f"- Candidate inventory digest: {reference['candidate_inventory_digest']}\n"
        f"- Candidate order digest: {reference['candidate_order_digest']}\n"
    )


def _enforce_single_snapshot_entry(artifact_root: Path, run_id: str) -> None:
    root_index_path = artifact_root / "index.json"
    if not root_index_path.exists():
        return
    root_payload = json.loads(root_index_path.read_text(encoding="utf-8"))
    runs_object = root_payload.get("runs", [])
    runs = runs_object if isinstance(runs_object, list) else []
    normalized_runs = [
        item
        for item in runs
        if isinstance(item, dict)
        and not (
            str(item.get("package_type", "")) == "discovery_snapshot"
            and str(item.get("run_id", "")) != run_id
        )
    ]
    _write_json(root_index_path, {"runs": normalized_runs})


def _load_canonical_snapshot_run_id(artifact_root: Path) -> str:
    root_index_path = artifact_root / "index.json"
    if not root_index_path.exists():
        raise ValueError("artifact root is missing index.json for canonical lookup")
    root_payload = json.loads(root_index_path.read_text(encoding="utf-8"))
    runs_object = root_payload.get("runs", [])
    runs = runs_object if isinstance(runs_object, list) else []
    snapshot_runs = [
        str(item.get("run_id", ""))
        for item in runs
        if isinstance(item, dict)
        and str(item.get("package_type", "")) == "discovery_snapshot"
    ]
    if len(snapshot_runs) != 1:
        raise ValueError(
            "artifact root must contain exactly one canonical discovery_snapshot entry"
        )
    return snapshot_runs[0]


def materialize_discovery_snapshot_package(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_id: str = "discovery_snapshot",
    profile: str = "discovery_snapshot",
    source_run_id: str = "discovery_analysis",
    corpus_run_id: str = "corpus_scaleout",
    promoted_snapshot_id: str | None = None,
    verification: tuple[VerificationCheck, ...] = (),
    tools: tuple[ToolStatus, ...] = (),
) -> Path:
    """Promote one canonical discovery snapshot from a tracked discovery run."""
    discovery_payload = _load_required_run(artifact_root, source_run_id)
    corpus_payload = _load_required_run(artifact_root, corpus_run_id)
    snapshot_reference = build_promoted_snapshot_reference(discovery_payload)
    snapshot_id = promoted_snapshot_id or f"{source_run_id}-{run_id}"
    run_dir = artifact_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    source_reference = _repo_source_reference(repo_root)
    corpus_reference = _corpus_reference(corpus_payload, corpus_run_id)
    payload = _package_header(
        run_id=run_id,
        profile=profile,
        package_type="discovery_snapshot",
        benchmark_scope=(
            "Canonical promotion record for one repository-local discovery-analysis "
            "snapshot."
        ),
        readiness="ready" if snapshot_reference["candidate_count"] else "degraded",
        verification=verification,
        tools=tools,
        summary={
            "candidate_count": snapshot_reference["candidate_count"],
            "package_reference_count": 2,
        },
        demonstrated=(
            "One repository-local discovery-analysis snapshot is promoted through an "
            "explicit record with digests and source references.",
        ),
        not_demonstrated=(
            "Promotion does not convert discovery outputs into broader scientific "
            "claims or publication readiness.",
        ),
        limitations=(
            "Promotion remains bounded by the repository-local hold-out snapshot and "
            "its recorded evidence levels.",
        ),
        warnings=(
            "manual_review_and_real_data_rerun_still_required",
        ),
        artifact_root=artifact_root,
    )
    payload["promoted_snapshot_id"] = snapshot_id
    payload["source_run_id"] = source_run_id
    payload["source_path"] = f"{source_run_id}/index.json"
    payload["source_reference"] = source_reference
    payload["corpus_reference"] = corpus_reference
    payload["package_references"] = _package_references(
        discovery_run_id=source_run_id,
        corpus_run_id=corpus_run_id,
    )
    payload["candidate_count"] = snapshot_reference["candidate_count"]
    payload["candidate_inventory"] = snapshot_reference["candidate_inventory"]
    payload["candidate_inventory_digest"] = snapshot_reference[
        "candidate_inventory_digest"
    ]
    payload["candidate_order"] = snapshot_reference["candidate_order"]
    payload["candidate_order_digest"] = snapshot_reference["candidate_order_digest"]
    payload["limitations"] = _string_list(payload, "limitations") + _string_list(
        discovery_payload, "limitations"
    )
    _write_json(run_dir / "index.json", payload)
    _write_markdown(run_dir / "summary.md", _package_dossier(payload))
    _write_markdown(run_dir / "dossier.md", _package_dossier(payload))
    _write_markdown(run_dir / "snapshot.md", _snapshot_summary(payload))
    _update_root_index(
        artifact_root=artifact_root,
        run_id=run_id,
        profile=profile,
        package_type="discovery_snapshot",
        readiness=str(payload["readiness"]),
        count=int(str(snapshot_reference["candidate_count"])),
    )
    _enforce_single_snapshot_entry(artifact_root, run_id)
    return run_dir / "index.json"


def validate_promoted_discovery_snapshot(
    *,
    artifact_root: Path,
    snapshot_run_id: str = "discovery_snapshot",
) -> JSONDict:
    """Validate that the promoted discovery snapshot still matches its source run."""
    canonical_run_id = _load_canonical_snapshot_run_id(artifact_root)
    if snapshot_run_id != canonical_run_id:
        raise ValueError(
            "requested promoted snapshot is not the canonical discovery snapshot: "
            f"{snapshot_run_id}"
        )
    snapshot_payload = _load_required_run(artifact_root, snapshot_run_id)
    source_run_id = str(snapshot_payload.get("source_run_id", ""))
    if not source_run_id:
        raise ValueError("promoted snapshot is missing source_run_id")
    discovery_payload = _load_required_run(artifact_root, source_run_id)
    current_reference = build_promoted_snapshot_reference(discovery_payload)
    promoted_corpus_reference = _mapping_value(snapshot_payload, "corpus_reference")
    corpus_run_id = str(promoted_corpus_reference.get("run_id", ""))
    if not corpus_run_id:
        raise ValueError("promoted snapshot is missing corpus_reference.run_id")
    current_corpus_reference = _corpus_reference(
        _load_required_run(artifact_root, corpus_run_id),
        corpus_run_id,
    )
    divergence_reasons: list[str] = []
    if int(str(snapshot_payload.get("candidate_count", 0))) != int(
        str(current_reference["candidate_count"])
    ):
        divergence_reasons.append("candidate_count")
    if _string_list(snapshot_payload, "candidate_order") != _string_list(
        current_reference, "candidate_order"
    ):
        divergence_reasons.append("candidate_order")
    if str(snapshot_payload.get("candidate_inventory_digest", "")) != str(
        current_reference["candidate_inventory_digest"]
    ):
        divergence_reasons.append("candidate_inventory")
    if str(snapshot_payload.get("candidate_order_digest", "")) != str(
        current_reference["candidate_order_digest"]
    ):
        divergence_reasons.append("candidate_order_digest")
    if promoted_corpus_reference != current_corpus_reference:
        divergence_reasons.append("corpus_reference")
    if divergence_reasons:
        joined = ", ".join(divergence_reasons)
        raise ValueError(
            "promoted discovery snapshot diverged from its source run: " f"{joined}"
        )
    return snapshot_payload
