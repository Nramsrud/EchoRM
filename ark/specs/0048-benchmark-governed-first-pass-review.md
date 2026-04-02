# 0048 Benchmark-Governed First-Pass Review

## Summary

Materialize a repository-local first-pass review package that uses tracked benchmark, discovery, and audit artifacts to define anchor calibrators, candidate review waves, and bounded dispositions for the current hold-out pool.

## Scope

- Record the benchmark anchors and validation packages that govern the first review wave, starting with `NGC 5548`, `NGC 3783`, and the tracked silver, continuum, efficacy, and audit summaries.
- Build deterministic candidate-review records from tracked discovery artifacts with wave assignment, disposition, rationale, benchmark links, and required next action.
- Emit a concise report that states the review strategy, current findings, and the claims boundary explicitly.
- Preserve evidence levels, limitations, and the requirement for real-data reruns before broader scientific interpretation.

## Non-Goals

- New discovery scoring or threshold tuning.
- External-release or publication claims.
- Replacing manual scientific judgment with automatic promotion.

## Global Constraints

- The package must derive from tracked benchmark, discovery, and audit artifacts rather than untracked notes.
- Hold-out candidates may not be retuned or promoted beyond their recorded evidence levels.
- Every disposition must state whether a real-data rerun is required before broader scientific interpretation.
- The package must remain explicit that current discovery evidence is repository-local and fixture-bounded.
- Wave assignment must be derived only from tracked `transition_detected`, `lag_state_change`, `line_response_ratio`, `rank_score`, `benchmark_links`, and `review_priority` fields.
- The primary review wave is limited to transition-led candidates with `transition_detected=true`, `lag_state_change>=1.2`, `line_response_ratio<=0.55`, and `rank_score>=0.76`.

## Acceptance Criteria

- A tracked command materializes a first-pass review package with anchor records, review waves, candidate dispositions, and a report.
- Every candidate record preserves score components, benchmark links, evidence level, limitations, rationale, and next action.
- The report states the first review wave, the deferred wave, and the current claims boundary for the hold-out pool.
- The report and candidate records keep every candidate under a real-data-rerun requirement before broader scientific interpretation.
- Tests verify package completeness, deterministic wave assignment, traceability, and claims-boundary language.

## Dependencies

- `0026`
- `0027`
- `0028`
- `0029`
- `0043`
- `0045`
