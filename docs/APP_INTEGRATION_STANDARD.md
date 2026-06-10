# App Integration Standard v7.1 — Deep Subsystem Spec

**Spec Status:** v7.1 / v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK.  
**Authority:** build contract for Codex and later implementation work.  
**Claim Boundary:** specification only; no runtime, host, model, security or deployment proof is implied.


## Purpose

App Integration Standard defines how any app connects to Odin while remaining app-sovereign and model-free. Apps must feel AI-native to users without embedding model logic.


## Bridge Files

Every app template should include an `odin/` folder with caller manifest, connector, event digest builder, context snapshot builder, Universal Work builder, candidate renderer, task map and apply gate bridge. These are thin adapters; they do not implement Odin's model routing.


## Task Map

The app task map converts UI actions into Universal Work templates. A button named `Improve` maps to `verb=rewrite`; `Review` maps to `verb=review`; `Suggest` maps to `verb=generate_candidate` or `plan` depending on artifact lens. UI labels should never expose implementation jargon like raw model prompts.


## Candidate Rendering

App renderers must treat all Response Packets as suggestions. Even if a candidate looks complete, the app must keep the apply gate. Candidate actions must be user-visible and app-owned. Odin must never call app mutation functions directly.


## App QIRC Bridge

If an app has its own event bus or QIRC-like system, it provides digest artifacts to Odin. Odin consumes those digests; it does not mirror or own the app event system. Bridge config must define allowed channels, blocked channels, digest mode and privacy class.



## Anchor — No LLM

This section establishes the required anchor `No LLM` for the v0.3.2 deep subsystem spec lock. The anchor is part of the implementation contract and must remain present unless the system map and validation rules are updated in the same change.


## Anchor — Odin Capability Bridge

This section establishes the required anchor `Odin Capability Bridge` for the v0.3.2 deep subsystem spec lock. The anchor is part of the implementation contract and must remain present unless the system map and validation rules are updated in the same change.


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
