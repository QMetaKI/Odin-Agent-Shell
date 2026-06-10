# REAL-PR-06 — SDKs, App Templates and App-QIRC Digest Bridge

## Objective

Make apps easy to connect without embedding LLMs and add digest-only bridge preparation for future app-owned QIRC/event systems.

## Actual PR Role

This is a real Codex pull request bundle. The existing internal PR tasks remain the execution ladder inside this bundle.

## Internal Tasks Covered

- PR-13
- PR-16

## Depends On

- REAL-PR-05

## Primary Files

- `sdk/`
- `templates/`
- `odin/apps/app_qirc_bridge.py`
- `docs/APP_INTEGRATION_STANDARD.md`
- `tests/`

## Required Behavior

- TypeScript/Python SDKs can build/send Universal Work to local API
- templates contain Odin bridge only, not LLM runtime
- app-QIRC bridge accepts digest artifacts only
- bridge preserves app ownership of state and event system

## Forbidden Scope

- no full app event mirror
- no app mutation event publish
- no provider credentials in templates
- no bundled app-specific LLM logic

## Required Tests

```bash
python -m odin.cli validate-all
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

Additional test expectations:

- unit tests for every new module introduced in this bundle
- negative tests for every boundary or forbidden scope item touched
- registry parity checks when registries or schemas change
- docs coverage checks when canonical docs are edited

## Documentation Updates

This bundle may update subsystem docs only when implementation reveals an ambiguity. It may not weaken Master Architecture v7.1, Master Specs v7.1, Candidate-only boundaries, app-owned state boundaries, or semantic bus local-only posture.

## Definition of Done

- All mapped internal tasks are implemented or explicitly left as documented follow-up inside the same bundle scope.
- Public API and schema names remain stable unless a canonical doc update is included.
- Candidate Artifact and Response Packet rules are preserved.
- No app-owned authority is moved into Odin.
- No external network route is enabled by default.
- Tests and validation commands are green.
- PR description includes the summary template below.

## Codex PR Summary Template

```markdown
## Bundle
REAL-PR-06 — SDKs, App Templates and App-QIRC Digest Bridge

## Internal Tasks Covered
PR-13, PR-16

## What Changed
- ...

## Boundaries Preserved
- no LLM in app
- candidate-only output
- app owns state/apply/external sends
- semantic bus local-only
- model routing resource-based, not hardware-name based

## Tests
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

## Remaining Follow-ups
- ...
```

## Rollback Notes

Rollback must remove implementation files and tests introduced by this bundle while preserving previous canonical docs, registries, schemas and the internal PR ladder.

## Bundle Execution Checklist

Before implementation, Codex must read the mapped internal task documents in order and keep their file-level guidance as the active checklist. During implementation, Codex should prefer minimal coherent changes, preserve import stability, and add tests close to the changed module. After implementation, Codex must verify that every touched boundary still follows the master architecture: app owns state, Odin returns candidates, models are projection workers, semantic bus stays local, and routing remains resource/profile based rather than hardware-name based.

## Review Focus

Reviewers should check whether the bundle introduced hidden coupling across later bundles. If a later bundle is required for a feature to work, the current bundle should expose a bounded stub, typed contract, or explicit not-yet-wired status instead of pretending completion. Public docs may describe intended behavior, but runtime-facing docs must distinguish implemented behavior from planned behavior until receipts exist.

## Failure Handling

If this bundle fails validation, the repair order is: schemas and registries first, protocol/data contracts second, implementation code third, documentation parity fourth, tests last. Do not weaken tests to make the bundle pass. Do not reduce claim-boundary wording. Do not remove internal task coverage to avoid work.

