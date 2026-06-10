# Shadow Runtime Acceptance Tests v7.1

## Purpose

These are the tests that define when the code-near Shadow Runtime is usable by Codex as a mechanical build source.

## Required Tests

### SR-TEST-001 — Shadow docs exist

Required files:

```text
docs/SHADOW_RUNTIME_LOCK_V7_1.md
docs/SHADOW_RUNTIME_CODE_NEAR_BOOK_V7_1.md
docs/SHADOW_RUNTIME_TO_REAL_BUILD_MAPPING_V7_1.md
docs/CONTRACT_TO_SHADOW_CODE_MAP_V7_1.md
docs/SHADOW_RUNTIME_STATE_MACHINES_V7_1.md
```

### SR-TEST-002 — Shadow registry exists

Required file:

```text
registries/shadow_runtime_contract_registry.json
```

The registry must include at least:

```text
binding_gate
universal_work_compile
semantic_bus_batch
model_route_plan
candidate_response_packet
shadow_final_gate
```

### SR-TEST-003 — Shadow code imports

The package `odin.shadow_runtime` must import without side effects.

### SR-TEST-004 — Valid markdown rewrite flow

Fixture:

```text
examples/shadow_runtime/markdown_rewrite_shadow_flow.valid.json
```

Expected:

```text
candidate_only true
route contains 3b_7b_8b_hybrid for standard_local
semantic bus batch contains #work.received and #candidate.ready
final gate passes
```

### SR-TEST-005 — Direct apply blocked

Fixture:

```text
examples/shadow_runtime/direct_apply_blocked.invalid.json
```

Expected:

```text
final gate blocks
reason includes direct_apply_forbidden
```

### SR-TEST-006 — Registry/task/bundle coverage

PR-23 must be in `codex_task_registry.json` and covered by REAL-PR-09.

## Validation Command

```text
python -m odin.cli validate-shadow-runtime
python -m odin.cli validate-all
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

## Completion Rule

The Shadow Runtime is accepted only if all tests pass and no cache artifacts are included in the ZIP.


---

## v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE

This release extends the Shadow Runtime from central spine coverage to full major-subsystem coverage. Every future addition must update the architecture/specs, internal PR ladder, REAL-PR bundles, registries, System Map, tests and FILE_MANIFEST. The Shadow Runtime remains candidate-only, local-only, non-authoritative and non-executing.

New coverage includes Artifact Lenses, Context Distillery, Worklet/Slot/Gaptext, Candidate Tournament, Low-Memory Strict Mode, Thor Bridge, Bounded Code Work, Storage/Trace/Receipt, Local API, App-QIRC Digest Bridge, Model Dojo, Security Redaction, Support Bundle, Windows Runtime and SDK/App Template validation.
