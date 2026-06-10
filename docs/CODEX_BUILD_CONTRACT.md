# Codex Build Contract

Status: v0.4.0 CODEX_TASK_LOCK.

Codex must treat `docs/codex/CODEX_TASK_LOCK_V0_4_0.md` and `registries/codex_task_registry.json` as the controlling implementation plan. The master architecture and master specs define what Odin is. The task lock defines the implementation sequence and PR boundaries.

## Required contract order

```text
Architecture canon
→ Master specs
→ Subsystem specs
→ Codex task lock
→ PR task file
→ schema/registry
→ implementation
→ tests
```

## Build rules

- Contracts before runtime.
- Schemas before validators.
- Validators before model calls.
- Candidate artifacts before app rendering.
- Semantic event envelope before bus behavior.
- Mock provider before real providers.
- Local-only before remote.
- 3B + 7B/8B hybrid remains default sweet spot.

## Required commands

```bash
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider
```

## No-claim rule

A task may report what it changed inside the repository. It may not claim external host behavior, audit status, deployment status, or real model behavior without concrete receipts in the repo.
