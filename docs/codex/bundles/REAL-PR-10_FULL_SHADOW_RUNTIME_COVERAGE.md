# REAL-PR-10 — Full Shadow Runtime Coverage

## Objective

Add full major-subsystem Shadow Runtime coverage so Codex can later build each Odin v7.1 subsystem from a code-near, fixture-backed contract rather than free interpretation.

## Internal Tasks Covered

```text
PR-24 — Full Shadow Runtime Coverage
```

## Primary Files

```text
odin/shadow_runtime/
examples/shadow_runtime/
docs/SHADOW_RUNTIME_FULL_COVERAGE_V7_1.md
docs/SHADOW_SUBSYSTEM_COVERAGE_MATRIX_V7_1.md
registries/shadow_runtime_contract_registry.json
tests/test_full_shadow_runtime_coverage.py
```

## Required Behavior

- Shadow Runtime covers all major v7.1 subsystems.
- All shadow functions remain pure, deterministic and side-effect free.
- Each contract maps to a real target file and future build PR.
- Every new coverage area has fixture and test coverage.
- The full coverage matrix is referenced by SYSTEM_MAP.
- Validation and pytest remain green.

## Forbidden Scope

- No live daemon proof.
- No model provider execution.
- No app mutation.
- No patch application.
- No external send.
- No public IRC or network feature.
- No production-ready claim.

## Definition of Done

- PR-24 task doc exists and passes task validation.
- REAL-PR-10 bundle doc exists and passes bundle validation.
- `shadow_runtime_contract_registry.json` contains full major-subsystem coverage.
- `validate-shadow-runtime` passes.
- `validate-all` passes.
- pytest passes.
- SYSTEM_MAP and FILE_MANIFEST are updated.

## Codex PR Summary Template

```text
Implemented REAL-PR-10 Full Shadow Runtime Coverage.
Added full major-subsystem code-near shadow coverage, fixtures, registry mapping and tests.
Preserved all Odin v7.1 boundaries: candidate-only, app-owned apply, semantic bus local-only, no live model calls, no runtime-proof claims.
```

## Review Checklist

- Are all major subsystems represented?
- Does every registry contract have shadow_file, real_target, fixture, test, task and bundle?
- Are the new shadow modules imported by odin.shadow_runtime?
- Do the fixtures stay small and local-only?
- Did the bundle registry cover PR-24?
- Did the internal task ladder include PR-24?

## Extended Review Notes

REAL-PR-10 exists because REAL-PR-09 proved the central mechanical build bridge but did not yet make every major subsystem mechanically explicit. This bundle closes that coverage gap. It should be treated as a preparation PR before live implementation work resumes. The reviewer should confirm that the new shadow modules do not create accidental runtime behavior. They should remain importable helper functions, not daemon services, not background workers and not model clients.

The coverage target is deliberately broad. It includes app-facing structures such as SDK templates and App-QIRC digest bridge, runtime structures such as Windows process planning and local API planning, safety structures such as redaction and support bundle boundaries, and quality structures such as candidate tournament and Model Dojo. Each area should be traceable from spec to shadow code to fixture to tests to future real target file.

A future Codex PR may implement a real subsystem only after this bundle gives it a corresponding shadow contract. If implementation discovers a missing contract, Codex must add the missing contract first or update this bundle in the same PR. That rule prevents architecture drift.

## Additional Definition of Done

- The coverage matrix includes every new shadow contract.
- The shadow contract registry has no orphan entry.
- Every fixture remains local-only and contains no secret material.
- The Support Bundle shadow contract never uploads anything.
- The Windows Runtime shadow contract never claims the host was validated.
- The API shadow contract never claims a server was started.
- The Model Dojo shadow contract never claims benchmark truth.
- The Security Redaction shadow contract never stores secrets.
