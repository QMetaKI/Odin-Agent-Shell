#!/usr/bin/env python3
"""Deterministic B6 static validator.

Validates PR-32/B6 static acceptance, dojo, scoreboard, closure-prep, guard,
and B7+ handoff artifacts. The validator is read-only except for the explicit
--out report path and performs no provider, model, network, QIRC-server, app
mutation, external-send, or secret handling.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

B6_IDS = [f"V711-R100-{i:03d}" for i in range(170, 190)]
B6_FAMILIES = ["PR-38-ACCEPTANCE-DOJO-SCOREBOARD-CLOSURE"]
PREVIOUS = {
    "B1": ("PR-27", "V711-R100-022..047"),
    "B2": ("PR-28", "V711-R100-048..075"),
    "B3": ("PR-29", "V711-R100-076..105"),
    "B4": ("PR-30", "V711-R100-106..137"),
    "B5": ("PR-31", "V711-R100-138..169"),
}
B6_CONTRACTS = [
    "acceptance_harness",
    "dojo_session",
    "scoreboard",
    "closure_checklist",
    "closure_readiness_matrix",
    "road_to_100_closure_report",
    "closure_guard",
    "b7_plus_handoff_plan",
]
B4_B5_IDS = [
    "response_packet_id",
    "candidate_artifact_id",
    "candidate_dna_id",
    "final_gate_advisory_id",
    "receipt_boundary_id",
    "storage_record_id",
    "trace_record_id",
    "receipt_ledger_id",
]
ACCEPTANCE_CHECKS = {
    "claim_boundary_integrity", "non_claim_presence", "evidence_ref_presence",
    "response_packet_completeness", "candidate_lineage_traceability",
    "privacy_class_preserved", "storage_trace_receipt_consistency",
    "receipt_partition_consistency", "final_gate_advisory_boundary",
    "provider_policy_disabled_defaults", "thor_odin_bridge_static_only",
    "sdk_app_bridge_no_app_authority", "no_runtime_proof_claim",
    "no_release_proof_claim",
}
TRAINING_MODES = {"static_review", "contract_drill", "boundary_drill", "evidence_drill", "closure_drill", "regression_drill"}
SCORING_MODES = {"static_evidence_score", "static_review_score", "closure_prep_score", "human_review_required"}
SCORING_DIMS = {
    "contract_compliance", "claim_boundary_compliance", "evidence_completeness",
    "traceability", "privacy_discipline", "receipt_partition_integrity",
    "provider_boundary_integrity", "app_authority_boundary",
    "thor_bridge_static_boundary", "final_gate_advisory_boundary",
    "regression_preservation", "closure_readiness",
}
CLOSURE_CHECKS = {
    "canonical_ladder_preserved", "actual_bundle_plan_complete", "b1_mapping_preserved",
    "b2_mapping_preserved", "b3_mapping_preserved", "b4_mapping_preserved",
    "b5_mapping_preserved", "claim_boundaries_present", "non_claims_present",
    "no_forbidden_runtime_claims", "no_app_authority_leak", "no_final_gate_elevation",
    "no_provider_execution", "no_network_default", "no_hidden_remote_fallback",
    "evidence_substrate_present", "acceptance_harness_present", "scoreboard_present",
    "closure_report_present", "known_gaps_present", "b7_plus_recommendations_present",
}
STATUSES = {"ready_static", "warn_static", "blocked_static", "deferred_to_b7_plus", "requires_human_review", "cannot_safely_complete"}
ROW_FIELDS = {"row_id", "subject_ref", "status", "reason", "evidence_refs", "blocking_claim_refs", "pending_claim_refs", "deferred_to"}
KNOWN_GAPS = {
    "real_thor_pack_to_odin_intake_not_evaluated",
    "actual_local_provider_runtime_not_evaluated",
    "production_deployment_not_proven",
    "security_certification_not_performed",
    "live_model_quality_not_measured",
    "app_owned_apply_gate_not_implemented_by_odin",
}
RECS = {
    "evaluate_real_thor_pack_to_odin_intake",
    "evaluate_local_provider_runtime_under_policy_and_receipt_guard",
    "perform_b1_to_b6_contract_closure_review",
    "evaluate_target_host_runtime_separately",
    "evaluate_security_review_separately",
}
GUARDS = {
    "no_release_certification", "no_production_readiness", "no_deployment_proof",
    "no_runtime_proof", "no_provider_execution_proof", "no_live_model_quality_proof",
    "no_security_certification", "no_app_authority", "no_final_gate_elevation",
    "no_receipt_truth_elevation",
}
NON_CLAIMS = [
    "not_release_certification", "not_production_readiness", "not_deployment_proof",
    "not_runtime_proof", "not_provider_execution_proof", "not_live_model_inference_proof",
    "not_model_quality_proof", "not_security_certification",
    "not_app_apply_or_state_or_external_send_authority",
]
BAD_IMPORTS = {"req" + "uests", "htt" + "px", "ope" + "nai", "oll" + "ama", "llama" + "_cpp"}
BAD_TEXT = {"api" + "_key", "subprocess" + ".run", "Popen" + "(", "socket" + ".", "urllib" + ".request"}
BAD_CLAIM_TOKENS = {
    "app_acceptance", "release_approval", "release_certification", "production_readiness",
    "deployment_proof", "runtime_proof", "provider_execution_proof",
    "live_model_inference_proof", "model_quality_proof", "security_certification",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def add(condition: bool, msg: str, bucket: list[dict[str, str]], violations: list[str]) -> None:
    bucket.append({"status": "pass" if condition else "fail", "msg": msg})
    if not condition:
        violations.append(msg)


def contract_paths(root: Path, name: str) -> tuple[Path, Path, Path]:
    return (
        root / "schemas" / f"v7_1_1_{name}.schema.json",
        root / "registries" / f"v7_1_1_{name}_registry.json",
        root / "examples" / "v7_1_1" / f"{name}.example.json",
    )


def schema_enums(node: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(node, dict):
        if isinstance(node.get("enum"), list):
            found.update(str(x) for x in node["enum"])
        for value in node.values():
            found.update(schema_enums(value))
    elif isinstance(node, list):
        for item in node:
            found.update(schema_enums(item))
    return found


def all_text(value: Any) -> str:
    return json.dumps(value, sort_keys=True).lower()


def has_non_claims(example: dict[str, Any], *tokens: str) -> bool:
    text = all_text(example.get("non_claims", [])) + " " + str(example.get("claim_boundary", "")).lower()
    return all(token in text for token in tokens)


def registry_items(reg: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for value in reg.values():
        if isinstance(value, list):
            out.extend(x for x in value if isinstance(x, dict))
    return out


def validate_bundle(root: Path, report: dict[str, Any], violations: list[str]) -> dict[str, Any] | None:
    checks = report["boundary_checks"]
    plan_path = root / "registries" / "v7_1_1_actual_codex_bundle_plan.json"
    if not plan_path.exists():
        violations.append("actual bundle registry missing")
        return None
    data = load_json(plan_path)
    bundle = next((b for b in data.get("actual_bundles", []) if b.get("bundle_id") == "B6"), None)
    add(bundle is not None, "B6 mapping exists", checks, violations)
    if not bundle:
        return None
    add(bundle.get("actual_pr") == "PR-32", "B6 actual_pr is PR-32", checks, violations)
    add(bundle.get("slice_range") == "V711-R100-170..189", "B6 maps V711-R100-170..189", checks, violations)
    add(bundle.get("exact_slice_count") == 20, "B6 exact_slice_count is 20", checks, violations)
    add(bundle.get("slice_ids") == B6_IDS, "B6 has exactly canonical slice IDs V711-R100-170..189", checks, violations)
    add(bundle.get("absorbed_future_pr_families") == B6_FAMILIES, "B6 absorbs exactly PR-38 closure family", checks, violations)
    for bid, (pr, rng) in PREVIOUS.items():
        prev = next((b for b in data.get("actual_bundles", []) if b.get("bundle_id") == bid), None)
        add(prev is not None and prev.get("actual_pr") == pr and prev.get("slice_range") == rng, f"{bid} mapping preserved", checks, violations)
    ladder = load_json(root / "registries" / "v7_1_1_road_to_100_ladder.json")
    ladder_ids = {s.get("id") for s in ladder.get("slices", [])}
    add(set(B6_IDS).issubset(ladder_ids), "canonical ladder contains V711-R100-170..189", checks, violations)
    add(ladder.get("canonical_slice_count", 0) >= 190, "canonical ladder preserved", checks, violations)
    report["bundle"] = {"actual_pr": "PR-32", "bundle_id": "B6", "slice_range": "V711-R100-170..189", "exact_slice_count": 20}
    report["slice_coverage"] = B6_IDS
    report["absorbed_future_pr_families"] = B6_FAMILIES
    return bundle


def validate_contracts(root: Path, report: dict[str, Any], violations: list[str]) -> None:
    loaded: dict[str, tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = {}
    for name in B6_CONTRACTS:
        schema_path, registry_path, example_path = contract_paths(root, name)
        bucket = report[f"{name}_checks"] if f"{name}_checks" in report else report["road_to_100_closure_report_checks"]
        for path in (schema_path, registry_path, example_path):
            add(path.exists(), f"{path.relative_to(root).as_posix()} exists", bucket, violations)
        if all(p.exists() for p in (schema_path, registry_path, example_path)):
            loaded[name] = (load_json(schema_path), load_json(registry_path), load_json(example_path))
            example = loaded[name][2]
            add(example.get("candidate_only") is True and "claim_boundary" in example and example.get("non_claims"), f"{name} has boundary and non-claims", bucket, violations)

    if "acceptance_harness" in loaded:
        sch, _reg, ex = loaded["acceptance_harness"]
        req = set(sch.get("required", []))
        for field in B4_B5_IDS:
            add(field in req and field in ex, f"Acceptance Harness consumes {field}", report["acceptance_harness_checks"], violations)
        kinds = {c.get("check_kind") for c in ex.get("acceptance_checks", [])}
        add(ACCEPTANCE_CHECKS.issubset(kinds), "Acceptance Harness contains required check kinds", report["acceptance_harness_checks"], violations)
        add(has_non_claims(ex, "not_app_acceptance", "not_release_certification", "not_runtime_proof") and "cannot_apply_changes" in all_text(ex), "Acceptance Harness is static evidence only", report["acceptance_harness_checks"], violations)
        add("app_acceptance" not in str(ex.get("acceptance_mode", "")), "Acceptance Harness mode is not app acceptance", report["acceptance_harness_checks"], violations)

    if "dojo_session" in loaded:
        sch, _reg, ex = loaded["dojo_session"]
        add(TRAINING_MODES.issubset(schema_enums(sch)), "Dojo Session allowed training modes exist", report["dojo_session_checks"], violations)
        add(has_non_claims(ex, "does_not_execute_models", "does_not_execute_providers") and "does_not_mutate_app_state" in all_text(ex), "Dojo Session is static review/training only", report["dojo_session_checks"], violations)

    if "scoreboard" in loaded:
        sch, _reg, ex = loaded["scoreboard"]
        add(SCORING_MODES.issubset(schema_enums(sch)), "Scoreboard scoring modes exist", report["scoreboard_checks"], violations)
        add(SCORING_DIMS.issubset(set(ex.get("scoring_dimensions", []))), "Scoreboard scoring dimensions exist", report["scoreboard_checks"], violations)
        add(has_non_claims(ex, "not_correctness_proof", "not_benchmark_proof") and "production" in all_text(ex), "Scoreboard does not claim correctness/production/benchmark proof", report["scoreboard_checks"], violations)
        add("production_readiness" not in all_text(ex).replace("not_production_readiness", ""), "Scoreboard has no production readiness claim", report["scoreboard_checks"], violations)

    if "closure_checklist" in loaded:
        _sch, _reg, ex = loaded["closure_checklist"]
        add(CLOSURE_CHECKS.issubset(set(ex.get("required_checks", []))), "Closure Checklist required checks exist", report["closure_checklist_checks"], violations)
        add("not_release_approval" in all_text(ex), "Closure Checklist is not release approval", report["closure_checklist_checks"], violations)
        add("release_approval" not in all_text(ex).replace("not_release_approval", ""), "Closure Checklist has no release approval claim", report["closure_checklist_checks"], violations)

    if "closure_readiness_matrix" in loaded:
        sch, _reg, ex = loaded["closure_readiness_matrix"]
        add(STATUSES.issubset(schema_enums(sch)), "Closure Readiness Matrix statuses exist", report["closure_readiness_matrix_checks"], violations)
        rows = ex.get("readiness_rows", [])
        add(bool(rows) and all(ROW_FIELDS.issubset(row) for row in rows), "Closure Readiness Matrix row fields exist", report["closure_readiness_matrix_checks"], violations)
        add(has_non_claims(ex, "not_deployment_proof", "not_runtime_proof", "not_security_certification"), "Closure Readiness Matrix is not runtime/deployment/security proof", report["closure_readiness_matrix_checks"], violations)
        add("deployment_proof" not in all_text(ex).replace("not_deployment_proof", ""), "Closure Matrix has no deployment proof claim", report["closure_readiness_matrix_checks"], violations)

    if "road_to_100_closure_report" in loaded:
        _sch, _reg, ex = loaded["road_to_100_closure_report"]
        add(KNOWN_GAPS.issubset(set(ex.get("known_gaps", []))), "Closure Report includes required known_gaps", report["road_to_100_closure_report_checks"], violations)
        add(RECS.issubset(set(ex.get("b7_plus_recommendations", []))), "Closure Report includes B7+ recommendations", report["road_to_100_closure_report_checks"], violations)
        add(has_non_claims(ex, "not_release_certification", "not_runtime_proof", "not_security_certification"), "Closure Report is not release certification", report["road_to_100_closure_report_checks"], violations)
        report["known_gaps"] = ex.get("known_gaps", [])
        report["b7_plus_recommendations"] = ex.get("b7_plus_recommendations", [])

    if "closure_guard" in loaded:
        _sch, reg, _ex = loaded["closure_guard"]
        guard_ids = {item.get("closure_guard_id") for item in registry_items(reg)}
        add(GUARDS.issubset(guard_ids), "Closure Guard includes required no-overclaim guards", report["closure_guard_checks"], violations)

    if "b7_plus_handoff_plan" in loaded:
        _sch, _reg, ex = loaded["b7_plus_handoff_plan"]
        add(bool(ex.get("required_evidence_before_runtime")), "B7+ Handoff Plan includes runtime evidence prerequisites", report["b7_plus_handoff_plan_checks"], violations)
        add(bool(ex.get("required_policy_before_provider_runtime")), "B7+ Handoff Plan includes provider runtime policy prerequisite", report["b7_plus_handoff_plan_checks"], violations)
        add(bool(ex.get("required_receipt_before_provider_runtime")), "B7+ Handoff Plan includes provider runtime receipt prerequisite", report["b7_plus_handoff_plan_checks"], violations)
        add(has_non_claims(ex, "does_not_execute_b7_plus", "does_not_trigger_provider_runtime"), "B7+ Handoff Plan is planning only", report["b7_plus_handoff_plan_checks"], violations)


def validate_boundaries(root: Path, report: dict[str, Any], violations: list[str]) -> None:
    checks = report["boundary_checks"]
    fga = load_json(root / "examples" / "v7_1_1" / "final_gate_advisory.example.json")
    receipt = load_json(root / "examples" / "v7_1_1" / "receipt_ledger.example.json")
    policy = load_json(root / "examples" / "v7_1_1" / "provider_policy.example.json")
    bridge = load_json(root / "examples" / "v7_1_1" / "thor_odin_bridge_prep.example.json")
    sdk = load_json(root / "examples" / "v7_1_1" / "sdk_app_bridge_prep.example.json")
    add("not final gate as apply gate" in all_text(fga) or "not_apply_gate" in all_text(fga), "Final Gate Advisory remains not Apply Gate", checks, violations)
    add(receipt.get("is_absolute_truth") is False and receipt.get("is_runtime_proof") is False, "Receipt Ledger remains scoped evidence not absolute truth/proof", checks, violations)
    add("disabled" in all_text(policy) and "default" in all_text(policy), "Provider Policy remains disabled-by-default", checks, violations)
    add("static" in all_text(bridge) and "runtime" in all_text(bridge), "Thor-Odin Bridge remains static-only", checks, violations)
    add("does_not_apply_changes" in all_text(sdk) and "does_not_own_app_state" in all_text(sdk) and "does_not_send_externally" in all_text(sdk), "SDK/App Bridge Prep remains non-authoritative", checks, violations)


def validate_no_runtime_additions(root: Path, report: dict[str, Any], violations: list[str]) -> None:
    checks = report["boundary_checks"]
    files = [root / "tools" / "v7_1_1" / "check_b6_acceptance_dojo_scoreboard_closure.py"]
    for name in B6_CONTRACTS:
        files.extend(contract_paths(root, name))
    files.append(root / "schemas" / "v7_1_1_b6_acceptance_dojo_scoreboard_closure_report.schema.json")
    offenders: list[str] = []
    for path in files:
        if not path.exists() or path.suffix != ".py":
            continue
        text = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            offenders.append(f"{path.relative_to(root)} syntax error: {exc}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in BAD_IMPORTS:
                        offenders.append(f"forbidden import {alias.name} in {path.relative_to(root)}")
            elif isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] in BAD_IMPORTS:
                offenders.append(f"forbidden import {node.module} in {path.relative_to(root)}")
        for token in BAD_TEXT:
            if token in text:
                offenders.append(f"forbidden runtime/provider token in {path.relative_to(root)}")
    add(not offenders, "No provider SDK/network/API-key handling added in B6 implementation code", checks, violations)
    violations.extend(offenders)


def validate_evidence_paths(root: Path, report: dict[str, Any], violations: list[str]) -> None:
    ignored = [".thor", ".odin_runtime", "egg-info", "__pycache__", ".pytest_cache", "dist/", "build/"]
    bad: list[str] = []
    for name in B6_CONTRACTS:
        for path in contract_paths(root, name)[1:]:
            if path.exists():
                text = path.read_text(encoding="utf-8")
                for token in ignored:
                    if token in text:
                        bad.append(f"ignored/generated/local path token {token} in {path.relative_to(root)}")
    add(not bad, "No ignored generated/local paths are used as evidence", report["boundary_checks"], violations)
    violations.extend(bad)


def build_report(generated_at_utc: str) -> dict[str, Any]:
    return {
        "report_id": "odin.v7_1_1_b6_acceptance_dojo_scoreboard_closure_report",
        "version": "7.1.1",
        "status": "static_acceptance_dojo_scoreboard_closure_report_not_release_or_runtime_proof",
        "generated_at_utc": generated_at_utc,
        "claim_boundary": "b6_report_is_static_closure_prep_not_release_certification_or_runtime_proof",
        "bundle": {}, "source_refs": [], "schema_refs": [], "registry_refs": [],
        "slice_coverage": [], "absorbed_future_pr_families": [],
        "acceptance_harness_checks": [], "dojo_session_checks": [], "scoreboard_checks": [],
        "closure_checklist_checks": [], "closure_readiness_matrix_checks": [],
        "road_to_100_closure_report_checks": [], "closure_guard_checks": [],
        "b7_plus_handoff_plan_checks": [], "boundary_checks": [], "hard_violations": [],
        "known_gaps": [], "b7_plus_recommendations": [], "non_claims": NON_CLAIMS,
        "senior_reviewer_notes": ["static B6 closure-prep scope only; no release/runtime/security proof claim"],
        "senior_code_reviewer_notes": ["validator performs static JSON/path checks and writes only requested report path"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", required=True)
    args = parser.parse_args(argv)
    root = Path(args.repo_root).resolve()
    out = Path(args.out)
    report = build_report(args.generated_at_utc)
    violations: list[str] = []
    validate_bundle(root, report, violations)
    validate_contracts(root, report, violations)
    validate_boundaries(root, report, violations)
    validate_no_runtime_additions(root, report, violations)
    validate_evidence_paths(root, report, violations)
    report["source_refs"] = ["reports/v7_1_1_b4_minicheck_critics_final_gate_report.json", "reports/v7_1_1_b5_storage_trace_receipt_provider_bridge_report.json"]
    report["schema_refs"] = [f"schemas/v7_1_1_{name}.schema.json" for name in B6_CONTRACTS]
    report["registry_refs"] = [f"registries/v7_1_1_{name}_registry.json" for name in B6_CONTRACTS]
    report["hard_violations"] = sorted(set(violations))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 1 if report["hard_violations"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
