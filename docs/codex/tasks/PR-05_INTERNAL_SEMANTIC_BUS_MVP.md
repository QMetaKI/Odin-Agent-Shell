# PR-05 — Internal Semantic Bus MVP

**Task Lock:** v0.4.0 CODEX_TASK_LOCK  
**Architecture:** Odin Agent Shell v7.1  
**Depends on:** PR-02

## 1. Objective

Build the local-only semantic event bus, event envelope validation and replay skeleton.

This task must implement only its own bounded slice. It may update docs, schemas, registries, validators and tests required to make the slice coherent. It must not steal scope from later tasks.

## 2. Canonical Inputs

Read in order:

1. `AGENTS.md`
2. `CODEX_START_HERE.md`
3. `docs/codex/CODEX_TASK_LOCK_V0_4_0.md`
4. this task file
5. `docs/MASTER_ARCHITECTURE_V7_1.md`
6. `docs/MASTER_SPECS_V7_1.md`
7. relevant subsystem docs
8. relevant schemas and registries

## 3. Primary Files and Directories

- `odin/semantic_bus/`
- `registries/semantic_bus_channels.json`
- `tests/test_semantic_event.py`

## 4. Required Behavior

- preserve the v7.1 contract vocabulary
- keep Universal Work as the core task shape
- keep Candidate Artifact as the output shape
- preserve app-owned state/apply/external-send
- use typed reasons for failure paths
- update validation when the contract changes
- update tests in the same task

## 5. Forbidden Scope

```text
no app LLM runtime
no direct app mutation by Odin
no direct external send by Odin
no WAN/LAN/public IRC exposure by default
no model-output-as-truth promotion
no hardware-specific hardcoding in route decisions
no remote provider behavior unless the task explicitly allows it
```

## 6. Implementation Steps

1. Inspect current files listed in Primary Files.
2. Identify the smallest contract addition for this PR.
3. Update schemas first when payload shape changes.
4. Update registries second when canonical values change.
5. Implement validators or packet helpers third.
6. Add unit tests for valid path and at least one negative path.
7. Update docs only where behavior actually changed.
8. Run the global gate commands.
9. Regenerate `FILE_MANIFEST.json` before packaging.

## 7. Required Tests

Every implementation task should include at least:

```text
one valid object/path test
one invalid object/path test
one boundary preservation test when relevant
one registry/schema parity test when canonical values changed
```

## 8. Definition of Done

```text
Task objective implemented for this slice
Schemas/registries updated where needed
Tests added or updated
Validation CLI clean
Pytest exits 0
No boundary regression
No unsupported claim promotion
Docs updated if contract changed
```

## 9. Out of Scope

This task does not make Odin a final product. It does not claim host behavior, external verification, security audit, provider quality, or Windows packaging finality.

## 10. Codex PR Summary Template

```text
Subsystem: Internal Semantic Bus MVP
Files changed:
Behavior added:
Validation:
Gates preserved:
Known scaffold remaining:
Claims not made:
Next task:
```

## 11. Review Checklist

- Does this task still obey No-LLM-in-App?
- Does every action-impacting output remain candidate-only?
- Does any semantic bus addition remain local-only by default?
- Does model routing preserve smallest-sufficient-worker discipline?
- Does the task keep app authority separate from Odin authority?
- Are failures explicit and typed?
- Are tests tied to the contract instead of implementation accidents?

## 12. Handoff Notes

The next task should be able to proceed using only repo files, not chat context. If a later task needs a decision from this task, write that decision into docs or registries, not into a PR comment only.
