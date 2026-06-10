# Flow Catalog v7.1 — Deep Subsystem Spec

**Spec Status:** v7.1 / v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK.  
**Authority:** build contract for Codex and later implementation work.  
**Claim Boundary:** specification only; no runtime, host, model, security or deployment proof is implied.


## Flow Catalog Purpose

Flows show how contracts and modules compose. Codex should implement tests for representative flows before adding provider complexity.


## Markdown Rewrite

Flow:

```text
App selects text -> Event Digest -> Universal Work rewrite -> Context Capsule -> Slot Forge micro_rewrite -> 3B or 7B -> Style Critic -> markdown_candidate.
```

Required checks:

```text
- binding valid
- app authority preserved
- candidate_only true
- privacy class respected
- semantic bus batch traceable when bus enabled
- response packet app-renderable
```


## JSON Repair

Flow:

```text
App passes json_object -> repair verb -> output json_candidate -> 3B JSON repair -> schema critic -> candidate.
```

Required checks:

```text
- binding valid
- app authority preserved
- candidate_only true
- privacy class respected
- semantic bus batch traceable when bus enabled
- response packet app-renderable
```


## Document Summary

Flow:

```text
document_excerpt -> summarize -> context distillery -> 3B short summary or 7B if long -> claim critic -> summary_candidate.
```

Required checks:

```text
- binding valid
- app authority preserved
- candidate_only true
- privacy class respected
- semantic bus batch traceable when bus enabled
- response packet app-renderable
```


## Traureden Section

Flow:

```text
project digest + selected section -> wedding_speech lens -> seeds/taste dials -> worklets -> 7B writer -> 3B critics -> ceremony_section_candidate.
```

Required checks:

```text
- binding valid
- app authority preserved
- candidate_only true
- privacy class respected
- semantic bus batch traceable when bus enabled
- response packet app-renderable
```


## Code PatchPlan

Flow:

```text
repo_context + plan -> code lens -> Thor lite -> worklet graph -> 7B/quality slot -> claim gate -> patchplan_candidate.
```

Required checks:

```text
- binding valid
- app authority preserved
- candidate_only true
- privacy class respected
- semantic bus batch traceable when bus enabled
- response packet app-renderable
```


## Error Log Explain

Flow:

```text
error_log -> explain -> log lens -> 3B extract + 7B explanation if needed -> debug_hypothesis_candidate.
```

Required checks:

```text
- binding valid
- app authority preserved
- candidate_only true
- privacy class respected
- semantic bus batch traceable when bus enabled
- response packet app-renderable
```


## Game NPC Line

Flow:

```text
game_state_digest + dialogue_context -> generate_candidate -> game lens -> 3B/7B route -> npc_line_candidate.
```

Required checks:

```text
- binding valid
- app authority preserved
- candidate_only true
- privacy class respected
- semantic bus batch traceable when bus enabled
- response packet app-renderable
```


## Workflow Next Step

Flow:

```text
workflow_state -> route/plan -> action card -> deterministic + 3B -> workflow_next_step_candidate.
```

Required checks:

```text
- binding valid
- app authority preserved
- candidate_only true
- privacy class respected
- semantic bus batch traceable when bus enabled
- response packet app-renderable
```


## Low Memory Assist

Flow:

```text
low_memory_strict -> semantic bus light -> static/template -> 1B/2B/3B micro -> small candidate.
```

Required checks:

```text
- binding valid
- app authority preserved
- candidate_only true
- privacy class respected
- semantic bus batch traceable when bus enabled
- response packet app-renderable
```


## App QIRC Digest

Flow:

```text
app event digest from app-owned QIRC -> Odin bus -> context capsule -> candidate -> app decides whether to emit app event.
```

Required checks:

```text
- binding valid
- app authority preserved
- candidate_only true
- privacy class respected
- semantic bus batch traceable when bus enabled
- response packet app-renderable
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
