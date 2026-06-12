# Final Local Runtime Hub Target v1

Artifact id: `final_local_runtime_hub_target_v1`.

Claim boundary: `planning_audit_only_not_runtime_provider_network_target_host_security_release_or_model_quality_proof`. This artifact is a repo-real planning/audit artifact only. It does not start runtime, run providers, call models, call network, read secrets, mutate app state, certify security, certify release status, prove target hosts, or prove live model quality.

Supersedes and source references are machine-readable in the matching registry.

## Target

Odin is a local background engine / Local Runtime Hub. Normal users clone or download it, run one simple start command, open or are given a localhost Browser Hub, see status, choose model/provider modes, connect apps, submit demo Universal Work, receive Candidate Artifacts / Response Packets, read plain-language activity, and stop cleanly.

## QIRC Cognitive Substrate Cluster

QIRC is the local IRC-centered coordination core of Odin. In the narrow technical sense, QIRC Core means a localhost-only IRC/QIRC-compatible server/runtime, a semantic Odin channel registry, local event routing, and worker/model/app/candidate/trace/receipt/proof-gap channels. In the broader Odin sense, QIRC means QIRC Core plus a local cognitive substrate cluster: File/Spool, CLI/Pipe, Browser Events, SDK/App Bridge, Trace/Receipt channels, and Dev Mode visibility. These surrounding systems are KI-ohne-KI support substrates, not LLMs. They support local LLMs indirectly by providing context structure, durable work queues, thread/history continuity, source intake, handoff packet flow, event routing, replay, traceability, receipts, proof gaps, and app/agent bridge packet exchange. Required formula: QIRC coordinates. Odin gates. Apps decide. Models work only as bounded workers.

### Hard Boundaries

- localhost-only by default
- no public rooms by default
- no LAN/WAN/federation by default
- no public network API claim
- no app apply authority
- no app-state mutation authority
- no external-send authority
- no Final Gate bypass
- no Receipt truth elevation
- no provider/model authority
- no hidden remote fallback
- no security certification
- no production network claim

## Dev Mode

Dev Mode exposes traces, receipts, proof gaps, validators, support bundle output, and raw JSON without granting apply, app-state, external-send, provider, or model authority.

## Q-Shabang / KI ohne KI / LLM-agent target

Preserve Q-Shabang: Universal Work, Candidate Law, QIRC/Semantic Bus, Context Distillery, Worklets, Slot Forge, Gaptext, critics, gates, receipts, Thor handoff discipline, and QoOO-style smallest sufficient worker routing.

Deterministic precompute, cache, rules, slots, contracts, validators, critics, and gates should shape work before model execution and remain visible enough that normal users and developers can see why model work was avoided or bounded.

LLMs and agents should receive bounded ModelWorkPackets, context capsules, route decisions, receipt boundaries, and candidate-only response contracts so 3B/7B/8B local models and advisory agents have more useful leverage without authority creep.

## Non-goals

- complex app builder
- Windows service/tray/installer as mandatory 100% criterion
- signed release
- store distribution
- public network API
- specific external app integration
- external sends
- app state mutation
- live model quality proof
- public IRC networks by default
- LAN/WAN/federation as mandatory target
- Matrix-like platform behavior
- ActivityPub/XMPP public network behavior
- external broker dependency

## Handoff-First Pre-Intake Layer

Handoff-First Pre-Intake Layer = Odin's first orientation layer for every raw input. It converts raw app/user/file/agent/QIRC/demo input into a structured Handoff Context before Universal Work compilation. A Handoff Context captures intent, task shape, source context, relevant artifacts, constraints, allowed outputs, forbidden actions, privacy boundary, model policy hints, expected candidate shape, proof/receipt expectations, return contract, known gaps, and handoff profile. It improves local LLM performance by reducing prompt chaos and producing better Universal Work and ModelWorkPackets.

Required formula: **Handoff orients. Universal Work bounds. Odin gates. QIRC coordinates. Apps decide. Models work only as bounded workers.**

Plain answer: Handoff-First is mandatory for the final target. It is the first normalization layer before Universal Work and ModelWorkPacket creation. It supports local LLM performance by reducing prompt chaos and producing structured, bounded work packets. Thor profile is mandatory. Generic profile is mandatory. Y and Mjölnir profiles are structured handoff dialect targets, not external runtime claims.

Repo-reality findings:

- Thor compiler/adapter: repo evidence exists in `docs/HANDOFF_POSTPROCESSING_CANDIDATE_PIPELINE_V7_1.md`, `odin/shadow_runtime/thor_handoff_compiler_shadow.py`, `registries/thor_handoff_mode_registry.json`, and Thor handoff docs; current status is partially implemented/candidate-only, without external Thor runtime proof.
- Generic profile: target concept added by this PR as schema/doc/roadmap coverage; implementation receipt remains a final roadmap slice.
- Thor profile: mandatory profile with docs/schema/shadow evidence; implementation proof remains future scoped work.
- Y profile: structured profile contract using existing Y handoff bridge evidence where present; not Y-node runtime proof.
- Mjölnir profile: structured focused patch/build/engine-prep profile contract using existing Mjölnir shadow/schema evidence where present; not Godot, Windows, target-host, engine, or external runtime proof.
- Handoff mapping: Handoff Context precedes Universal Work, then maps to Context Capsule, ModelWorkPacket, QIRC channels, Trace/Receipts, Final Gate expectations, Candidate Artifact/Response Packet, and app-owned decision.
- Dev Mode visibility: planned Dev Mode Handoff Viewer shows Handoff Context, profile, and Handoff → Universal Work → ModelWorkPacket → QIRC/Trace/Receipt mapping; normal user UI remains limited to prepared, candidate-ready, blocked, and needs context.

Roadmap placement: FINAL-PR-02 carries Handoff-First policy, generic profile, and handoff-to-Universal-Work mapping. FINAL-PR-03 carries QIRC/Trace/Receipt mapping and Dev Mode Handoff Viewer. FINAL-PR-04 carries Thor/Y/Mjölnir profile contracts and file/spool/CLI/agent handoff intake. FINAL-PR-05 carries final acceptance/docs cleanup. Final PR count remains 5.

Non-claims: this audit amendment does not implement runtime behavior, does not call providers or models, does not execute network/API-key paths, does not grant app apply/state/external-send authority, does not bypass Universal Work or Final Gate, and does not claim external Thor/Y/Y-node/Mjölnir/Godot/Windows/engine runtime proof.
