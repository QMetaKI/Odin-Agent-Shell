# REAL-PR-09 — Shadow Runtime Mechanical Build Bridge

## Objective

Add the code-near Shadow Runtime layer that converts Odin v7.1 architecture/specs into mechanical Codex build instructions. This is the bridge between repo-prep and real implementation.

## Internal Tasks Covered

```text
PR-23 — Shadow Runtime Code-Near Lock
```

## Primary Files

```text
docs/SHADOW_RUNTIME_LOCK_V7_1.md
docs/SHADOW_RUNTIME_CODE_NEAR_BOOK_V7_1.md
docs/SHADOW_RUNTIME_TO_REAL_BUILD_MAPPING_V7_1.md
docs/CONTRACT_TO_SHADOW_CODE_MAP_V7_1.md
docs/SHADOW_RUNTIME_STATE_MACHINES_V7_1.md
docs/SHADOW_RUNTIME_ACCEPTANCE_TESTS_V7_1.md
docs/YNODE_SHADOW_RUNTIME_PATTERN_ADAPTATION_V7_1.md
odin/shadow_runtime/
examples/shadow_runtime/
registries/shadow_runtime_contract_registry.json
tests/test_shadow_runtime_lock.py
```

## Required Behavior

- Codex can identify exact real target files for each shadow contract.
- Valid shadow flow produces an in-memory candidate-only result.
- Invalid direct-apply flow is blocked before any app mutation.
- Semantic bus remains local-only and non-authoritative.
- Model route remains resource-based and defaults to 3B + 7B/8B hybrid.
- Shadow final gate blocks authority escalation.
- The Shadow Runtime remains explicitly non-executing and non-authoritative.

## Forbidden Scope

- No real model provider calls.
- No actual daemon runtime claims.
- No external network.
- No public IRC.
- No app state mutation.
- No app-owned apply inside Odin.
- No remote route enablement.

## Definition of Done

- PR-23 task doc exists and passes codex task validation.
- REAL-PR-09 bundle doc exists and passes bundle validation.
- `shadow_runtime_contract_registry.json` is valid and covers central contracts.
- `validate-shadow-runtime` passes.
- `validate-all` passes.
- pytest passes.
- SYSTEM_MAP and FILE_MANIFEST are updated.

## Codex PR Summary Template

```text
Implemented REAL-PR-09 Shadow Runtime Mechanical Build Bridge.
Added code-near shadow runtime, fixtures, docs, registry and tests.
Preserved all Odin v7.1 boundaries: candidate-only, app-owned apply, semantic bus local-only, no live model calls, no runtime-proof claims.
```

## Implementation Notes

This bundle is intentionally after REAL-PR-08 because it hardens the repo for the next real build wave. It does not replace the earlier PR bundles. It gives Codex a code-near shape for implementing them with less interpretation risk. In review, the main question is not whether Odin now has live runtime behavior. The main question is whether future live runtime behavior has a precise, gated, fixture-backed path.

## Review Checklist

- The Shadow Runtime docs are present and substantial.
- PR-23 exists and is covered by this bundle.
- Shadow contracts map to future real targets.
- The example valid flow produces candidate-only output.
- The direct-apply invalid flow is blocked.
- No network, model provider, app apply or external send was introduced.
- All validation and tests remain green.
- The bundle registry and SYSTEM_MAP reflect the new layer.

## Follow-Up Boundary

The next real implementation may use this bundle as a build source, but it must still implement real modules under their own PR boundaries. This bundle is a bridge, not a shortcut around REAL-PR-01 through REAL-PR-08.

