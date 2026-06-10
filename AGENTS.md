# AGENTS.md — Codex / Agent Operating Contract

## Role

You are implementing **Odin Agent Shell v7.1** from a canon-locked architecture/spec repository.

## Mandatory reading order

1. `START_HERE.md`
2. `CANON_ENTRY.md`
3. `SYSTEM_MAP.json`
4. `docs/MASTER_ARCHITECTURE_V7_1.md`
5. `docs/MASTER_SPECS_V7_1.md`
6. relevant subsystem doc under `docs/`
7. relevant schema under `schemas/v7_1/`
8. relevant registry under `registries/`
9. `docs/codex/CODEX_TASK_LOCK_V0_4_0.md`
10. exact PR task file under `docs/codex/tasks/`

## Non-negotiable laws

- Do not put LLM runtime logic in app templates.
- Do not make Odin mutate app state.
- Do not make Odin directly apply changes or send externally.
- Do not bypass `ODIN_BINDING` or Caller Manifest checks.
- Do not bypass output contracts.
- Do not send raw app state to models when a Context Capsule is required.
- Do not treat model output as truth.
- Do not use a bigger model when deterministic, 3B micro, 7B/8B, or hybrid route is sufficient.
- Do not expose Internal Semantic Bus to WAN/LAN/public IRC by default.
- Do not add positive claims of runtime, security, deployment or test verification without receipts.

## Required workflow for each change

1. Identify target subsystem.
2. Read subsystem doc.
3. Read schema and registry.
4. Write a small patch.
5. Add or update tests.
6. Run:

```bash
python -m odin.cli validate-all
pytest -q
```

7. Summarize what changed, what is still scaffold, and what is not claimed.

## Preferred implementation sequence

Follow `docs/codex/PHASE_*.md`. Do not implement Windows UI before the Universal Work Kernel, validation, semantic bus envelope, and core packet structures are stable.

## Claim boundary

Allowed:

- architecture implemented in part
- schema added
- validator added
- test added
- candidate produced
- mock provider path tested

Forbidden without concrete receipts:

- runtime is verified
- host is validated
- security is verified
- production ready
- deployment verified
- patch applied externally
- tests passed outside local command output
- model inference verified without local run receipt


## v0.4.0 Codex Task Lock

Before implementing any feature, identify the matching PR package in `registries/codex_task_registry.json` and read its task document under `docs/codex/tasks/`.

Do not merge scope across PR packages unless a canon document explicitly requires the shared update. Prefer small, contract-bound patches with tests.

## v0.4.1 Real PR Bundle Overlay

The PR-00 through PR-21 documents remain the internal implementation ladder. For actual future Codex pull requests, use the bundle overlay:

- `docs/codex/CODEX_REAL_PR_BUNDLE_PLAN_V0_4_1.md`
- `docs/codex/REAL_PR_BUNDLE_INDEX_V0_4_1.md`
- `registries/codex_pr_bundle_registry.json`
- `docs/codex/bundles/`

Rule: create real PRs by REAL-PR bundle; complete the mapped internal PR tasks inside each bundle.


## v0.5.0 Shadow Runtime Rule

Agents must update the Shadow Runtime docs, `odin/shadow_runtime/`, PR-23/REAL-PR-09 references, registries and tests whenever they change architecture-to-code mapping. Shadow modules remain non-authoritative and candidate-only.


## v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE

This repo prep now includes full major-subsystem Shadow Runtime coverage. Future changes must update specs, internal PR ladder, REAL-PR bundles, registries, tests, System Map and FILE_MANIFEST.
