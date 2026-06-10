# Model Scale Ladder v7.1 — Deep Subsystem Spec

**Spec Status:** v7.1 / v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK.  
**Authority:** build contract for Codex and later implementation work.  
**Claim Boundary:** specification only; no runtime, host, model, security or deployment proof is implied.


## Routing Principle

Odin routes by measured resource profile and task requirements, not hardware brand. The architecture must not hardcode named GPUs or machines. It discovers RAM, VRAM, CPU threads, provider availability, loaded models, quantization, context capacity, latency target and current resource pressure.


## Scale Ladder

| Level | Route | Use |
| --- | --- | --- |
| L0 | deterministic_no_model | templates/rules/cache |
| L1 | 1b_2b_micro | ultra-low memory micro tasks |
| L2 | 3b_micro | routing/critic/extract |
| L3 | 3b_multi_slot | multi-step small tasks |
| L4 | 7b_8b_quality | writing/synthesis |
| L5 | 3b_7b_8b_hybrid | canonical sweet spot |
| L6 | 3b_13b_14b_quality_hybrid | quality escalation |
| L7 | 3b_22b_32b_heavy_local | heavy local/batch |
| L8 | moe_heavy_local_offload | MoE/offload tasks |
| L9 | 70b_class_batch | rare batch/offload |
| L10 | remote_optional_explicit | explicit opt-in only |
| L11 | cannot_safely_complete | safe refusal/needs context |


## Resource Profile Detection

Resource profiles are computed from actual observed constraints:

```text
low_memory_strict: constrained RAM, no GPU or high pressure
standard_local: comfortable 3B+7B/8B route
quality_local: can run 13B/14B quality routes acceptably
aheavy_local: can run 22B/32B routes in batch/draft modes
max_local_batch: very large local/offload only for non-interactive work
remote_optional: remote route allowed by caller and user policy
```

The router must consider latency mode before model size. Interactive work should prefer smaller well-prepared routes.


## Escalation Discipline

Before escalating model size, Odin must try:

```text
better context distillation
worklet splitting
slot tightening
semantic bus precompute
candidate tournament
critic cascade
3B+7B/8B hybrid
ask_context
```

A larger model is a route, not the architecture. The architecture remains small-model-first.



## Anchor — 3B + 7B/8B

This section establishes the required anchor `3B + 7B/8B` for the v0.3.2 deep subsystem spec lock. The anchor is part of the implementation contract and must remain present unless the system map and validation rules are updated in the same change.


## Anchor — remote optional

This section establishes the required anchor `remote optional` for the v0.3.2 deep subsystem spec lock. The anchor is part of the implementation contract and must remain present unless the system map and validation rules are updated in the same change.


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
