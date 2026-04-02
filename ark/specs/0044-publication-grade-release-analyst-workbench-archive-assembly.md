# 0044 Publication-Grade Release, Analyst Workbench, and Archive Assembly

## Summary

Assemble the literal root-plan release outputs, analyst workbench views, publication artifacts, and provenance-complete benchmark and audio archives.

## Scope

- Build methods-paper and catalog-paper artifact bundles from tracked evidence.
- Build an open-source release bundle with code, configs, manifests, workflows, benchmark tables, and reproducibility checklist.
- Build benchmark and audio archives with provenance-complete manifests.
- Extend the analyst workbench to expose benchmark, optimization, discovery, and release evidence directly from structured artifacts.

## Non-Goals

- New method development.
- New discovery searches.

## Global Constraints

- Release artifacts must remain traceable to validated inputs and frozen provenance.
- Publication-facing outputs may not overstate scope beyond the tracked evidence.
- Root-closeout promotion may not use placeholder release summaries as substitute deliverables.

## Acceptance Criteria

- Methods-paper, catalog-paper, benchmark-archive, audio-archive, and open-source release bundles all exist as tracked outputs.
- The analyst workbench exposes benchmark, optimization, discovery, release, and conformance artifacts through one read-only surface.
- Release manifests record code references, configuration references, provenance records, and artifact hashes.
- Tests verify bundle completeness, workbench coverage, and provenance completeness.

## Dependencies

- `0020`
- `0036`
- `0037`
- `0041`
- `0042`
- `0043`
- `0038`
