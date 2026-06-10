# Small Model Power Layer v7.1 — Deep Subsystem Spec

**Spec Status:** v7.1 / v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK.  
**Authority:** build contract for Codex and later implementation work.  
**Claim Boundary:** specification only; no runtime, host, model, security or deployment proof is implied.


## Purpose

The Small Model Power Layer is the performance core of Odin. Its goal is to make small local models useful by shaping the work around them. This layer does not assume that a small model can reason globally. It assumes a small model can perform narrow tasks well when context, slot, output shape and critic question are precise.


## Subsystem Matrix

| Subsystem | Primary Job | Model Relief | Bus Channels |
| --- | --- | --- | --- |
| Context Distillery | turn broad state into capsule | less prompt mass | #context.distill #context.capsule |
| Worklet Graph | split large tasks | smaller model jobs | #worklet.graph #worklet.node |
| Slot Forge | build exact slot contracts | reduces ambiguity | #slot.forge #slot.contract |
| Predictive Precompute | prepare cheap state early | faster click response | #precompute.route |
| Fit Radar | score route/candidate fit | fewer poor calls | #precompute.fit |
| Mirror Critic Cascade | narrow checks | 3B as critic | #critic.* |
| Seed Weaver | continuity without raw memory | less repeated context | #precompute.seed |
| Candidate Tournament | generate/select/refine | quality without huge model | #candidate.tournament |
| Style Stabilizer | normalize drift | less 7B retry | #critic.style |
| Anti-Generic Engine | force specificity | less bland output | #critic.generic |


## Context Distillery Spec

Context Distillery consumes event digests, selected artifacts, caller manifest, work intent and output contract. It produces compact context capsules. It must prefer short, structured, evidence-linked context over long raw text.

Capsule construction phases:

```text
collect -> filter -> rank -> compress -> bind -> redact -> score -> emit
```

Capsule scoring dimensions:

```text
task_center_clarity
must_use_coverage
must_not_use_precision
privacy_safety
output_shape_fit
model_size_fit
evidence_link_density
```

A low capsule score triggers one of:

```text
ask_app_context
split_work
reduce_scope
route_to_larger_model
cannot_safely_complete
```


## Worklet Graph Spec

Worklet Graph Compiler turns one Universal Work into a DAG of bounded worklets. Worklets must be small enough for smallest-sufficient routing. A worklet may be deterministic, 1B/2B, 3B, 7B/8B, quality, heavy, remote explicit, or no-route.

Worklet types:

```text
extract
classify
compress
route
outline
slot_fill
rewrite
synthesize
critic_check
schema_repair
candidate_merge
candidate_compose
response_wrap
```

Graph constraints:

```text
- no cycles unless explicitly marked iterative with max_rounds
- every model node has slot_contract_ref
- every output node maps to Candidate Artifact or intermediate local_derived artifact
- every high-risk branch has critic node
- every app-action output keeps requires_app_apply_gate true
```


## Slot Forge Spec

Slot Forge produces `ODIN_SLOT_CONTRACT` objects. It considers artifact lens, verb, output contract, current resource profile, model route and semantic pressure.

Slot contract must define:

```text
slot_class
input_budget
output_budget
allowed_models
forbidden_claims
output_schema
fallback_route
repair_policy
critic_policy
claim_boundary
```

A slot is invalid if it requires a model to infer app authority, mutate app state, decide truth, or produce unbounded output.


## Tiny Specialist Modes

Odin treats one 3B model as multiple narrow specialists by slot mode:

```text
3B-Extractor: extract typed facts only
3B-Router: select route from fixed enum
3B-JSON-Repair: repair schema violations only
3B-Claim-Critic: find unsupported claims only
3B-Style-Critic: score tone mismatch only
3B-Context-Compressor: reduce capsule only
3B-Question-Generator: propose missing context questions only
3B-ActionCard-Builder: fill app-native card fields only
3B-Genericness-Critic: detect template-like language only
```

Each mode must have its own prompt/gaptext template, output schema and retry policy. The mode name is never exposed as authority to the app.


## Candidate Tournament

Candidate Tournament is used only when multiple alternatives can improve quality without excessive latency. It is not mandatory for every request.

Tournament modes:

```text
cheap_multi_3b
quality_dual_7b
hybrid_select_refine
merge_best_parts
critic_only_selection
```

Tournament result must record candidate DNA for each candidate and explain why the selected candidate was chosen. It must not hide rejected candidates if the app asked for alternatives.


## Low-Memory Strict Mode

Low-memory strict mode makes weak machines useful. It emphasizes deterministic processing, semantic bus light, small cache, small context windows, 1B/2B/3B micro slots and no heavy local routes.

Route ladder in this mode:

```text
static_template -> decision_table -> event_digest_lookup -> context_capsule -> semantic_script -> shadow_candidate -> gaptext_fill -> 1b/2b_micro -> 3b_micro -> ask_context -> optional_remote_explicit -> cannot_safely_complete
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
