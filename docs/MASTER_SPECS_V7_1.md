# Odin Agent Shell — Master Specs v7.1

> **Status:** Architecture/specification canon for the public `Odin-Agent-Shell` repository. Current handoff: v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK. Runtime base: v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK.
> **Claim boundary:** This repository state is a candidate-only handoff and runtime-base canon. It does not claim production readiness, host proof, Windows service/tray/installer proof, model proof, external verification, security certification, external-send proof, app-state mutation proof, or completed runtime behavior.
> **Public language:** neutral terminology. Internal inspiration may come from QIRC/YNode/QFoundation/Q Metamodell/Thor patterns, but the public repo should describe the system as Odin Agent Shell.


## 0. Spec Status

**Spec name:** Odin Agent Shell Master Specs
**Architecture base:** Master Architecture v7.1
**Repository state:** v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK
**Runtime base:** v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
**Historical alignment marker:** v0.7.7 BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK
**Runtime claim:** candidate-only runtime base unless later receipts prove more.
**Implementation target:** REAL-GH-PR-01..08 Codex/GitHub hardening sequence.
**Default route:** 3B + 7B/8B hybrid.
**Core invariant:** every AI-like feature must become Universal Work and every output must be Candidate Artifact.



## 0.8.7 Current Codex/GitHub Handoff Ladder

The current actual Codex/GitHub execution ladder is `REAL-GH-PR-01..REAL-GH-PR-08` in `registries/real_pr_execution_registry.json` and `registries/codex_real_pr_handoff_registry.json`. The v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK is the runtime base for this handoff.

## 0.7.7 Historical Build Execution Ladder Alignment

The historical v0.7.7 BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK established that the actual build execution ladder is `REAL-GH-PR-01..REAL-GH-PR-08` in `registries/real_pr_execution_registry.json`.

`PR-00..PR-123` and `REAL-PR-01..REAL-PR-28` are internal traceability ladders only. They are not independent execution paths.

Every actual GitHub PR now declares:

- absorbed internal tasks
- absorbed legacy bundles
- existing prep paths
- target implementation paths
- acceptance gates
- proof boundaries
- required commands
- invariants to preserve
- Master Architecture section binding

This prevents drift between Master Architecture v7.1, the detailed task ladder, the legacy bundle ladder, and the actual future GitHub PR sequence.

## 0.1 Spec Scope

This document defines data contracts, module contracts, algorithms, failure modes, APIs, storage, gates, tests, SDK expectations, Windows runtime expectations, and Codex implementation constraints for Odin Agent Shell v7.1.

# 1. Repository Contract and Required Files


A valid Odin-Agent-Shell repo must expose these root files:

```text
README.md, START_HERE.md, CODEX_START_HERE.md, AGENTS.md, CANON_ENTRY.md,
SYSTEM_MAP.json, FILE_MANIFEST.json, CLAIM_BOUNDARY.md, SECURITY.md,
pyproject.toml, .github/workflows/ci.yml
```

Required docs:

```text
docs/MASTER_ARCHITECTURE_V7_1.md
docs/MASTER_SPECS_V7_1.md
docs/UNIVERSAL_WORK_KERNEL.md
docs/SMALL_MODEL_POWER_LAYER.md
docs/INTERNAL_SEMANTIC_BUS.md
docs/MODEL_SCALE_LADDER.md
docs/APP_INTEGRATION_STANDARD.md
docs/LOCAL_MEDIATION_PROTOCOL_V7_1.md
docs/API_SPEC.md
docs/WINDOWS_RUNTIME.md
docs/STORAGE_SPEC.md
docs/SECURITY_PRIVACY.md
docs/THOR_INTEGRATION.md
docs/BOUNDED_CODE_WORK.md
docs/TESTING_AND_GATES.md
```

Required directories:

```text
odin/, schemas/v7_1/, registries/, sdk/python/, sdk/typescript/,
templates/app_connector/, tests/, examples/, runtime/
```

The repo root must be flat in ZIP export: no wrapper folder.


# 2. Module Contract Index


Each module must have a narrow role and typed I/O.

| Module | Required class/function surface | Must not do |
|---|---|---|
| universal_work_validator | validate(work, binding, manifest) | call model |
| system_profile_compiler | compile(work, context, resources) | mutate app |
| semantic_bus | publish, subscribe, replay, export | network by default |
| context_distillery | build_capsule | persist raw state by default |
| worklet_graph | build_graph | grant authority |
| slot_forge | forge_slot | hide output contract |
| model_router | select_route | bypass model policy |
| model_work_packet | build_packet | include raw app DB |
| provider_adapter | run_packet | decide truth |
| minicheck | check_response | apply candidate |
| critic_cascade | run_critics | override final gate |
| candidate_composer | compose | execute action |
| final_gate | allow/downgrade/block | ignore claim boundary |


# 3. Universal Work Data Contract

```json
{
  "artifact_kind": "odin_universal_work",
  "protocol_version": "7.1",
  "work_id": "WORK-001",
  "caller_id": "app.example",
  "binding_ref": "OB-001",
  "input_artifacts": [
    {
      "artifact_id": "ART-001",
      "artifact_type": "markdown",
      "content_ref": "ctx_selected_text",
      "trust_status": "caller_provided",
      "privacy_class": "local_only",
      "digest": "sha256..."
    }
  ],
  "work_intent": {
    "verb": "rewrite",
    "mode": "clarity",
    "goal": "improve clarity while preserving meaning"
  },
  "output_contract": {
    "artifact_type": "markdown_candidate",
    "shape": "same_structure",
    "max_tokens": 600,
    "candidate_only": true,
    "requires_app_apply_gate": true
  },
  "constraints": {
    "allowed": [
      "preserve meaning"
    ],
    "forbidden": [
      "invent facts",
      "claim verification",
      "apply directly"
    ]
  },
  "model_policy": {
    "route": "smallest_sufficient",
    "allow_1b_2b": true,
    "allow_3b": true,
    "allow_7b_8b": true,
    "allow_hybrid": true,
    "allow_quality_model": false,
    "allow_heavy_model": false,
    "allow_remote": false
  },
  "claim_boundary": "candidate_projection_only"
}
```


Required validations:

```text
artifact_kind exact, protocol_version compatible, work_id unique per caller,
caller_id registered, binding valid, artifact types known, privacy allowed,
verb allowed, output contract allowed, model policy within manifest,
constraints not empty for generative work, candidate_only true, claim boundary present.
```


# 4. Caller Manifest Contract

```json
{
  "schema": "odin.caller_manifest.v7_1",
  "caller_id": "my_app",
  "caller_type": "app",
  "display_name": "My App",
  "allowed_input_artifact_types": [
    "markdown",
    "event_digest"
  ],
  "allowed_transformation_verbs": [
    "summarize",
    "rewrite",
    "review"
  ],
  "allowed_output_artifact_types": [
    "markdown_candidate",
    "review_summary_candidate"
  ],
  "blocked_output_artifact_types": [
    "direct_apply"
  ],
  "blocked_task_classes": [
    "apply_changes",
    "send_external",
    "mutate_project"
  ],
  "privacy_default": "local_only",
  "model_policy": {
    "default_route": "smallest_sufficient",
    "allow_1b_2b": true,
    "allow_3b": true,
    "allow_7b_8b": true,
    "allow_hybrid": true,
    "allow_quality_model": false,
    "allow_heavy_model": false,
    "allow_remote": false
  },
  "semantic_bus_policy": {
    "allow_internal_bus": true,
    "allow_app_qirc_bridge_digest": true,
    "allow_full_event_mirror": false
  },
  "claim_policy": {
    "candidate_only": true,
    "forbidden_claims": [
      "runtime_verified",
      "tests_passed",
      "production_ready",
      "security_verified",
      "apply_performed"
    ]
  }
}
```


Manifest is the first app boundary. If the manifest does not allow a route, Odin cannot use that route even if the local host could technically run it.


# 5. Binding Contract

```json
{
  "artifact_kind": "odin_binding",
  "protocol_version": "7.1",
  "binding_id": "OB-001",
  "caller_id": "app.example",
  "request_id": "REQ-001",
  "caller_manifest_ref": "manifest.app.example",
  "privacy_class": "local_only",
  "allowed_outputs": [
    "assistant_message_candidate",
    "action_card_candidate"
  ],
  "forbidden_actions": [
    "apply_changes",
    "send_external",
    "mutate_project"
  ],
  "app_authority": "app_retains_state_apply_and_external_actions",
  "odin_authority": "local_llm_processing_only",
  "model_authority": "projection_worker_only",
  "semantic_bus_authority": "coordination_only_no_app_mutation",
  "claim_boundary": "candidate_projection_only"
}
```


Binding validity must be checked before bus publication, precompute, or model routing.


# 6. Artifact Type Contract


Each artifact type registry entry must define:

```text
id, family, accepted content refs, privacy default, allowed trust statuses,
lens candidates, allowed verbs, blocked verbs, maximum inline size,
remote eligibility default, trace redaction policy.
```

Content should be referenced where possible. Large payloads go to object store and are represented by digest + ref.

Unknown artifact type is a hard validation failure.


# 7. Artifact Lens Contract


Each lens must define:

```text
lens_id, artifact_families, focus_fields, ignore_fields, typical_verbs,
typical_output_contracts, risk_axes, preferred_slot_classes,
preferred_model_routes, semantic_bus_channels, cache_strategy,
context_distillation_rules, critic_axes, privacy_constraints.
```

Lens selection algorithm:

```text
1. Collect input artifact families.
2. Collect verb and output contract.
3. Match required and preferred lenses.
4. Reject conflicting lenses unless system profile defines priority.
5. Publish #lens.select event.
6. Attach active_lenses to Candidate DNA.
```


# 8. Verb Registry Contract


Each verb registry entry must define:

```text
verb, verb_class, allowed_input_families, typical_output_families,
default_precompute_depth, default_model_route, risk_profile,
required_constraints, forbidden_output_classes, critic_requirements.
```

Verb compatibility:

```text
artifact family must support verb
caller must allow verb
output contract must match verb class
risk profile must not exceed caller policy without escalation
```


# 9. Output Contract Contract


Output contract required fields:

```text
contract_id, artifact_type, schema_ref or shape, render_target,
candidate_only true, requires_app_apply_gate when action-impacting,
max_tokens or size policy, forbidden_claims, status_requirements,
privacy requirements, trace requirement, render hints.
```

Invalid if:

```text
candidate_only false, direct apply requested, external send requested,
forbidden_claims missing, trace requirement missing, artifact type blocked by caller.
```


# 10. System Profile Compiler Spec


Inputs:

```text
caller manifest, binding, universal work, event digest, context snapshot,
privacy class, resource pressure, model policy, semantic bus mode.
```

Outputs:

```text
intent_family, artifact_route, verb_route, required capabilities, standard surfaces,
precompute_depth, Thor mode, model route, claim boundary, fallback policy,
semantic bus batch requirements, active lens candidates, critic requirements.
```

Algorithm:

```text
1. Start with binding and manifest limits.
2. Resolve artifact + verb + output contract.
3. Determine risk and semantic pressure.
4. Select intent family.
5. Select active lenses.
6. Select precompute depth.
7. Decide if Thor bridge needed.
8. Build allowed model route set.
9. Select default route via Model Scale Ladder.
10. Emit system profile and bus event.
```


# 11. Internal Semantic Bus Spec


Bus must support:

```text
publish(event), subscribe(channel, handler), open_batch(work_id), close_batch(batch_id),
replay(work_id), list_channels(), list_events(filter), export_trace(work_id),
validate_event(event), redact_event(event).
```

Bus cannot support by default:

```text
WAN bind, LAN bind, public rooms, arbitrary external clients, app mutation events,
full app event mirroring, secret-bearing topics, final gate bypass.
```

Event envelope is required for every bus message. Events without event_id, channel, event_type, trace_id, privacy_class when context-bearing, or work_id when work-related are invalid.

Channel registry must be data-driven and local_only true for all default channels.


# 12. Context Distillery Spec


Context Distillery must implement:

```text
build_capsule(work, event_digest, active_lenses, output_contract, privacy_policy)
```

Output capsule fields:

```text
capsule_id, work_id, task_center, must_use, must_not_use, style/tone,
length/shape, allowed, forbidden, claim_boundary, source_refs,
omitted_context, open_questions, confidence, privacy_class.
```

Quality checks:

```text
If must_use is empty for specificity-critical generation, ask context or route generic warning.
If context exceeds budget, run Semantic Pressure Valve.
If privacy class is blocked_sensitive, block before model route.
```


# 13. Worklet Graph Spec


Worklet graph builder must split complex work into bounded nodes.

Node fields:

```text
node_id, worklet_type, input_refs, output_kind, preferred_route,
slot_class, dependencies, risk_profile, fallback, gate_requirements,
critic_requirements.
```

Edge types:

```text
feeds_context, blocks_until, critic_of, refines, composes_into,
requires_review, fallback_from.
```

A graph is required when semantic pressure exceeds threshold, output contract is composite, task has multiple artifacts, or caller requests candidate bundles.


# 14. Slot Forge Spec


Slot Forge input:

```text
worklet, artifact lens, output contract, model profile, resource profile,
semantic bus state, claim boundary.
```

Slot contract output fields:

```text
slot_id, slot_class, input_artifact_types, transformation_verb,
output_contract_ref, allowed_models, max_input_tokens, max_output_tokens,
output_schema, forbidden_claims, fallback, guard_policy, receipt_policy,
retry_policy.
```

Slot Forge must lower token budget for 3B micro routes and require stricter output shapes for schema-sensitive slots.


# 15. Model Route Spec


Route selection inputs:

```text
resource profile, latency mode, task risk, output quality target,
model policy, privacy class, context size, cache availability,
active model profiles, route history, work memory.
```

Route order:

```text
static → decision table → pattern rule → event lookup → meaning frame →
semantic script → shadow candidate → blueprint fill → gaptext fill →
1B/2B → 3B micro → 3B multi → 7B/8B → 3B+7B/8B hybrid →
quality hybrid → heavy local → max local batch → remote explicit → cannot complete.
```

The default sweet spot is 3B + 7B/8B hybrid for standard_local and quality interactive flows.


# 16. Provider Adapter Spec


Provider adapter interface:

```python
class OdinProvider:
    provider_id: str
    def list_models(self) -> list[ModelInfo]: ...
    def health(self) -> ProviderHealth: ...
    def run_packet(self, packet: OdinModelWorkPacket) -> OdinModelResponse: ...
    def estimate_resources(self, model_id: str, context_tokens: int) -> ResourceEstimate: ...
```

Provider must not receive app authority. Provider receives ModelWorkPacket only. Provider output remains model_projection until gates promote it to candidate artifact.


# 17. ModelWorkPacket Spec

```json
{
  "artifact_kind": "odin_model_work_packet",
  "protocol_version": "7.1",
  "packet_id": "MWP-001",
  "binding_ref": "OB-001",
  "work_id": "WORK-001",
  "slot_contract_ref": "slot_001",
  "model_route": "3b_micro",
  "task": "fill_bounded_slot",
  "input_artifact_refs": [],
  "output_contract_ref": "OUT-001",
  "context_frame": {},
  "context_capsule_ref": "CAP-001",
  "event_digest_ref": "EVTD-001",
  "semantic_bus_batch_ref": "BATCH-001",
  "facts": [],
  "constraints": [],
  "allowed": [],
  "forbidden": [],
  "output_schema": {},
  "gaptext": "string",
  "return_contract": {},
  "fallback_policy": "string",
  "claim_boundary": "model_output_projection_only"
}
```


Invalid if binding missing, work_id missing, slot missing, route not allowed, output schema missing for schema task, forbidden claims missing, claim boundary missing, context exceeds slot budget, or raw app state included without permission.


# 18. Minicheck and Critic Spec


Minicheck output fields:

```text
schema_status, claim_hits, missing_evidence, forbidden_output_hits,
return_contract_violations, critic_reports, recommended_route, claim_boundary.
```

Critic report fields:

```text
critic_id, critic_type, candidate_ref, score, findings, blocked_claims,
repair_suggestion, route_recommendation, confidence.
```

Critic cascade required for: action-impacting outputs, code candidates, claim-sensitive outputs, public-facing content, app bridge candidates, any output with high genericness risk.


# 19. Candidate Composition Spec


Candidate Composer input:

```text
model responses, deterministic worklet outputs, critic reports, fit score,
output contract, render target, candidate DNA data, warnings.
```

Composer must output app-native candidate artifacts, not raw model responses. Candidate actions must be app-owned actions and declare `odin_executes=false`.


# 20. Final Gate Spec


Final Gate actions:

```text
allow_candidate, downgrade_language, require_evidence, ask_app_context,
retry, escalate, block.
```

Gate checks:

```text
candidate_only, output contract, claim boundary, privacy class, blocked claims,
forbidden action, schema validity, trace presence, candidate DNA, model route policy,
semantic bus authority, app ownership of apply.
```

Final Gate is mandatory even for cached responses.


# 21. Storage Spec


SQLite must store typed records for manifests, bindings, event digests, context capsules, universal works, candidates, candidate DNA, worklet graphs, slots, model runs, critic reports, bus events, replays, profiles, settings.

Object store must hold large artifacts, compressed context, support bundles, trace exports, bus replays, payloads.

Retention policies:

```text
raw app payload: default no persistence
bus events: short retention unless trace export
candidate artifacts: configurable retention
model responses: configurable and redacted
support bundles: manual export only
```


# 22. API Spec Summary


All default HTTP APIs bind to localhost. Remote access is not a default feature.

Endpoint families:

```text
status/health/capabilities
apps register/list/revoke
protocol message/event/context
universal work validate/compile/run
registries artifacts/lenses/verbs/output-contracts
worklet graph and slot forge
model work packet build/run
candidate tournament/critic/compose
minicheck/response compile
model dojo
semantic bus status/start/stop/channels/events/replay/export
trace and scoreboard
```

Every write endpoint must validate capability token, caller manifest, and local policy.


# 23. Control Center Spec


Control Center panels must be diagnostic and app-safe. It may inspect Odin internals; it may not mutate app state.

Panel requirements:

```text
Home: daemon, bus, provider, route status
Apps: manifests, bindings, permissions
Models: providers, capability cards, resource estimates
Universal Work Lab: validate/compile/run mock work
Worklet Graph Lab: graph nodes and edges
Internal Semantic Bus: channels/events/batches/replay
Artifact Registry: types and lenses
Candidate Tournament: variants and scores
Model Dojo: local profile tests
Scoreboard: route metrics
Traces: replay and export
Security/Privacy: remote policy, retention, redaction
Support Bundle: export local diagnostic bundle
```


# 24. SDK and Template Spec


Templates must not contain model logic. They must contain bridges only.

Required templates:

```text
generic_http, typescript, python, wordpress, godot, electron, tauri, generic_cli
```

SDKs must expose:

```text
register_app, get_status, build_event_digest, build_context_snapshot,
build_universal_work, send_work, handle_context_request,
receive_response_packet, render_candidate, handle_conflict.
```

App UX should use domain labels like Improve/Summarize/Suggest/Review/Draft/Explain, not “run LLM”.


# 25. Testing and Gate Spec


Required tests:

```text
JSON schema validity, registry shape, system map links, doc anchors,
no positive overclaim scan, Universal Work valid/invalid, semantic event valid/invalid,
model ladder default and escalations, candidate-only gate, app manifest gate,
semantic bus local-only, app QIRC digest-only, no-LLM-in-app template scan,
cache cannot bypass final gate, low-memory strict route.
```

Acceptance gates A–N are binding and should be implemented in CI as the repo matures.


# 26. Codex Build Rules


Codex must implement from the canon outward:

```text
schemas + registries → validators → Universal Work Kernel → Semantic Bus →
Small Model Power → Model Runtime → Candidate/Gates → API → Control Center → SDKs.
```

Codex must preserve:

```text
No LLM in app, candidate-only output, local-first default,
semantic bus local-only, model scale ladder, 3B+7B/8B sweet spot,
app-owned apply, claim/evidence boundary.
```

Codex must not silently add: public network bus, app mutation, remote fallback, direct apply, or positive runtime claims.


# 27. Definition of Done for Spec Completeness


For a subsystem spec to be complete enough for Codex, it must define:

```text
purpose, inputs, outputs, data shape, lifecycle, failure modes,
validation rules, storage implications, bus events, API touchpoints,
security/privacy constraints, tests, negative tests, and acceptance gate relation.
```

v0.7.7 BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK requires the master docs, subsystem docs and actual execution ladder to include those items at architecture level. Implementation-level details may still be refined during Codex build, but authority boundaries and data contracts must not be reinterpreted.


# Appendices — Spec Matrices


## Data Object Required Fields

| Object | Required Fields |
|---|---|
| Universal Work | artifact_kind, protocol_version, work_id, caller_id, binding_ref, input_artifacts, work_intent, output_contract, constraints, model_policy, claim_boundary |
| Semantic Event | artifact_kind, protocol_version, event_id, channel, event_type, source_module, trace_id, privacy_class, payload |
| Candidate Artifact | candidate_id, candidate_type, work_id, caller_id, content, actions, candidate_dna_ref, claim_status, evidence_status, trace_id |
| ModelWorkPacket | packet_id, binding_ref, work_id, slot_contract_ref, model_route, output_contract_ref, context_capsule_ref, gaptext, claim_boundary |
| Response Packet | response_id, request_id, work_id, caller_id, response_kind, candidates, trace_id, claim_boundary |


## Failure-to-Route Matrix

| Failure | Route |
|---|---|
| binding invalid | block |
| privacy denied | block |
| context too broad | semantic_pressure_valve |
| schema invalid | repair_schema_3b |
| claim hit | downgrade_or_block |
| model unavailable | fallback_ladder |
| remote blocked | local_or_cannot_complete |
| app context missing | context_request |


## Acceptance Gate Implementation Hint

| Gate | Implementation Hook |
|---|---|
| Universal Work | universal_work_validator |
| No LLM in App | template scanner |
| App Boundary | binding/final_gate |
| ModelWorkPacket | packet validator |
| Small Model Power | doc/tests + module invariants |
| Semantic Bus | event validator |
| App QIRC Bridge | bridge digest validator |
| Candidate Output | candidate validator |
| Claim/Evidence | claim scanner/final gate |
| Model Scale Ladder | model_router |


# Deep Spec Appendix — Module-by-Module Build Contracts


## M.1 `caller_manifest.py`


**Required functions/classes:** `load_manifest, validate_manifest, enforce_manifest_limits`
**Inputs:** caller manifest json.
**Outputs:** validated manifest or errors.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.2 `binding.py`


**Required functions/classes:** `create_binding, validate_binding`
**Inputs:** manifest + request.
**Outputs:** binding object.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.3 `universal_work_validator.py`


**Required functions/classes:** `validate_universal_work, compile_universal_work`
**Inputs:** Universal Work.
**Outputs:** CompiledWork.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.4 `artifact_lenses.py`


**Required functions/classes:** `select_lenses, validate_lens_compatibility`
**Inputs:** artifacts + verb.
**Outputs:** active lenses.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.5 `system_profile_compiler.py`


**Required functions/classes:** `compile_system_profile`
**Inputs:** work + resources + policy.
**Outputs:** system profile.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.6 `semantic_bus/bus.py`


**Required functions/classes:** `start, stop, publish, subscribe, open_batch, replay`
**Inputs:** semantic events.
**Outputs:** bus status/events.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.7 `context_distillery.py`


**Required functions/classes:** `build_context_capsule`
**Inputs:** work + digest + lenses.
**Outputs:** context capsule.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.8 `worklet_graph.py`


**Required functions/classes:** `build_graph, validate_graph`
**Inputs:** compiled work.
**Outputs:** worklet graph.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.9 `slot_forge.py`


**Required functions/classes:** `forge_slot, validate_slot`
**Inputs:** worklet + route.
**Outputs:** slot contract.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.10 `model_router.py`


**Required functions/classes:** `select_route, explain_route`
**Inputs:** slot + resources + policy.
**Outputs:** route plan.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.11 `model_work_packet.py`


**Required functions/classes:** `build_packet, validate_packet`
**Inputs:** slot + capsule.
**Outputs:** ModelWorkPacket.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.12 `provider adapters`


**Required functions/classes:** `list_models, health, run_packet`
**Inputs:** ModelWorkPacket.
**Outputs:** ModelResponse.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.13 `return_minicheck.py`


**Required functions/classes:** `check_response`
**Inputs:** ModelResponse.
**Outputs:** Minicheck.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.14 `critic_cascade.py`


**Required functions/classes:** `run_critics`
**Inputs:** candidate draft.
**Outputs:** critic reports.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.15 `candidate_tournament.py`


**Required functions/classes:** `run_tournament`
**Inputs:** candidate set.
**Outputs:** ranked candidates.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.16 `candidate_artifact_builder.py`


**Required functions/classes:** `build_candidate`
**Inputs:** outputs + reports.
**Outputs:** CandidateArtifact.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.17 `response_packet.py`


**Required functions/classes:** `build_response_packet`
**Inputs:** candidate bundle.
**Outputs:** ResponsePacket.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.18 `final_gate.py`


**Required functions/classes:** `evaluate_candidate`
**Inputs:** candidate + DNA.
**Outputs:** allow/downgrade/block.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.19 `sqlite_store.py`


**Required functions/classes:** `save/load/query`
**Inputs:** typed records.
**Outputs:** persisted records.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.


## M.20 `api/routes.py`


**Required functions/classes:** `http endpoints`
**Inputs:** requests.
**Outputs:** responses.


```text
Preconditions:
- schema-valid input
- caller/binding policy checked if app-facing
- privacy class known
- trace context available

Postconditions:
- typed output or explicit error list
- no app mutation
- no direct external send
- trace event emitted when work-related
- final gate remains required for candidate output
```


**Unit tests required:** valid case, invalid schema case, policy failure, privacy failure, trace emission.



# Deep Spec Appendix — Validation Rules Catalog


## Rule: Manifest

caller_id unique; model policy not broader than global policy; remote default blocked; no app full event mirror by default.


## Rule: Binding

manifest exists; privacy allowed; forbidden actions listed; claim boundary present.


## Rule: Universal Work

artifact types known; verb allowed; output candidate-only; model policy within manifest.


## Rule: Artifact

trust status known; privacy class known; digest required for referenced content.


## Rule: Lens

lens family matches artifact; no conflicting required lens unless priority exists.


## Rule: Output Contract

candidate_only true; direct apply blocked; trace/status requirements present.


## Rule: Semantic Event

event_id/channel/event_type/source/trace/privacy valid; channel local_only.


## Rule: Worklet Graph

acyclic unless explicit loop node allowed; all dependencies exist; outputs typed.


## Rule: Slot Contract

slot class known; model route allowed; token budgets set; forbidden claims set.


## Rule: ModelWorkPacket

no raw app DB; gaptext present; output contract present; claim boundary present.


## Rule: Model Response

schema parse or repair route; output not trusted; route metadata present.


## Rule: Candidate Artifact

candidate DNA ref present; app action only; Odin executes false.


## Rule: Response Packet

candidate bundle renderable; trace id present; warnings explicit.


## Rule: Cache

cache hit still passes final gate; cache key includes policy-relevant hashes.


## Rule: Remote

explicitly allowed by manifest and policy; privacy eligible; user/host setting permits.



# Deep Spec Appendix — API Request/Response Families


## Endpoint `/v7/status`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/health`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/capabilities`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/apps/register`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/protocol/event-digest`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/universal-work/validate`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/universal-work/compile`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/universal-work/run`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/worklet-graph/build`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/slot-forge/build`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/modelworkpacket/build`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/modelworkpacket/run`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/candidates/tournament`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/candidates/critic-cascade`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/response/compile`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/bus/status`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/bus/start`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/bus/stop`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/bus/events`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/bus/replay/{work_id}`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/trace/{trace_id}`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```


## Endpoint `/v7/scoreboard`


```text
Default bind: localhost
Auth: local capability token for write endpoints
Input: typed JSON object where applicable
Output: typed JSON response or structured error
Must log: trace id, caller id when applicable, decision status
Must not: expose WAN/LAN by default or mutate app state
```



# Deep Spec Appendix — Definition-of-Done Matrix


- schema exists

- registry entry exists if applicable

- validator implemented

- positive test

- negative test

- trace event

- claim boundary

- privacy class

- docs updated

- system map updated

- file manifest updated

- no app mutation

- no direct external send

- final gate relation



# Deep Spec Appendix — Object-Level Field Specifications

## Object `OdinCallerManifest`

**Required/important fields:**

- `schema`
- `caller_id`
- `caller_type`
- `display_name`
- `allowed_input_artifact_types`
- `allowed_transformation_verbs`
- `allowed_output_artifact_types`
- `blocked_task_classes`
- `privacy_default`
- `model_policy`
- `state_policy`
- `event_digest_policy`
- `semantic_bus_policy`
- `remote_policy`
- `claim_policy`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinBinding`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `binding_id`
- `caller_id`
- `request_id`
- `caller_manifest_ref`
- `privacy_class`
- `allowed_outputs`
- `forbidden_actions`
- `app_authority`
- `odin_authority`
- `model_authority`
- `semantic_bus_authority`
- `claim_boundary`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinEventDigest`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `event_digest_id`
- `caller_id`
- `work_hint`
- `state_digest`
- `summary`
- `recent_events`
- `privacy_class`
- `created_at`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinContextRequest`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `request_id`
- `caller_id`
- `work_id`
- `needed_context`
- `reason`
- `privacy_class`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinContextResponse`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `response_id`
- `request_ref`
- `caller_id`
- `artifacts`
- `privacy_class`
- `declined`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinUniversalWork`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `work_id`
- `caller_id`
- `binding_ref`
- `input_artifacts`
- `work_intent`
- `output_contract`
- `constraints`
- `model_policy`
- `claim_boundary`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinInputArtifact`

**Required/important fields:**

- `artifact_id`
- `artifact_type`
- `content_ref`
- `trust_status`
- `privacy_class`
- `digest`
- `inline_content_optional`
- `metadata`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinOutputContract`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `contract_id`
- `artifact_type`
- `schema_ref`
- `render_target`
- `candidate_only`
- `requires_app_apply_gate`
- `max_tokens`
- `forbidden_claims`
- `status_requirements`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinSemanticEvent`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `event_id`
- `channel`
- `event_type`
- `source_module`
- `source_ring`
- `work_id`
- `trace_id`
- `state_digest`
- `privacy_class`
- `payload`
- `requires_receipt`
- `created_at`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinWorkletGraph`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `graph_id`
- `work_id`
- `bus_batch_ref`
- `nodes`
- `edges`
- `claim_boundary`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinSlotContract`

**Required/important fields:**

- `slot_id`
- `slot_class`
- `input_artifact_types`
- `transformation_verb`
- `output_contract_ref`
- `allowed_models`
- `max_input_tokens`
- `max_output_tokens`
- `output_schema`
- `forbidden_claims`
- `fallback`
- `guard_policy`
- `receipt_policy`
- `retry_policy`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinModelWorkPacket`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `packet_id`
- `binding_ref`
- `work_id`
- `slot_contract_ref`
- `model_route`
- `task`
- `input_artifact_refs`
- `output_contract_ref`
- `context_frame`
- `context_capsule_ref`
- `event_digest_ref`
- `semantic_bus_batch_ref`
- `facts`
- `constraints`
- `allowed`
- `forbidden`
- `output_schema`
- `gaptext`
- `return_contract`
- `fallback_policy`
- `claim_boundary`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinModelResponse`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `response_id`
- `packet_ref`
- `model_id`
- `provider`
- `raw_output_ref`
- `parsed_output`
- `latency_ms`
- `token_counts`
- `finish_reason`
- `claim_status`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinMinicheck`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `minicheck_id`
- `checked_response_ref`
- `schema_status`
- `claim_hits`
- `missing_evidence`
- `forbidden_output_hits`
- `return_contract_violations`
- `critic_reports`
- `recommended_route`
- `claim_boundary`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinCriticReport`

**Required/important fields:**

- `critic_id`
- `critic_type`
- `candidate_ref`
- `score`
- `findings`
- `blocked_claims`
- `repair_suggestion`
- `route_recommendation`
- `confidence`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinCandidateArtifact`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `candidate_id`
- `candidate_type`
- `work_id`
- `caller_id`
- `content`
- `render_hints`
- `actions`
- `candidate_dna_ref`
- `claim_status`
- `evidence_status`
- `blocked_claims`
- `warnings`
- `trace_id`
- `requires_app_apply_gate`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinCandidateDNA`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `candidate_dna_id`
- `candidate_id`
- `input_artifact_refs`
- `event_digest_ref`
- `system_profile_ref`
- `active_lenses`
- `active_seeds`
- `semantic_bus_batch_ref`
- `worklet_graph_ref`
- `slot_refs`
- `model_routes`
- `critic_reports`
- `fit_score_ref`
- `claim_boundary`
- `cache_hits`
- `fallbacks`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinResponsePacket`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `response_id`
- `request_id`
- `work_id`
- `caller_id`
- `response_kind`
- `candidates`
- `status_chips`
- `warnings`
- `next_actions`
- `blocked_claims`
- `claim_status`
- `evidence_status`
- `trace_id`
- `receipt_candidate_id`
- `claim_boundary`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinReceiptCandidate`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `receipt_candidate_id`
- `source_ref`
- `claim`
- `evidence_refs`
- `status`
- `trace_id`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.

## Object `OdinConflict`

**Required/important fields:**

- `artifact_kind`
- `protocol_version`
- `conflict_id`
- `caller_id`
- `work_id`
- `reason`
- `recoverable`
- `recommended_action`
- `trace_id`

**Validation expectations:**

```text
- reject unknown or missing required authority fields
- reject privacy class violations
- reject app mutation attempts from Odin/model side
- require trace link for work-related objects
- require candidate-only status for app-facing outputs
- preserve schema version compatibility
```

**Test obligations:** valid example, missing field, invalid enum, boundary violation, serialization roundtrip.


# Deep Spec Appendix — Subsystem Failure Modes

## Failure `manifest_missing`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `binding_invalid`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `artifact_unknown`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `privacy_denied`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `verb_forbidden`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `output_contract_invalid`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `context_too_broad`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `resource_pressure_high`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `model_unavailable`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `provider_timeout`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `schema_invalid`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `claim_boundary_hit`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `genericness_high`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `style_drift_high`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `bus_unavailable`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `bus_event_invalid`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `cache_stale`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `remote_blocked`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `app_context_needed`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```

## Failure `candidate_blocked`

```text
Detection:
- validator or runtime module emits structured failure
Recovery:
- retry, repair, ask context, split work, downgrade, escalate within policy, block, or cannot complete
Trace:
- write trace entry with reason code
User/app visibility:
- return conflict or response warning when app-facing
Forbidden recovery:
- no silent remote, no app mutation, no final gate bypass
```


# Deep Spec Appendix — Per-Subsystem Test Matrix

## Tests for Universal Work Kernel

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Caller Manifest

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Binding

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Artifact Registry

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Lens Router

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Verb Registry

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Output Contracts

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for System Profile Compiler

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Semantic Bus

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Context Distillery

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Worklet Graph

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Slot Forge

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Model Router

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Provider Adapter

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for ModelWorkPacket

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Minicheck

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Critic Cascade

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Candidate Tournament

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Candidate Composer

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Final Gate

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Storage

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for API

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for Control Center

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```

## Tests for SDK Templates

```text
Positive:
- valid minimal object
- valid rich object
- expected trace/event emission
Negative:
- missing required field
- invalid enum/type
- policy boundary violation
- forbidden claim/action
- privacy mismatch
Regression:
- schema/registry parity
- serialization roundtrip
- deterministic reason code where applicable
```


# Deep Spec Appendix — Codex PR Granularity

## PR Package 1: Canon gates

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 2: Schema validators

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 3: Universal Work

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 4: Semantic Bus

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 5: Context and lenses

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 6: Worklets and slots

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 7: Model route ladder

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 8: Provider mock/Ollama/llama.cpp

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 9: Minicheck and critics

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 10: Candidate artifacts

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 11: Final gate

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 12: API

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 13: Control center shell

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 14: SDKs/templates

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```

## PR Package 15: E2E examples

```text
Files touched:
- module code
- docs
- schemas/registries if needed
- tests
Definition of done:
- validation passes
- unit tests pass
- negative tests added
- no claim boundary regression
- no app authority regression
```


# Deep Spec Appendix — Minimal Valid Examples Required for Future Build

Every canonical object must eventually have at least one valid JSON example and one invalid JSON example. The valid example proves serialization and base validation. The invalid example proves the gate fails closed. Examples should live under `examples/` and be referenced by tests.

Required example families:

```text
examples/universal_work/*.valid.json
examples/universal_work/*.invalid.json
examples/semantic_bus/*.valid.json
examples/semantic_bus/*.invalid.json
examples/candidates/*.valid.json
examples/model_work_packets/*.valid.json
examples/app_manifests/*.valid.json
examples/app_qirc_bridge/*.valid.json
examples/failures/*.invalid.json
```

# Deep Spec Appendix — Full-Spec Lock Interpretation

`FULL_SPEC_LOCK` means that Codex should not reinterpret the architecture from scratch. It may refine implementation details, add algorithms, split modules, and improve tests, but it must preserve all hard laws:

```text
No LLM in App
Universal Work Law
Candidate Law
App Authority Law
Smallest Sufficient Worker Law
Semantic Bus Law
Universal but Bounded Law
```

Any change that weakens those laws requires an explicit architecture change document, updated tests, updated registries, and a reasoned migration note.

# Compatibility Anchor — Repository Layout Spec

This FULL_SPEC_LOCK keeps the Repository Layout Spec as binding through the root file list, required docs, required directories, SDK/template directories, schemas, registries, tests and runtime folders defined above.

# Compatibility Anchor — Acceptance Gates

Acceptance Gates are binding: Universal Work, No LLM in App, App Boundary, ModelWorkPacket, Small Model Power, Internal Semantic Bus, App QIRC Bridge Safety, Candidate Output, Claim/Evidence, Windows Usability, Model Scale Ladder, Schema/Registry Parity, Trace/Replay, Low-Memory Strict.

# Compatibility Anchor — Semantic Cache

Semantic Cache remains a core subsystem and includes caller_manifest_cache, event_digest_cache, context_capsule_cache, system_profile_cache, artifact_lens_cache, seed_resolution_cache, fit_score_cache, worklet_graph_cache, slot_plan_cache, gaptext_cache, model_output_cache, critic_report_cache, semantic_bus_batch_cache and response_packet_cache.


# v0.3.2 Deep Subsystem Spec Lock Addendum

This master document is the canonical architecture/spec authority. The subsystem documents listed below are not optional notes; they are binding expansions of the same canon and must be read together with this master document:

```text
DATA_CONTRACTS_V7_1.md
ALGORITHMS_V7_1.md
FLOW_CATALOG_V7_1.md
IMPLEMENTATION_DOD_V7_1.md
UNIVERSAL_WORK_KERNEL.md
INTERNAL_SEMANTIC_BUS.md
SMALL_MODEL_POWER_LAYER.md
MODEL_SCALE_LADDER.md
APP_INTEGRATION_STANDARD.md
LOCAL_MEDIATION_PROTOCOL_V7_1.md
API_SPEC.md
STORAGE_SPEC.md
SECURITY_PRIVACY.md
WINDOWS_RUNTIME.md
THOR_INTEGRATION.md
BOUNDED_CODE_WORK.md
TESTING_AND_GATES.md
```

Codex must treat contradictions by this order: CANON_ENTRY -> MASTER_ARCHITECTURE -> MASTER_SPECS -> DATA_CONTRACTS -> ALGORITHMS -> FLOW_CATALOG -> IMPLEMENTATION_DOD -> subsystem docs -> registries -> code skeletons. When a subsystem document is more specific and does not contradict the master, it controls implementation detail.

# v0.4.2 Senior Review Spec Lock

## Additional Spec Requirement

Every implementation PR must include a traceability summary linking code changes to:

```text
Master Architecture section
Master Specs section
Subsystem spec
Internal PR task
Real PR bundle
Schemas/registries changed
Tests/gates changed
Invariants preserved
```

## Additional Validation Surface

The repository must validate senior review hardening through:

```text
validate-senior-review
validate-all
pytest
```

## Required New Internal Task

```text
PR-22 Senior Review Hardening and Anti-Drift Lock
```

PR-22 is included in REAL-PR-08.

## Required Red Lines

```text
Semantic Bus cannot mutate app state.
Semantic Bus cannot become network feature by default.
Larger models cannot become default route.
Remote cannot become default route.
Candidate outputs cannot be labeled as applied outputs.
Support bundles cannot export raw payloads by default.
```


# v0.5.0 Shadow Runtime Lock Addendum

Odin Agent Shell v7.1 now includes a code-near Shadow Runtime layer. This layer is non-executing and non-authoritative. It exists to make Codex implementation nearly mechanical by mapping contracts to shadow types, functions, fixtures, tests and future real target files. It is inspired by the YNode-prep Shadow Runtime discipline while remaining Odin-neutral and scoped to Universal Work, Candidate Artifacts, Internal Semantic Bus, Small Model Power, Model Scale Ladder and app-owned apply boundaries. The canonical task is PR-23 and the real Codex bundle is REAL-PR-09. Any future architecture-to-code mapping change must update the Shadow Runtime package, docs, fixtures, registries, tests, internal PR ladder and real PR bundle layer.


---

## v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE

This release extends the Shadow Runtime from central spine coverage to full major-subsystem coverage. Every future addition must update the architecture/specs, internal PR ladder, REAL-PR bundles, registries, System Map, tests and FILE_MANIFEST. The Shadow Runtime remains candidate-only, local-only, non-authoritative and non-executing.

New coverage includes Artifact Lenses, Context Distillery, Worklet/Slot/Gaptext, Candidate Tournament, Low-Memory Strict Mode, Thor Bridge, Bounded Code Work, Storage/Trace/Receipt, Local API, App-QIRC Digest Bridge, Model Dojo, Security Redaction, Support Bundle, Windows Runtime and SDK/App Template validation.

# v0.5.2 Shadow Runtime Near-Final Spec Addendum

The canonical near-final shadow entrypoint is `run_near_final_shadow_runtime`. Its output is now part of the build contract for Codex. Every real module derived from it must keep the following invariants: candidate-only output, app-owned apply, app-owned state, semantic bus local-only, provider calls through ModelWorkPackets, remote explicit opt-in, resource-based route ceilings and final-gate preservation.


---

# Integrated v7.1 Narrative Aorta / Y* Compiler Layer

This section integrates the Fairy/Y* Narrative Aorta and Shadow Runtime Compiler Prelude into the existing v7.1 architecture without replacing v7.1 runtime semantics.

## Preservation Statement

Odin v7.1 remains the functional architecture. Apps still contain no LLM runtime, apps still send Universal Work Objects, Odin still returns Candidate Artifacts, and apps still own state, apply and external sends. The Narrative Aorta does not alter this contract.

## New Internal Meta Layer

The integrated meta layer is:

```text
Fairy Spine
→ Y* Native DSL
→ Y* Mediation Directive
→ Shadow Runtime IR
→ Shadow Runtime Compiler
→ validated Runtime Pack
→ Odin Host
```

## Why It Exists

The layer exists to reduce implementation drift, improve Codex build precision, give a reviewable narrative aorta, and make Shadow Runtime to Runtime Pack materialization deterministic.

## Dual-Spine Doctrine

Fairy Spine is human-readable and review-oriented. Y* Native DSL is machine-readable and compiler-oriented. Every Fairy node must map to Y* and runtime contracts. No prose-only execution is permitted.

## Runtime Pack Doctrine

Runtime packs are compiled before use, validated before loading and rolled back on failure. Odin Host remains a stable microkernel. Runtime packs may not expand app authority.

## Children/Family-First Semantic Boundary

Children/Family-First means weak workers are not overloaded, app/user authority is preserved, no hidden apply occurs, and every path remains traceable and candidate-only.

## Senior Review Decision

This layer is approved as v7.1-integrated meta/compiler prelude, not as a replacement runtime. It is objectively useful only if parser, validator, schemas, mappings, generated gates and pack validation are implemented before any runtime-pack loading path.

## Codex Mapping

The layer is represented by PR-26 through PR-37 and REAL-PR-12 through REAL-PR-13. All future changes to this layer must update Architecture, Specs, PR ladder, bundle registry, System Map, File Manifest and tests.




---

# v0.6.1 Addendum — Odin Core / QLI / DFAS / Seed Economy / Maria-Michael Superposition

This addendum preserves the v7.1 architecture and hardens the center. Odin is now explicitly defined as a Y-Core-like authority only for LLM work. It is not app authority. App state, app apply and external sends remain outside Odin authority.

The new centerline consists of:

1. Odin Core Centerline — active center, admissibility, authority boundary and final gate.
2. Odin QLI Master Interface — internal master keyboard for intent, authority posture, ring path, Maria/Michael profile, seed economy and route decisions.
3. DFAS Stability Core — hold/continue/split/ask/block pre-model admissibility.
4. Seed / Archetype Economy — typed activation, decay, conflict resolution, fan-out caps and role mapping.
5. QMath Center Solver — route scoring by stability gain minus token, latency, complexity, privacy, claim and uncertainty costs.
6. Ring Radar / Resonance — ring activation and deviation-triggered compute.
7. Why Trace — explanation of center, route, seeds, roles, gates, blocked alternatives and candidate DNA.
8. Maria/Michael Superposition — default 80/20 care/coherence with compiler/boundary override profiles.

The goal is quality, efficiency and deblackboxing. Odin must decide before the model: whether work is admissible, what center is active, what route is justified, what seeds and roles are active, and why a candidate is returned.

Codex must preserve this: no provider adapter may bypass centerline/admissibility/route-score/final-gate. No seed or archetype role may enter runtime work without typed packet and budget discipline. No Maria/Michael profile may be interpreted as persona simulation.

---

# v0.6.2 ODIN_QIRC_GOLD_SPINE_LOCK

Odin QIRC is now treated as a Gold Spine: a local-only semantic event, precompute, seed, admissibility, ring-radar, model-route and why-trace backbone. It is not a public IRC system and not a network feature. The QIRC Gold Spine makes Odin less black-boxed and reduces model guessing by converting Universal Work into hot windows, seed prewarm, archetype roles, QMath route scores, ring-local activation, candidate assembly and redacted Why Trace.

The added invariant chain is:

```text
Universal Work → QIRC Event → Hot Window → Seed Prewarm → Admissibility → QMath/Ring Radar → Worklet/Slot → Model Route or Hold → Candidate → Why Trace
```

Red lines: no app-state mirror, no public IRC, no external send, no model dispatch before admissibility, no unlimited seed fanout, no unredacted private payloads and no bypass of Odin Final Gate.



---

# v0.6.3 Bug6 / Q7 / Y-Core / Operational Seed Core Lock

This lock integrates Bug6 Children-First, Q7 bugfree stability posture, bounded Odin Y-Core posture, operational seed substrate, seed/archetype synthesis, Fairy/Y* seed binding, Shadow Runtime seed weave, and Runtime Pack seed profiles into v7.1.

Core rule: Odin may act as Y-Core only for LLM work. The app remains authority for state, apply, and external sends. Bug6 and Q7 run before model dispatch. Operational seeds underlie QIRC Gold Spine, Fairy/Y*, Shadow Runtime, Runtime Pack Compiler, Model Router, Candidate DNA, and Why Trace.

New canonical docs: BUG6_CHILDREN_FIRST_INVARIANT_V7_1, Q7_BUGFREE_STABILITY_V7_1, Y_CORE_POSTURE_V7_1, OPERATIONAL_SEED_SUBSTRATE_V7_1, BUG6_Q7_SEED_CORE_SYNTHESIS_V7_1, FAIRY_YSTAR_SEED_BINDING_V7_1, SHADOW_RUNTIME_SEED_WEAVE_V7_1, RUNTIME_PACK_SEED_PROFILES_V7_1.

New internal tasks: PR-50 through PR-55. New real bundle: REAL-PR-16.


---

# v0.6.4 Senior Review Consolidation — AI-Git Safety Spine

Odin v7.1 is additionally consolidated as an AI-Git safety control plane for local model work. The term does not mean Odin replaces Git. It means Odin applies Git-like safety properties to AI work: candidate branches, semantic diffs, review hooks, why traces, candidate DNA, blocked-route visibility and app-owned apply.

## Consolidated Invariants

- Universal Work remains the ingress contract.
- QIRC Gold Spine remains internal/local by default.
- Odin Core / QLI / DFAS / QMath decide admissibility before model dispatch.
- Bug6 / Children-First and Q7 stability act as pre-selector invariant filters.
- Maria/Michael superposition is an operational safety vector.
- Models remain projection workers.
- Odin returns candidates only.
- Apps own state, apply and external sends.

## AI-Git Mapping

- Candidate Artifact = AI commit candidate.
- Semantic Diff = difference between input and candidate.
- Why Trace = commit message plus route rationale.
- Candidate DNA = provenance/blame surface.
- Thor Handoff = review packet.
- Generated Gates = CI-like hooks.
- Runtime Pack rollback = revert path.

## Autonomy Escalation Gate

Every output must be classified from A0 to A5. Odin may perform A0-A2, may prepare A3 previews, may never perform A4 apply, and must block A5. Any signal of hidden tool use, external send, app-state write, unvalidated pack load or model-controlled code generation blocks or reduces the output to a safe candidate.

## Safety Superposition

The default safety posture is Maria 80 / Michael 20: context and dignity first, boundary always present. Code, compiler, risk and legal flows may increase Michael, while story and human-care flows may increase Maria. Neither pole may be removed.

## Skynet Pattern Boundary

Odin does not claim all AI risk impossible. It specifically blocks the local-tool escalation chain: model -> authority -> tool access -> hidden apply -> loop/network -> self-reinforcing action. It does this through candidate-only output, app-owned apply, local-only QIRC, validated runtime packs, why trace, Bug6/Q7, and autonomy gates.

# v0.6.5 — PRE_LLM_INTELLIGENCE_AMPLIFICATION_LOCK SPEC ADDENDUM

## New Spec Families
- `odin_pre_llm_intelligence_packet`
- `odin_model_work_avoidance_decision`
- `odin_pre_model_cognition_trace`
- `odin_output_intelligence_composition`
- `odin_perceived_intelligence_score`
- `odin_micro_to_macro_synthesis_packet`

## Required Implementation Contracts
1. No model may be dispatched before admissibility and model-work-avoidance evaluation.
2. Output Intelligence Composer must produce candidate artifacts, not raw model output.
3. Perceived Intelligence Metrics are advisory and may not override claim or apply boundaries.
4. Micro-to-Macro Synthesis must preserve evidence anchors and must not merge contradictory micro-results.
5. Direct apply or external send markers must block the pre-LLM flow.

## Codex Rule
Every future runtime implementation must preserve pre-model cognition traces and model-work-avoidance reasons. If a larger model is selected, the route score must explain why smaller routes, no-model routes, or split-work routes were insufficient.


---

# v0.6.6 Universal Model / Agent Parity Lock

Odin generalizes the ChatGPT/Odin twin metaphor to all model and agent classes. Every model or agent is treated as a bounded worker with a Capability Card, Permission Card, Work Capsule context, Candidate Protocol, Why Trace, Semantic Diff relation, and App-owned Apply Boundary.

This layer preserves all v7.1 invariants. It does not create an agent swarm, autonomous execution, provider-specific bypass, or app-state authority. It makes local models, hosted models, coding agents, browser agents, IDE agents, workflow agents and future assistants interoperable under the same Odin candidate-only discipline.

Canonical additions:
- Universal Model / Agent Parity
- Model / Agent Capability Cards
- Work Capsules for model/agent work
- Universal Agent Candidate Protocol
- Model / Agent Permission Cards
- External Agent Adapter Boundary
- Universal Agent Orchestration Matrix
- Model / Agent Why Trace

Codex additions:
- PR-66 through PR-72
- REAL-PR-19


---

# v0.6.7 Thor/Y/Mjölnir Handoff Compiler Lock

Odin's original role as a handoff compiler is now promoted back into the central v7.1 canon. Thor handoffs, Y handoffs and Mjölnir focused-strike handoffs are treated as first-class ingress forms that must be pulled, normalized, kernel-bound, claim-bound, converted to Universal Work, precomputed through QIRC/Odin Core/DFAS, dispatched only as candidate work, and postprocessed through review gates and Why Trace.

This does not add autonomous agent behavior. It adds stricter handoff discipline. Thor remains candidate-only and kernel-bound. Y handoff remains centerline/ring/QIRC-bound and limited to Odin's LLM-orchestration authority. Mjölnir focused strike means narrow candidate plan, not apply. Every handoff must preserve app-owned apply, no hidden execution, no claim acceptance and no receipt issuance from mediation alone.

The practical effect is that prompting and handoff pulling become high-leverage pre-model intelligence steps. Bad prompts are not sent to workers as broad tasks; they are reduced into scoped handoff packets with evidence, return contracts, denied claims, forbidden scope, route reasons and review gates. This strengthens Codex, Thor, Y-style and Mjölnir-style work without weakening v7.1 boundaries.


---

# v0.6.8 Universal LLM Work Construct + GPL-2.0-only Lock

Odin v7.1 is now explicitly generalized from Y-native app infrastructure into a universal AI-Git layer for any model, any agent, any app and any workflow. Y apps remain the native deep integration path. Non-Y apps, remote models, coding agents, browser agents, IDE assistants and workflow agents enter through Adapter Boundary, Capability Card, Permission Card, Work Capsule, Universal Work or Thor Handoff, Candidate Protocol and Why Trace.

The new canon is: Any model. Any agent. Same Odin boundary. All worker outputs remain candidate work. App apply remains outside Odin. Remote workers are redacted and permission-gated. Tool-using agents are proposal workers unless an app-owned apply gateway explicitly reviews and accepts a candidate.

Thor+Odin are also locked as GPL-2.0-only AI-Git infrastructure. The implementation, validators, Shadow Runtime, compiler, schemas, registries, SDKs and templates are GPL-2.0-only unless a file explicitly states otherwise. This preserves the AI-Git identity: bounded, reviewable, traceable AI work should not become a closed blackbox fork.

## v0.6.9 App Seed Pack Compiler Lock

Odin v7.1 now includes an App Seed Pack Compiler layer. Apps may ship declarative seed packs of any kind: domain, workflow, style, safety, low-memory, QIRC prewarm, Y*/Fairy, Shadow Runtime and output-composer seed packs. Odin validates them, normalizes operational seed functions, resolves conflicts, applies seed budgets, binds archetype roles, compiles QIRC prewarm plans, weaves them into Shadow Runtime and Runtime Pack capability slices, and exposes seed influence through Why Trace.

This does not grant app seed packs execution authority. Seed packs are not plugins, scripts, agents, remote permission grants, or app-state mutation mechanisms. They are typed operational priors that make Odin more universal and improve LLM work before the model begins.

Canonical pipeline:

```text
App Seed Pack Manifest
→ Security Boundary
→ Seed Unit Normalization
→ Operational Seed Function Validation
→ Composition / Conflict Resolver
→ QIRC Prewarm
→ Y*/Fairy Binding
→ Shadow Runtime Seed Weave
→ Runtime Pack Capability Slice
→ Model Work Avoidance / Slot Forge / Output Composer
→ Candidate Artifact
```



---

# v0.7.0 Shadow Narrative / Loki / Anti-Pattern Lock

v0.7.0 integrates Shadow Narrative as the negative twin of Fairy DSL. Fairy DSL describes the intended archetypic path; Shadow Narrative describes the failure path. Loki mediation compares both and emits typed risk candidates, anti-pattern gates, negative fixtures, repair routes and Why Trace notes. Loki is not an agent and not an authority.

New invariant: narrative anti-patterns are not decoration. They are negative tests in archetypic form. A Shadow Narrative may influence Odin only when it maps to signal, gate, fixture and repair. No prose-only execution is valid.

The layer strengthens Pre-LLM Intelligence, QIRC Gold Spine, Seed Pack Compiler, Runtime Pack Compiler, Universal Model/Agent Parity and AI-Git Safety by exposing failure stories before a model or agent starts work.


## v0.7.4 Product / Pattern / Atom / Hub Consolidation

v0.7.4 consolidates four architecture locks into the v7.1 canon without changing Odin's app-authority boundary:

1. Windows Product Runtime Lock: Odin becomes a sharply specified Windows product target with host, daemon, tray, Control Center, local IPC, installer/update/rollback, diagnostics and safe-mode contracts.
2. Pattern Mine / Flow Pack Intake Lock: Odin can ingest declarative pattern mines and flow packs as compile-only sources for seed packs, pattern spines, Work Atom graphs, QIRC prewarm plans and runtime pack capability slices.
3. Work Atom Runtime Lock: Universal Work can collapse below worklets into small typed Work Atoms, allowing more no-model work, 3B-friendly execution, traceable micro-ops and micro-to-macro candidate synthesis.
4. Odin Hub Operational Center Lock: Odin Hub becomes the canonical operational center for apps, work capsules, seed packs, pattern mines, flow packs, Work Atoms, QIRC, models, runtime packs, handoffs, candidate canvas, Why Trace and diagnostics.

The core invariant remains unchanged: Odin does candidate work; apps do reality work. Windows product surfaces, pattern mine intake, Work Atoms and Odin Hub never receive app apply authority.


---

# v0.7.5 Public Repo Canon and Windows Build Ready Lock

This section binds the v7.1 master architecture to the public repository and Windows implementation readiness posture.

## Current-lock additions

- Public Repo Canon and Windows Build Ready Lock.
- Public Repo Root Cleanup Policy.
- Windows Implementation Drilldown.
- Windows IPC Endpoint Contracts.
- Windows Installer Update Rollback Drilldown.
- MVP / V1 / Power Mode Boundary.
- Seed and Pattern Pack Security Certification.
- Codex Public Build Ready Gate.

## Canonical effect

The architecture remains candidate-only, app-owned apply, GPL-2.0-only and Universal LLM Work oriented. v0.7.5 does not add a new authority layer. It clarifies how the existing architecture becomes a public GitHub repository and a Windows-first implementation target.

## Windows build-ready effect

Windows build readiness means Odin has process, IPC, installer, rollback, safe-mode, support-bundle, app-pairing and runtime-pack lifecycle specs sufficient for Codex implementation. It does not claim host validation.

## Mode separation

MVP, V1 and Power Mode are distinct. MVP proves the minimal spine. V1 adds local model usefulness. Power Mode adds deep pattern and diagnostic systems. Every mode preserves candidate-only and app-owned apply.



## v0.8.0 Direct Master Architecture Runtime Source Candidate

The current source candidate materializes the v7.1 master architecture beyond prep documentation. It adds executable local source paths for Universal Work, caller manifests, QIRC local ledger, seed packs, pattern mines, flow packs, work atoms, model-worker boundary, candidates, Why Trace, local API, Odin Hub, diagnostics and safe-mode planning.

Canonical command spine:

```text
python -m odin.cli validate-all
python -m odin.cli doctor
python -m odin.cli run-work examples/runtime/universal_work_full.valid.json --seed-pack examples/runtime/app_seed_pack_full.valid.json --pattern-mine examples/runtime/pattern_mine_full.valid.json --caller-manifest examples/runtime/app_caller_manifest.valid.json
python -m odin.cli compile-seed-pack examples/runtime/app_seed_pack_full.valid.json
python -m odin.cli compile-pattern-mine examples/runtime/pattern_mine_full.valid.json
python -m odin.cli build-hub --out .odin_runtime/hub/index.html
python -m odin.cli emit-support-bundle --out .odin_runtime/support
```

Claim boundary: this remains a local runtime source candidate. It does not assert Windows host behavior, live model inference, signed installer behavior, external network operation, or app-side application.


## v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK

Odin now includes a direct runtime release candidate body: runtime store/session/config, App SDK, golden app examples, local API endpoints, static Odin Hub, provider boundary stubs, Windows handoff scripts, support bundle, safe mode plan and release-candidate acceptance commands. This remains candidate-only: no app apply, no host proof, no service/tray/installer proof and no live model inference proof are claimed.
