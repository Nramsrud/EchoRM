# Repository Working Rules

## Authority Documents
- `agn_quasar_reverberation_sonification_project_plan.md`
- `agn_quasar_reverberation_sonification_agent_spec.yaml`
- the active specification and implementation plan under `ark/`

## Public Artifact Rules

- All committed documentation must remain formal, concise, precise, and limited to essential content.
- Committed text may reference only committed repository files or widely understood public concepts.
- Private tooling, local automation artifacts, internal roles, and unpublished procedures are excluded from committed text.
- Remove filler, repetition, and placeholder text.

## Technical Baseline

- Default implementation stack is Python 3.12.
- Quality commands are `python3 -m pytest`, `python3 -m ruff check .`, and `python3 -m mypy src tests`.
- The local acceptance gate before every commit and push is `bash scripts/ci/run_local_scientific_validation.sh`.
- Install the committed local git hooks with `bash scripts/ci/install_git_hooks.sh`.
- Large raw data, rendered audio, and other generated artifacts belong in dedicated artifact directories rather than normal versioned content.

## Scientific Rigor Requirements

- Treat benchmark scope, evidence level, and claims boundaries as explicit implementation requirements.
- Distinguish operational readiness, fixture-backed real-data checks, synthetic benchmarks, and broader scientific validation in code, tests, specifications, plans, and summaries.
- Treat repository-local readiness, release, and root-closeout artifacts as bounded by their recorded evidence levels, limitations, and non-demonstrated capabilities.
- Preserve provenance, benchmark labels, assumptions, limitations, and non-demonstrated capabilities in committed artifacts.
- Do not describe the system as scientifically benchmark-ready beyond the coverage demonstrated by tracked benchmark artifacts.
