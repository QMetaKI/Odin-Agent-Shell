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

    gap = load_json(repo_root, "registries/final_repo_reality_gap_audit_v1.json")
    rows = {row.get("capability_id"): row for row in gap.get("capabilities", [])}
    for cid in REQUIRED_GAP_IDS:
        add(checks, violations, cid in rows, f"gap audit covers {cid}")
        if cid in rows:
            row = rows[cid]
            add(checks, violations, row.get("current_status") in VALID_STATUSES, f"{cid} has valid status")
            for key in ["missing_work", "proof_needed", "recommended_slice"]:
                add(checks, violations, bool(row.get(key)), f"{cid} has {key}")
            if row.get("current_status") in {"missing", "partially_implemented", "schema_or_doc_only", "blocked_pending_decision", "cannot_determine_from_repo"}:
                add(checks, violations, bool(row.get("recommended_slice")), f"{cid} partial/missing maps to slice")

    qmat = load_json(repo_root, "registries/final_q_shabang_capability_matrix_v1.json")
    qrows = {row.get("capability_id"): row for row in qmat.get("capabilities", [])}
    for cid in REQUIRED_Q_IDS:
        add(checks, violations, cid in qrows, f"Q-Shabang matrix covers {cid}")
        if cid in qrows:
            for key in ["architecture_coverage_score_0_5", "repo_artifact_coverage_score_0_5", "validator_coverage_score_0_5", "runtime_proof_score_0_5", "normal_user_visibility_score_0_5"]:
                val = qrows[cid].get(key)
                add(checks, violations, isinstance(val, int) and 0 <= val <= 5, f"{cid} {key} score is 0-5")

    catalog = load_json(repo_root, "registries/final_buildable_slice_catalog_v1.json")
    slice_ids = {row.get("slice_id") for row in catalog.get("slices", [])}
    for fam in REQUIRED_SLICE_FAMILIES:
        add(checks, violations, fam in slice_ids or bool(catalog.get("consolidation_justification")), f"slice family covered: {fam}")

    roadmap = load_json(repo_root, "registries/final_minimal_road_to_100_pr_roadmap_v1.json")
    pr_count = int(roadmap.get("recommended_pr_count", 0))
    add(checks, violations, 3 <= pr_count <= 5 or bool(roadmap.get("more_than_five_justification")), "roadmap has 3-5 PRs or justification")
    for pr in roadmap.get("prs", []):
        pid = pr.get("pr_id", "<unknown>")
        for key in ["success_criteria", "tests_required", "proof_commands", "non_goals", "known_risks", "merge_order"]:
            add(checks, violations, bool(pr.get(key)), f"{pid} has {key}")

    acceptance = load_json(repo_root, "registries/final_100_percent_acceptance_definition_v1.json")
    positives = set(acceptance.get("positive_criteria", []))
    nongoals = set(acceptance.get("non_goals_not_required", []))
    for item in REQUIRED_POSITIVE:
        add(checks, violations, item in positives, f"acceptance includes positive {item}")
    for item in REQUIRED_NON_GOALS:
        add(checks, violations, item in nongoals, f"acceptance excludes mandatory {item}")

    report = load_json(repo_root, "reports/final_road_to_100_rebaseline_audit_v1.json")
    for key in ["architecture_score", "runtime_score", "normal_user_ux_score", "q_shabang_score", "ki_ohne_ki_score", "llm_agent_effectiveness_score", "hard_blockers", "soft_blockers", "recommended_final_pr_count", "next_action"]:
        add(checks, violations, key in report and report.get(key) not in (None, [], ""), f"report includes {key}")
    forbidden_claims = ["runtime proof completed", "security certification completed", "release certification completed", "target host proof completed", "live model inference proof completed", "model quality proof completed"]
    report_for_scan = {key: report.get(key) for key in ["target_summary", "claim_boundary", "non_claims", "deferred_non_goals"]}
    serialized = json.dumps({"target": target, "gap": gap, "qmat": qmat, "catalog": catalog, "roadmap": roadmap, "acceptance": acceptance, "report": report_for_scan}, sort_keys=True).lower()
    for claim in forbidden_claims:
        add(checks, violations, claim not in serialized, f"forbidden unreceipted claim token absent: {claim}")
    add(checks, violations, "api_key" not in serialized and "read environment" not in serialized, "no API-key/env execution claim in final artifacts")

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
        "target_summary": report.get("target_summary"),
        "repo_reality_summary": report.get("repo_reality_summary"),
        "architecture_score": report.get("architecture_score"),
        "runtime_score": report.get("runtime_score"),
        "normal_user_ux_score": report.get("normal_user_ux_score"),
        "q_shabang_score": report.get("q_shabang_score"),
        "ki_ohne_ki_score": report.get("ki_ohne_ki_score"),
        "llm_agent_effectiveness_score": report.get("llm_agent_effectiveness_score"),
        "clone_start_readiness_score": report.get("clone_start_readiness_score"),
        "app_connection_readiness_score": report.get("app_connection_readiness_score"),
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
