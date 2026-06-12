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
