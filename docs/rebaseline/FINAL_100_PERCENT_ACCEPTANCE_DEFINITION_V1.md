# Final 100 Percent Acceptance Definition v1

Artifact id: `final_100_percent_acceptance_definition_v1`.

Claim boundary: `planning_audit_only_not_runtime_provider_network_target_host_security_release_or_model_quality_proof`. This artifact is a repo-real planning/audit artifact only. It does not start runtime, run providers, call models, call network, read secrets, mutate app state, certify security, certify release status, prove target hosts, or prove live model quality.

Supersedes and source references are machine-readable in the matching registry.

## Must Pass

- `clone_or_download_path_documented`
- `install_path_documented_and_tested`
- `one_start_command_works_with_local_receipt`
- `localhost_runtime_starts_with_receipt`
- `browser_hub_opens_or_is_reachable_with_receipt`
- `normal_user_status_understandable`
- `model_picker_works_with_mock_and_local_candidate_providers`
- `connected_apps_panel_works`
- `demo_generic_app_bridge_works`
- `universal_work_demo_works`
- `candidate_artifact_and_response_packet_visible`
- `activity_feed_visible`
- `trace_receipt_proof_gaps_visible_in_dev_mode`
- `support_bundle_works`
- `validate_all_passes`
- `golden_flow_passes`
- `full_acceptance_local_receipt_passes`
- `non_goals_remain_non_claims`
- `qirc_core_localhost_only_receipt`
- `qirc_semantic_channels_registered`
- `qirc_browser_event_bridge_receipt`
- `qirc_app_bridge_event_mapping_receipt`
- `qirc_file_spool_packet_bridge_receipt`
- `qirc_cli_agent_pipe_bridge_receipt`
- `qirc_trace_receipt_channel_mapping_receipt`
- `qirc_dev_mode_event_viewer_visible`

## Must Be Visible

- Home status
- Models picker
- Apps connections
- Activity timeline
- Dev Mode traces receipts proof gaps validators support bundle raw JSON
- QIRC event status in Dev Mode
- QIRC channel/event viewer in Dev Mode
- Trace/receipt channel mapping
- App/agent packet flow status

## Not Mandatory For 100 Percent

- `windows_service_tray_installer`
- `signed_release`
- `store_distribution`
- `production_readiness`
- `security_certification`
- `public_network_api`
- `live_model_quality_proof`
- `specific_external_app_integration`
- `external_sends`
- `app_state_mutation`
- `public_irc_network`
- `lan_wan_qirc`
- `federation`
- `matrix_like_platform`
- `activitypub_xmpp_public_network`
- `external_broker_dependency`

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

## v1 Amendment: FINAL-PR-06..09 Preparation Acceptance Items

The acceptance definition now recognizes that full Release / Closure moves to FINAL-PR-09, after FINAL-PR-06 Operational Seed Spine, FINAL-PR-07 Field Selection / Coherence / Review Axes, and FINAL-PR-08 Projection Spine / Expression Packet / Shadow Candidate Graph.

Preparation acceptance items added:

- `operational_seed_spine_prepared`
- `field_selection_spine_prepared`
- `projection_spine_prepared`
- `final_pr_06_claude_prompt_ready`
- `final_pr_07_claude_prompt_ready`
- `final_pr_08_claude_prompt_ready`
- `final_pr_09_release_prompt_skeleton_ready`
- `release_closure_shifted_to_final_pr_09`

These items are preparation criteria only. They do not mark PR06, PR07, PR08, or PR09 complete and do not claim runtime, provider/model, public network, app authority, production readiness, or security certification proof.
