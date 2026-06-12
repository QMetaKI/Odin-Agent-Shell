#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DOCS = [
    "docs/rebaseline/FINAL_LOCAL_RUNTIME_HUB_TARGET_V1.md",
    "docs/rebaseline/FINAL_REPO_REALITY_GAP_AUDIT_V1.md",
    "docs/rebaseline/FINAL_Q_SHABANG_CAPABILITY_MATRIX_V1.md",
    "docs/rebaseline/FINAL_BUILDABLE_SLICE_CATALOG_V1.md",
    "docs/rebaseline/FINAL_MINIMAL_ROAD_TO_100_PR_ROADMAP_V1.md",
    "docs/rebaseline/FINAL_100_PERCENT_ACCEPTANCE_DEFINITION_V1.md",
    "docs/codex/audits/PR_35_B9_FINAL_ROAD_TO_100_AUDIT.md",
    "docs/codex/reports/PR_35_B9_FINAL_ROAD_TO_100_RETURN_REPORT.md",
]
SCHEMAS = [
    "schemas/final_local_runtime_hub_target_v1.schema.json",
    "schemas/final_repo_reality_gap_audit_v1.schema.json",
    "schemas/final_q_shabang_capability_matrix_v1.schema.json",
    "schemas/final_buildable_slice_catalog_v1.schema.json",
    "schemas/final_minimal_road_to_100_pr_roadmap_v1.schema.json",
    "schemas/final_100_percent_acceptance_definition_v1.schema.json",
]
REGISTRIES = [
    "registries/final_local_runtime_hub_target_v1.json",
    "registries/final_repo_reality_gap_audit_v1.json",
    "registries/final_q_shabang_capability_matrix_v1.json",
    "registries/final_buildable_slice_catalog_v1.json",
    "registries/final_minimal_road_to_100_pr_roadmap_v1.json",
    "registries/final_100_percent_acceptance_definition_v1.json",
]
EXAMPLES = [
    "examples/final_local_runtime_hub_target_v1.example.json",
    "examples/final_repo_reality_gap_audit_v1.example.json",
    "examples/final_q_shabang_capability_matrix_v1.example.json",
    "examples/final_buildable_slice_catalog_v1.example.json",
    "examples/final_minimal_road_to_100_pr_roadmap_v1.example.json",
    "examples/final_100_percent_acceptance_definition_v1.example.json",
]
REPORTS = ["reports/final_road_to_100_rebaseline_audit_v1.json"]
REQUIRED_TARGET_KEYS = [
    "normal_user_target", "dev_mode_target", "q_shabang_target", "ki_ohne_ki_target",
    "llm_agent_target", "runtime_target", "ui_target", "model_picker_target",
    "connected_apps_target", "candidate_workflow_target", "proof_gap_target",
]
REQUIRED_GAP_IDS = [
    "clone_install_path", "one_command_start", "localhost_runtime_api", "browser_hub_ui",
    "model_picker", "multiple_models", "provider_status", "connected_apps_view", "app_bridge",
    "sdk_bridge", "universal_work_submit", "candidate_artifact_response", "response_packet_view",
    "activity_feed", "trace_viewer", "receipt_viewer", "proof_gap_viewer", "support_bundle",
    "dev_mode_toggle", "local_provider_probe", "mock_provider", "ollama_candidate",
    "llama_cpp_candidate", "no_remote_fallback", "qirc_semantic_bus",
    "worklet_slot_gaptext_visibility", "ki_ohne_ki_precompute_visibility",
    "agent_operator_mode", "thor_compatibility", "golden_flow",
    "full_acceptance_local_receipt", "security_static_review", "runtime_security_review",
    "target_host_review", "dependency_tooling", "release_package", "windows_convenience",
    "normal_user_docs",
]
VALID_STATUSES = {
    "implemented_and_locally_proven", "implemented_without_recent_local_proof", "partially_implemented",
    "schema_or_doc_only", "missing", "deferred_non_goal", "blocked_pending_decision",
    "cannot_determine_from_repo",
}
REQUIRED_Q_IDS = [
    "ki_ohne_ki", "universal_work", "candidate_artifacts", "response_packets", "qirc_semantic_bus",
    "context_distillery", "lenses", "worklets", "slot_forge", "gaptext", "modelworkpacket",
    "smallest_sufficient_worker", "3b_7b_hybrid_route_roles", "critic_cascade", "tournament",
    "candidate_dna", "final_gate_advisory", "receipt_boundary", "receipt_ledger", "trace_records",
    "provider_policy", "local_provider_seam", "thor_handoff", "thor_pack_intake", "sdk_app_bridge",
    "security_review_track", "local_runtime_hub_ui", "app_connections", "dev_mode",
]
REQUIRED_SLICE_FAMILIES = [
    "simple_local_hub_start", "browser_hub_normal_user_ui", "model_picker_provider_status",
    "connected_apps_bridge_view", "demo_universal_work_flow", "activity_trace_receipt_view",
    "dev_mode_diagnostics", "runtime_security_smoke", "target_host_smoke", "local_provider_probe",
    "final_acceptance_cleanup", "docs_quickstart_polish",
]
REQUIRED_POSITIVE = [
    "clone_or_download_path_documented", "install_path_documented_and_tested",
    "one_start_command_works_with_local_receipt", "localhost_runtime_starts_with_receipt",
    "browser_hub_opens_or_is_reachable_with_receipt", "normal_user_status_understandable",
    "model_picker_works_with_mock_and_local_candidate_providers", "connected_apps_panel_works",
    "demo_generic_app_bridge_works", "universal_work_demo_works",
    "candidate_artifact_and_response_packet_visible", "activity_feed_visible",
    "trace_receipt_proof_gaps_visible_in_dev_mode", "support_bundle_works",
    "validate_all_passes", "golden_flow_passes", "full_acceptance_local_receipt_passes",
    "non_goals_remain_non_claims",
]
REQUIRED_NON_GOALS = [
    "windows_service_tray_installer", "signed_release", "store_distribution", "production_readiness",
    "security_certification", "public_network_api", "live_model_quality_proof",
    "specific_external_app_integration", "external_sends", "app_state_mutation",
]
FORBIDDEN_MANIFEST_PARTS = [".thor/", ".odin_runtime/", "__pycache__", ".pytest_cache", "dist/", "build/", "egg-info", ".pyc"]

REQUIRED_QIRC_GAP_IDS = [
    "qirc_core_local_irc_server", "qirc_semantic_channel_registry", "qirc_browser_event_bridge",
    "qirc_sdk_app_event_mapping", "qirc_file_spool_bridge", "qirc_cli_agent_pipe_bridge",
    "qirc_trace_receipt_channel_mapping", "qirc_dev_mode_event_viewer", "qirc_cognitive_substrate_cluster",
]
OPTIONAL_QIRC_GAP_IDS = [
    "qirc_feed_source_intake", "qirc_thread_archive", "qirc_local_discovery",
    "qirc_lightweight_pubsub_adapter", "qirc_federation_future",
]
REQUIRED_QIRC_SLICE_FAMILIES = [
    "qirc_core_local_irc_runtime", "qirc_semantic_channel_registry", "qirc_browser_event_bridge",
    "qirc_app_bridge_event_mapping", "qirc_file_spool_packet_bridge", "qirc_cli_agent_pipe_bridge",
    "qirc_trace_receipt_event_mapping", "qirc_dev_mode_event_viewer",
]
REQUIRED_QIRC_POSITIVE = [
    "qirc_core_localhost_only_receipt", "qirc_semantic_channels_registered",
    "qirc_browser_event_bridge_receipt", "qirc_app_bridge_event_mapping_receipt",
    "qirc_file_spool_packet_bridge_receipt", "qirc_cli_agent_pipe_bridge_receipt",
    "qirc_trace_receipt_channel_mapping_receipt", "qirc_dev_mode_event_viewer_visible",
]
REQUIRED_QIRC_VISIBLE = [
    "QIRC event status in Dev Mode", "QIRC channel/event viewer in Dev Mode",
    "Trace/receipt channel mapping", "App/agent packet flow status",
]
REQUIRED_QIRC_NON_GOALS = [
    "public_irc_network", "lan_wan_qirc", "federation", "matrix_like_platform",
    "activitypub_xmpp_public_network", "external_broker_dependency",
]

REQUIRED_HANDOFF_GAP_IDS = [
    "handoff_first_pre_intake_policy", "handoff_context_schema", "handoff_packet_candidate_shape",
    "generic_handoff_profile", "thor_handoff_profile", "y_handoff_profile", "mjolnir_handoff_profile",
    "thor_handoff_compiler_discovery", "handoff_to_universal_work_mapping",
    "handoff_to_context_capsule_mapping", "handoff_to_modelworkpacket_mapping",
    "handoff_to_qirc_channel_mapping", "handoff_to_trace_receipt_mapping",
    "handoff_to_final_gate_expectation_mapping", "dev_mode_handoff_viewer",
    "normal_user_handoff_hidden_status",
]
REQUIRED_HANDOFF_Q_IDS = [
    "handoff_first_pre_intake_policy", "handoff_context_schema", "generic_handoff_profile",
    "thor_handoff_profile", "y_handoff_profile", "mjolnir_handoff_profile",
    "thor_handoff_compiler_discovery", "handoff_to_universal_work_mapping",
    "handoff_to_modelworkpacket_mapping", "handoff_to_qirc_channel_mapping",
    "handoff_to_trace_receipt_mapping", "dev_mode_handoff_viewer",
]
REQUIRED_HANDOFF_SLICE_FAMILIES = [
    "handoff_first_pre_intake_policy", "handoff_context_schema_and_profiles",
    "thor_handoff_compiler_adapter", "y_mjolnir_handoff_profiles",
    "handoff_to_universal_work_mapping", "handoff_to_modelworkpacket_mapping",
    "handoff_qirc_trace_receipt_mapping", "dev_mode_handoff_viewer",
]
REQUIRED_HANDOFF_POSITIVE = [
    "handoff_first_pre_intake_policy_defined", "handoff_context_schema_defined",
    "generic_handoff_profile_receipt", "thor_handoff_profile_receipt",
    "handoff_to_universal_work_mapping_receipt", "handoff_to_modelworkpacket_mapping_receipt",
    "handoff_to_qirc_channel_mapping_receipt", "handoff_to_trace_receipt_mapping_receipt",
    "dev_mode_handoff_viewer_visible", "y_handoff_profile_contract_defined",
    "mjolnir_handoff_profile_contract_defined",
]
REQUIRED_HANDOFF_VISIBLE = [
    "Handoff Context", "Handoff profile", "Handoff → Universal Work mapping",
    "Handoff → ModelWorkPacket mapping", "Handoff → QIRC channel mapping",
    "Handoff → Trace/Receipt mapping",
]
REQUIRED_HANDOFF_NORMAL_STATUSES = ["prepared", "candidate-ready", "blocked", "needs context"]
REQUIRED_HANDOFF_NON_GOALS = [
    "external_thor_runtime", "external_y_runtime", "external_ynode_runtime",
    "external_mjolnir_runtime", "godot_target_host_proof", "windows_target_host_proof",
    "engine_runtime_proof",
]
HANDOFF_CLAIM_BOUNDARY = "handoff_is_orientation_not_truth_not_apply_not_send_not_runtime_proof"
HANDOFF_EFFECTIVENESS_NOTE = "Handoff-First improves local LLM performance by converting raw app/user/agent/file/QIRC/demo inputs into structured Handoff Context before Universal Work and ModelWorkPacket creation, reducing prompt chaos, preserving intent, and strengthening candidate-only boundaries."


def load_json(root: Path, rel: str) -> dict[str, Any]:
    return json.loads((root / rel).read_text(encoding="utf-8"))


def add(checks: list[dict[str, Any]], violations: list[str], ok: bool, name: str) -> None:
    checks.append({"name": name, "ok": bool(ok)})
    if not ok:
        violations.append(name)


def validate(repo_root: Path, generated_at_utc: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    violations: list[str] = []
    for rel in DOCS + SCHEMAS + REGISTRIES + EXAMPLES + REPORTS + ["tools/rebaseline/check_final_road_to_100_rebaseline_audit.py"]:
        add(checks, violations, (repo_root / rel).exists(), f"required artifact exists: {rel}")

    target = load_json(repo_root, "registries/final_local_runtime_hub_target_v1.json")
    for key in REQUIRED_TARGET_KEYS:
        add(checks, violations, bool(target.get(key)), f"target includes {key}")
    add(checks, violations, target.get("candidate_only") is True, "target is candidate_only")
    add(checks, violations, target.get("local_only") is True, "target is local_only")
    for key in ["app_owned_apply", "app_owned_state", "app_owned_external_send"]:
        add(checks, violations, target.get(key) is True, f"target preserves {key}")
    qirc_target = target.get("qirc_cognitive_substrate_cluster_target", "")
    add(checks, violations, bool(qirc_target), "target includes QIRC Cognitive Substrate Cluster definition")
    add(checks, violations, "local IRC-centered coordination core" in qirc_target, "QIRC is local IRC-centered coordination core")
    add(checks, violations, "QIRC coordinates. Odin gates. Apps decide. Models work only as bounded workers." in target.get("qirc_required_formula", ""), "QIRC required formula present")
    qirc_boundaries = " ".join(target.get("qirc_hard_boundaries", [])).lower()
    for phrase in ["localhost-only", "no public rooms", "no lan/wan/federation", "no app apply", "no app-state mutation", "no external-send", "no final gate bypass", "no receipt truth", "no provider/model authority"]:
        add(checks, violations, phrase in qirc_boundaries, f"QIRC boundary present: {phrase}")
    handoff_target = target.get("handoff_first_pre_intake_target", "")
    handoff_formula = target.get("handoff_first_required_formula", "")
    handoff_boundaries = " ".join(target.get("handoff_first_hard_boundaries", [])).lower()
    add(checks, violations, "Handoff-First Pre-Intake Layer" in handoff_target, "target includes Handoff-First Pre-Intake Layer")
    add(checks, violations, "before Universal Work" in handoff_target, "Handoff-First precedes Universal Work")
    add(checks, violations, "ModelWorkPacket" in handoff_target, "Handoff-First maps toward ModelWorkPacket creation")
    add(checks, violations, handoff_formula == "Handoff orients. Universal Work bounds. Odin gates. QIRC coordinates. Apps decide. Models work only as bounded workers.", "Handoff required formula present")
    profiles = target.get("handoff_first_profiles", {})
    for profile in ["generic_handoff_profile", "thor_handoff_profile", "y_handoff_profile", "mjolnir_handoff_profile"]:
        add(checks, violations, profile in profiles, f"target includes {profile}")
    add(checks, violations, "not ynode runtime proof" in json.dumps(profiles).lower(), "Y profile is contract not YNode runtime proof")
    add(checks, violations, "not target-host" in json.dumps(profiles).lower() or "not target host" in json.dumps(profiles).lower(), "Mjölnir profile is contract not target-host runtime proof")
    for phrase in ["does not bypass universal work", "does not bypass final gate", "no app truth", "no app apply", "no app-state mutation", "no external-send", "no direct provider/model/network/api-key execution"]:
        add(checks, violations, phrase in handoff_boundaries, f"Handoff boundary present: {phrase}")

    gap = load_json(repo_root, "registries/final_repo_reality_gap_audit_v1.json")
    rows = {row.get("capability_id"): row for row in gap.get("capabilities", [])}
    for cid in REQUIRED_GAP_IDS + REQUIRED_QIRC_GAP_IDS + OPTIONAL_QIRC_GAP_IDS + REQUIRED_HANDOFF_GAP_IDS:
        add(checks, violations, cid in rows, f"gap audit covers {cid}")
        if cid in rows:
            row = rows[cid]
            add(checks, violations, row.get("current_status") in VALID_STATUSES, f"{cid} has valid status")
            for key in ["missing_work", "proof_needed", "recommended_slice"]:
                add(checks, violations, bool(row.get(key)), f"{cid} has {key}")
            if row.get("current_status") in {"missing", "partially_implemented", "schema_or_doc_only", "blocked_pending_decision", "cannot_determine_from_repo"}:
                add(checks, violations, bool(row.get("recommended_slice")), f"{cid} partial/missing maps to slice")
            if cid in OPTIONAL_QIRC_GAP_IDS:
                add(checks, violations, row.get("current_status") in {"deferred_non_goal", "blocked_pending_decision"}, f"optional QIRC ring deferred/non-goal: {cid}")
            if cid in REQUIRED_HANDOFF_GAP_IDS:
                add(checks, violations, row.get("claim_boundary") == HANDOFF_CLAIM_BOUNDARY, f"{cid} has handoff claim boundary")

    qmat = load_json(repo_root, "registries/final_q_shabang_capability_matrix_v1.json")
    qrows = {row.get("capability_id"): row for row in qmat.get("capabilities", [])}
    for cid in REQUIRED_Q_IDS + REQUIRED_QIRC_GAP_IDS + REQUIRED_HANDOFF_Q_IDS:
        add(checks, violations, cid in qrows, f"Q-Shabang matrix covers {cid}")
        if cid in qrows:
            for key in ["architecture_coverage_score_0_5", "repo_artifact_coverage_score_0_5", "validator_coverage_score_0_5", "runtime_proof_score_0_5", "normal_user_visibility_score_0_5"]:
                val = qrows[cid].get(key)
                add(checks, violations, isinstance(val, int) and 0 <= val <= 5, f"{cid} {key} score is 0-5")
            if cid in REQUIRED_HANDOFF_Q_IDS:
                add(checks, violations, HANDOFF_EFFECTIVENESS_NOTE in qrows[cid].get("effectiveness_notes", ""), f"{cid} has Handoff effectiveness note")

    catalog = load_json(repo_root, "registries/final_buildable_slice_catalog_v1.json")
    slice_ids = {row.get("slice_id") for row in catalog.get("slices", [])}
    for fam in REQUIRED_SLICE_FAMILIES + REQUIRED_QIRC_SLICE_FAMILIES + REQUIRED_HANDOFF_SLICE_FAMILIES:
        add(checks, violations, fam in slice_ids or bool(catalog.get("consolidation_justification")) or bool(catalog.get("qirc_consolidation_justification")), f"slice family covered: {fam}")

    roadmap = load_json(repo_root, "registries/final_minimal_road_to_100_pr_roadmap_v1.json")
    pr_count = int(roadmap.get("recommended_pr_count", 0))
    add(checks, violations, 3 <= pr_count <= 5 or bool(roadmap.get("more_than_five_justification")), "roadmap has 3-5 PRs or justification")
    roadmap_blob = json.dumps(roadmap, sort_keys=True).lower()
    for required in ["qirc core", "qirc_core_local_irc_runtime", "qirc_browser_event_bridge", "qirc_app_bridge_event_mapping", "qirc_file_spool_packet_bridge", "qirc_cli_agent_pipe_bridge", "qirc_trace_receipt_event_mapping", "qirc_dev_mode_event_viewer"]:
        add(checks, violations, required.lower() in roadmap_blob, f"roadmap includes QIRC required ring: {required}")
    for required in ["handoff_first_pre_intake_policy", "generic_handoff_profile", "thor_handoff_profile", "y_handoff_profile", "mjolnir_handoff_profile", "handoff_to_universal_work_mapping", "handoff_to_qirc_channel_mapping", "handoff_to_trace_receipt_mapping", "dev_mode_handoff_viewer"]:
        add(checks, violations, required in roadmap_blob, f"roadmap integrates handoff capability: {required}")
    add(checks, violations, pr_count <= 5, "roadmap integrates Handoff-First without increasing final PR count beyond 5")
    for status in REQUIRED_HANDOFF_NORMAL_STATUSES:
        add(checks, violations, status in roadmap_blob, f"normal-user handoff status planned: {status}")
    add(checks, violations, "raw handoff internals by default" in roadmap_blob, "normal UI does not expose raw handoff internals by default")
    for pr in roadmap.get("prs", []):
        pid = pr.get("pr_id", "<unknown>")
        for key in ["success_criteria", "tests_required", "proof_commands", "non_goals", "known_risks", "merge_order"]:
            add(checks, violations, bool(pr.get(key)), f"{pid} has {key}")

    acceptance = load_json(repo_root, "registries/final_100_percent_acceptance_definition_v1.json")
    positives = set(acceptance.get("positive_criteria", []))
    nongoals = set(acceptance.get("non_goals_not_required", []))
    for item in REQUIRED_POSITIVE + REQUIRED_QIRC_POSITIVE + REQUIRED_HANDOFF_POSITIVE:
        add(checks, violations, item in positives, f"acceptance includes positive {item}")
    visible = set(acceptance.get("visible_criteria", []))
    for item in REQUIRED_QIRC_VISIBLE + REQUIRED_HANDOFF_VISIBLE:
        add(checks, violations, item in visible, f"acceptance includes QIRC visible surface {item}")
    for item in REQUIRED_NON_GOALS + REQUIRED_QIRC_NON_GOALS + REQUIRED_HANDOFF_NON_GOALS:
        add(checks, violations, item in nongoals, f"acceptance excludes mandatory {item}")

    report = load_json(repo_root, "reports/final_road_to_100_rebaseline_audit_v1.json")
    for key in ["architecture_score", "runtime_score", "normal_user_ux_score", "q_shabang_score", "ki_ohne_ki_score", "llm_agent_effectiveness_score", "hard_blockers", "soft_blockers", "recommended_final_pr_count", "next_action"]:
        add(checks, violations, key in report and report.get(key) not in (None, [], ""), f"report includes {key}")
    forbidden_claims = ["runtime proof completed", "security certification completed", "release certification completed", "target host proof completed", "live model inference proof completed", "model quality proof completed"]
    report_for_scan = {key: report.get(key) for key in ["target_summary", "claim_boundary", "non_claims", "deferred_non_goals"]}
    serialized = json.dumps({"target": target, "gap": gap, "qmat": qmat, "catalog": catalog, "roadmap": roadmap, "acceptance": acceptance, "report": report_for_scan}, sort_keys=True).lower()
    for claim in forbidden_claims:
        add(checks, violations, claim not in serialized, f"forbidden unreceipted claim token absent: {claim}")
    forbidden_qirc_authority = ["qirc may apply", "qirc can apply", "qirc mutates app state", "qirc may mutate app state", "qirc sends externally", "qirc may send externally", "qirc bypasses final gate", "receipt is truth"]
    for phrase in forbidden_qirc_authority:
        add(checks, violations, phrase not in serialized, f"QIRC forbidden authority absent: {phrase}")
    forbidden_handoff_authority = ["handoff bypasses universal work", "handoff bypasses final gate", "handoff grants apply", "handoff grants send", "handoff grants tool authority", "handoff packet is truth", "handoff packet is app approval", "handoff is app approval", "handoff treats qirc event as truth", "external thor runtime proof claimed", "external y runtime proof claimed", "external ynode runtime proof claimed", "external mjolnir runtime proof claimed", "godot runtime proof claimed", "windows runtime proof claimed"]
    for phrase in forbidden_handoff_authority:
        add(checks, violations, phrase not in serialized, f"Handoff forbidden authority/proof absent: {phrase}")
    add(checks, violations, "raw request → handoff → model" not in serialized and "raw request -> handoff -> model" not in serialized, "Handoff does not route raw input directly to model")
    add(checks, violations, "public by default" not in serialized and " federation by default" not in serialized and "lan/wan by default" not in serialized, "QIRC is not public network/federation by default")
    add(checks, violations, "api_key" not in serialized and "read environment" not in serialized and "provider execution introduced" not in serialized and "model execution introduced" not in serialized and "network execution introduced" not in serialized, "no API-key/env/provider/model/network execution claim in final artifacts")

    manifest = load_json(repo_root, "FILE_MANIFEST.json")
    paths = [entry.get("path", "") for entry in manifest.get("files", [])]
    add(checks, violations, not any(any(part in path for part in FORBIDDEN_MANIFEST_PARTS) for path in paths), "FILE_MANIFEST excludes forbidden temp/build/cache artifacts")

    hard_violations = sorted(set(violations))
    return {
        "report_id": "final_road_to_100_rebaseline_audit_v1",
        "generated_at_utc": generated_at_utc,
        "status": "ok" if not hard_violations else "failed",
        "checks": checks,
        "hard_violations": hard_violations,
        "target_summary": "Odin Local Runtime Hub with first-class QIRC Cognitive Substrate Cluster and mandatory Handoff-First Pre-Intake Layer before Universal Work and ModelWorkPacket creation.",
        "repo_reality_summary": report.get("repo_reality_summary") or "Repo audit records Handoff-First as target/roadmap/validator coverage; Thor handoff evidence is partial/candidate-only; Generic/Y/Mjölnir profile implementation receipts remain mapped buildable slices.",
        "handoff_first_pre_intake_layer": {
            "mandatory_for_final_target": True,
            "plain_answer": "Handoff-First is mandatory for the final target. It is the first normalization layer before Universal Work and ModelWorkPacket creation. It supports local LLM performance by reducing prompt chaos and producing structured, bounded work packets. Thor profile is mandatory. Generic profile is mandatory. Y and Mjölnir profiles are structured handoff dialect targets, not external runtime claims.",
            "flow": target.get("handoff_first_flow"),
            "formula": target.get("handoff_first_required_formula"),
            "profiles": target.get("handoff_first_profiles"),
            "thor_compiler_adapter": "partial/candidate-only repo evidence in docs, schemas, registries and shadow_runtime; no external Thor runtime proof claimed",
            "generic_profile": "mandatory target profile; schema/doc/roadmap coverage in this PR; implementation receipt mapped to buildable slice",
            "thor_profile": "mandatory target profile; partial candidate-only repo evidence; implementation receipt mapped to buildable slice",
            "y_profile": "mandatory structured profile contract; not YNode runtime proof",
            "mjolnir_profile": "mandatory structured profile contract; not Godot/Windows/engine/external Mjölnir runtime proof",
            "dev_mode_visibility": "planned Dev Mode Handoff Viewer for Handoff Context/profile and Handoff to Universal Work/ModelWorkPacket/QIRC/Trace/Receipt chain",
            "normal_user_visibility": REQUIRED_HANDOFF_NORMAL_STATUSES,
            "claim_boundary": HANDOFF_CLAIM_BOUNDARY,
        },
        "architecture_score": report.get("architecture_score"),
        "runtime_score": report.get("runtime_score"),
        "normal_user_ux_score": report.get("normal_user_ux_score"),
        "q_shabang_score": report.get("q_shabang_score"),
        "ki_ohne_ki_score": report.get("ki_ohne_ki_score"),
        "llm_agent_effectiveness_score": report.get("llm_agent_effectiveness_score"),
        "clone_start_readiness_score": report.get("clone_start_readiness_score"),
        "app_connection_readiness_score": report.get("app_connection_readiness_score"),
        "qirc_cognitive_substrate_score": report.get("qirc_cognitive_substrate_score"),
        "qirc_core_status": report.get("qirc_core_status"),
        "qirc_required_rings": report.get("qirc_required_rings"),
        "qirc_optional_rings": report.get("qirc_optional_rings"),
        "missing_capabilities": report.get("missing_capabilities"),
        "slice_count": report.get("slice_count"),
        "recommended_final_pr_count": report.get("recommended_final_pr_count"),
        "recommended_prs": report.get("recommended_prs"),
        "hard_blockers": report.get("hard_blockers"),
        "soft_blockers": report.get("soft_blockers"),
        "deferred_non_goals": report.get("deferred_non_goals"),
        "next_action": report.get("next_action"),
        "claim_boundary": report.get("claim_boundary"),
        "non_claims": report.get("non_claims"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", required=True)
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    out = Path(args.out)
    report = validate(repo_root, args.generated_at_utc)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
