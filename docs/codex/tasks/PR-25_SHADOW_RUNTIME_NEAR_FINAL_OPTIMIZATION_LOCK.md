# PR-25 — Shadow Runtime Near-Final Optimization Lock

## Objective

Turn the v0.5.1 full shadow coverage into a near-final, mechanically convertible Shadow Runtime that behaves like the finished Odin Agent Shell architecture without claiming runtime execution.

## Primary Files

- `odin/shadow_runtime/e2e_orchestrator_shadow.py`
- `odin/shadow_runtime/policy_engine_shadow.py`
- `odin/shadow_runtime/resource_scheduler_shadow.py`
- `odin/shadow_runtime/state_machine_shadow.py`
- `odin/shadow_runtime/failure_recovery_shadow.py`
- `odin/shadow_runtime/provider_adapter_shadow.py`
- `odin/shadow_runtime/registry_consistency_shadow.py`
- `docs/SHADOW_RUNTIME_NEAR_FINAL_LOCK_V7_1.md`
- `docs/SHADOW_RUNTIME_E2E_ORCHESTRATOR_V7_1.md`
- `docs/SHADOW_RUNTIME_POLICY_ENGINE_V7_1.md`
- `docs/SHADOW_RUNTIME_STATE_FAILURE_MATRIX_V7_1.md`
- `docs/SHADOW_RUNTIME_RESOURCE_PROVIDER_PLAN_V7_1.md`
- `docs/SHADOW_RUNTIME_CODEX_CONVERSION_PLAYBOOK_V7_1.md`
- `docs/SHADOW_RUNTIME_REAL_MODULE_MAP_V7_1.md`
- `tests/test_shadow_runtime_near_final.py`

## Required Behavior

- Provide a near-final shadow entrypoint that assembles the full Odin pipeline into one pure result.
- Block non-candidate output before model routing.
- Expose resource posture and route ceiling without named hardware profiles.
- Expose canonical success/failure state machine.
- Expose provider adapter plan without calling providers.
- Expose failure recovery plan for blocked requests.
- Preserve candidate-only, app-owned apply, local-only bus and no-runtime-claim boundaries.

## Forbidden Scope

- No live model calls.
- No sockets.
- No app mutation.
- No file writes during shadow execution.
- No external sends.
- No runtime verification claims.
- No weakening of PR-00..PR-24 boundaries.

## Definition of Done

- `run_near_final_shadow_runtime` returns a full shadow result.
- Valid fixture covers major subsystem outputs.
- Invalid fixture is blocked before route execution.
- Shadow registry includes near-final contracts.
- Internal task registry includes PR-25.
- Real PR bundle registry includes REAL-PR-11.
- `python -m odin.cli validate-all` passes.
- `python -m pytest -q -p no:cacheprovider` passes.

## Codex PR Summary Template

```text
Implemented PR-25 Shadow Runtime Near-Final Optimization Lock.
Added near-final shadow orchestrator, policy engine, resource scheduler, state machine, failure recovery, provider adapter and registry consistency report.
Preserved candidate-only, app-owned-apply, local-only semantic bus and no-runtime-claim boundaries.
```
