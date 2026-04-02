# 0046 Adversarial Root Authority Gap-Closure Plan

## Goal

Maintain an adversarial review checklist for repository-local status language, package summaries, and release claims.

## Governing Rule

When a status summary exceeds the scope of the tracked artifacts, the summary is wrong and must be corrected.

## Scope

This plan governs documentation and review updates over the repository-local root-closeout surface on `main`.

## Workstreams

### W1. Status Review

- Audit release notes, package notes, and top-level repository guidance for stale branch-only or pre-integration wording.
- Remove summaries that imply full-survey, literal, or external-release closure where the artifacts record narrower evidence.

### W2. Claims-Boundary Review

- Ensure documentation preserves evidence levels, limitations, hold-out rules, and non-demonstrated capabilities from generated packages.
- Require release and audit language to remain repository-local unless an explicit external review decision is recorded.

### W3. Regression Prevention

- Add targeted documentation tests that fail when stale phrases or claims-boundary regressions reappear.

## Sequencing

1. Review status documents first.
2. Tighten claims-boundary language next.
3. Add regression-prevention tests last.

## Verification

- `python3 -m pytest tests/test_public_artifact_rules.py tests/test_documentation_state.py`
- `python3 -m ruff check .`

## Exit Criteria

This plan is complete when repository-local documentation can be read without stale branch notes, silent scope expansion, or missing claims boundaries.
