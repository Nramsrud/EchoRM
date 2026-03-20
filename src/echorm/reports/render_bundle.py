"""Finalized object bundle builders."""

from __future__ import annotations


def build_render_bundle(
    *,
    object_uid: str,
    manifests: tuple[dict[str, object], ...],
) -> dict[str, object]:
    """Assemble a standardized render bundle for one object."""
    stems = [str(manifest["audio_path"]) for manifest in manifests]
    return {
        "object_uid": object_uid,
        "audio_stems": stems,
        "science_audio_path": stems[0] if stems else "",
        "presentation_audio_path": stems[-1] if stems else "",
        "visualization_path": f"reports/{object_uid}/timeline.svg",
        "sync_review_path": f"reports/{object_uid}/synchronized_review.html",
        "legend": {
            "mapping_families": [
                str(manifest["mapping_family"]) for manifest in manifests
            ],
            "uncertainty_modes": [
                str(manifest["uncertainty_mode"]) for manifest in manifests
            ],
        },
        "provenance_records": [
            {
                "sonification_id": str(manifest["sonification_id"]),
                "mapping_config_hash": str(manifest["mapping_config_hash"]),
                "provenance_hash": str(manifest["provenance_hash"]),
            }
            for manifest in manifests
        ],
    }
