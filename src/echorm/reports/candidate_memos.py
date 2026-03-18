"""Follow-up report builders."""

from __future__ import annotations

from ..anomaly.candidates import CandidateRecord


def build_candidate_memo(candidate: CandidateRecord) -> str:
    """Build a concise follow-up memo for one candidate."""
    return (
        f"Object: {candidate.object_uid}\n"
        f"Category: {candidate.anomaly_category}\n"
        f"Rank score: {candidate.rank_score:.3f}\n"
        f"Evidence: {candidate.evidence_bundle}\n"
    )
