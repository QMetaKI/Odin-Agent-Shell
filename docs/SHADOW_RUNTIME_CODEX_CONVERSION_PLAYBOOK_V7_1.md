# Shadow Runtime Codex Conversion Playbook v7.1

## Rule

Codex must treat Shadow Runtime as the mechanical blueprint for real implementation. It may refine internals, but it may not change system authority boundaries.

## Conversion Pattern

For every shadow subsystem:

```text
shadow function
→ real module interface
→ schema or dataclass
→ validator
→ golden fixture
→ negative fixture
→ unit test
→ integration test
→ registry update
→ FILE_MANIFEST update
```

## Forbidden Shortcuts

- bypassing Universal Work validation
- using raw prompts instead of ModelWorkPackets
- letting app templates contain model routing
- letting Odin execute app actions
- skipping Candidate DNA
- treating bus events as authority
- enabling remote by default
- adding live provider code before mock provider parity

## Required PR Updates

Every new implementation PR must update:

- internal PR task doc
- real PR bundle doc
- task registry
- bundle registry
- traceability matrix if scope changes
- tests
- FILE_MANIFEST

## PR-25 Role

PR-25 locks the near-final Shadow Runtime. It is not a runtime release PR. It exists to make later PRs more mechanical and less interpretive.
