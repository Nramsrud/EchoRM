# EchoRM

EchoRM is a methods-focused research codebase for uncertainty-aware sonification of AGN and quasar reverberation mapping, with initial emphasis on benchmarkable AGN Watch and SDSS-RM workflows.

## Authority Documents

- `agn_quasar_reverberation_sonification_project_plan.md`
- `agn_quasar_reverberation_sonification_agent_spec.yaml`

These documents define the scientific scope and the operational constraints for committed artifacts.

## Program Structure

- `ark/projectlist.md` records the numbered work packages and release sequence.
- `ark/specs/` contains scoped specifications derived from the authority documents.
- `ark/plans/` contains implementation plans after a specification is approved.
- `docs/releases/` contains public release indexes and summaries.

## Technical Baseline

- Python 3.12
- `pyproject.toml` defines package metadata and the verification configuration.
- `src/` and `tests/` contain the executable code and the verification suite.

## Local Validation

- Install the committed git hooks with `bash scripts/ci/install_git_hooks.sh`.
- The local acceptance gate before every commit and push is `bash scripts/ci/run_local_scientific_validation.sh`.
- The local gate runs `python3 -m ruff check .`, `python3 -m mypy src tests`, `python3 -m pytest`, and `snakemake --snakefile workflows/Snakefile --dry-run`.

All published documentation in this repository must remain formal, concise, precise, and limited to essential content.
