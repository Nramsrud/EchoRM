"""Object identity and alias models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SurveyIdentifier:
    """One survey-local identifier."""

    survey: str
    local_id: str


@dataclass(frozen=True, slots=True)
class CanonicalObjectIdentity:
    """Canonical object identity across surveys."""

    object_uid: str
    canonical_name: str
    aliases: tuple[str, ...]
    survey_ids: tuple[SurveyIdentifier, ...]
    reference_epoch_mjd: float

    @property
    def alias_group(self) -> str:
        return ",".join(self.aliases)


def resolve_identity(
    *,
    canonical_name: str,
    aliases: tuple[str, ...],
    survey_ids: tuple[SurveyIdentifier, ...],
    reference_epoch_mjd: float,
) -> CanonicalObjectIdentity:
    """Resolve a canonical identity from survey-local identifiers."""
    object_uid = canonical_name.lower().replace(" ", "").replace("-", "")
    return CanonicalObjectIdentity(
        object_uid=object_uid,
        canonical_name=canonical_name,
        aliases=aliases,
        survey_ids=survey_ids,
        reference_epoch_mjd=reference_epoch_mjd,
    )
