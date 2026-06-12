#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

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
B1_B7_REPORTS = [
    "reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json",
    "reports/v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.json",
    "reports/v7_1_1_b3_modelworkpacket_scale_hybrid_report.json",
    "reports/v7_1_1_b4_minicheck_critics_final_gate_report.json",
    "reports/v7_1_1_b5_storage_trace_receipt_provider_bridge_report.json",
    "reports/v7_1_1_b6_acceptance_dojo_scoreboard_closure_report.json",
    "reports/v7_1_1_b7_closure_thor_provider_eval_report.json",
]
B1_B7_REGISTRIES = [
    "registries/v7_1_1_actual_codex_bundle_plan.json",
    "registries/v7_1_1_claim_boundary_registry.json",
    "registries/v7_1_1_forbidden_claim_registry.json",
    "registries/v7_1_1_b7_evaluation_report_registry.json",
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
SURFACE_PATH_CLASSES = {"odin/cli.py", "tools/v7_1_1/", "schemas/", "registries/", "reports/", "docs/codex/", "examples/"}
BOUNDARY_CATEGORIES = {
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
FLOW_CATEGORIES = {
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
THREAT_CATEGORIES = {
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
RISK_STATUSES = {
    "open_static",
    "mitigated_by_boundary",
    "partially_mitigated_static",
    "deferred_to_security_review",
    "deferred_to_target_host_review",
    "deferred_to_provider_runtime_review",
    "requires_human_review",
    "cannot_safely_complete",
}
REQUIRED_KNOWN_GAPS = {
    "no_penetration_test_performed",
    "no_dynamic_runtime_security_test_performed",
    "no_target_host_security_test_performed",
    "no_external_secret_scan_performed",
    "no_dependency_vulnerability_tool_proof",
    "no_provider_runtime_security_review",
    "no_network_runtime_security_review",
    "no_security_certification",
}
SENSITIVE_NON_CLAIMS = {
    "not_a_complete_secret_scan",
    "does_not_read_environment_variables",
    "does_not_contact_external_secret_scanning_service",
    "does_not_certify_absence_of_secrets",
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
FORBIDDEN_MANIFEST_PARTS = [".thor/", "__pycache__/", ".pytest_cache/", "dist/", "build/", ".egg-info", ".pyc"]
POSITIVE_CLAIM_MARKERS = [
    "security_certification_claimed",
    "security certification claimed",
    "vulnerability_free_claimed",
    "vulnerability-free claimed",
    "vulnerability free claimed",
    "production_readiness_claimed",
    "production readiness claimed",
    "release_approval_claimed",
    "release approved",
    "deployment_proof_claimed",
    "runtime_proof_claimed",
    "provider_execution_proof_claimed",
    "model_execution_proof_claimed",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def add(ok: bool, message: str, checks: list[dict[str, str]], violations: list[str]) -> None:
    checks.append({"check": message, "status": "pass" if ok else "fail"})
    if not ok:
        violations.append(message)


def values_for_key(data: Any, key: str) -> list[Any]:
    found: list[Any] = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                found.append(v)
            found.extend(values_for_key(v, key))
    elif isinstance(data, list):
        for item in data:
            found.extend(values_for_key(item, key))
    return found


def flattened_strings(data: Any) -> list[str]:
    if isinstance(data, str):
        return [data]
    if isinstance(data, dict):
        out: list[str] = []
        for k, v in data.items():
            out.append(str(k))
            out.extend(flattened_strings(v))
        return out
    if isinstance(data, list):
        out: list[str] = []
        for item in data:
            out.extend(flattened_strings(item))
        return out
    return [str(data)] if isinstance(data, bool | int | float) else []


def positive_claim_seen(data: Any) -> bool:
    text = "\n".join(flattened_strings(data)).lower().replace("_", " ")
    normalized_markers = [m.replace("_", " ") for m in POSITIVE_CLAIM_MARKERS]
    return any(marker in text for marker in normalized_markers)


def contract(root: Path, name: str) -> tuple[Path, Path, Path]:
    return (
        root / "schemas" / f"v7_1_1_{name}.schema.json",
        root / "registries" / f"v7_1_1_{name}_registry.json",
        root / "examples" / "v7_1_1" / f"{name}.example.json",
    )


def validate(root: Path, generated_at_utc: str) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    violations: list[str] = []
    loaded: dict[str, dict[str, Any]] = {}

    for rel in B1_B7_REPORTS + B1_B7_REGISTRIES:
        path = root / rel
        add(path.exists(), f"prior B1-B7 mapping source exists: {rel}", checks, violations)
        if path.exists():
            try:
                load_json(path)
            except Exception as exc:
                add(False, f"prior source is readable JSON: {rel}: {exc}", checks, violations)

    for name in B8_NAMES:
        schema_path, registry_path, example_path = contract(root, name)
        for path in [schema_path, registry_path, example_path]:
            add(path.exists(), f"B8 artifact exists: {path.relative_to(root).as_posix()}", checks, violations)
            if path.exists():
                try:
                    load_json(path)
                except Exception as exc:
                    add(False, f"B8 artifact is readable JSON: {path.relative_to(root).as_posix()}: {exc}", checks, violations)
        if example_path.exists():
            try:
                loaded[name] = load_json(example_path)
            except Exception:
                loaded[name] = {}

    report_path = root / "reports" / "v7_1_1_b8_security_review_report.json"
    add(report_path.exists(), "B8 generated security review report exists", checks, violations)
    report_data: dict[str, Any] = {}
    if report_path.exists():
        try:
            report_data = load_json(report_path)
        except Exception as exc:
            add(False, f"B8 generated report is readable JSON: {exc}", checks, violations)

    scope = loaded.get("b8_security_review_scope", {})
    add(scope.get("review_type") == "static_security_review_track", "security review scope type is static_security_review_track", checks, violations)
    add(EXPLICIT_NON_METHODS.issubset(set(scope.get("explicit_non_methods", []))), "security review scope includes all explicit non-methods", checks, violations)

    surface = loaded.get("static_security_surface_inventory", {})
    reviewed_paths = set(surface.get("reviewed_paths", [])) | set(surface.get("security_relevant_paths", []))
    add(SURFACE_PATH_CLASSES.issubset(reviewed_paths), "surface inventory covers CLI/tools/schemas/registries/reports/docs/examples", checks, violations)

    matrix = loaded.get("trust_boundary_matrix", {})
    add(BOUNDARY_CATEGORIES.issubset(set(matrix.get("boundaries", []))), "trust boundary matrix includes required categories", checks, violations)
    add(bool(matrix.get("allowed_crossings")) and bool(matrix.get("forbidden_crossings")) and bool(matrix.get("required_evidence_for_crossing")), "trust boundary matrix records crossings and evidence", checks, violations)

    flow = loaded.get("static_security_flow_map", {})
    flow_categories = {item.get("flow_category") for item in flow.get("flows", []) if isinstance(item, dict)}
    add(FLOW_CATEGORIES.issubset(flow_categories), "static security flow map includes required flow categories", checks, violations)

    threat = loaded.get("static_threat_model", {})
    threat_categories = {item.get("threat_category") for item in threat.get("threats", []) if isinstance(item, dict)}
    add(THREAT_CATEGORIES.issubset(threat_categories), "static threat model includes required threat categories", checks, violations)

    risk = loaded.get("security_risk_register", {})
    risks = risk.get("risks", [])
    add(bool(risks), "security risk register has risk entries", checks, violations)
    add(all(item.get("status") in RISK_STATUSES for item in risks if isinstance(item, dict)), "security risk register statuses are valid", checks, violations)

    control = loaded.get("security_control_coverage_matrix", {})
    add(bool(control.get("covered_controls")) and bool(control.get("partially_covered_controls")) and bool(control.get("uncovered_controls")), "control coverage matrix has covered, partial, and uncovered controls", checks, violations)

    sensitive = loaded.get("static_sensitive_pattern_review", {})
    add(SENSITIVE_NON_CLAIMS.issubset(set(sensitive.get("non_claims", [])) | set(sensitive.get("known_gaps", []))), "sensitive pattern review includes required non-claims", checks, violations)

    audit = loaded.get("thor_odin_effectiveness_audit", {})
    add(bool(audit), "Thor/Odin effectiveness audit exists", checks, violations)
    add({"B1", "B2", "B3", "B4", "B5", "B6", "B7"}.issubset(set(audit.get("reviewed_bundles", []))), "Thor/Odin audit reviews B1-B7", checks, violations)
    scores = audit.get("quantitative_proxy_scores", {}) if isinstance(audit.get("quantitative_proxy_scores"), dict) else {}
    add(SCORE_KEYS.issubset(set(scores)), "Thor/Odin audit includes required proxy score keys", checks, violations)
    add(all(isinstance(scores.get(k), int) and 0 <= scores.get(k) <= 5 for k in SCORE_KEYS), "Thor/Odin proxy scores are bounded 0-5", checks, violations)
    add(all(audit.get(k) for k in ["what_was_strong", "what_was_medium", "what_was_weak", "what_was_overbuilt", "qualitative_findings"]), "Thor/Odin audit includes qualitative strength/medium/weak/overbuilt findings", checks, violations)
    add(all(audit.get(k) for k in ["recommendations_keep", "recommendations_improve", "recommendations_reduce", "recommendations_defer"]), "Thor/Odin audit includes keep/improve/reduce/defer recommendations", checks, violations)

    add(REQUIRED_KNOWN_GAPS.issubset(set(report_data.get("known_security_gaps", []))), "B8 report contains required known security gaps", checks, violations)
    add("security_certification" in set(report_data.get("denied_claims", [])) and "vulnerability_free_claim" in set(report_data.get("denied_claims", [])), "B8 report denies security certification and vulnerability-free claims", checks, violations)
    denied = set(report_data.get("denied_claims", []))
    add({"production_readiness", "release_approval", "deployment_proof", "runtime_proof"}.issubset(denied), "B8 report denies production/release/deployment/runtime proof", checks, violations)

    all_b8_data = {"examples": loaded, "report": report_data}
    add(not positive_claim_seen(all_b8_data), "no positive security certification, vulnerability-free, production, release, deployment, runtime, provider, or model proof claim exists", checks, violations)

    for rel in ["tools/v7_1_1/check_b8_security_review_track.py", "tests/test_v7_1_1_b8_security_review_track.py", "odin/cli.py"]:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        add(not any(token in text for token in FORBIDDEN_IMPORT_TOKENS), f"no provider/network/API-key SDK imports in {rel}", checks, violations)

    manifest_path = root / "FILE_MANIFEST.json"
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        paths = [item.get("path", "") for item in manifest.get("files", []) if isinstance(item, dict)]
        add(not any(any(part in path for part in FORBIDDEN_MANIFEST_PARTS) for path in paths), "FILE_MANIFEST excludes .thor/cache/build/dist/egg-info/pyc artifacts", checks, violations)
    else:
        add(False, "FILE_MANIFEST.json exists", checks, violations)

    for name, data in loaded.items():
        add(bool(data.get("claim_boundary")), f"{name} has claim_boundary", checks, violations)
        add(data.get("candidate_only") is True, f"{name} is candidate_only", checks, violations)
        add(bool(data.get("non_claims")), f"{name} has non_claims", checks, violations)

    generated = dict(report_data) if report_data else {}
    generated.update(
        {
            "generated_at_utc": generated_at_utc,
            "validator_id": "tools/v7_1_1/check_b8_security_review_track.py",
            "validation_checks": checks,
            "hard_violations": violations,
            "known_security_gaps": report_data.get("known_security_gaps", sorted(REQUIRED_KNOWN_GAPS)),
            "claim_boundary": report_data.get("claim_boundary", "b8_validator_report_is_static_review_not_runtime_proof"),
            "candidate_only": report_data.get("candidate_only", True),
            "non_claims": report_data.get("non_claims", []),
        }
    )
    return generated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", required=True)
    args = parser.parse_args(argv)
    root = Path(args.repo_root).resolve()
    out = Path(args.out)
    report = validate(root, args.generated_at_utc)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 1 if report.get("hard_violations") else 0


if __name__ == "__main__":
    raise SystemExit(main())
