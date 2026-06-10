# Local API v7.1 — Deep Subsystem Spec

**Spec Status:** v7.1 / v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK.  
**Authority:** build contract for Codex and later implementation work.  
**Claim Boundary:** specification only; no runtime, host, model, security or deployment proof is implied.


## API Boundary

The API is localhost-first. It exposes app registration, protocol message exchange, Universal Work validation/run, semantic bus introspection, trace lookup and scoreboards. It must not expose public network features by default.


## Endpoint Families

| Family | Endpoints | Purpose |
| --- | --- | --- |
| Status | GET /v7/status /health /capabilities | local runtime introspection |
| Apps | POST /v7/apps/register GET /v7/apps | caller pairing |
| Protocol | POST /v7/protocol/* | message/digest/context exchange |
| Universal Work | POST /v7/universal-work/validate|compile|run | core work flow |
| Registries | GET /v7/artifacts/types /verbs /output-contracts | discovery |
| Worklets | POST /v7/worklet-graph/build /slot-forge/build | debug/compile |
| Models | POST /v7/modelworkpacket/build|run | bounded model work |
| Candidates | POST /v7/candidates/* | tournament/compose |
| Bus | GET/POST /v7/bus/* | local semantic bus |
| Trace | GET /v7/trace/{id} | debug |


## Request/Response Rules

All write-like endpoints still produce candidates or internal state changes inside Odin only. No endpoint may mutate an app. App-owned actions are returned as descriptors with `odin_executes=false`.

Every request must include either a binding reference or caller token where appropriate. Sensitive payloads should use content references.



## Anchor — /v7/universal-work/run

This section establishes the required anchor `/v7/universal-work/run` for the v0.3.2 deep subsystem spec lock. The anchor is part of the implementation contract and must remain present unless the system map and validation rules are updated in the same change.


## Anchor — /v7/bus/status

This section establishes the required anchor `/v7/bus/status` for the v0.3.2 deep subsystem spec lock. The anchor is part of the implementation contract and must remain present unless the system map and validation rules are updated in the same change.


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
