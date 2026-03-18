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
- Large raw data, rendered audio, and other generated artifacts belong in dedicated artifact directories rather than normal versioned content.
