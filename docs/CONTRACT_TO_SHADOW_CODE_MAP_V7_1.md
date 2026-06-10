# Contract to Shadow Code Map v7.1

## Objective

This is the exact map Codex should use when converting v7.1 contracts into real code.

## Contract: Binding Gate

Source docs:

- `docs/MASTER_SPECS_V7_1.md`
- `docs/DATA_CONTRACTS_V7_1.md`
- `docs/APP_INTEGRATION_STANDARD.md`

Shadow functions:

```text
odin.shadow_runtime.boundary.ensure_binding_policy
odin.shadow_runtime.boundary.ensure_candidate_only
```

Real targets:

```text
odin/protocol/binding.py
odin/apps/caller_manifest.py
odin/core/final_gate.py
```

Failure states:

```text
BINDING_INVALID
PRIVACY_DENIED
OUTPUT_CONTRACT_INVALID
FORBIDDEN_ACTION
```

## Contract: Universal Work Compile

Shadow functions:

```text
odin.shadow_runtime.universal_work_shadow.validate_shadow_universal_work
odin.shadow_runtime.pipeline.run_shadow_pipeline
```

Real targets:

```text
odin/universal_work/universal_work_validator.py
odin/universal_work/universal_work_compiler.py
```

Required outputs:

```text
context_capsule_candidate
worklet_graph_candidate
slot_contract_candidate
model_route_plan_candidate
candidate_artifact_candidate
```

## Contract: Semantic Bus Batch

Shadow functions:

```text
odin.shadow_runtime.semantic_bus_shadow.make_shadow_bus_event
odin.shadow_runtime.semantic_bus_shadow.make_shadow_bus_batch
```

Real targets:

```text
odin/semantic_bus/event_envelope.py
odin/semantic_bus/bus.py
odin/semantic_bus/replay.py
```

Red lines:

```text
no public IRC
no LAN mesh
no app event ownership
no app mutation
```

## Contract: Model Route Plan

Shadow functions:

```text
odin.shadow_runtime.model_route_shadow.choose_shadow_route
```

Real targets:

```text
odin/models/model_router.py
odin/models/hybrid_director.py
```

Default route:

```text
3b_7b_8b_hybrid
```

Escalation:

```text
low_memory_strict → 1b_2b_or_3b_micro
standard_local → 3b_7b_8b_hybrid
quality_local → 3b_13b_14b_quality_hybrid
heavy_local → 22b_32b_heavy_local
max_local_batch → 70b_class_batch
remote_optional → remote_optional_explicit
```

## Contract: Candidate Artifact

Shadow functions:

```text
odin.shadow_runtime.candidate_shadow.make_shadow_candidate
odin.shadow_runtime.candidate_shadow.make_shadow_response_packet
```

Real targets:

```text
odin/packets/response_packet.py
odin/packets/receipt_candidate.py
```

Required states:

```text
candidate_only = true
requires_app_apply_gate = true
claim_status = shadow_projection or model_projection
```

## Contract: Final Gate

Shadow functions:

```text
odin.shadow_runtime.boundary.shadow_final_gate
```

Real targets:

```text
odin/core/final_gate.py
odin/quality/output_guard.py
odin/quality/claim_scanner.py
```

Block if:

```text
candidate_only false
direct apply requested
external send requested
semantic bus network requested
app mutation requested
remote route without permission
```


---

## v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE

This release extends the Shadow Runtime from central spine coverage to full major-subsystem coverage. Every future addition must update the architecture/specs, internal PR ladder, REAL-PR bundles, registries, System Map, tests and FILE_MANIFEST. The Shadow Runtime remains candidate-only, local-only, non-authoritative and non-executing.

New coverage includes Artifact Lenses, Context Distillery, Worklet/Slot/Gaptext, Candidate Tournament, Low-Memory Strict Mode, Thor Bridge, Bounded Code Work, Storage/Trace/Receipt, Local API, App-QIRC Digest Bridge, Model Dojo, Security Redaction, Support Bundle, Windows Runtime and SDK/App Template validation.
