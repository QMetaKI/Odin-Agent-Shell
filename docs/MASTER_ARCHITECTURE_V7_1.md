# Odin Agent Shell — Master Architecture v7.1

> **Status:** Architecture/specification canon for the future public `Odin-Agent-Shell` repository.
> **Claim boundary:** This repository state is a build-prep canon and scaffold. It does not claim host proof, model proof, external verification, or completed runtime behavior.
> **Public language:** neutral terminology. Internal inspiration may come from QIRC/YNode/QFoundation/Q Metamodell/Thor patterns, but the public repo should describe the system as Odin Agent Shell.


## 0. Architecture Status

**Version:** v7.1  
**Repository state:** v0.7.7 BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK  
**Primary target:** Windows-first local daemon + tray + control center + SDKs  
**Primary consumer:** independent apps that need local LLM capability without embedding models  
**Primary KPI:** maximum quality, speed, safety, universality, traceability and app-visible usefulness from small local models.  
**Default model strategy:** 3B + 7B/8B hybrid.  
**Optional acceleration/coordination layer:** Internal Semantic IRC Bus.  
**Architectural posture:** local-first, candidate-only, app-sovereign, small-model-first, resource-aware.



## 0.7.7 Build Execution Ladder

The current actual build execution ladder is `REAL-GH-PR-01..REAL-GH-PR-08` in `registries/real_pr_execution_registry.json`.

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

## 0.1 Executive Definition

Odin Agent Shell v7.1 is a Windows-first, local-first, protocol-bound Universal Semantic Work Kernel, Small-Model Performance OS, and optional Internal Semantic IRC precompute engine. It lets independent apps expose AI-native features without embedding LLM runtimes, providers, routers, prompt stacks, hybrid orchestration, claim/evidence gates, or model scoreboards. Apps build Universal Work Objects and receive Candidate Artifacts. Odin does all LLM-adjacent orchestration outside the app.

```text
Functionally LLM-native.
Technically Odin-delegated.
Operationally candidate-only.
Qualitatively Odin-amplified.
Internally bus-coordinated.
Resource-aware by model scale ladder.
```



## 0.2 One-Line Canon

```text
Anything in, bounded work, semantic-bus coordinated, smallest sufficient worker, candidate artifact out.
```


# 1. System Intention and Non-Goals


Odin is not a model wrapper, not a chat assistant, not an app framework, and not a public network. It is the local semantic work layer that makes multiple independent apps feel AI-native while keeping all model/runtime/policy complexity outside the app.

Core move:

```text
Do not make apps smart by embedding AI.
Make apps smart by connecting them to Odin through bounded work contracts.
```

Odin exists to centralize: model preparation, local inference routing, context distillation, worklet decomposition, slot contracts, model scale decisions, semantic cache, critic passes, candidate assembly, claim/evidence boundaries, and app-safe response packets.

Explicit non-goals:

```text
No public IRC service.
No app-state ownership.
No direct apply actions.
No external sends by Odin.
No hidden autonomous agent authority.
No model truth promotion.
No requirement that apps understand models.
No requirement that a single model solve a full task.
```

Design consequences:

| Decision | Consequence |
|---|---|
| Apps contain no LLM runtime | App repos stay smaller and safer. |
| Odin returns candidates only | Product authority remains with app/user workflow. |
| Model scale ladder | Bigger models are route options, not the architecture. |
| Internal Semantic Bus | More work happens before the model call. |
| Small Model Power Layer | 3B/7B models get engineered work conditions. |


# 2. Architectural Laws


The v7.1 architecture is governed by non-negotiable laws.

## 2.1 No LLM in App Law

Apps must not contain:

```text
LLM provider handling
model routing
prompt orchestration
3B / 7B / hybrid logic
remote fallback logic
Thor handoff logic
claim/evidence checking layer
model capability cards
model fallback ladder
context compression logic
small model scoreboard
semantic bus logic
candidate tournament logic
```

Apps may contain:

```text
Odin Capability Bridge
Caller Manifest
Event Digest Builder
Context Snapshot Builder
Universal Work Builder
Candidate Renderer
App-owned Apply Gate
App-owned UX / state / workflow / domain logic
```

## 2.2 Universal Work Law

Every AI-like app feature must be expressible as:

```text
Input Artifact(s)
+ Transformation Verb
+ Output Contract
+ Constraints
+ Boundary
+ Model Policy
```

## 2.3 Candidate Law

```text
Odin outputs candidates.
Apps perform reality-changing actions.
```

## 2.4 Smallest Sufficient Worker Law

```text
Use deterministic before model.
Use 1B/2B before 3B if enough.
Use 3B before 7B/8B when safe.
Use 7B/8B before larger models when sufficient.
Use 3B + 7B/8B hybrid as canonical sweet spot.
Use 13B/14B as quality escalation.
Use 22B/32B as heavy local escalation.
Use 70B-class as rare local batch/offload.
Use remote only by explicit permission.
Use cannot-safely-complete before unsafe escalation.
```

## 2.5 Semantic Bus Law

```text
Internal bus events may coordinate work.
They may not grant authority.
They may not mutate app state.
They may not bypass Odin Final Gate.
They may not expose public networking by default.
```

## 2.6 Work Environment Law

Small models should never receive raw chaos. They receive distilled context, tight slots, output contracts, anti-patterns, boundaries, and the exact current moment.

## 2.7 Universal but Bounded Law

```text
Universal in processing.
Bounded in authority.
Candidate-only in output.
App-owned in action.
Local-first in runtime.
```


# 3. Responsibility Boundaries


## App owns

```text
UI, UX, domain state, domain database, files, project data, event system,
QIRC-like app bus if present, workflows, apply pipeline, external sends,
business rules, game runtime, plugin runtime, storage, permissions,
domain audit ledger, user accounts, domain-specific validation.
```

## Odin owns

```text
local mediation protocol, caller registration, manifest validation, binding,
event digest reading, context requests, universal work validation, artifact registry,
artifact lens registry, verb registry, output contract resolver, system profile compiler,
adaptive precompute compiler, internal semantic bus, small model power layer,
pattern foundry, seed continuity, fit/coherence scoring, mirror-axis checks,
Thor bridge, slot contracts, gaptext, ModelWorkPackets, model routing,
model execution through providers, minicheck, claim/evidence/reality gates,
candidate artifact construction, response packets, traces, receipt candidates,
semantic cache, small model scoreboard.
```

## Thor owns, when invoked

```text
handoff score, guard, expected output, return contract, mediation shape,
review boundary, receipt boundary, claim-bound candidate coordination.
```

## Models may do

```text
classify, extract, summarize, rewrite, translate, repair, draft,
review candidate, score candidate, explain candidate, generate candidate,
schema fill, style rewrite, minicheck.
```

## Models may not do

```text
decide authority, mutate state, apply changes, send externally, claim tests passed,
verify runtime, claim security, claim deployment, raise reality status, become truth.
```


# 4. Layer Stack


Odin v7.1 contains the following layers, ordered from host surface to semantic core.

| Layer | Role | Output |
|---|---|---|
| Windows Runtime Layer | Daemon, tray, control center, local API, process supervision | local service |
| App Integration Standard | Bridge files, manifest, event digest builder, candidate renderer | app-facing contract |
| Local Mediation Protocol | Message and artifact exchange format | typed envelopes |
| Universal Work Kernel | Bounded semantic work compiler | validated work plan |
| Registries | Artifact, verb, lens, slot, route, output contract registries | deterministic lookup |
| Internal Semantic IRC Bus | Local semantic event coordination | traceable event batches |
| Adaptive Precompute Compiler | Early ordering, context, pattern, seed, fit | precomputed work context |
| Small Model Power Layer | Distill, worklet, slot, critic, tournament, style | model workload reduction |
| System Palette Compiler | Select neutral system patterns for task families | system profile |
| Thor Bridge | Candidate-only handoff/review/receipt discipline | handoff candidate |
| Model Runtime | Provider adapters, routes, fallback ladder, hybrid director | model response |
| Candidate Layer | Candidate Artifact, Candidate DNA, Response Packet | app-renderable output |
| Gate Layer | Claim/evidence/reality validation | allowed/blocked/downgraded result |
| Storage/Trace/Receipt | SQLite/object store/cache/log/receipt candidates | replayability |
| Control Center/Labs | Debug surfaces, registries, traces, bus, model dojo | operator visibility |
| SDK/Templates | App onboarding and compatibility | repeatable integrations |


# 5. Canonical End-to-End Flow


The standard work cycle is:

```text
User uses app feature
→ app builds Event Digest and Universal Work
→ Odin validates caller and binding
→ Universal Work Kernel validates artifact/verb/output contract/boundary
→ System Profile Compiler selects route family
→ Internal Semantic Bus opens work batch
→ Context Distillery builds Context Capsule
→ Artifact Lens System activates lenses
→ Adaptive Precompute runs deterministic ordering
→ Worklet Graph Compiler decomposes work if needed
→ Slot Forge creates slot contracts
→ Model Scale Ladder selects route
→ Gaptext Builder creates bounded model input
→ ModelWorkPacket sent to provider
→ Model Response received
→ Minicheck validates schema/claims/shape
→ Mirror Critic Cascade evaluates risk/style/genericness/context
→ Candidate Tournament may select/merge candidates
→ Native Output Composer builds Candidate Artifact
→ Candidate DNA links inputs, bus batch, slots, model routes, critic reports
→ Odin Final Gate allows/downgrades/blocks
→ Response Packet returns to app
→ App renders and decides
```

The flow must remain valid if the model step is skipped. Many tasks can be solved by deterministic templates, caches, bus precompute, or gaptext fill without model inference.


# 6. Universal Work Kernel Architecture


Universal Work is the kernel abstraction. It ensures Odin is universal without becoming unbounded.

## Required Universal Work components

| Component | Meaning | Gate |
|---|---|---|
| Input Artifacts | Bounded input references or payloads | artifact type + privacy |
| Transformation Verb | What should happen semantically | verb registry |
| Output Contract | Shape and candidate status of output | output registry |
| Constraints | Allowed/forbidden moves | claim boundary |
| Boundary | Reality and authority boundary | final gate |
| Model Policy | Allowed route classes | model ladder |

## Universal Work validation failure examples

```text
binding missing
caller manifest invalid
input artifact type unknown
privacy class exceeds caller policy
verb not allowed for caller
output contract not allowed
candidate_only false
hidden apply/send/mutate intent detected
remote allowed without explicit policy
claim boundary missing
blocked_sensitive artifact present
```

## Universal Work lifecycle

```text
RECEIVED → VALIDATING → COMPILED → PRECOMPUTED → ROUTED → EXECUTING → CHECKING → COMPOSING → GATED → READY | BLOCKED | NEEDS_CONTEXT
```

Universal Work is not prompt text. It is a typed semantic work object. Prompt/gaptext is a derived internal artifact, not the public integration interface.


# 7. Artifact Registry and Artifact Lens Architecture


Artifacts are typed. Lenses interpret artifact families.

## Artifact families

Text/document: plain_text, markdown, html_fragment, document_excerpt, transcript, translation_source.  
Data/config: json_object, yaml_object, csv_excerpt, schema, contract, form_data.  
Code/repo: code_reference, code_excerpt, repo_context, diff, patch, error_log, stack_trace, test_output, build_log.  
App/runtime: event_digest, state_snapshot, workflow_state, ui_selection, tool_result, trace_log, receipt_ref.  
Game/interactive: game_state_digest, scene_state_digest, npc_state, quest_state, dialogue_context, simulation_tick_digest.  
Media references: image_reference, audio_reference, video_reference, file_reference, preview_digest, ocr_text, caption, metadata_digest.

## Trust statuses

```text
caller_provided, local_derived, tool_result, model_projection,
accepted_projection, external_reference, verified_receipt, unknown
```

## Privacy classes

```text
local_only, local_with_cache, local_redacted_trace,
remote_allowed_explicit, blocked_sensitive
```

## Lens contract

A Lens defines:

```text
what matters, what can be ignored, typical verbs, output contracts, risk zones,
preferred slot classes, preferred model routes, critic axes, bus channels,
cache strategy, context compression strategy, privacy rules.
```

Lenses prevent universal processing from becoming generic processing.


# 8. Transformation Verb and Output Contract Architecture


Verbs define semantic action. Output contracts define app-safe shape.

## Universal verbs

```text
classify, extract, summarize, rewrite, translate, expand, compress, compare,
rank, score, validate, repair, normalize, structure, convert, explain, plan,
draft, review, simulate, route, decompose, compose, map, merge, split,
annotate, generate_candidate
```

## Verb classes

```text
read, transform, generate, evaluate, route, repair, plan, compose, convert, simulate
```

## Output contract rules

Every output contract must define:

```text
artifact_type, schema_ref or shape, candidate_only true,
requires_app_apply_gate when action-impacting, max_tokens or size policy,
forbidden_claims, status requirements, render target, privacy requirements.
```

Invalid output contracts include direct apply, direct external send, missing trace requirement, or caller-disallowed artifact type.


# 9. Candidate Artifact, Response Packet, and Candidate DNA


Odin returns Candidate Artifacts wrapped in Response Packets.

## Candidate Artifact requirements

```text
candidate_id, candidate_type, work_id, caller_id, content, render_hints,
actions, candidate_dna_ref, claim_status, evidence_status, warnings,
blocked_claims, trace_id, requires_app_apply_gate.
```

## Candidate DNA links

```text
input artifacts, event digest, context capsule, system profile, active lenses,
active seeds, semantic bus batch, worklet graph, slots, model routes,
critic reports, fit score, cache hits, fallbacks, claim boundary.
```

## Response Packet requirements

```text
response_id, request_id, work_id, caller_id, response_kind, candidates,
status chips, warnings, next actions, blocked claims, claim status,
evidence status, trace id, optional receipt candidate id, claim boundary.
```

Candidate DNA makes app-visible intelligence auditable without exposing raw app state or model internals unnecessarily.


# 10. Internal Semantic IRC Bus Architecture


The Internal Semantic IRC Bus is optional but central to the full v7.1 power profile. It is a local-only semantic coordination layer, not a public network.

## Purpose

```text
coordinate precompute, route semantic signals, build traceable work batches,
reduce model context size, increase cache reuse, improve critic chaining,
and prepare digest-only bridges to future app-owned event/QIRC systems.
```

## Core properties

```text
local-only, inspectable, replayable, traceable, bounded, module-oriented,
no public rooms, no federation, no LAN/WAN by default, no app mutation.
```

## IRC features used

| Feature | Odin use |
|---|---|
| Channels | semantic lanes such as #context.distill or #critic.claim |
| Topics | active constraints for a lane |
| Message tags | work_id, trace_id, privacy, state_digest, route |
| Module nicks | bounded service modules such as slot-forge |
| Modes | local-only, no-model, model-allowed, critic-only |
| Notices | warnings and boundary hits |
| Batches | group all events for a Universal Work run |
| Replay | reconstruct work path for debug and scoring |

## Required channel families

```text
#odin.*, #app.*, #work.*, #context.*, #lens.*, #precompute.*,
#worklet.*, #slot.*, #gaptext.*, #model.*, #critic.*,
#candidate.*, #response.*, #trace.*, #receipt.*, #claim.*, #reality.*
```

## Bus lifecycle

```text
DISABLED → STARTING → ACTIVE_LOCAL → DEGRADED → VERIFICATION_ONLY → STOPPING → DISABLED
```

The bus must always be optional: Odin minimal mode must work without it.


# 11. Semantic Event Envelope and Bus Batches


Every internal bus event uses a typed envelope.

Required fields:

```text
artifact_kind=odin_semantic_event, protocol_version, event_id, channel,
event_type, source_module, work_id when work-related, trace_id,
privacy_class for context-bearing events, state_digest when state-derived,
payload, requires_receipt, created_at.
```

Batch lifecycle:

```text
BATCH_OPENED → WORK_RECEIVED → BINDING_CHECKED → EVENT_DIGEST_ACCEPTED →
UNIVERSAL_WORK_VALIDATED → CONTEXT_CAPSULE_CREATED → SYSTEM_PROFILE_SELECTED →
PRECOMPUTE_DONE → WORKLET_GRAPH_BUILT → SLOT_FORGED → MODEL_ROUTE_SELECTED →
MODEL_RESPONSE_RECEIVED → CRITIC_CASCADE_DONE → CANDIDATE_COMPOSED →
FINAL_GATE_DONE → RESPONSE_PACKET_READY → BATCH_CLOSED
```

Failure states:

```text
BINDING_INVALID, PRIVACY_DENIED, ARTIFACT_BLOCKED, VERB_FORBIDDEN,
OUTPUT_CONTRACT_INVALID, CONTEXT_TOO_BROAD, MODEL_ROUTE_BLOCKED,
CLAIM_BOUNDARY_HIT, SCHEMA_INVALID, NEEDS_CONTEXT, CANNOT_SAFELY_COMPLETE
```


# 12. Small Model Power Layer Architecture


The Small Model Power Layer is the reason Odin can extract high utility from small local models.

## Modules

```text
Context Distillery, Worklet Graph Compiler, Slot Forge, Predictive Precompute,
Resonance/Fit Radar, Mirror Critic Cascade, Seed Memory Weaver,
Native Output Composer, Model Dojo, Candidate Tournament, Tiny Specialist Modes,
Artifact Lenses, Style Stabilizer, Anti-Generic Engine, Taste Dials,
Work Memory, Shadow Candidate Ghost Run, Semantic Pressure Valve, Candidate DNA.
```

## Operating principle

```text
Reduce semantic pressure before increasing model size.
Split broad work into narrow worklets.
Use deterministic and bus-precomputed structures first.
Let 3B handle tiny roles.
Let 7B/8B handle quality writing/synthesis.
Let larger models be escalation, not default.
```

## Small model roles

3B roles: extractor, router, compressor, schema repair, no-go critic, claim critic, style critic, genericness critic, short candidate generator.  
7B/8B roles: writer, synthesizer, document section drafter, patchplan candidate drafter, review summarizer, style rewriter.  
Hybrid: 3B scouts/checks, 7B writes/synthesizes, Odin composes/gates.


# 13. Context Distillery Architecture


Context Distillery converts broad app state into exact model context.

Pipeline:

```text
Raw App State → Event Digest → Semantic Bus Events → Relevance Filter →
Moment Frame → Work Context → Context Capsule → Slot Context
```

A Context Capsule must include:

```text
task_center, must_use, must_not_use, style/tone, length/shape,
claim boundary, source refs, privacy class, compression summary,
context omissions, unanswered questions, confidence of relevance.
```

Rules:

```text
Never pass raw app databases by default.
Prefer digest and selected artifacts.
Mark omitted important context.
Ask app for context if capsule quality is too low.
Bind capsule to output contract and privacy class.
```


# 14. Worklet Graph and Slot Forge Architecture


Complex work becomes a graph of small worklets.

Worklet nodes define:

```text
node_id, worklet_type, input_refs, output_kind, preferred_route,
slot_class, dependencies, risk profile, fallback, gate requirements.
```

Edges define:

```text
feeds_context, blocks_until, critic_of, refines, composes_into,
requires_human_review, fallback_from.
```

Slot Forge creates optimal slot contracts from artifact + verb + output + model profile + bus state.

Slot contracts define:

```text
slot_id, slot_class, input types, output contract, allowed routes,
max input tokens, max output tokens, output schema, forbidden claims,
fallback, guard policy, receipt policy, retry policy.
```

Slot law:

```text
Prompt engineering is secondary.
Slot engineering is primary.
Slot forging is adaptive.
```


# 15. Model Scale Ladder Architecture


Odin routes by measured resources and task requirements, not hardcoded hardware names.

## Ladder

```text
L0 deterministic / no-model
L1 1B–2B micro
L2 3B micro / critic / router
L3 3B multi-slot
L4 7B/8B quality
L5 3B + 7B/8B hybrid
L6 3B + 13B/14B quality hybrid
L7 3B + 22B/32B heavy local
L8 MoE / Mixtral-style heavy local/offload
L9 70B-class local/offload batch
L10 remote optional explicit
L11 cannot safely complete
```

## Resource profiles

low_memory_strict: templates, deterministic, bus light, 1B/2B/3B micro.  
standard_local: 3B + 7B/8B sweet spot.  
quality_local: 3B + 13B/14B optional quality.  
heavy_local: 22B/32B or MoE/offload for batch-friendly work.  
max_local_batch: very large local/offload, not live UX.  
remote_optional: explicit permission only.

## Latency modes

interactive, draft, batch, overnight.

## Escalation rule

Do not use a bigger model if context distillation, worklet splitting, slot tightening, semantic bus precompute, candidate tournament, critic cascade, or the 3B+7B/8B hybrid route can solve it.


# 16. Model Runtime and Provider Architecture


Model Runtime owns provider adapters, model registry, capability cards, routing, execution, fallback ladder, and hybrid director.

Required provider adapters:

```text
mock_provider, ollama_provider, llama_cpp_provider
```

Optional:

```text
openai_compatible_provider, custom_http_provider, remote_provider_explicit
```

Capability Card fields:

```text
model_id, provider, size_class, quantization, context_window,
preferred_context_tokens, safe_slot_classes, blocked_slot_classes,
latency_band, memory_band, json_strictness, language quality,
retry stability, profile status, dojo scores.
```

Provider rules:

```text
Provider is transport, not authority.
Provider cannot bypass model policy.
Remote provider requires explicit manifest and user policy.
Raw prompts are not public interface; ModelWorkPackets are.
```


# 17. ModelWorkPacket and Gaptext Architecture


Models receive ModelWorkPackets, not raw app requests.

ModelWorkPacket includes:

```text
packet_id, binding, work_id, slot contract, model route, task,
input refs, output contract, context frame, context capsule, event digest,
semantic bus batch, facts, constraints, allowed/forbidden, output schema,
gaptext, return contract, fallback policy, claim boundary.
```

Gaptext format:

```text
TASK
CENTER
KNOWN FACTS
APP EVENT DIGEST
CONTEXT CAPSULE
ALLOWED
FORBIDDEN
OUTPUT SHAPE
CLAIM BOUNDARY
SELF-CHECK
RETURN
```

Gaptext must be derived from validated work and never contain hidden permissions.


# 18. Critic Cascade, Minicheck, Candidate Tournament


The quality path has three complementary mechanisms.

## Minicheck

Fast structural and boundary check: schema, forbidden claims, output shape, return contract, model route.

Routes: accept, retry_same_model, repair_schema_3b, escalate_7b_8b, escalate_hybrid, ask_app_context, block, human_review, thor_review.

## Mirror Critic Cascade

Narrow critics: claim, evidence, context, style, genericness, schema, boundary.

A small critic works well if the question is narrow enough.

## Candidate Tournament

Multiple cheap candidates can beat one broad attempt. Modes: 3B multi-candidate, 7B dual-candidate, 3B critic select, hybrid refine best, merge best parts.


# 19. Style, Specificity, and Taste Architecture


Style is not only prompt wording. It is output contract + seed + lens + critic + stabilizer + taste dials.

## Style Stabilizer corrections

```text
too cold → warmer
too kitschy → clearer
too long → shorter
too generic → add project anchors
too authoritative → candidate language
too chaotic → structured
too technical → simpler
too vague → concrete
```

## Anti-Generic Engine checks

```text
specific project anchors present?
could this apply to any user/project?
does it reuse cliché phrases?
does it avoid available concrete details?
does it sound template-like?
```

## Taste Dials

```text
warmer/clearer, shorter/more detailed, bolder/safer,
more humorous/more serious, more poetic/more grounded,
more technical/simpler, more formal/looser, more specific/more general.
```

Taste Dials modify output contracts and slot constraints, not only prompt text.


# 20. Work Memory, Semantic Cache, and Model Dojo


Odin learns workflow performance without storing unnecessary private chat history.

## Work Memory stores

```text
artifact digest, successful slot contract, preferred output shape, failed route,
accepted candidate style, app feedback, model score, boundary issue,
fallback success, bus route success, critic cascade result.
```

## Work Memory does not store by default

```text
raw private user chat, full app databases, secrets, unneeded personal context.
```

## Semantic Cache layers

caller manifest, event digest, context capsule, system profile, lens, pattern spine, seed, fit score, worklet graph, slot plan, gaptext, model output, critic report, tournament, semantic bus batch, response packet, fallback.

Cache may accelerate; it may never bypass Odin Final Gate.

## Model Dojo

Dojo tests profile local models for JSON fill, claim boundary, German rewrite, summary, schema repair, style control, event digest, no-go detection, short dialogue, patchplan micro, context compression, genericness, semantic bus route.


# 21. App Integration and App-QIRC Bridge Architecture


Apps integrate through a Capability Bridge.

Required app-side files:

```text
caller_manifest.json, odin_connector.*, event_digest_builder.*,
context_snapshot_builder.*, universal_work_builder.*, candidate_renderer.*,
odin_task_map.*, odin_apply_gate_bridge.*
```

Future apps may have their own event/QIRC systems. Odin can consume digest-only bridges:

```text
App QIRC/Event System → App-owned Event Digest → Odin Internal Semantic Bus →
Odin Precompute/Model Work → Candidate Artifact → App Response
```

Bridge law:

```text
Odin may subscribe to app-provided digests.
Odin may not become app QIRC.
Odin may not mirror full app state by default.
Odin may not publish app-state mutation events.
```


# 22. Thor Bridge and Bounded Code Work


Thor is invoked when a work item requires strict handoff/review/receipt discipline.

Use Thor for: repo/code/patchplan structure, return contract, agent mediation shape, review boundary, receipt candidate, claim-bound coordination.

Bounded Code Work examples:

```text
repo_context + plan → patchplan_candidate
diff + review → review_summary_candidate
error_log + explain → debug_hypothesis_candidate
test_output + summarize → test_report_candidate
schema + validate → schema_review_candidate
```

Forbidden code claims without receipts:

```text
patch_applied, tests_passed, build_passed, runtime_verified,
security_verified, repair_complete, production_ready
```

Code work is candidate-only unless app/Codex applies later with separate receipts.


# 23. Windows Runtime Architecture


Windows-first runtime contains daemon, tray, control center, CLI, model runner, worker process, optional semantic bus process.

## Required daemon responsibilities

```text
single-instance lock, health endpoint, graceful shutdown, crash recovery,
watchdog, structured logs, model runner supervision, worker supervision,
resource pressure tracking, local-only default, app pairing, manifest registry,
capability token validation, semantic bus lifecycle, support bundle export.
```

## Control Center panels

Home, Apps, Models, Universal Work Lab, Worklet Graph Lab, Internal Semantic Bus, Artifact Registry, Lens Registry, Handoff Lab, Candidate Tournament View, Small Model Dojo, Small Model Scoreboard, Traces, Settings, Security/Privacy, Support Bundle.

## Runtime modes

minimal, local, local_semantic_bus, degraded, low_memory_strict, verification_only, developer.

## Bus modes

disabled, active_local, verification_only, degraded, debug_separate_process.


# 24. Local API Architecture


The API is local-first and bound to localhost by default.

Core endpoints:

```text
GET /v7/status
GET /v7/health
GET /v7/capabilities
POST /v7/apps/register
GET /v7/apps
POST /v7/apps/{app_id}/revoke
POST /v7/protocol/message
POST /v7/protocol/event-digest
POST /v7/protocol/context-response
POST /v7/universal-work/validate
POST /v7/universal-work/compile
POST /v7/universal-work/run
GET /v7/artifacts/types
GET /v7/artifacts/lenses
GET /v7/verbs
GET /v7/output-contracts
POST /v7/worklet-graph/build
POST /v7/slot-forge/build
POST /v7/modelworkpacket/build
POST /v7/modelworkpacket/run
POST /v7/candidates/tournament
POST /v7/candidates/critic-cascade
POST /v7/candidates/compose
POST /v7/return/minicheck
POST /v7/response/compile
GET /v7/model-dojo
POST /v7/model-dojo/run
GET /v7/bus/status
POST /v7/bus/start
POST /v7/bus/stop
GET /v7/bus/channels
GET /v7/bus/events
GET /v7/bus/replay/{work_id}
POST /v7/bus/export-trace/{work_id}
GET /v7/trace/{trace_id}
GET /v7/scoreboard
```

No public network endpoints by default.


# 25. Storage, Trace, and Retention Architecture


Storage uses SQLite plus object store.

## SQLite domains

```text
caller_manifests, bindings, event_digests, context_frames, context_capsules,
universal_works, input_artifacts, artifact_lenses, output_contracts,
candidate_artifacts, candidate_dna, system_profiles, pattern_spines,
seed_profiles, work_memory, fit_scores, mirror_axis_reports, worklet_graphs,
slot_contracts, gaptexts, model_work_packets, model_runs, model_responses,
minichecks, critic_reports, candidate_tournaments, conflicts, response_packets,
trace_entries, receipt_candidates, cache_entries, model_profiles,
model_dojo_results, provider_profiles, app_pairings, semantic_bus_events,
semantic_bus_channels, semantic_bus_topics, semantic_bus_batches,
semantic_bus_replays, app_qirc_bridge_configs, bus_module_status, settings.
```

## Object store domains

handoff packs, compressed context, large artifacts, payloads, candidates, returns, traces, support bundles, model dojo reports, bus replays, bus trace exports, semantic event batches.

Retention must be policy-driven. Raw context should not be retained by default. Debug payloads should be opt-in and redacted.


# 26. Security, Privacy, and Claim Boundary Architecture


Default posture:

```text
local-only, remote disabled, raw app state not persisted by default,
candidate-only outputs, per-app manifest required, capability tokens required,
no arbitrary code execution, no plugin execution by default, no external send by Odin,
semantic bus local-only, no WAN/LAN by default.
```

Secret handling:

```text
do not request secrets, do not store secrets, redact detected secrets in traces,
redact detected secrets in bus payloads, block remote if secrets detected,
warn app if event digest appears overbroad, block blocked_sensitive artifacts,
never use secrets in channel names or topics.
```

Claim boundary:

Odin must distinguish model projection, local derived context, candidate artifact, receipt candidate, and externally verified evidence. It must downgrade language or block output when evidence is missing.


# 27. Testing, Gates, and Build Acceptance Architecture


Acceptance gates:

```text
A Universal Work
B No LLM in App
C App Boundary
D ModelWorkPacket
E Small Model Power
F Internal Semantic Bus
G App QIRC Bridge Safety
H Candidate Output
I Claim / Evidence
J Windows Usability
K Model Scale Ladder
L Schema/Registry Parity
M Trace/Replay
N Low-Memory Strict
```

Golden tests include Universal Work examples, bus event examples, model route examples, candidate artifacts, app bridge examples, and negative tests.

Negative tests must block direct apply, unsupported output contract, remote route without explicit permission, blocked sensitive artifacts, bus external network attempt, app QIRC full mirror attempt, positive overclaim phrases, and cache/final-gate bypass.


# 28. Codex Build Interpretation


Codex should treat this repo as build-prep canon, not a finished runtime. Codex must preserve the laws and boundaries while implementing concrete modules.

Codex order:

```text
0 Canon and schema gates
1 Universal Work Kernel
2 Internal Semantic Bus MVP
3 Small Model Power core
4 Model Runtime and providers
5 Candidate/Response/Gates
6 Windows app/control center
7 SDK/templates/app examples
8 End-to-end host/model receipts later
```

Codex must not add model logic to app templates. It must not make Odin apply app changes. It must not turn the semantic bus into a network feature. It must not convert forbidden claims into positive runtime statements.


# 29. Final Canon


```text
Odin Agent Shell v7.1 is a Windows-first, local-first, protocol-bound
Universal Semantic Work Kernel, Small-Model Performance OS and optional
Internal Semantic IRC precompute engine.

Apps contain no LLM runtime.
Apps contain only Odin Capability Bridge.

Apps send Universal Work Objects:
Input Artifacts + Transformation Verbs + Output Contracts + Constraints + Boundaries + Model Policies.

Odin validates work, reads app event digests, coordinates semantic precompute through its internal local IRC-like bus, distills context, selects system profiles, applies adaptive precompute, builds worklet graphs, forges slots, creates ModelWorkPackets, routes to deterministic workers, 1B/2B, 3B, 7B/8B, 3B+7B/8B hybrid, larger local models or explicit remote, runs critic cascades, candidate tournaments, style stabilization, anti-generic checks, claim/evidence gates, and returns Candidate Artifacts wrapped in Response Packets.

Apps render and decide.
Apps own apply.
Apps own state.
Apps own external sends.
Apps may later expose their own QIRC/Event systems through digest-only bridges.

Odin consumes digests.
Odin does not own app QIRC.
Odin does not mutate app state.

The Internal Semantic Bus is optional, local-only, inspectable and traceable.
When enabled, it turns Odin from a strong local LLM shell into a living semantic precompute engine.

The canonical model sweet spot remains 3B + 7B/8B hybrid.
Larger models are escalation routes, not the architecture.

Universal in processing.
Bounded in authority.
Candidate-only in output.
Small-model-first in execution.
Native-feeling in apps.
Bus-coordinated internally.
```


# Appendices — Architecture Matrices


## Subsystem-to-Layer Matrix

| Subsystem | Layer | Primary Inputs | Primary Outputs | Hard Boundary |
|---|---|---|---|---|
| Universal Work Kernel | Semantic Core | Universal Work | Compiled Work | No direct model call before validation |
| Internal Semantic Bus | Coordination | Semantic Events | Bus Batches | Local-only, no app mutation |
| Context Distillery | Precompute | Event Digest, Artifacts | Context Capsule | No raw DB by default |
| Slot Forge | Small Model Power | Worklet, Output Contract | Slot Contract | No hidden permissions |
| Model Runtime | Execution | ModelWorkPacket | Model Response | Provider is not authority |
| Candidate Composer | Output | Model Response, Critics | Candidate Artifact | Candidate only |
| Final Gate | Boundary | Candidate, DNA, Evidence | Allow/Downgrade/Block | No overclaims |


## Model Route Decision Matrix

| Task Shape | Default Route | Escalation | Fallback |
|---|---|---|---|
| Label/classify | deterministic/1B/2B/3B | 3B multi | ask_context |
| Short rewrite | 3B micro | 7B/8B | deterministic template |
| Quality section draft | 7B/8B | 3B+7B/8B hybrid | ask_context |
| Complex document | 3B+7B/8B hybrid | 13B/14B quality | split_work |
| Heavy architecture | hybrid | 22B/32B batch | human review |
| High-risk claim | critic cascade | human review | block |


## Bus Channel Responsibility Matrix

| Channel Family | Producer | Consumer | Purpose |
|---|---|---|---|
| #work.* | Universal Work Kernel | System Profile, Trace | work state |
| #context.* | Context Distillery | Slot Forge, Model Router | context capsule |
| #lens.* | Lens Router | Precompute, Slots | artifact interpretation |
| #slot.* | Slot Forge | ModelWorkPacket Builder | bounded model work |
| #model.* | Model Runtime | Critics, Trace | model route/response |
| #critic.* | Critic Cascade | Composer, Gate | candidate checks |
| #candidate.* | Composer | Response Builder | artifact assembly |


# Deep Architecture Appendix — v7.1 Full-System Detail


## A.1 Windows Runtime Layer


**Purpose:** daemon/tray/control center/cli/model runner/worker supervision/resource posture/support bundle.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.2 App Integration Standard


**Purpose:** caller manifest/capability bridge/event digest/context snapshot/universal work builder/candidate renderer/app apply gate.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.3 Local Mediation Protocol


**Purpose:** typed artifacts between app Odin model bus trace candidate.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.4 Universal Work Kernel


**Purpose:** artifact plus verb plus output contract plus constraints plus boundary plus model policy.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.5 Artifact Registry


**Purpose:** typed artifact families trust status privacy classes and lens binding.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.6 Artifact Lens System


**Purpose:** domain/task specific interpretation logic for universal-but-not-generic processing.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.7 Transformation Verb Registry


**Purpose:** semantic action vocabulary and compatibility control.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.8 Output Contract Registry


**Purpose:** candidate output shapes and app-native rendering contracts.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.9 Internal Semantic IRC Bus


**Purpose:** local-only channel/topic/tag/nick/batch/replay event coordination.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.10 Adaptive Precompute Compiler


**Purpose:** deterministic ordering, context, seed, fit, mirror, pressure and work shape.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.11 Small Model Power Layer


**Purpose:** context distillery worklet graph slot forge critics tournaments style anti-generic.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.12 System Palette Compiler


**Purpose:** neutral task/system pattern selector used before model work.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.13 Thor Bridge


**Purpose:** candidate-only handoff/review/receipt structure for code and agent mediation.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.14 Model Runtime


**Purpose:** provider adapters capability cards route ladder model packets responses fallback.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.15 Hybrid Director


**Purpose:** 3B scout/check plus 7B/8B write/synthesis plus Odin gate/compose.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.16 Candidate Artifact Layer


**Purpose:** candidate artifacts response packets render hints actions and candidate DNA.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.17 Claim Evidence Reality Gate


**Purpose:** boundary validation language downgrades blocks and receipts.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.18 Storage Trace Receipt Layer


**Purpose:** SQLite object store cache retention bus replay support bundles.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.19 Control Center Labs


**Purpose:** Universal Work Lab bus view worklet graph model dojo traces registries.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```


## A.20 SDK Templates


**Purpose:** Python/TypeScript/app connector templates with no model logic.


**Inputs:**


```text
caller manifest
binding
universal work or derived internal artifact
event digest
resource posture
privacy policy
active registries
trace context
```


**Outputs:**


```text
validated internal artifact
semantic bus event
trace entry
candidate or intermediate candidate
failure state or route recommendation
updated cache/profile entry where allowed
```


**Must do:**


```text
preserve app authority
preserve candidate-only posture
validate schemas and registries
respect model policy and privacy class
emit traceable decisions
fail closed on missing boundary
remain local-first by default
```


**Must not do:**


```text
mutate app state
send externally
silently escalate remote
promote model output to truth
skip final gate
store raw sensitive payload by default
reinterpret app-owned QIRC as Odin-owned state
```


**Primary acceptance signals:**


```text
positive valid example passes
negative invalid example fails
trace event emitted
schema or registry coverage exists
claim boundary preserved
app-owned apply remains external to Odin
```



# Deep Architecture Appendix — Canonical Flow Catalog


## Flow: Simple Rewrite


**Formula:** `selected markdown -> rewrite verb -> markdown_candidate`  
**Default route:** 3B micro or 7B if quality required.


```text
Validate binding
Resolve artifact lens
Create context capsule
Open semantic bus batch
Build worklet graph if needed
Forge slot
Select model route
Run model or deterministic worker
Run minicheck and critics
Compose candidate
Run final gate
Return response packet
```


**Failure handling:** ask context, split work, downgrade language, retry, escalate within policy, block, or cannot-safely-complete.


## Flow: Document Summary


**Formula:** `document excerpt -> summarize -> summary_candidate`  
**Default route:** 3B for short; 7B/8B for long; split if broad.


```text
Validate binding
Resolve artifact lens
Create context capsule
Open semantic bus batch
Build worklet graph if needed
Forge slot
Select model route
Run model or deterministic worker
Run minicheck and critics
Compose candidate
Run final gate
Return response packet
```


**Failure handling:** ask context, split work, downgrade language, retry, escalate within policy, block, or cannot-safely-complete.


## Flow: Action Card


**Formula:** `workflow_state -> plan/review -> action_card_candidate`  
**Default route:** deterministic + 3B; candidate only.


```text
Validate binding
Resolve artifact lens
Create context capsule
Open semantic bus batch
Build worklet graph if needed
Forge slot
Select model route
Run model or deterministic worker
Run minicheck and critics
Compose candidate
Run final gate
Return response packet
```


**Failure handling:** ask context, split work, downgrade language, retry, escalate within policy, block, or cannot-safely-complete.


## Flow: Code PatchPlan


**Formula:** `repo_context -> plan -> patchplan_candidate`  
**Default route:** Thor bridge + hybrid; no patch apply.


```text
Validate binding
Resolve artifact lens
Create context capsule
Open semantic bus batch
Build worklet graph if needed
Forge slot
Select model route
Run model or deterministic worker
Run minicheck and critics
Compose candidate
Run final gate
Return response packet
```


**Failure handling:** ask context, split work, downgrade language, retry, escalate within policy, block, or cannot-safely-complete.


## Flow: Error Explain


**Formula:** `error_log -> explain -> debug_hypothesis_candidate`  
**Default route:** 3B/7B depending complexity.


```text
Validate binding
Resolve artifact lens
Create context capsule
Open semantic bus batch
Build worklet graph if needed
Forge slot
Select model route
Run model or deterministic worker
Run minicheck and critics
Compose candidate
Run final gate
Return response packet
```


**Failure handling:** ask context, split work, downgrade language, retry, escalate within policy, block, or cannot-safely-complete.


## Flow: Wedding Speech Section


**Formula:** `project digest -> draft -> ceremony_section_candidate`  
**Default route:** 3B extract/check + 7B write.


```text
Validate binding
Resolve artifact lens
Create context capsule
Open semantic bus batch
Build worklet graph if needed
Forge slot
Select model route
Run model or deterministic worker
Run minicheck and critics
Compose candidate
Run final gate
Return response packet
```


**Failure handling:** ask context, split work, downgrade language, retry, escalate within policy, block, or cannot-safely-complete.


## Flow: Game NPC Line


**Formula:** `game_state_digest -> generate_candidate -> npc_line_candidate`  
**Default route:** 3B fast/7B quality.


```text
Validate binding
Resolve artifact lens
Create context capsule
Open semantic bus batch
Build worklet graph if needed
Forge slot
Select model route
Run model or deterministic worker
Run minicheck and critics
Compose candidate
Run final gate
Return response packet
```


**Failure handling:** ask context, split work, downgrade language, retry, escalate within policy, block, or cannot-safely-complete.


## Flow: App QIRC Digest


**Formula:** `bridge digest -> summarize/route -> context capsule`  
**Default route:** bus local digest only.


```text
Validate binding
Resolve artifact lens
Create context capsule
Open semantic bus batch
Build worklet graph if needed
Forge slot
Select model route
Run model or deterministic worker
Run minicheck and critics
Compose candidate
Run final gate
Return response packet
```


**Failure handling:** ask context, split work, downgrade language, retry, escalate within policy, block, or cannot-safely-complete.


## Flow: Low Memory Assist


**Formula:** `event digest -> template/gaptext -> small candidate`  
**Default route:** deterministic/1B/2B/3B.


```text
Validate binding
Resolve artifact lens
Create context capsule
Open semantic bus batch
Build worklet graph if needed
Forge slot
Select model route
Run model or deterministic worker
Run minicheck and critics
Compose candidate
Run final gate
Return response packet
```


**Failure handling:** ask context, split work, downgrade language, retry, escalate within policy, block, or cannot-safely-complete.


## Flow: Heavy Batch Draft


**Formula:** `large doc set -> compose -> document_section_bundle`  
**Default route:** quality/heavy local batch.


```text
Validate binding
Resolve artifact lens
Create context capsule
Open semantic bus batch
Build worklet graph if needed
Forge slot
Select model route
Run model or deterministic worker
Run minicheck and critics
Compose candidate
Run final gate
Return response packet
```


**Failure handling:** ask context, split work, downgrade language, retry, escalate within policy, block, or cannot-safely-complete.



# Deep Architecture Appendix — State Machines


## State Machine: Universal Work


```text
RECEIVED -> VALIDATING -> COMPILED -> PRECOMPUTED -> ROUTED -> EXECUTING -> CHECKING -> COMPOSING -> GATED -> READY|BLOCKED|NEEDS_CONTEXT
```


## State Machine: Semantic Bus


```text
DISABLED -> STARTING -> ACTIVE_LOCAL -> DEGRADED|VERIFICATION_ONLY -> STOPPING -> DISABLED
```


## State Machine: Model Route


```text
UNRESOLVED -> RESOURCE_CHECKED -> POLICY_CHECKED -> ROUTE_SELECTED -> PACKET_BUILT -> RUNNING -> RESPONSE_RECEIVED -> CHECKED -> ACCEPTED|RETRY|ESCALATE|BLOCK
```


## State Machine: Candidate


```text
DRAFTED -> CHECKED -> CRITICIZED -> COMPOSED -> GATED -> RESPONSE_READY|BLOCKED
```


## State Machine: App Bridge


```text
UNPAIRED -> REGISTERING -> MANIFEST_VALIDATED -> BOUND -> ACTIVE -> REVOKED|ERROR
```


# Deep Architecture Appendix — Failure, Degradation, and Resource Modes

## Resource Profile `low_memory_strict`

templates, deterministic routes, semantic bus light, 1B/2B/3B micro; no heavy graph/tournament; short retention; small cache.

```text
Allowed architectural moves:
- reduce context first
- split work where possible
- keep app authority external
- preserve candidate-only output
- emit trace and route reason
Blocked architectural moves:
- silent remote escalation
- final gate bypass
- app mutation
- raw sensitive payload retention
```

## Resource Profile `standard_local`

3B + 7B/8B hybrid default; interactive latency; bus active; standard cache; normal traces.

```text
Allowed architectural moves:
- reduce context first
- split work where possible
- keep app authority external
- preserve candidate-only output
- emit trace and route reason
Blocked architectural moves:
- silent remote escalation
- final gate bypass
- app mutation
- raw sensitive payload retention
```

## Resource Profile `quality_local`

adds 13B/14B route for quality; draft latency; stronger synthesis; more critic passes.

```text
Allowed architectural moves:
- reduce context first
- split work where possible
- keep app authority external
- preserve candidate-only output
- emit trace and route reason
Blocked architectural moves:
- silent remote escalation
- final gate bypass
- app mutation
- raw sensitive payload retention
```

## Resource Profile `heavy_local`

22B/32B or MoE/offload; batch latency; long candidate work; trace-heavy.

```text
Allowed architectural moves:
- reduce context first
- split work where possible
- keep app authority external
- preserve candidate-only output
- emit trace and route reason
Blocked architectural moves:
- silent remote escalation
- final gate bypass
- app mutation
- raw sensitive payload retention
```

## Resource Profile `max_local_batch`

large local/offload; overnight; explicit; not live app UX.

```text
Allowed architectural moves:
- reduce context first
- split work where possible
- keep app authority external
- preserve candidate-only output
- emit trace and route reason
Blocked architectural moves:
- silent remote escalation
- final gate bypass
- app mutation
- raw sensitive payload retention
```

## Resource Profile `remote_optional`

remote only explicit; privacy gates; not default; strong warning and trace.

```text
Allowed architectural moves:
- reduce context first
- split work where possible
- keep app authority external
- preserve candidate-only output
- emit trace and route reason
Blocked architectural moves:
- silent remote escalation
- final gate bypass
- app mutation
- raw sensitive payload retention
```


# Deep Architecture Appendix — Risk Classes

## Risk Class `low_risk_transform`

```text
Required evaluation:
- binding policy
- output contract
- privacy class
- evidence status
- model route policy
- critic cascade need
- candidate renderer shape
- app apply gate requirement
```

## Risk Class `medium_risk_generation`

```text
Required evaluation:
- binding policy
- output contract
- privacy class
- evidence status
- model route policy
- critic cascade need
- candidate renderer shape
- app apply gate requirement
```

## Risk Class `high_risk_claim`

```text
Required evaluation:
- binding policy
- output contract
- privacy class
- evidence status
- model route policy
- critic cascade need
- candidate renderer shape
- app apply gate requirement
```

## Risk Class `code_candidate`

```text
Required evaluation:
- binding policy
- output contract
- privacy class
- evidence status
- model route policy
- critic cascade need
- candidate renderer shape
- app apply gate requirement
```

## Risk Class `public_facing_candidate`

```text
Required evaluation:
- binding policy
- output contract
- privacy class
- evidence status
- model route policy
- critic cascade need
- candidate renderer shape
- app apply gate requirement
```

## Risk Class `privacy_sensitive`

```text
Required evaluation:
- binding policy
- output contract
- privacy class
- evidence status
- model route policy
- critic cascade need
- candidate renderer shape
- app apply gate requirement
```

## Risk Class `action_impacting`

```text
Required evaluation:
- binding policy
- output contract
- privacy class
- evidence status
- model route policy
- critic cascade need
- candidate renderer shape
- app apply gate requirement
```

## Risk Class `external_send_adjacent`

```text
Required evaluation:
- binding policy
- output contract
- privacy class
- evidence status
- model route policy
- critic cascade need
- candidate renderer shape
- app apply gate requirement
```

## Risk Class `schema_strict`

```text
Required evaluation:
- binding policy
- output contract
- privacy class
- evidence status
- model route policy
- critic cascade need
- candidate renderer shape
- app apply gate requirement
```

## Risk Class `creative_quality`

```text
Required evaluation:
- binding policy
- output contract
- privacy class
- evidence status
- model route policy
- critic cascade need
- candidate renderer shape
- app apply gate requirement
```


# Deep Architecture Appendix — Public Repo Philosophy

Odin-Agent-Shell should be readable by developers without Q-internal vocabulary. Internal QIRC/YNode/QFoundation/Q Metamodell/Thor lineage appears only as neutralized architecture patterns: semantic bus, pattern foundry, system palette, bounded handoff, candidate artifacts, claim/evidence gates, and local runtime posture. The public repo should be transparent, implementable, and not dependent on private chat context.

# Deep Architecture Appendix — End-to-End Domain Examples

## Example: Wedding Speech / Ceremony Studio

```text
App selection or project digest
→ Event Digest with couple/story/ritual/no-go/tone fields
→ Wedding Speech Lens
→ Context Capsule with must_use/must_not_use/tone/length
→ Worklet Graph: extract facts, scene bank, red thread, draft section, critic checks
→ 3B: extraction, no-go, genericness, style critic
→ 7B/8B: section drafting and synthesis
→ Candidate Artifact: ceremony_section_candidate with render hints and app-owned actions
→ App decides whether to use/edit/discard
```

Boundary: Odin never publishes a speech, never sends to client, never claims final wording, never overrides human editorial authority.

## Example: Developer PatchPlan

```text
Repo context / error log
→ Code Lens
→ Thor Bridge if handoff/review discipline required
→ Context Capsule with files, error, constraints, forbidden claims
→ Worklet Graph: classify error, isolate probable area, draft patchplan, critic review
→ Candidate Artifact: patchplan_candidate or debug_hypothesis_candidate
```

Boundary: Odin does not apply a patch, does not claim tests passed, and does not claim runtime behavior.

## Example: Low-Memory Strict App Helper

```text
Small event digest
→ deterministic template or 1B/2B/3B micro
→ short action card or summary candidate
→ final gate
```

Boundary: Odin must prefer asking for context or splitting work over trying a broad local generation.

## Example: App-Owned QIRC Digest

```text
App event system emits app-owned digest
→ Odin bridge validates digest-only policy
→ Internal Semantic Bus publishes #app.event_digest
→ Context Distillery consumes digest
→ Candidate Artifact returns to app
```

Boundary: Odin does not mirror the full app bus, does not become app QIRC, and does not publish app mutation events.

# Deep Architecture Appendix — Implementation Boundary Narratives

## Why Odin is not an app framework

Odin provides semantic work infrastructure, not product ownership. An app may use Odin for drafting, review, extraction, classification, explanation or planning, but the app remains the authority for state, domain rules, publishing, payments, accounts, files and external communication. This is what allows Odin to be universal across WordPress plugins, desktop apps, game tools, CLI tools, builder apps and domain-specific studios without swallowing their product logic.

## Why Odin is not just a model router

A simple router chooses a model. Odin designs the work before routing. It reduces semantic pressure, chooses lenses, opens bus batches, builds context capsules, splits work into worklets, forges slot contracts, creates ModelWorkPackets, runs critics and assembles candidates. Model routing is one step inside a larger semantic compiler.

## Why the Internal Semantic Bus matters

The bus turns invisible intermediate reasoning into structured local events. Those events are inspectable, replayable and cacheable. Instead of one broad prompt, Odin can publish `#context.distill`, `#lens.select`, `#slot.forge`, `#model.route`, `#critic.claim` and `#candidate.compose` events. This allows many deterministic and tiny-model operations to happen before the quality model is called. The bus is therefore a performance, traceability and coordination layer rather than a user-facing chat surface.

## Why the 3B + 7B/8B hybrid remains the sweet spot

The 3B model is best treated as a fleet of narrow specialists: extractor, router, compressor, schema repairer, no-go checker, claim critic, style critic and genericness critic. The 7B/8B model is best treated as writer, synthesizer and quality worker. Odin provides the compiler, slots, bus, gates and candidate composer. This division gives better practical value than forcing a single larger model into every task.

## Why bigger models are routes, not the architecture

13B/14B, 22B/32B, MoE/offload and 70B-class models can be useful. They should be explicit quality/heavy/batch routes selected by resource profile, latency target, privacy policy and task pressure. They should not replace the small-model-first architecture because model scale alone does not provide app authority, output contracts, event digests, traceability, candidate DNA, semantic bus coordination or claim/evidence gates.

## Why candidate-only output is non-negotiable

Candidate-only output keeps Odin safe and reusable. The same Candidate Artifact can be rendered in a chat UI, document editor, code-review panel, game editor, workflow dashboard or WordPress admin screen. The app chooses whether to apply it. This makes Odin useful without making it dangerous or app-specific.

## Why app-owned QIRC stays app-owned

If a future app has its own QIRC or event system, it is part of the app's domain runtime. Odin may consume digest-only bridge artifacts to improve context and precompute. It may not become that app's bus, mirror all events, or publish state mutation events. This keeps integration powerful without collapsing system boundaries.

# Deep Architecture Appendix — Boundary Decision Table

| Situation | Odin action | Must not do |
|---|---|---|
| User asks app to improve selected text | Return rewrite candidate | overwrite app text directly |
| App asks for workflow next step | Return action card candidate | execute workflow action |
| Code error is provided | Return debug hypothesis or patchplan candidate | apply patch or claim build result |
| Context is too broad | Split work or ask app for context | send giant raw prompt |
| Local model is weak | Tighten slot or route smaller work | silently claim high confidence |
| Remote would help | request explicit route permission | silently send data remotely |
| App QIRC digest arrives | consume digest and precompute | mirror full app bus |
| Bus event contains sensitive data | redact/block based on privacy class | persist raw secret |
| Candidate lacks evidence | downgrade/block/ask context | present as verified fact |
| Heavy model is available | use only if route policy and latency mode allow | make heavy route default |

# Deep Architecture Appendix — Architecture Completion Criteria

A future implementation can be considered aligned with this architecture only if all of the following are true:

```text
- app templates contain no model providers or routers
- Universal Work validation fails closed
- Semantic Bus is local-only by default
- ModelWorkPackets are the only model input path
- Candidate Artifacts are the only app-facing AI output path
- Final Gate runs after model output and after cache hits
- 3B + 7B/8B hybrid route exists as default sweet spot
- larger model routes are explicit escalations
- low_memory_strict mode works without GPU assumptions
- app QIRC bridge is digest-only by default
- traces link work, bus batch, slots, models, critics and candidate DNA
- no unsupported runtime/security/deploy/test/apply claims are emitted
```

# Deep Architecture Appendix — Final Implementation North Star

The north star for every implementation decision is: make independent apps feel as if they have excellent native AI, while keeping all model/runtime/precompute/boundary complexity inside Odin and all product authority inside the app. If a proposed implementation makes apps smarter by adding model logic to apps, it is wrong. If it makes Odin more powerful by taking app authority, it is wrong. If it improves small models by giving them smaller, cleaner, typed, bounded work, it is right.

This means Odin's architecture is complete only when the smallest sufficient worker can be selected, explained, traced, checked, composed into a candidate, and returned without app-authority leakage. The model is a worker. The app is the product. Odin is the semantic operating layer between them.


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

# v0.4.2 Senior Review Hardening

## Senior Review Canon

v0.4.2 adds a senior-review anti-drift layer to the v7.1 architecture. The architecture remains unchanged in its core: Universal Work Kernel, Small Model Power Layer, Internal Semantic IRC Bus, Model Scale Ladder, app-owned state/apply, candidate-only output, and 3B + 7B/8B hybrid sweet spot.

The new rule is procedural and architectural:

```text
Every future change must update both implementation surfaces and canon surfaces.
```

That means architecture/specs, schemas, registries, internal PR ladder, real PR bundles, tests, gates, SYSTEM_MAP and FILE_MANIFEST move together.

## Senior Review Additions

The following docs are part of the architecture canon:

```text
docs/reviews/SENIOR_REVIEW_SIMULATION_V0_4_2.md
docs/SENIOR_REVIEW_REMEDIATION_PLAN_V0_4_2.md
docs/CODEX_ANTI_DRIFT_POLICY.md
docs/TRACEABILITY_MATRIX_V7_1.md
docs/QUALITY_RISK_REGISTER_V7_1.md
docs/SEMANTIC_BUS_RED_LINES_V7_1.md
docs/PUBLIC_REPO_RELEASE_CHECKLIST_V7_1.md
```

## Senior Review Invariant

```text
Complexity is allowed only while authority remains bounded.
```

This invariant specifically protects the Internal Semantic IRC Bus, larger model escalation routes, provider adapters, SDK templates and Control Center surfaces.


# v0.5.0 Shadow Runtime Lock Addendum

Odin Agent Shell v7.1 now includes a code-near Shadow Runtime layer. This layer is non-executing and non-authoritative. It exists to make Codex implementation nearly mechanical by mapping contracts to shadow types, functions, fixtures, tests and future real target files. It is inspired by the YNode-prep Shadow Runtime discipline while remaining Odin-neutral and scoped to Universal Work, Candidate Artifacts, Internal Semantic Bus, Small Model Power, Model Scale Ladder and app-owned apply boundaries. The canonical task is PR-23 and the real Codex bundle is REAL-PR-09. Any future architecture-to-code mapping change must update the Shadow Runtime package, docs, fixtures, registries, tests, internal PR ladder and real PR bundle layer.


---

## v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE

This release extends the Shadow Runtime from central spine coverage to full major-subsystem coverage. Every future addition must update the architecture/specs, internal PR ladder, REAL-PR bundles, registries, System Map, tests and FILE_MANIFEST. The Shadow Runtime remains candidate-only, local-only, non-authoritative and non-executing.

New coverage includes Artifact Lenses, Context Distillery, Worklet/Slot/Gaptext, Candidate Tournament, Low-Memory Strict Mode, Thor Bridge, Bounded Code Work, Storage/Trace/Receipt, Local API, App-QIRC Digest Bridge, Model Dojo, Security Redaction, Support Bundle, Windows Runtime and SDK/App Template validation.

# v0.5.2 Shadow Runtime Near-Final Addendum

The Shadow Runtime is now treated as the near-final mechanical blueprint for Odin Agent Shell. It covers not only subsystem contracts but the full end-to-end orchestration shape: policy, resource posture, universal work, semantic bus, context, worklets, model routing, provider planning, candidate tournament, candidate output, trace, support bundle and Windows runtime planning. This remains non-authoritative and non-executing. The real runtime must be built by preserving this sequence and replacing shadow projections with validated implementations.


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

# v0.6.5 — PRE_LLM_INTELLIGENCE_AMPLIFICATION_LOCK

Odin v7.1 now includes a consolidated Pre-LLM Intelligence Layer. This layer preserves all prior v7.1 contracts and adds the explicit rule that Odin should perform every safe deterministic, symbolic, QIRC, seed, archetype, QMath, DFAS, runtime-pack, template, cache, gate and output-composition operation before invoking a model.

## Architectural Addition
Pre-LLM Intelligence sits before ModelWorkPacket dispatch:

```text
Universal Work → Binding Gate → QIRC Hot Window → Seed/Archetype Prewarm → DFAS Admissibility → QMath Route Score → Model Work Avoidance → Slot Forge → Model Dispatch only if needed → Output Intelligence Composer
```

## Core Purpose
The layer is designed for all model sizes, not only 3B. It makes 1B/3B useful, stabilizes 7B/8B, improves 13B/14B efficiency, and prevents 30B/70B waste by using large models only for high-value synthesis.

## User-Visible Intelligence
Odin may make small models feel significantly more capable only by actually doing more non-model work: context hot windows, seed pruning, archetype roles, route scoring, candidate composition, and Why Trace. It may not fake verification, execution, testing, apply, or external send.

## New Red Line
Perceived intelligence must be truthful orchestration, not deceptive presentation.


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
