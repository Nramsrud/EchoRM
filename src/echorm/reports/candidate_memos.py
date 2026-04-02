"""Follow-up report builders."""

from __future__ import annotations

from ..anomaly.candidates import CandidateRecord


def build_candidate_memo(candidate: CandidateRecord) -> str:
    """Build a concise follow-up memo for one candidate."""
    return (
        f"Object: {candidate.object_uid}\n"
        f"Canonical name: {candidate.canonical_name}\n"
        f"Category: {candidate.anomaly_category}\n"
        f"Rank score: {candidate.rank_score:.3f}\n"
        f"Review priority: {candidate.review_priority}\n"
        f"Method support count: {candidate.method_support_count}\n"
        f"Limitations: {candidate.limitations}\n"
        f"Evidence: {candidate.evidence_bundle}\n"
    )
