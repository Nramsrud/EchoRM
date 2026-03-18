# 0002 Public Repository Boundary and Documentation Standard Plan

## Goal

Make the public repository boundary explicit, testable, and durable across all committed documentation.

## Implementation Approach

State the publication rules directly in committed guidance, keep the detailed editorial checklist in the local-only layer, and add a repository check that detects references to private artifacts or prohibited wording in public documentation.

## Steps

1. Normalize the public guidance in `README.md`, `AGENTS.md`, `ark/projectlist.md`, and the numbered specs so the publication rules are stated directly and consistently.
2. Keep the detailed editorial checklist in the local-only layer and ensure that local prompts, not public docs, point to it.
3. Add a documentation-boundary check that scans committed documentation for references to private artifacts, unpublished procedures, or non-public workflow language.
4. Add tests or fixtures that prove the boundary check catches representative failure cases without flagging legitimate committed file references.

## Expected File Changes

### New Files

- `tests/test_public_artifact_rules.py` - repository-level checks for prohibited references in committed documentation

### Modified Files

- `README.md` - public repository boundary and documentation rules
- `AGENTS.md` - public working rules stated without private-path dependencies
- `ark/projectlist.md` - project tracking language aligned with the public boundary
- `ark/specs/*.md` - consistent global constraints language where needed

## Validation

- `python3 -m pytest tests/test_public_artifact_rules.py`
- `rg -n "private tooling|local automation artifacts|internal roles|unpublished" README.md AGENTS.md ark`

## Exit Criteria

- The publication boundary is stated consistently in committed guidance.
- Public files do not rely on local-only paths for their meaning.
- Automated checks detect prohibited references in committed documentation.

## Risks

| Risk | Mitigation |
|------|------------|
| Boundary checks become overly broad and block legitimate references | Test representative allowed and disallowed examples before enforcing the check |
| Public guidance drifts from the local editorial checklist | Keep the public rules concise and principle-based, and confine implementation detail to the local-only file |

## Dependencies

- `0001`
