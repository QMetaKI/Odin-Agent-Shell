# Data Contracts v7.1 — Deep Subsystem Spec

**Spec Status:** v7.1 / v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK.  
**Authority:** build contract for Codex and later implementation work.  
**Claim Boundary:** specification only; no runtime, host, model, security or deployment proof is implied.


## Contract Philosophy

Every important object in Odin is a contract. Codex must not invent ad hoc JSON shapes in code when a schema or documented contract exists. New structures require schema, registry entry where applicable, tests and System Map update.


## Contract Families

| Family | Objects | Authority |
| --- | --- | --- |
| Caller | Caller Manifest Binding App Pairing | app permissions |
| Work | Universal Work Input Artifact Output Contract | semantic task |
| Precompute | Context Capsule System Profile Worklet Graph Slot Contract | model preparation |
| Bus | Semantic Event Batch Channel Topic Replay | coordination |
| Model | Model Capability Card ModelWorkPacket ModelResponse Minicheck | bounded inference |
| Candidate | Candidate Artifact Candidate DNA Response Packet | app-renderable output |
| Trace | Trace Entry Receipt Candidate Conflict | debug/audit |


## Versioning

All contracts carry `protocol_version`. Minor-compatible changes may add optional fields. Breaking changes require new schema id and registry version. v7.1 implementation should reject unknown required fields and preserve unknown optional metadata only if policy allows.


## Caller Manifest Contract

Required implementation behavior for `Caller Manifest`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Caller Manifest` as a runtime object.


## Binding Contract

Required implementation behavior for `Binding`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Binding` as a runtime object.


## Universal Work Contract

Required implementation behavior for `Universal Work`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Universal Work` as a runtime object.


## Input Artifact Contract

Required implementation behavior for `Input Artifact`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Input Artifact` as a runtime object.


## Output Contract Contract

Required implementation behavior for `Output Contract`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Output Contract` as a runtime object.


## Context Capsule Contract

Required implementation behavior for `Context Capsule`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Context Capsule` as a runtime object.


## Semantic Event Contract

Required implementation behavior for `Semantic Event`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Semantic Event` as a runtime object.


## Worklet Graph Contract

Required implementation behavior for `Worklet Graph`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Worklet Graph` as a runtime object.


## Slot Contract Contract

Required implementation behavior for `Slot Contract`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Slot Contract` as a runtime object.


## ModelWorkPacket Contract

Required implementation behavior for `ModelWorkPacket`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `ModelWorkPacket` as a runtime object.


## Model Response Contract

Required implementation behavior for `Model Response`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Model Response` as a runtime object.


## Minicheck Contract

Required implementation behavior for `Minicheck`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Minicheck` as a runtime object.


## Candidate Artifact Contract

Required implementation behavior for `Candidate Artifact`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Candidate Artifact` as a runtime object.


## Candidate DNA Contract

Required implementation behavior for `Candidate DNA`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Candidate DNA` as a runtime object.


## Response Packet Contract

Required implementation behavior for `Response Packet`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Response Packet` as a runtime object.


## Conflict Contract

Required implementation behavior for `Conflict`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Conflict` as a runtime object.


## Receipt Candidate Contract

Required implementation behavior for `Receipt Candidate`:

```text
- has schema under schemas/v7_1 when persisted or exchanged
- has validation path in odin.cli or subsystem validator
- appears in SYSTEM_MAP if canonical
- has at least one valid example when part of external protocol
- has negative tests for boundary-sensitive fields
- does not allow additional authority by omission
- respects candidate-only and app-authority laws where applicable
```

Codex must implement parser, validator, minimal constructor and error messages before using `Receipt Candidate` as a runtime object.



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
