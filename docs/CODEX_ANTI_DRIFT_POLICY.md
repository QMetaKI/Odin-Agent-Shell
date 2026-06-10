# Codex Anti-Drift Policy v7.1

## Purpose

Codex must implement Odin. Codex must not reinterpret Odin.

This policy prevents implementation drift away from Master Architecture v7.1, Master Specs v7.1 and the Deep Subsystem Spec Lock.

## Authority Order

```text
1. CLAIM_BOUNDARY.md
2. CANON_ENTRY.md
3. docs/MASTER_ARCHITECTURE_V7_1.md
4. docs/MASTER_SPECS_V7_1.md
5. Deep subsystem specs
6. Schemas
7. Registries
8. Internal PR tasks
9. Real PR bundles
10. Implementation code
```

If code conflicts with the canon, code is wrong until the canon is explicitly updated.

## Anti-Drift Requirements

Every meaningful change must answer:

```text
What architecture section does this implement?
What spec section does this implement?
What internal task does this satisfy?
What real PR bundle does this belong to?
What invariant could this weaken?
What test proves it did not weaken that invariant?
```

## Forbidden Codex Shortcuts

```text
Do not put LLM logic into app templates.
Do not let Odin mutate app state.
Do not let Semantic Bus become network feature by default.
Do not return applied outputs from Odin.
Do not skip Candidate DNA for candidate outputs.
Do not enable remote providers by default.
Do not replace Universal Work with raw prompt execution.
Do not treat bigger models as default architecture.
Do not loosen claim boundary to make demos look better.
```

## Required Drift Gates

```text
validate-all
pytest
schema validation
registry parity
claim boundary scan
codex task coverage
real bundle coverage
senior review coverage
file manifest refresh
```

## Handling Necessary Spec Changes

If implementation reveals a legitimate spec issue:

1. Update architecture/spec docs first.
2. Update schemas/registries.
3. Update internal task and real bundle docs.
4. Add/adjust tests.
5. Update manifest.
6. Then implement code.

No silent divergence is allowed.
