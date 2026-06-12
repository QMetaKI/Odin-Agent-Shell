from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B8_NAMES = [
    "b8_security_review_scope",
    "static_security_surface_inventory",
    "trust_boundary_matrix",
    "static_security_flow_map",
    "static_threat_model",
    "security_risk_register",
    "security_control_coverage_matrix",
    "static_sensitive_pattern_review",
    "thor_odin_effectiveness_audit",
    "b8_security_review_report",
]
EXPLICIT_NON_METHODS = {
    "no_penetration_test",
    "no_dynamic_runtime_test",
    "no_target_host_test",
    "no_network_scan",
    "no_secret_scan_of_environment",
    "no_external_security_service",
    "no_provider_execution",
    "no_model_execution",
    "no_security_certification",
}
BOUNDARIES = {
    "app_authority_boundary",
    "provider_runtime_boundary",
    "receipt_truth_boundary",
    "final_gate_advisory_boundary",
    "thor_intake_boundary",
    "thor_pack_boundary",
    "sdk_app_bridge_boundary",
    "storage_trace_privacy_boundary",
    "security_review_boundary",
    "target_host_boundary",
    "release_boundary",
}
FLOWS = {
    "candidate_input_flow",
    "schema_validation_flow",
    "registry_reference_flow",
    "report_generation_flow",
    "receipt_evidence_flow",
    "provider_policy_flow",
    "thor_intake_flow",
    "cli_validation_flow",
    "external_runtime_deferred_flow",
}
THREATS = {
    "claim_overreach",
    "authority_leak",
    "provider_runtime_leak",
    "secret_or_token_leak",
    "path_leak",
    "unsafe_file_write",
    "network_or_remote_leak",
    "receipt_truth_elevation",
    "final_gate_elevation",
    "thor_pack_artifact_commit",
    "security_certification_overclaim",
    "target_host_overclaim",
    "release_overclaim",
    "audit_theater_risk",
    "process_overhead_risk",
}
STATUSES = {
    "open_static",
    "mitigated_by_boundary",
    "partially_mitigated_static",
    "deferred_to_security_review",
    "deferred_to_target_host_review",
    "deferred_to_provider_runtime_review",
    "requires_human_review",
    "cannot_safely_complete",
}
SCORE_KEYS = {
    "scope_control",
    "claim_boundary_control",
    "evidence_traceability",
    "repo_cognition_helpfulness",
    "prompt_quality_improvement",
    "audit_quality_improvement",
    "implementation_speed_support",
    "merge_confidence_support",
    "false_confidence_reduction",
    "overhead_cost",
    "complexity_cost",
    "maintainer_clarity",
    "security_review_helpfulness",
}
FORBIDDEN_IMPORT_TOKENS = [
    "import " + "requests",
    "from " + "requests",
    "import " + "httpx",
    "from " + "httpx",
    "import " + "openai",
    "from " + "openai",
    "import " + "ollama",
    "from " + "ollama",
    "import " + "llama_cpp",
    "from " + "llama_cpp",
]


def load_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def example(name: str) -> dict:
    return load_json(f"examples/v7_1_1/{name}.example.json")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validator_module():
    path = ROOT / "tools/v7_1_1/check_b8_security_review_track.py"
    spec = importlib.util.spec_from_file_location("b8_validator_for_tests", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_validator(repo: Path, out: Path) -> dict:
    module = validator_module()
    code = module.main(["--repo-root", str(repo), "--out", str(out), "--generated-at-utc", "2026-01-01T00:00:00Z"])
    return {"code": code, "data": json.loads(out.read_text(encoding="utf-8"))}


def make_repo_copy(tmp_path: Path) -> Path:
    dst = tmp_path / "repo"
    ignore = shutil.ignore_patterns(".git", ".thor", ".venv", "venv", "__pycache__", ".pytest_cache", "dist", "build", "*.egg-info")
    shutil.copytree(ROOT, dst, ignore=ignore)
    return dst


def test_b8_schemas_registries_examples_exist():
    for name in B8_NAMES:
        assert (ROOT / "schemas" / f"v7_1_1_{name}.schema.json").exists()
        assert (ROOT / "registries" / f"v7_1_1_{name}_registry.json").exists()
        assert (ROOT / "examples" / "v7_1_1" / f"{name}.example.json").exists()


def test_b8_report_and_validator_exist():
    assert (ROOT / "reports/v7_1_1_b8_security_review_report.json").exists()
    assert (ROOT / "tools/v7_1_1/check_b8_security_review_track.py").exists()


def test_security_review_scope_explicit_non_methods():
    scope = example("b8_security_review_scope")
    assert scope["review_type"] == "static_security_review_track"
    assert EXPLICIT_NON_METHODS.issubset(set(scope["explicit_non_methods"]))


def test_surface_inventory_includes_required_path_classes():
    surface = example("static_security_surface_inventory")
    paths = set(surface["reviewed_paths"]) | set(surface["security_relevant_paths"])
    for item in ["odin/cli.py", "tools/v7_1_1/", "schemas/", "registries/", "reports/", "docs/codex/", "examples/"]:
        assert item in paths


def test_trust_boundary_matrix_required_categories():
    assert BOUNDARIES.issubset(set(example("trust_boundary_matrix")["boundaries"]))


def test_static_security_flow_map_required_categories():
    cats = {item["flow_category"] for item in example("static_security_flow_map")["flows"]}
    assert FLOWS.issubset(cats)


def test_threat_model_required_categories():
    cats = {item["threat_category"] for item in example("static_threat_model")["threats"]}
    assert THREATS.issubset(cats)


def test_risk_register_has_valid_statuses():
    risks = example("security_risk_register")["risks"]
    assert risks
    assert all(risk["status"] in STATUSES for risk in risks)


def test_control_coverage_matrix_has_covered_partial_uncovered():
    matrix = example("security_control_coverage_matrix")
    assert matrix["covered_controls"]
    assert matrix["partially_covered_controls"]
    assert matrix["uncovered_controls"]


def test_sensitive_pattern_review_denies_complete_secret_scan_claim():
    review = example("static_sensitive_pattern_review")
    assert "not_a_complete_secret_scan" in review["non_claims"]
    assert "does_not_read_environment_variables" in review["non_claims"]
    assert "does_not_contact_external_secret_scanning_service" in review["non_claims"]
    assert "does_not_certify_absence_of_secrets" in review["non_claims"]


def test_thor_odin_effectiveness_audit_required_content():
    audit = example("thor_odin_effectiveness_audit")
    assert audit
    assert {"B1", "B2", "B3", "B4", "B5", "B6", "B7"}.issubset(set(audit["reviewed_bundles"]))
    assert SCORE_KEYS.issubset(audit["quantitative_proxy_scores"])
    assert all(0 <= audit["quantitative_proxy_scores"][key] <= 5 for key in SCORE_KEYS)
    assert audit["what_was_strong"]
    assert audit["what_was_medium"]
    assert audit["what_was_weak"]
    assert audit["what_was_overbuilt"]
    assert audit["recommendations_keep"]
    assert audit["recommendations_improve"]
    assert audit["recommendations_reduce"]
    assert audit["recommendations_defer"]
    assert audit["where_process_cost_was_high"]
    assert audit["where_process_increased_overhead"]


def test_b8_report_denies_forbidden_proof_claims_and_contains_gaps():
    report = load_json("reports/v7_1_1_b8_security_review_report.json")
    denied = set(report["denied_claims"])
    assert "security_certification" in denied
    assert "vulnerability_free_claim" in denied
    assert {"production_readiness", "release_approval", "deployment_proof", "runtime_proof"}.issubset(denied)
    assert set(report["known_security_gaps"]).issuperset({
        "no_penetration_test_performed",
        "no_dynamic_runtime_security_test_performed",
        "no_target_host_security_test_performed",
        "no_external_secret_scan_performed",
        "no_dependency_vulnerability_tool_proof",
        "no_provider_runtime_security_review",
        "no_network_runtime_security_review",
        "no_security_certification",
    })


def test_no_provider_network_api_key_model_execution_imports_added():
    for rel in ["tools/v7_1_1/check_b8_security_review_track.py", "tests/test_v7_1_1_b8_security_review_track.py", "odin/cli.py"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert not any(token in text for token in FORBIDDEN_IMPORT_TOKENS)


def test_no_thor_or_pack_artifacts_in_file_manifest():
    manifest = load_json("FILE_MANIFEST.json")
    paths = [item["path"] for item in manifest["files"]]
    assert not any(path.startswith(".thor/") or "/.thor/" in path for path in paths)
    assert not any("PACK_MANIFEST" in path and "Thor-Agent-Kit" in path for path in paths)
    assert not any(part in path for path in paths for part in ["__pycache__/", ".pytest_cache/", "dist/", "build/", ".egg-info", ".pyc"])


def test_validator_runs_deterministically(tmp_path):
    out1 = tmp_path / "one.json"
    out2 = tmp_path / "two.json"
    first = run_validator(ROOT, out1)
    second = run_validator(ROOT, out2)
    assert first["code"] == 0
    assert second["code"] == 0
    assert first["data"] == second["data"]
    assert first["data"]["hard_violations"] == []


def test_validator_fails_closed_on_security_certification_claim(tmp_path):
    repo = make_repo_copy(tmp_path)
    path = repo / "examples/v7_1_1/b8_security_review_report.example.json"
    data = json.loads(path.read_text())
    data["accepted_static_findings"].append("security certification claimed")
    write_json(path, data)
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("positive security certification" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_vulnerability_free_claim(tmp_path):
    repo = make_repo_copy(tmp_path)
    path = repo / "examples/v7_1_1/b8_security_review_report.example.json"
    data = json.loads(path.read_text())
    data["accepted_static_findings"].append("vulnerability-free claimed")
    write_json(path, data)
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("vulnerability-free" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_missing_known_gaps(tmp_path):
    repo = make_repo_copy(tmp_path)
    path = repo / "reports/v7_1_1_b8_security_review_report.json"
    data = json.loads(path.read_text())
    data["known_security_gaps"] = []
    write_json(path, data)
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("known security gaps" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_thor_odin_score_outside_range(tmp_path):
    repo = make_repo_copy(tmp_path)
    path = repo / "examples/v7_1_1/thor_odin_effectiveness_audit.example.json"
    data = json.loads(path.read_text())
    data["quantitative_proxy_scores"]["scope_control"] = 6
    write_json(path, data)
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("bounded 0-5" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_missing_effectiveness_audit(tmp_path):
    repo = make_repo_copy(tmp_path)
    (repo / "examples/v7_1_1/thor_odin_effectiveness_audit.example.json").unlink()
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("Thor/Odin effectiveness audit exists" in item for item in result["data"]["hard_violations"])


def test_validator_fails_closed_on_provider_import_in_b8_code(tmp_path):
    repo = make_repo_copy(tmp_path)
    path = repo / "tools/v7_1_1/check_b8_security_review_track.py"
    path.write_text(path.read_text() + "\nimport " + "requests\n", encoding="utf-8")
    result = run_validator(repo, tmp_path / "out.json")
    assert result["code"] == 1
    assert any("SDK imports" in item for item in result["data"]["hard_violations"])


def test_prior_pr25_through_pr33_test_files_remain_present():
    for rel in [
        "tests/test_v7_1_1_operational_coverage_gap_compiler.py",
        "tests/test_v7_1_1_canon_boundary_integrity.py",
        "tests/test_v7_1_1_b1_app_boundary_universal_work_qirc_spine.py",
        "tests/test_v7_1_1_b2_context_lenses_worklets_slot_gaptext.py",
        "tests/test_v7_1_1_b3_modelworkpacket_scale_hybrid.py",
        "tests/test_v7_1_1_b4_minicheck_critics_final_gate.py",
        "tests/test_v7_1_1_b5_storage_trace_receipt_provider_bridge.py",
        "tests/test_v7_1_1_b6_acceptance_dojo_scoreboard_closure.py",
        "tests/test_v7_1_1_b7_closure_thor_provider_eval.py",
    ]:
        assert (ROOT / rel).exists()


def test_validate_all_and_cli_b8_integration_are_registered():
    text = (ROOT / "odin/cli.py").read_text(encoding="utf-8")
    assert "validate-b8-security-review-track" in text
    assert "validate_b8_security_review_track()" in text
    assert "errors.extend(validate_b8_security_review_track())" in text


def test_full_pytest_command_is_documented_in_return_report():
    text = (ROOT / "docs/codex/reports/PR_34_B8_SECURITY_REVIEW_RETURN_REPORT.md").read_text(encoding="utf-8")
    assert "python -m pytest -q -p no:cacheprovider" in text
    assert "python -m odin.cli validate-all" in text
