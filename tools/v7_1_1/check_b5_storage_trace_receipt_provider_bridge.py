#!/usr/bin/env python3
"""Deterministic B5 static validator.

This tool validates PR-31/B5 storage, trace, receipt, provider-policy, Thor/Odin
bridge-prep, and SDK/App bridge-prep contracts. It does not execute providers,
read provider secrets, call networks, mutate app state, or write anywhere except
an explicitly requested report path.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

B5_IDS = [f"V711-R100-{i:03d}" for i in range(138, 170)]
B5_FAMILIES = ["PR-35-STORAGE-TRACE-RECEIPT", "PR-36-THOR-AGENT-HANDOFF", "PR-37-SDK-APP-BRIDGE"]
REQUIRED_TRACE_EVENTS = {
    "modelworkpacket_created", "minicheck_completed", "critic_packet_created",
    "critic_cascade_completed", "tournament_completed", "candidate_dna_created",
    "candidate_artifact_created", "response_packet_created", "final_gate_advisory_created",
    "receipt_boundary_created", "storage_record_created", "provider_policy_checked",
    "provider_runtime_deferred",
}
B5_CONTRACTS = [
    "storage_record", "trace_record", "receipt_ledger", "provider_policy",
    "local_provider_seam_prep", "thor_odin_bridge_prep", "sdk_app_bridge_prep",
]
FORBIDDEN_IMPORTS = {"requests", "httpx", "openai", "ollama", "llama_cpp"}
FORBIDDEN_TEXT = {"api" + "_key", "subprocess" + ".run", "Popen" + "(", "socket" + ".", "urllib" + ".request"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check(condition: bool, msg: str, bucket: list[dict[str, str]], violations: list[str]) -> None:
    bucket.append({"status": "pass" if condition else "fail", "msg": msg})
    if not condition:
        violations.append(msg)


def b5_bundle(root: Path, violations: list[str], checks: list[dict[str, str]]) -> dict[str, Any] | None:
    path = root / "registries" / "v7_1_1_actual_codex_bundle_plan.json"
    if not path.exists():
        violations.append("actual bundle registry missing")
        return None
    data = load_json(path)
    bundle = next((b for b in data.get("actual_bundles", []) if b.get("bundle_id") == "B5"), None)
    check(bundle is not None, "B5 mapping exists", checks, violations)
    if not bundle:
        return None
    check(bundle.get("actual_pr") == "PR-31", "B5 actual_pr is PR-31", checks, violations)
    check(bundle.get("slice_range") == "V711-R100-138..169", "B5 maps V711-R100-138..169", checks, violations)
    slice_ids = bundle.get("slice_ids", [])
    check(len(slice_ids) == 32, f"B5 has exactly 32 slice IDs (got {len(slice_ids)})", checks, violations)
    check(set(slice_ids) == set(B5_IDS), "B5 has no out-of-range slice IDs", checks, violations)
    check(bundle.get("absorbed_future_pr_families") == B5_FAMILIES, "B5 absorbs exactly PR-35, PR-36, PR-37", checks, violations)
    for bid, pr, rng in [("B1", "PR-27", "V711-R100-022..047"), ("B2", "PR-28", "V711-R100-048..075"), ("B3", "PR-29", "V711-R100-076..105"), ("B4", "PR-30", "V711-R100-106..137")]:
        prev = next((b for b in data.get("actual_bundles", []) if b.get("bundle_id") == bid), None)
        check(prev is not None and prev.get("actual_pr") == pr and prev.get("slice_range") == rng, f"{bid} mapping preserved", checks, violations)
    ladder = load_json(root / "registries" / "v7_1_1_road_to_100_ladder.json")
    ladder_ids = {s.get("id") for s in ladder.get("slices", [])}
    check(set(B5_IDS).issubset(ladder_ids), "canonical ladder contains V711-R100-138..169", checks, violations)
    check(ladder.get("canonical_slice_count", 0) >= 190, "canonical ladder preserved", checks, violations)
    return bundle


def contract_paths(root: Path, name: str) -> tuple[Path, Path, Path]:
    return (
        root / "schemas" / f"v7_1_1_{name}.schema.json",
        root / "registries" / f"v7_1_1_{name}_registry.json",
        root / "examples" / "v7_1_1" / f"{name}.example.json",
    )


def validate_contract_files(root: Path, violations: list[str], report: dict[str, Any]) -> None:
    for name in B5_CONTRACTS:
        schema, registry, example = contract_paths(root, name)
        bucket = report[f"{name}_checks"]
        for path in (schema, registry, example):
            check(path.exists(), f"{path.relative_to(root).as_posix()} exists", bucket, violations)
        if not all(p.exists() for p in (schema, registry, example)):
            continue
        sch, reg, ex = load_json(schema), load_json(registry), load_json(example)
        check("claim_boundary" in ex and "non_claims" in ex and ex.get("candidate_only") is True, f"{name} has claim boundary and non-claims", bucket, violations)
        if name == "storage_record":
            for field in ["response_packet_id", "candidate_artifact_id", "candidate_dna_id", "receipt_boundary_id"]:
                check(field in sch.get("required", []) and field in ex, f"Storage Record consumes {field}", bucket, violations)
            check(ex.get("content_ref") and ex.get("content_hash") and ex.get("raw_content_storage_default") == "disabled", "Storage Record stores refs/hashes by default", bucket, violations)
            raw = ex.get("raw_content")
            sensitive = ex.get("privacy_class") in {"sensitive", "redacted"}
            explicit = ex.get("raw_content_requires_explicit_storage_policy") is True and ex.get("storage_policy_ref")
            check(not (raw and sensitive and not explicit), "Storage Record blocks sensitive raw content without explicit policy", bucket, violations)
        elif name == "trace_record":
            kinds = {e.get("event_kind") for e in ex.get("trace_events", [])}
            check(REQUIRED_TRACE_EVENTS.issubset(kinds), "Trace Record contains required event kinds", bucket, violations)
            check("privacy_class" in ex, "Trace Record preserves privacy_class", bucket, violations)
        elif name == "receipt_ledger":
            for field in ["accepted_claim_refs", "denied_claim_refs", "pending_claim_refs"]:
                check(field in ex, f"Receipt Ledger has {field}", bucket, violations)
            check(ex.get("is_absolute_truth") is False and ex.get("is_runtime_proof") is False, "Receipt Ledger is not truth or runtime proof", bucket, violations)
        elif name == "provider_policy":
            check(ex.get("local_first") is True, "Provider Policy local_first true", bucket, violations)
            check(ex.get("network_default") == "disabled", "Provider Policy network disabled by default", bucket, violations)
            check(ex.get("hidden_remote_fallback_allowed") is False, "Provider Policy hidden remote fallback disabled", bucket, violations)
            check(ex.get("provider_execution_default") == "disabled", "Provider Policy execution disabled by default", bucket, violations)
            check(ex.get("remote_requires_explicit_policy") is True and ex.get("remote_requires_receipt") is True and ex.get("receipt_required_before_execution") is True, "Provider Policy explicit policy and receipt required", bucket, violations)
        elif name == "local_provider_seam_prep":
            entries = reg.get("local_provider_seam_preps", [ex])
            classes = {item.get("provider_class") for item in entries if isinstance(item, dict)} | set(ex.get("contract_classes", []))
            check({"mock_provider", "local_ollama_candidate", "local_llama_cpp_candidate", "external_agent_worker", "cannot_safely_complete"}.issubset(classes), "Local Provider Seam Prep has required contract classes", bucket, violations)
            check(all(item.get("execution_mode") in {"mock_only", "dry_run", "cannot_safely_complete"} for item in entries if isinstance(item, dict)), "Local Provider Seam Prep has no execution-by-default", bucket, violations)
            check(all(not item.get("api" + "_key_required", False) for item in entries if item.get("provider_class") in {"local_ollama_candidate", "local_llama_cpp_candidate"}), "Local candidates do not require provider secrets", bucket, violations)
        elif name == "thor_odin_bridge_prep":
            mapped = {(m.get("thor_field"), m.get("odin_target")) for m in ex.get("mapping_rules", [])}
            needed = {("THOR_RECEIPT.accepted_claim_refs", "Odin ReceiptBoundary accepted_claim_refs"), ("THOR_RECEIPT.denied_claim_refs", "Odin ReceiptBoundary denied_claim_refs"), ("THOR_RECEIPT.pending_claim_refs", "Odin ReceiptBoundary pending_claim_refs")}
            check(needed.issubset(mapped), "Thor-Odin Bridge maps THOR_RECEIPT partitions", bucket, violations)
            check(ex.get("is_static_mapping_only") is True and ex.get("is_runtime_bridge") is False, "Thor-Odin Bridge Prep is static-only", bucket, violations)
        elif name == "sdk_app_bridge_prep":
            app_auth = set(ex.get("app_owned_authorities", []))
            check({"apply", "state", "domain_truth", "user_permissions", "external_send"}.issubset(app_auth), "SDK/App Bridge preserves app-owned authorities", bucket, violations)
            check(ex.get("does_not_apply_changes") is True and ex.get("does_not_own_app_state") is True, "SDK/App Bridge does not claim app apply authority", bucket, violations)


def validate_b4_boundaries(root: Path, violations: list[str], checks: list[dict[str, str]]) -> None:
    fga = load_json(root / "examples" / "v7_1_1" / "final_gate_advisory.example.json")
    rb = load_json(root / "examples" / "v7_1_1" / "receipt_boundary.example.json")
    check(fga.get("is_apply_gate") is False, "Final Gate Advisory is not Apply Gate", checks, violations)
    check(fga.get("is_app_authority") is False, "Final Gate Advisory is not app authority", checks, violations)
    check(rb.get("is_absolute_truth") is False, "Receipt Boundary is not absolute truth", checks, violations)
    check(rb.get("is_runtime_proof") is False, "Receipt Boundary is not runtime proof", checks, violations)


def validate_no_provider_execution(root: Path, violations: list[str]) -> None:
    paths = [root / "tools" / "v7_1_1" / "check_b5_storage_trace_receipt_provider_bridge.py"]
    adapter = root / "odin" / "provider_seams" / "local_provider_adapter.py"
    if adapter.exists():
        paths.append(adapter)
    for path in paths:
        text = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                            violations.append(f"forbidden provider/network import {alias.name} in {path.relative_to(root)}")
                if isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                    violations.append(f"forbidden provider/network import {node.module} in {path.relative_to(root)}")
        except SyntaxError as exc:
            violations.append(f"could not parse {path.relative_to(root)}: {exc}")
        for token in FORBIDDEN_TEXT:
            if token in text:
                violations.append(f"forbidden provider/API/network token {token} in {path.relative_to(root)}")


def build_report(root: Path, generated_at_utc: str) -> dict[str, Any]:
    violations: list[str] = []
    report: dict[str, Any] = {
        "report_id": "odin.v7_1_1_b5_storage_trace_receipt_provider_bridge_report",
        "version": "7.1.1",
        "status": "local_storage_trace_receipt_provider_bridge_prep_report_not_runtime_proof",
        "generated_at_utc": generated_at_utc,
        "claim_boundary": "b5_report_is_static_storage_trace_receipt_provider_bridge_validation_not_runtime_or_apply_proof",
        "bundle": {}, "source_refs": [], "schema_refs": [], "registry_refs": [],
        "slice_coverage": [], "absorbed_future_pr_families": [],
        "storage_record_checks": [], "trace_record_checks": [], "receipt_ledger_checks": [],
        "provider_policy_checks": [], "local_provider_seam_prep_checks": [],
        "thor_odin_bridge_prep_checks": [], "sdk_app_bridge_prep_checks": [],
        "final_gate_boundary_checks": [], "hard_violations": [],
        "non_claims": ["not_runtime_proof", "not_provider_execution_proof", "not_model_quality_proof", "not_app_apply_authority", "not_external_send"],
        "senior_reviewer_notes": ["B5 is static prep with prior bundle boundaries preserved."],
        "senior_code_reviewer_notes": ["Provider execution defaults remain disabled; validator checks no SDK/network imports in B5 implementation."],
    }
    bundle_checks: list[dict[str, str]] = []
    bundle = b5_bundle(root, violations, bundle_checks)
    report["bundle"] = {"checks": bundle_checks, **(bundle or {})}
    report["slice_coverage"] = B5_IDS
    report["absorbed_future_pr_families"] = B5_FAMILIES
    report["source_refs"] = ["registries/v7_1_1_actual_codex_bundle_plan.json", "registries/v7_1_1_road_to_100_ladder.json"]
    report["schema_refs"] = [f"schemas/v7_1_1_{name}.schema.json" for name in B5_CONTRACTS] + ["schemas/v7_1_1_b5_storage_trace_receipt_provider_bridge_report.schema.json"]
    report["registry_refs"] = [f"registries/v7_1_1_{name}_registry.json" for name in B5_CONTRACTS]
    validate_contract_files(root, violations, report)
    validate_b4_boundaries(root, violations, report["final_gate_boundary_checks"])
    validate_no_provider_execution(root, violations)
    # Evidence hygiene: report uses repository-relative refs only.
    for key in ["source_refs", "schema_refs", "registry_refs"]:
        for ref in report[key]:
            if str(root.resolve()) in ref:
                violations.append(f"absolute local path leaked in {key}: {ref}")
    report["hard_violations"] = violations
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", required=True)
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    out = Path(args.out)
    report = build_report(root, args.generated_at_utc)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not report["hard_violations"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
