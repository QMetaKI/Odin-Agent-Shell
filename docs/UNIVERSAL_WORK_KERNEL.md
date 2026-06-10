# Universal Work Kernel v7.1 — Deep Subsystem Spec

**Spec Status:** v7.1 / v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK.  
**Authority:** build contract for Codex and later implementation work.  
**Claim Boundary:** specification only; no runtime, host, model, security or deployment proof is implied.


## Purpose and Boundary

The Universal Work Kernel is the mandatory center of every AI-like operation in Odin. It ensures that no app-specific feature is treated as a raw prompt and no model receives unbounded app context. Every request must be normalized into a Universal Work Object before routing, precompute, semantic bus batching, slot forging or model execution.

The kernel owns the transformation from app-native intent into bounded semantic work. It does not own app state, app authority, app UI, app apply, app persistence or external sends. It produces Candidate Artifacts only.

Core invariant:

```text
Input Artifacts + Verb + Output Contract + Constraints + Boundary + Model Policy -> Candidate Artifact
```


## Object Lifecycle

1. App builds or asks Odin to help build an `ODIN_UNIVERSAL_WORK` object.
2. Binding validation confirms caller identity, manifest rules and app authority boundary.
3. Input artifacts are checked for type, privacy class, trust status and digest integrity.
4. Transformation verb is resolved against the verb registry and caller manifest.
5. Output contract is resolved and checked for candidate-only posture.
6. Boundary/constraints are scanned for forbidden action intent.
7. System Profile Compiler assigns intent family, precompute depth, lens set and route class.
8. Internal Semantic Bus opens a work batch if enabled.
9. Adaptive Precompute creates context capsule, semantic script, worklet graph and slot plan.
10. ModelWorkPackets are generated for only the required bounded slots.
11. Candidate Artifacts are assembled and wrapped in a Response Packet.


## Universal Work Required Fields

| Field | Required | Meaning | Reject If Missing |
| --- | --- | --- | --- |
| artifact_kind | yes | must be odin_universal_work | yes |
| protocol_version | yes | must be 7.1-compatible | yes |
| work_id | yes | stable work identifier | yes |
| caller_id | yes | app/tool id | yes |
| binding_ref | yes | authority and policy boundary | yes |
| input_artifacts | yes | bounded inputs | yes |
| work_intent | yes | verb/mode/goal | yes |
| output_contract | yes | candidate output shape | yes |
| constraints | yes | allowed/forbidden work rules | yes |
| model_policy | yes | route permissions | yes |
| claim_boundary | yes | projection-only boundary | yes |


## Validation Rules Catalog

The Universal Work validator must fail closed. Validation errors are not warnings; they prevent routing. Warnings may be returned only after a valid work object exists.

Validation categories:

```text
structure_validity
binding_validity
manifest_permission
artifact_type_permission
artifact_privacy_permission
verb_permission
output_contract_permission
candidate_only_integrity
forbidden_action_scan
remote_policy_check
claim_boundary_check
resource_policy_check
semantic_bus_policy_check
```

Example hard rejections:

```text
- output_contract.candidate_only is false
- action requests app mutation by Odin
- remote route is requested but caller manifest blocks remote
- blocked_sensitive artifact appears in input_artifacts
- app asks for direct send, apply, deploy, or test-result assertion
- model_policy exceeds current resource profile policy
```


## Input Artifact Contract

Every input artifact is a typed reference, not an informal blob. Large or sensitive payloads should be referenced through app-owned content references or redacted local object store references. The artifact digest allows cache and trace linkage without requiring Odin to persist raw app state.

Artifact fields:

```json
{
  "artifact_id": "ART-001",
  "artifact_type": "markdown",
  "content_ref": "ctx_selected_text",
  "trust_status": "caller_provided",
  "privacy_class": "local_only",
  "digest": "sha256...",
  "role": "primary_input",
  "size_hint": {"tokens": 800},
  "redaction_status": "not_required"
}
```

Rules:

```text
- digest required for cacheable artifacts
- privacy_class required for every artifact
- blocked_sensitive never enters model or semantic bus
- unknown trust status downgrades evidence posture
- model_projection artifacts cannot become verified evidence by themselves
```


## Output Contract Contract

The output contract is the app-native target shape. It defines not only text length or schema shape, but how the Candidate Artifact may be rendered, which app-owned actions may be displayed, and which claims remain blocked.

Output contract must include:

```text
artifact_type
schema_ref or shape
candidate_only = true
requires_app_apply_gate when action-impacting
max_tokens or max_structural_size
forbidden_claims
status_requirements
render_target
```

Output contracts are resolved before model routing. The model never chooses its own output authority.


## State Machine

Universal Work state progression:

```text
created
received
binding_checked
validated
profiled
bus_batch_opened
precomputed
worklet_graph_built
slots_forged
model_packets_built
model_route_completed
critic_checked
candidate_built
response_packet_built
returned
closed
```

Failure states:

```text
binding_invalid
artifact_blocked
verb_forbidden
output_contract_invalid
boundary_hit
resource_route_blocked
semantic_pressure_too_high
needs_context
cannot_safely_complete
```

State transitions must be traceable. Failed validation must create a conflict or blocked response packet, not a silent failure.


## Codex Implementation Requirements

Codex must implement Universal Work before model provider depth. Provider work without Universal Work validation is out of order. The first implementation target is a mock-provider flow that proves the complete candidate-only route without local model dependency.

Minimum implementation order:

```text
1. schema load
2. registry load
3. caller manifest parse
4. binding validate
5. universal work validate
6. output contract resolve
7. candidate artifact build
8. response packet return
9. negative test matrix
10. semantic bus batch hooks
```



## Anchor — Binding Validation

This section establishes the required anchor `Binding Validation` for the v0.3.2 deep subsystem spec lock. The anchor is part of the implementation contract and must remain present unless the system map and validation rules are updated in the same change.


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
