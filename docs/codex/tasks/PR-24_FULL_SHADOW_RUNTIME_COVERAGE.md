# PR-24 — Full Shadow Runtime Coverage

## Objective

Extend the Odin v7.1 Shadow Runtime from central-spine coverage to full major-subsystem coverage. The result must give Codex a mechanical contract-to-code bridge for every major subsystem before live implementation begins.

## Primary Files

```text
odin/shadow_runtime/artifact_lens_context_shadow.py
odin/shadow_runtime/worklet_slot_shadow.py
odin/shadow_runtime/candidate_tournament_shadow.py
odin/shadow_runtime/low_memory_shadow.py
odin/shadow_runtime/thor_bridge_shadow.py
odin/shadow_runtime/bounded_code_shadow.py
odin/shadow_runtime/storage_trace_shadow.py
odin/shadow_runtime/api_shadow.py
odin/shadow_runtime/app_qirc_bridge_shadow.py
odin/shadow_runtime/model_dojo_shadow.py
odin/shadow_runtime/security_redaction_shadow.py
odin/shadow_runtime/support_bundle_shadow.py
odin/shadow_runtime/windows_runtime_shadow.py
odin/shadow_runtime/sdk_template_shadow.py
docs/SHADOW_RUNTIME_FULL_COVERAGE_V7_1.md
docs/SHADOW_SUBSYSTEM_COVERAGE_MATRIX_V7_1.md
examples/shadow_runtime/
tests/test_full_shadow_runtime_coverage.py
registries/shadow_runtime_contract_registry.json
```

## Required Behavior

- Every major subsystem has a shadow module.
- Every shadow module is pure in-memory and side-effect free.
- Every shadow contract maps to a real target file.
- Every shadow contract has a fixture, test, internal task and REAL-PR bundle.
- Candidate-only, app-owned apply, semantic bus local-only and no-real-model-call laws remain intact.
- `validate-shadow-runtime` enforces the full coverage contract.

## Forbidden Scope

- No real model provider calls.
- No sockets or server startup.
- No public IRC, LAN mesh, federation or external network.
- No app state mutation.
- No file patch application.
- No external send.
- No runtime-proof claims.

## Definition of Done

- `python -m odin.cli validate-shadow-runtime` passes.
- `python -m odin.cli validate-all` passes.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider` passes.
- PR-24 is listed in `codex_task_registry.json`.
- PR-24 is covered by REAL-PR-10.
- Shadow registry contains full major-subsystem coverage entries.
- SYSTEM_MAP references full coverage docs.
- FILE_MANIFEST includes every changed file.

## Codex PR Summary Template

```text
Implemented PR-24 Full Shadow Runtime Coverage.
Added code-near shadow modules, fixtures, registry coverage and tests for all major Odin v7.1 subsystems.
Preserved candidate-only, app-owned apply, local-only semantic bus, no live model calls and no runtime-proof claims.
Validation:
- python -m odin.cli validate-all
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

## Review Checklist

- Does every major subsystem have a shadow module?
- Does every shadow module map to a real target?
- Are fixtures present for all new contracts?
- Do tests exercise success and boundary failure cases?
- Are PR ladder and REAL-PR bundles updated?
- Is semantic bus still local-only?
- Is Odin still candidate-only and app-authority-preserving?
