from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

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
REPORTS = ["reports/final_road_to_100_rebaseline_audit_v1.json"]

EXAMPLES = [
    "examples/final_local_runtime_hub_target_v1.example.json",
    "examples/final_repo_reality_gap_audit_v1.example.json",
    "examples/final_q_shabang_capability_matrix_v1.example.json",
    "examples/final_buildable_slice_catalog_v1.example.json",
    "examples/final_minimal_road_to_100_pr_roadmap_v1.example.json",
    "examples/final_100_percent_acceptance_definition_v1.example.json",
]
GAP_IDS = [
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
Q_IDS = [
    "ki_ohne_ki", "universal_work", "candidate_artifacts", "response_packets", "qirc_semantic_bus",
    "context_distillery", "lenses", "worklets", "slot_forge", "gaptext", "modelworkpacket",
    "smallest_sufficient_worker", "3b_7b_hybrid_route_roles", "critic_cascade", "tournament",
    "candidate_dna", "final_gate_advisory", "receipt_boundary", "receipt_ledger", "trace_records",
    "provider_policy", "local_provider_seam", "thor_handoff", "thor_pack_intake", "sdk_app_bridge",
    "security_review_track", "local_runtime_hub_ui", "app_connections", "dev_mode",
]
SLICE_FAMILIES = [
    "simple_local_hub_start", "browser_hub_normal_user_ui", "model_picker_provider_status",
    "connected_apps_bridge_view", "demo_universal_work_flow", "activity_trace_receipt_view",
    "dev_mode_diagnostics", "runtime_security_smoke", "target_host_smoke", "local_provider_probe",
    "final_acceptance_cleanup", "docs_quickstart_polish",
]
POSITIVE_CRITERIA = [
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


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_new_docs_exist() -> None:
    for rel in DOCS:
        assert (ROOT / rel).read_text(encoding="utf-8").strip()


def test_new_schemas_exist() -> None:
    for rel in SCHEMAS:
        assert load(rel).get("$schema")


def test_new_registries_exist() -> None:
    for rel in REGISTRIES:
        assert load(rel)


def test_new_examples_exist() -> None:
    for rel in EXAMPLES:
        assert load(rel)


def test_new_report_exists() -> None:
    assert load("reports/final_road_to_100_rebaseline_audit_v1.json")["report_id"] == "final_road_to_100_rebaseline_audit_v1"


def test_validator_exists() -> None:
    assert (ROOT / "tools/rebaseline/check_final_road_to_100_rebaseline_audit.py").exists()


def test_target_definition_includes_required_targets() -> None:
    target = load("registries/final_local_runtime_hub_target_v1.json")
    assert "Normal users" in target["normal_user_target"]
    assert "Dev Mode" in target["dev_mode_target"]
    assert "Q-Shabang" in target["q_shabang_target"]
    assert "Deterministic" in target["ki_ohne_ki_target"]
    assert "LLMs and agents" in target["llm_agent_target"]


def test_gap_audit_covers_required_capability_ids_and_statuses() -> None:
    rows = {row["capability_id"]: row for row in load("registries/final_repo_reality_gap_audit_v1.json")["capabilities"]}
    assert set(GAP_IDS) <= set(rows)
    for row in rows.values():
        assert row["current_status"] in VALID_STATUSES


def test_every_missing_partial_or_doc_only_maps_to_slice() -> None:
    rows = load("registries/final_repo_reality_gap_audit_v1.json")["capabilities"]
    for row in rows:
        if row["current_status"] in {"missing", "partially_implemented", "schema_or_doc_only"}:
            assert row["recommended_slice"]


def test_q_shabang_matrix_covers_required_ids_and_scores_are_0_to_5() -> None:
    rows = {row["capability_id"]: row for row in load("registries/final_q_shabang_capability_matrix_v1.json")["capabilities"]}
    assert set(Q_IDS) <= set(rows)
    for row in rows.values():
        for key, value in row.items():
            if key.endswith("_score_0_5"):
                assert isinstance(value, int)
                assert 0 <= value <= 5


def test_slice_catalog_has_required_families_or_justified_consolidation() -> None:
    catalog = load("registries/final_buildable_slice_catalog_v1.json")
    slices = {row["slice_id"] for row in catalog["slices"]}
    for family in SLICE_FAMILIES:
        assert family in slices or catalog.get("consolidation_justification")


def test_roadmap_has_three_to_five_prs_or_justified_exception() -> None:
    roadmap = load("registries/final_minimal_road_to_100_pr_roadmap_v1.json")
    count = roadmap["recommended_pr_count"]
    assert 3 <= count <= 5 or roadmap.get("more_than_five_justification")


def test_every_roadmap_pr_has_proof_commands_and_non_goals() -> None:
    for pr in load("registries/final_minimal_road_to_100_pr_roadmap_v1.json")["prs"]:
        assert pr["proof_commands"]
        assert pr["non_goals"]


def test_acceptance_definition_includes_positive_criteria_and_excludes_non_mandatory_items() -> None:
    acceptance = load("registries/final_100_percent_acceptance_definition_v1.json")
    assert set(POSITIVE_CRITERIA) <= set(acceptance["positive_criteria"])
    non_goals = set(acceptance["non_goals_not_required"])
    assert "windows_service_tray_installer" in non_goals
    assert "production_readiness" in non_goals
    assert "security_certification" in non_goals
    assert "signed_release" in non_goals


def test_report_includes_scores_blockers_final_pr_count_and_next_pr() -> None:
    report = load("reports/final_road_to_100_rebaseline_audit_v1.json")
    for key in ["architecture_score", "runtime_score", "normal_user_ux_score", "q_shabang_score", "ki_ohne_ki_score", "llm_agent_effectiveness_score"]:
        assert isinstance(report[key], int)
    assert report["hard_blockers"]
    assert report["soft_blockers"]
    assert report["recommended_final_pr_count"] == 5
    assert "FINAL-PR-01" in report["next_action"]


def test_no_runtime_provider_network_api_key_execution_added_to_final_artifacts() -> None:
    blob = "\n".join((ROOT / rel).read_text(encoding="utf-8") for rel in DOCS + REGISTRIES + EXAMPLES + REPORTS).lower()
    for forbidden in ["api key", "api_key", "called network", "ran provider", "ran model"]:
        assert forbidden not in blob


def test_no_thor_or_external_temp_artifacts_in_file_manifest() -> None:
    paths = [entry["path"] for entry in load("FILE_MANIFEST.json")["files"]]
    forbidden = [".thor/", ".odin_runtime/", "__pycache__", ".pytest_cache", "egg-info", ".pyc"]
    assert not [path for path in paths if any(part in path for part in forbidden)]


def test_validator_runs_deterministically(tmp_path: Path) -> None:
    validator = ROOT / "tools/rebaseline/check_final_road_to_100_rebaseline_audit.py"
    spec = importlib.util.spec_from_file_location("final_audit_validator", validator)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out1 = tmp_path / "one.json"
    out2 = tmp_path / "two.json"
    args = ["--repo-root", str(ROOT), "--generated-at-utc", "2026-01-01T00:00:00Z"]
    assert module.main([*args, "--out", str(out1)]) == 0
    assert module.main([*args, "--out", str(out2)]) == 0
    assert out1.read_text(encoding="utf-8") == out2.read_text(encoding="utf-8")
