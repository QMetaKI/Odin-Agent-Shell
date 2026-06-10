# REAL-PR-11 — Shadow Runtime Near-Final Optimization Bridge

## Objective

Make the Shadow Runtime almost mechanically convertible into the real Odin implementation by adding a near-final pure orchestrator, policy engine, resource scheduler, state machine, failure matrix, provider adapter plan and Codex conversion playbook.

## Internal Tasks Covered

- PR-25 — Shadow Runtime Near-Final Optimization Lock

## Primary Files

- `odin/shadow_runtime/e2e_orchestrator_shadow.py`
- `odin/shadow_runtime/policy_engine_shadow.py`
- `odin/shadow_runtime/resource_scheduler_shadow.py`
- `odin/shadow_runtime/state_machine_shadow.py`
- `odin/shadow_runtime/failure_recovery_shadow.py`
- `odin/shadow_runtime/provider_adapter_shadow.py`
- `odin/shadow_runtime/registry_consistency_shadow.py`
- `docs/SHADOW_RUNTIME_NEAR_FINAL_LOCK_V7_1.md`
- `docs/SHADOW_RUNTIME_CODEX_CONVERSION_PLAYBOOK_V7_1.md`
- `registries/shadow_runtime_contract_registry.json`
- `tests/test_shadow_runtime_near_final.py`

## Required Behavior

- Valid near-final shadow flow produces a complete response projection.
- Invalid policy flow is blocked before route execution.
- Provider plan remains side-effect free.
- State machine exposes canonical terminal success and failure states.
- Registry consistency report stays green.
- All new scope is reflected in PR ladder, bundle registry, System Map and file manifest.

## Forbidden Scope

- No live providers.
- No live API server.
- No Windows service start.
- No app state mutation.
- No external send.
- No runtime-proof claim.

## Definition of Done

- PR-25 task doc exists and is registered.
- REAL-PR-11 bundle doc exists and is registered.
- Shadow runtime contract registry contains near-final contracts.
- Validation CLI passes.
- Test suite passes.
- FILE_MANIFEST updated.

## Codex PR Summary Template

```text
Implemented REAL-PR-11 Shadow Runtime Near-Final Optimization Bridge.
Added near-final orchestrator and conversion docs while preserving all Odin authority and candidate-only boundaries.
```

## Senior Reviewer Notes

This bundle deliberately does not build the real daemon, real API, real provider adapters or real Windows service. Its value is mechanical alignment. After this bundle, a later implementation PR should be able to ask: "Which shadow object corresponds to this real module?" and receive an exact answer.

The near-final bridge is especially important because Odin has several anti-drift invariants that normal coding agents may accidentally weaken:

- treating bus events as if they authorize actions;
- treating model output as verified truth;
- allowing app templates to contain prompt orchestration;
- skipping Candidate DNA because it seems like metadata;
- making route decisions from hardware names rather than resource profiles;
- allowing remote fallback too early;
- turning support bundles into upload/export mechanisms rather than local redacted bundles.

REAL-PR-11 must make these mistakes mechanically harder. It does this by adding a pure orchestrator whose output shape is broad enough to show the future system but bounded enough that every field is candidate-only.

## Review Checklist

- Does the near-final result contain policy, route, state, failure, provider, candidate, trace and support-bundle sections?
- Does invalid work stop before model routing?
- Does every provider plan state that no live provider was called?
- Does every app-facing candidate require app apply gate?
- Does the bundle registry cover PR-25?
- Does the shadow contract registry include the new near-final contracts?
- Do tests verify both success and policy-block paths?

## Merge Condition

Merge only when the validation CLI and test suite pass with cache disabled and when no new runtime-proof wording is introduced. The bundle is a conversion bridge, not a runtime release.
