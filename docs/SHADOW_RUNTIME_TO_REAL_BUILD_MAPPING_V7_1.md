# Shadow Runtime to Real Build Mapping v7.1

## Purpose

This document binds every central Shadow Runtime contract to real target files, tests, fixtures and Codex tasks. It prevents implementation drift.

## Mapping Table

| Contract | Shadow file | Real target | Fixture | Test | Internal task | Real bundle |
|---|---|---|---|---|---|---|
| Universal Work validation | `odin/shadow_runtime/universal_work_shadow.py` | `odin/universal_work/universal_work_validator.py` | `examples/shadow_runtime/markdown_rewrite_shadow_flow.valid.json` | `tests/test_shadow_runtime_lock.py` | PR-23 | REAL-PR-09 |
| Candidate-only boundary | `odin/shadow_runtime/boundary.py` | `odin/core/final_gate.py` | `examples/shadow_runtime/direct_apply_blocked.invalid.json` | `tests/test_shadow_runtime_lock.py` | PR-23 | REAL-PR-09 |
| Semantic bus event sequence | `odin/shadow_runtime/semantic_bus_shadow.py` | `odin/semantic_bus/` | `examples/shadow_runtime/semantic_bus_shadow_batch.valid.json` | `tests/test_shadow_runtime_lock.py` | PR-23 | REAL-PR-09 |
| Model route plan | `odin/shadow_runtime/model_route_shadow.py` | `odin/models/model_router.py` | `examples/shadow_runtime/model_route_standard.valid.json` | `tests/test_shadow_runtime_lock.py` | PR-23 | REAL-PR-09 |
| Candidate artifact and DNA | `odin/shadow_runtime/candidate_shadow.py` | `odin/packets/` | `examples/shadow_runtime/markdown_rewrite_shadow_flow.valid.json` | `tests/test_shadow_runtime_lock.py` | PR-23 | REAL-PR-09 |
| End-to-end shadow pipeline | `odin/shadow_runtime/pipeline.py` | future `odin/orchestrator.py` or daemon coordinator | `examples/shadow_runtime/markdown_rewrite_shadow_flow.valid.json` | `tests/test_shadow_runtime_lock.py` | PR-23 | REAL-PR-09 |

## Build Direction

Codex should implement from left to right:

```text
contract → shadow file → fixture → test → real target
```

The shadow file is not the final implementation. It is the source of shape, states, boundaries and sequencing.

## Drift Lock

Any future change to a shadow contract must update:

- this mapping document;
- `registries/shadow_runtime_contract_registry.json`;
- PR-23 task doc or successor task;
- REAL-PR-09 bundle doc or successor bundle;
- relevant tests;
- FILE_MANIFEST.

## Mandatory Preservation

Every real target must preserve:

```text
candidate_only
app_owns_apply
semantic_bus_local_only
model_output_projection_only
no_public_network
no_auto_remote
smallest_sufficient_worker
trace_required
```


---

## v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE

This release extends the Shadow Runtime from central spine coverage to full major-subsystem coverage. Every future addition must update the architecture/specs, internal PR ladder, REAL-PR bundles, registries, System Map, tests and FILE_MANIFEST. The Shadow Runtime remains candidate-only, local-only, non-authoritative and non-executing.

New coverage includes Artifact Lenses, Context Distillery, Worklet/Slot/Gaptext, Candidate Tournament, Low-Memory Strict Mode, Thor Bridge, Bounded Code Work, Storage/Trace/Receipt, Local API, App-QIRC Digest Bridge, Model Dojo, Security Redaction, Support Bundle, Windows Runtime and SDK/App Template validation.
