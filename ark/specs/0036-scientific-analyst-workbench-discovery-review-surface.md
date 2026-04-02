# 0036 Scientific Analyst Workbench and Discovery Review Surface

## Summary

Extend the read-only review application into the analyst-facing workbench required for benchmark, discovery, and release-phase scientific review.

## Scope

- Add review routes for advanced-method, corpus-scaleout, optimization, discovery, and release packages.
- Add candidate, catalog, and release navigation over tracked artifact files.
- Expose claims boundaries, provenance completeness, hold-out status, and review priority directly in the interface.
- Preserve the read-only contract and ensure every displayed value originates from tracked artifact files.

## Non-Goals

- Interactive editing or annotation.
- Untracked local process state.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- The interface remains read-only and artifact-backed.
- Review views must preserve scope, evidence level, limitations, and non-demonstrated capability explicitly.

## Acceptance Criteria

- Analysts can navigate benchmark, discovery, and release artifacts through one tracked review surface.
- Candidate and release pages expose provenance, method support, warnings, and claims boundaries.
- New review routes are covered by tests and operate against generated artifacts.

## Dependencies

- `0033`
- `0035`
