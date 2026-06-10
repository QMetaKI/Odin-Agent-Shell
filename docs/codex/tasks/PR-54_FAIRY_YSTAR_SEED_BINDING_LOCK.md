# PR-54 — Fairy / Y* seed binding lock

## Objective

Implement the Fairy / Y* seed binding lock as part of the Odin v7.1 Bug6/Q7/Y-Core/Operational Seed Core hardening. This task extends the existing architecture without changing the app authority boundary, candidate-only posture, local-first policy, or 3B + 7B/8B sweet spot.

## Internal Context

This task belongs to REAL-PR-16 — Bug6 / Q7 / Y-Core / Operational Seed Core Lock. It follows the QIRC Gold Spine and must preserve all v7.1 contracts. It is a center-hardening task, not a feature-sprawl task.

## Primary Files

- docs/FAIRY_YSTAR_SEED_BINDING_V7_1.md
- odin/shadow_runtime/fairy_ystar_seed_binding_shadow.py

## Required Behavior

- Preserve app-owned state, apply, and external sends.
- Preserve Odin candidate-only output.
- Preserve local-first and smallest-sufficient-worker routing.
- Add typed packet, registry, shadow module, or documentation anchors for this task.
- Ensure Bug6, Q7, or seed posture is visible in Why Trace and Candidate DNA where relevant.
- Add or update fixtures and tests where code-near behavior is introduced.

## Forbidden Scope

- No real model calls.
- No network QIRC expansion.
- No public IRC.
- No runtime proof claims.
- No prose-only Fairy execution.
- No app mutation.
- No external send.
- No hidden apply.

## Definition of Done

- `python -m odin.cli validate-all` returns OK.
- `python -m pytest -q -p no:cacheprovider` remains green.
- The task updates registries when new IDs are introduced.
- The task updates SYSTEM_MAP and FILE_MANIFEST when files change.
- The task is covered by REAL-PR-16.
- All new behavior is candidate-only and boundary-preserving.

## Codex PR Summary Template

```text
PR-54: Fairy / Y* seed binding lock
- Added/updated:
- Tests:
- Boundaries preserved:
- Known non-claims:
```


## Additional Implementation Notes

This task must be implemented as a bounded build unit. Codex should first read the relevant architecture document, then the schema, then the registry, then the shadow module, then the fixture, then the test. The task must not introduce executable authority beyond its declared scope. The output of the task is a stronger contract surface, not a product claim.

### Traceability Requirements

Every implementation change must be traceable through:

```text
spec document → schema or registry → shadow module → fixture → test → PR task → REAL-PR bundle
```

If a new artifact kind is introduced, Codex must update `SYSTEM_MAP.json`, the relevant registry, the validation CLI if necessary, and `FILE_MANIFEST.json`. If the task touches route behavior, it must also preserve `candidate_only`, `app_authority_preserve`, `local_first`, and `smallest_sufficient_worker`.

### Safety Requirements

The implementation must not create a shortcut around binding validation, Bug6 invariant checks, Q7 stability checks, seed budget gates, QIRC admissibility, or Odin Final Gate. Any failure should return a hold, split, ask-context, block, or candidate error path. It must not silently escalate to a larger model or remote route.

### Test Requirements

Tests should include one positive path and one negative path whenever the task adds behavior. Positive tests prove the contract can be produced. Negative tests prove the boundary blocks invalid state, hidden apply, unsupported authority, missing seeds, missing trace, or unbounded route expansion.
