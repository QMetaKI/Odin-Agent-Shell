# Final Minimal Road-to-100 PR Roadmap v1

Artifact id: `final_minimal_road_to_100_pr_roadmap_v1`.

Claim boundary: `planning_audit_only_not_runtime_provider_network_target_host_security_release_or_model_quality_proof`. This artifact is a repo-real planning/audit artifact only. It does not start runtime, run providers, call models, call network, read secrets, mutate app state, certify security, certify release status, prove target hosts, or prove live model quality.

Supersedes and source references are machine-readable in the matching registry.

Recommended final follow-up PR count: 5. This stays inside the preferred maximum and avoids unsafe megadiffs.

## QIRC Roadmap Statement

QIRC Core is mandatory for 100%. Browser bridge, SDK/App event mapping, File/Spool, CLI/Agent Pipe, Trace/Receipt mapping, and Dev Mode event viewer are mandatory for the final Local Runtime Hub target. Feed/thread/discovery/pubsub/federation rings are optional/deferred.

## FINAL-PR-01: Simple Local Hub Start + Normal User Browser UI

- Goal: Absorb simple_local_hub_start, browser_hub_normal_user_ui, docs_quickstart_polish into a reviewable final follow-up PR. Include low-risk static affordance for QIRC status only.
- Slices absorbed: simple_local_hub_start, browser_hub_normal_user_ui, docs_quickstart_polish, qirc_status_placeholder
- Proof commands: python -m odin.cli validate-all, PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- Success criteria: simple_local_hub_start has implementation or explicit non-goal proof boundary, browser_hub_normal_user_ui has implementation or explicit non-goal proof boundary, docs_quickstart_polish has implementation or explicit non-goal proof boundary, QIRC boundaries preserved: localhost-only default, no public rooms/network/federation, no app apply/state/external-send, no Final Gate bypass, no Receipt truth elevation
- Non-goals: no provider/model execution unless explicitly configured and receipted, no app state mutation, no app apply authority, no external-send authority, no hidden remote fallback
- Merge order: 1

## FINAL-PR-02: Model Picker + Connected Apps + Demo Universal Work

- Goal: Absorb model_picker_provider_status, connected_apps_bridge_view, demo_universal_work_flow into a reviewable final follow-up PR.
- Slices absorbed: model_picker_provider_status, connected_apps_bridge_view, demo_universal_work_flow, qirc_app_bridge_event_mapping
- Proof commands: python -m odin.cli validate-all, PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- Success criteria: model_picker_provider_status has implementation or explicit non-goal proof boundary, connected_apps_bridge_view has implementation or explicit non-goal proof boundary, demo_universal_work_flow has implementation or explicit non-goal proof boundary, QIRC boundaries preserved: localhost-only default, no public rooms/network/federation, no app apply/state/external-send, no Final Gate bypass, no Receipt truth elevation
- Non-goals: no provider/model execution unless explicitly configured and receipted, no app state mutation, no app apply authority, no external-send authority, no hidden remote fallback
- Merge order: 2

## FINAL-PR-03: Activity, Trace, Receipt, Dev Mode + Support Bundle

- Goal: Absorb activity_trace_receipt_view, dev_mode_diagnostics into a reviewable final follow-up PR.
- Slices absorbed: activity_trace_receipt_view, dev_mode_diagnostics, qirc_core_local_irc_runtime, qirc_semantic_channel_registry, qirc_browser_event_bridge, qirc_trace_receipt_event_mapping, qirc_dev_mode_event_viewer
- Proof commands: python -m odin.cli validate-all, PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- Success criteria: activity_trace_receipt_view has implementation or explicit non-goal proof boundary, dev_mode_diagnostics has implementation or explicit non-goal proof boundary, QIRC boundaries preserved: localhost-only default, no public rooms/network/federation, no app apply/state/external-send, no Final Gate bypass, no Receipt truth elevation
- Non-goals: no provider/model execution unless explicitly configured and receipted, no app state mutation, no app apply authority, no external-send authority, no hidden remote fallback
- Merge order: 3

## FINAL-PR-04: Runtime Security Smoke + Target Host Smoke + Local Provider Probe

- Goal: Absorb runtime_security_smoke, target_host_smoke, local_provider_probe into a reviewable final follow-up PR.
- Slices absorbed: runtime_security_smoke, target_host_smoke, local_provider_probe, qirc_file_spool_packet_bridge, qirc_cli_agent_pipe_bridge
- Proof commands: python -m odin.cli validate-all, PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- Success criteria: runtime_security_smoke has implementation or explicit non-goal proof boundary, target_host_smoke has implementation or explicit non-goal proof boundary, local_provider_probe has implementation or explicit non-goal proof boundary, QIRC boundaries preserved: localhost-only default, no public rooms/network/federation, no app apply/state/external-send, no Final Gate bypass, no Receipt truth elevation
- Non-goals: no provider/model execution unless explicitly configured and receipted, no app state mutation, no app apply authority, no external-send authority, no hidden remote fallback
- Merge order: 4

## FINAL-PR-05: Final Acceptance Cleanup, Docs, Packaging Polish

- Goal: Absorb final_acceptance_cleanup into a reviewable final follow-up PR.
- Slices absorbed: final_acceptance_cleanup, final_qirc_cluster_receipts
- Proof commands: python -m odin.cli validate-all, PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- Success criteria: final_acceptance_cleanup has implementation or explicit non-goal proof boundary, QIRC boundaries preserved: localhost-only default, no public rooms/network/federation, no app apply/state/external-send, no Final Gate bypass, no Receipt truth elevation
- Non-goals: no provider/model execution unless explicitly configured and receipted, no app state mutation, no app apply authority, no external-send authority, no hidden remote fallback
- Merge order: 5

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

## v1 Amendment: FINAL-PR-06..09 Operational Seed / Field Selection / Projection Shift

This amendment moves Release / Closure from FINAL-PR-05 follow-up framing to FINAL-PR-09 because repo-real review found three deterministic preparation layers that should land before full acceptance.

- FINAL-PR-06: Operational Seed Spine + Role Profiles + Seed-to-Work-Capsule Compiler.
- FINAL-PR-07: DFAS Field Selection + Coherence / Review Axes + Route Scoring.
- FINAL-PR-08: Projection Spine + Expression Packet + Shadow Candidate Graph.
- FINAL-PR-09: Release / Closure / Full Acceptance.

Acceptance items added for preparation, not completion:

- `operational_seed_spine_prepared`
- `field_selection_spine_prepared`
- `projection_spine_prepared`
- `final_pr_06_claude_prompt_ready`
- `final_pr_07_claude_prompt_ready`
- `final_pr_08_claude_prompt_ready`
- `final_pr_09_release_prompt_skeleton_ready`
- `release_closure_shifted_to_final_pr_09`

Non-claims: PR06..09 are not complete in this prep PR. This amendment does not add provider/model execution, public network, app apply/state/external-send authority, production readiness, security certification, religious interpretation, source-pattern runtime import, or hidden authority.
