# Internal Semantic IRC Bus v7.1 — Deep Subsystem Spec

**Spec Status:** v7.1 / v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK.  
**Authority:** build contract for Codex and later implementation work.  
**Claim Boundary:** specification only; no runtime, host, model, security or deployment proof is implied.


## Purpose and Boundary

The Internal Semantic IRC Bus is a local-only coordination layer. It exists to make Odin's precompute, worklets, critics, routing and candidate assembly more deterministic and inspectable. It is not public chat, not a network feature, not an app-state owner and not an agent swarm.


## Runtime Modes

| Mode | Description | Allowed |
| --- | --- | --- |
| disabled | no bus | all core flows still work |
| embedded_local | in daemon | default power mode |
| separate_local | own process | debug/heavy |
| verification_only | validate events no dispatch | CI/tests |
| degraded_no_bus | fallback when bus fails | continue with direct calls |


## Channel Registry Contract

Every channel entry must define name, family, local_only, payload class, retention policy and producer/consumer modules. Channels start with `#`. Public or WAN channels are not allowed in v7.1.

Required families:

```text
odin_status
app_intake
universal_work
context
artifact_lens
precompute
worklets_slots
models
critics
candidates
response
trace_receipts
```


## Semantic Event Envelope

Every event must satisfy:

```text
event_id present
protocol_version compatible
channel starts with #
event_type present
source_module present
trace_id present for traceable work
work_id present for work events
privacy_class present for context events
payload is JSON-object-like
```

Payload must not contain secrets, blocked_sensitive raw data or full app-state firehose. Large payloads use content references.


## IRC Feature Mapping

| IRC Feature | Odin Meaning | Constraint |
| --- | --- | --- |
| channel | semantic lane | local only |
| topic | active constraints | no secrets |
| tag | metadata | work/trace/privacy ids |
| nick | module surface | not autonomous agent |
| notice | warning | non-authoritative |
| batch | work run group | traceable |
| replay | debug reconstruction | redacted by default |


## Module Bot Contract

Module bots are deterministic or bounded module surfaces. They may subscribe/publish semantic events. They cannot grant authority, mutate app state, apply changes, send externally, bypass final gate or claim reality status.

Required bots:

```text
binding-guard
event-digest-reader
universal-work-validator
artifact-lens-router
context-distiller
system-profile-router
middle-out-collapser
seed-weaver
fit-radar
mirror-axis-checker
semantic-pressure-valve
worklet-graph-builder
slot-forge
gaptext-builder
model-router
claim-critic
style-critic
genericness-critic
schema-critic
candidate-composer
response-packet-builder
trace-recorder
```


## Bridge to App-Owned QIRC

Apps may later have their own event/QIRC systems. Odin must consume digest artifacts only. It may not mirror full app state by default and may not publish mutation events. App QIRC remains app-owned.

Bridge flow:

```text
app event system -> app-owned digest -> Odin bus #app.event_digest -> precompute/model work -> Candidate Artifact -> app decides whether to emit app event
```



## Anchor — #context.distill

This section establishes the required anchor `#context.distill` for the v0.3.2 deep subsystem spec lock. The anchor is part of the implementation contract and must remain present unless the system map and validation rules are updated in the same change.


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
