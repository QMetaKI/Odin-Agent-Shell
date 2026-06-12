# Final Local Runtime Hub Target v1

Artifact id: `final_local_runtime_hub_target_v1`.

Claim boundary: `planning_audit_only_not_runtime_provider_network_target_host_security_release_or_model_quality_proof`. This artifact is a repo-real planning/audit artifact only. It does not start runtime, run providers, call models, call network, read secrets, mutate app state, certify security, certify release status, prove target hosts, or prove live model quality.

Supersedes and source references are machine-readable in the matching registry.

## Target

Odin is a local background engine / Local Runtime Hub. Normal users start Odin, choose model(s), connect apps, and see status. Apps do the real app UX. Odin handles candidate work, routing, precompute, traces, receipts, proof gaps, and local API/bridge behavior. Dev Mode exposes diagnostics and raw evidence.

## Normal User Path

Odin is a local background engine / Local Runtime Hub. Normal users clone or download it, run one simple start command, open or are given a localhost Browser Hub, see status, choose model/provider modes, connect apps, submit demo Universal Work, receive Candidate Artifacts / Response Packets, read plain-language activity, and stop cleanly.

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
