# 0002 Public Repository Boundary and Documentation Standard

## Summary

Define the boundary between published repository content and local private artifacts, and establish the required editorial standard for all committed documentation.

## Scope

- Define the repository-wide documentation rules for committed artifacts.
- Prohibit references to private tooling, local automation artifacts, internal roles, and unpublished operational procedures in committed files.
- Require committed text to cite only committed repository files or widely understood public concepts.
- Apply the standard to repository-level guides and future specifications.

## Non-Goals

- Implement scientific data pipelines or inference backends.
- Define local operator workflows or private automation behavior.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Published text must remain formal, concise, precise, and evidentiary.

## Acceptance Criteria

- The repository states the publication boundary and the writing standard in committed guidance.
- `README.md`, `AGENTS.md`, `ark/projectlist.md`, and numbered specifications are consistent with that standard.
- No committed documentation instructs readers to use private tooling, internal roles, or local-only artifacts.

## Dependencies

- `0001`
