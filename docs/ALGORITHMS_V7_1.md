# Algorithms v7.1 — Deep Subsystem Spec

**Spec Status:** v7.1 / v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK.  
**Authority:** build contract for Codex and later implementation work.  
**Claim Boundary:** specification only; no runtime, host, model, security or deployment proof is implied.


## Algorithm Catalog

This document defines algorithms at pseudocode level. Codex may implement details differently only if behavior and acceptance tests remain equivalent.


## Universal Work Validation

Pseudocode:

```text
universal_work_validation:
  input: documented contract objects
  steps: validate structure; load binding; load manifest; check artifact types; check privacy; resolve verb; resolve output contract; check candidate_only; scan forbidden action intent; check model policy; return errors or normalized work.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## System Profile Compilation

Pseudocode:

```text
system_profile_compilation:
  input: documented contract objects
  steps: read work intent; map verb/artifact/output to intent family; activate lenses; choose precompute depth; choose semantic bus mode; choose route class; emit system profile with reason codes.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## Context Distillation

Pseudocode:

```text
context_distillation:
  input: documented contract objects
  steps: collect candidate context; drop irrelevant fields; rank by task center; redact by privacy; compress into must_use/must_not_use/style/length/evidence refs; score capsule.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## Semantic Bus Batch

Pseudocode:

```text
semantic_bus_batch:
  input: documented contract objects
  steps: open batch; publish work.received; publish validation/profile/context/slot/model/candidate events; validate envelope; close batch; store replay refs according to retention.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## Worklet Graph Build

Pseudocode:

```text
worklet_graph_build:
  input: documented contract objects
  steps: determine if task is simple or compound; split into deterministic/model/critic nodes; enforce DAG; attach slot requirements; mark high-risk branches; return graph.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## Slot Forge

Pseudocode:

```text
slot_forge:
  input: documented contract objects
  steps: combine lens+verb+output+model_profile+resource_profile; compute token budgets; set forbidden claims; attach fallback; create slot contract.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## Model Route Selection

Pseudocode:

```text
model_route_selection:
  input: documented contract objects
  steps: prefer deterministic; check low-memory; check 3B sufficiency; use sweet spot for standard; escalate only when output quality/semantic pressure requires; obey privacy/remote policy.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## Candidate Tournament

Pseudocode:

```text
candidate_tournament:
  input: documented contract objects
  steps: generate allowed candidates; score fit; critic check; select/merge; record DNA; return selected and optionally alternatives.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## Critic Cascade

Pseudocode:

```text
critic_cascade:
  input: documented contract objects
  steps: run schema, claim, context, style, genericness and boundary checks based on risk profile; emit route accept/retry/escalate/block.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## Response Packet Assembly

Pseudocode:

```text
response_packet_assembly:
  input: documented contract objects
  steps: collect candidate artifacts; attach status chips; attach warnings; strip forbidden claims; attach trace id; return app-renderable packet.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## Claim Gate

Pseudocode:

```text
claim_gate:
  input: documented contract objects
  steps: scan candidate content and metadata; downgrade or block unsupported strong claims; require receipts for host/test/security/deploy assertions.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.


## Resource Profile Detection

Pseudocode:

```text
resource_profile_detection:
  input: documented contract objects
  steps: sample RAM/VRAM/CPU/provider/model availability; derive resource profile; update on pressure changes; avoid heavy routes under interactive latency.
  output: normalized object, candidate object, route decision or validation errors
  failure: return typed reason code; do not silently continue
```

Required reason codes: `ok`, `needs_context`, `blocked_by_policy`, `resource_route_blocked`, `schema_invalid`, `claim_boundary_hit`, `cannot_safely_complete`.



## Deep Detail Expansion — Contract Detail

This subsystem is part of the Odin Agent Shell v7.1 canonical build contract. Codex must treat this document as binding detail under `MASTER_ARCHITECTURE_V7_1.md` and `MASTER_SPECS_V7_1.md`.

### Authority and Boundary

- The subsystem may create local derived artifacts only when the relevant input contract allows it.
- The subsystem may emit trace events, reason codes, warnings, conflicts and Candidate Artifacts.
- The subsystem may not mutate app state, send externally, bypass caller manifest policy, or promote model output into factual authority.
- All app-impacting output must remain candidate-only and must be routed through an app-owned apply gate.
- All state transitions must be observable through trace entries or semantic bus events when that bus is enabled.

### Inputs

The implementation must accept only typed inputs. Raw dictionaries are not accepted as internal domain objects after the validation boundary. Every input path must either load from schema, registry, examples, app bridge, semantic bus event or an explicitly typed constructor.

Expected input safeguards:

```text
schema validation
protocol_version compatibility
privacy_class check
caller manifest check
resource profile check
claim boundary check
semantic bus local-only check where applicable
```

### Outputs

Every output must carry a reason code or trace id. Where the output is app-renderable, it must be wrapped as Candidate Artifact or Response Packet. Where the output is internal, it must remain local derived context and must not claim app truth.

Output requirements:

```text
candidate_only where app-facing
traceable where work-related
redacted where privacy-sensitive
schema-shaped where contract-defined
fallback route where unsafe or incomplete
```

### Validation Rules

Implementation must include positive and negative tests. Negative tests are as important as success examples because Odin's core value is bounded authority. The subsystem must reject invalid state early and must not silently repair boundary violations unless the repair is explicitly part of its job, such as schema repair.

Required validation categories:

```text
missing required fields
invalid enum values
privacy mismatch
forbidden route
unsupported artifact type
non-candidate output
semantic bus escape attempt
remote route without policy
claim boundary violation
resource profile mismatch
```

### Trace and Diagnostics

The subsystem must emit debug data without leaking secrets. Trace entries should contain identifiers, reason codes, route choices, validation outcomes and digest references. They should not contain raw sensitive payloads unless an explicit debug policy allows it.

Trace expectations:

```text
trace_id on work-related records
work_id where applicable
candidate_dna_ref for output assembly
semantic_bus_batch_ref when bus is enabled
model_route_ref when model work is invoked
```

### Codex Implementation Notes

Codex must implement the simplest valid path first, then add deeper branches. The correct build order is validator, example, negative test, minimal runtime function, trace integration, registry/system-map update, then optional optimization. New behavior without a test and without documentation is drift.

### Done Criteria

A subsystem change is done only when:

```text
docs updated
schemas updated where applicable
registries updated where applicable
examples updated where applicable
validation CLI clean
tests cover success and rejection
no app authority drift
no remote behavior added implicitly
FILE_MANIFEST refreshed
```


## Deep Detail Expansion — Contract Detail

This subsystem is part of the Odin Agent Shell v7.1 canonical build contract. Codex must treat this document as binding detail under `MASTER_ARCHITECTURE_V7_1.md` and `MASTER_SPECS_V7_1.md`.

### Authority and Boundary

- The subsystem may create local derived artifacts only when the relevant input contract allows it.
- The subsystem may emit trace events, reason codes, warnings, conflicts and Candidate Artifacts.
- The subsystem may not mutate app state, send externally, bypass caller manifest policy, or promote model output into factual authority.
- All app-impacting output must remain candidate-only and must be routed through an app-owned apply gate.
- All state transitions must be observable through trace entries or semantic bus events when that bus is enabled.

### Inputs

The implementation must accept only typed inputs. Raw dictionaries are not accepted as internal domain objects after the validation boundary. Every input path must either load from schema, registry, examples, app bridge, semantic bus event or an explicitly typed constructor.

Expected input safeguards:

```text
schema validation
protocol_version compatibility
privacy_class check
caller manifest check
resource profile check
claim boundary check
semantic bus local-only check where applicable
```

### Outputs

Every output must carry a reason code or trace id. Where the output is app-renderable, it must be wrapped as Candidate Artifact or Response Packet. Where the output is internal, it must remain local derived context and must not claim app truth.

Output requirements:

```text
candidate_only where app-facing
traceable where work-related
redacted where privacy-sensitive
schema-shaped where contract-defined
fallback route where unsafe or incomplete
```

### Validation Rules

Implementation must include positive and negative tests. Negative tests are as important as success examples because Odin's core value is bounded authority. The subsystem must reject invalid state early and must not silently repair boundary violations unless the repair is explicitly part of its job, such as schema repair.

Required validation categories:

```text
missing required fields
invalid enum values
privacy mismatch
forbidden route
unsupported artifact type
non-candidate output
semantic bus escape attempt
remote route without policy
claim boundary violation
resource profile mismatch
```

### Trace and Diagnostics

The subsystem must emit debug data without leaking secrets. Trace entries should contain identifiers, reason codes, route choices, validation outcomes and digest references. They should not contain raw sensitive payloads unless an explicit debug policy allows it.

Trace expectations:

```text
trace_id on work-related records
work_id where applicable
candidate_dna_ref for output assembly
semantic_bus_batch_ref when bus is enabled
model_route_ref when model work is invoked
```

### Codex Implementation Notes

Codex must implement the simplest valid path first, then add deeper branches. The correct build order is validator, example, negative test, minimal runtime function, trace integration, registry/system-map update, then optional optimization. New behavior without a test and without documentation is drift.

### Done Criteria

A subsystem change is done only when:

```text
docs updated
schemas updated where applicable
registries updated where applicable
examples updated where applicable
validation CLI clean
tests cover success and rejection
no app authority drift
no remote behavior added implicitly
FILE_MANIFEST refreshed
```
