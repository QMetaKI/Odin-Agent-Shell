#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

B7_NAMES = [
    "b7_closure_review",
    "thor_v4_1_2_intake_report",
    "thor_pack_intake_evaluation",
    "provider_runtime_evaluation_policy",
    "provider_runtime_receipt_guard",
    "local_provider_runtime_evaluation_prep",
    "security_review_separation",
    "target_host_runtime_separation",
    "b7_evaluation_report",
]
B1_B6_REPORTS = [
    "reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json",
    "reports/v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.json",
    "reports/v7_1_1_b3_modelworkpacket_scale_hybrid_report.json",
    "reports/v7_1_1_b4_minicheck_critics_final_gate_report.json",
    "reports/v7_1_1_b5_storage_trace_receipt_provider_bridge_report.json",
    "reports/v7_1_1_b6_acceptance_dojo_scoreboard_closure_report.json",
]
B1_B6_REGISTRIES = [
    "registries/v7_1_1_provider_policy_registry.json",
    "registries/v7_1_1_local_provider_seam_prep_registry.json",
    "registries/v7_1_1_receipt_ledger_registry.json",
    "registries/v7_1_1_receipt_boundary_registry.json",
    "registries/v7_1_1_closure_guard_registry.json",
    "registries/v7_1_1_b7_plus_handoff_plan_registry.json",
]
EXPECTED_THOR_PACK_FILES = {
    "README.md",
    "HANDOFF.md",
    "PATCHPLAN.md",
    "GUARD.md",
    "EXPECTED_OUTPUT.md",
    "RETURN_CONTRACT.md",
    "REPO_CONTEXT.md",
    "READ_ORDER.md",
    "CHECKLIST.md",
    "RETURN_MANIFEST_TEMPLATE.json",
    "PACK_MANIFEST.json",
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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def add(ok: bool, message: str, bucket: list[dict[str, Any]], violations: list[str]) -> None:
    bucket.append({"check": message, "status": "pass" if ok else "fail"})
    if not ok:
        violations.append(message)


def first_item(registry: dict[str, Any], key: str) -> dict[str, Any]:
    value = registry.get(f"{key}s")
    if isinstance(value, list) and value and isinstance(value[0], dict):
        return value[0]
    for value in registry.values():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            return value[0]
    return {}


def read_contract(root: Path, name: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return (
        load_json(root / "schemas" / f"v7_1_1_{name}.schema.json"),
        load_json(root / "registries" / f"v7_1_1_{name}_registry.json"),
        load_json(root / "examples" / "v7_1_1" / f"{name}.example.json"),
    )


def all_repo_files(root: Path):
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        if any(part in {".git", "__pycache__", ".pytest_cache", ".mypy_cache"} for part in path.parts):
            continue
        if path.is_file():
            yield rel, path


def validate(root: Path, generated_at_utc: str) -> dict[str, Any]:
    report: dict[str, Any] = {
        "report_id": "odin.v7_1_1_b7_closure_thor_provider_eval_report",
        "version": "7.1.1",
        "status": "b7_static_eval_not_runtime_release_security_or_target_host_proof",
        "generated_at_utc": generated_at_utc,
        "claim_boundary": "b7_report_is_static_eval_not_runtime_release_security_or_target_host_proof",
        "source_refs": [],
        "closure_review_checks": [],
        "thor_v4_1_2_intake_checks": [],
        "thor_pack_intake_checks": [],
        "provider_runtime_policy_checks": [],
        "provider_runtime_receipt_guard_checks": [],
        "local_provider_runtime_prep_checks": [],
        "security_separation_checks": [],
        "target_host_separation_checks": [],
        "hard_violations": [],
        "known_gaps": [],
        "deferred_items": [],
        "next_recommendations": [],
        "non_claims": [
            "not_release_certification",
            "not_production_readiness",
            "not_security_certification",
            "not_target_host_runtime_proof",
            "not_provider_execution_proof",
            "no_provider_runtime_execution",
            "no_model_inference",
            "no_api_key_read",
            "no_network_provider_call",
        ],
    }
    violations = report["hard_violations"]

    for rel in B1_B6_REPORTS + B1_B6_REGISTRIES:
        add((root / rel).exists(), f"{rel} exists", report["closure_review_checks"], violations)
        if (root / rel).exists():
            report["source_refs"].append(rel)

    loaded: dict[str, dict[str, Any]] = {}
    for name in B7_NAMES:
        paths = [
            root / "schemas" / f"v7_1_1_{name}.schema.json",
            root / "registries" / f"v7_1_1_{name}_registry.json",
            root / "examples" / "v7_1_1" / f"{name}.example.json",
        ]
        bucket = report["closure_review_checks"]
        if name.startswith("thor_v4"):
            bucket = report["thor_v4_1_2_intake_checks"]
        elif name.startswith("thor_pack"):
            bucket = report["thor_pack_intake_checks"]
        elif name.startswith("provider_runtime_evaluation"):
            bucket = report["provider_runtime_policy_checks"]
        elif name.startswith("provider_runtime_receipt"):
            bucket = report["provider_runtime_receipt_guard_checks"]
        elif name.startswith("local_provider"):
            bucket = report["local_provider_runtime_prep_checks"]
        elif name.startswith("security"):
            bucket = report["security_separation_checks"]
        elif name.startswith("target"):
            bucket = report["target_host_separation_checks"]
        for path in paths:
            add(path.exists(), f"{path.relative_to(root).as_posix()} exists", bucket, violations)
        if all(p.exists() for p in paths):
            _schema, registry, example = read_contract(root, name)
            loaded[name] = example
            add(example.get("candidate_only") is True, f"{name} candidate_only true", bucket, violations)
            add(bool(example.get("claim_boundary")) and bool(example.get("non_claims")), f"{name} boundary and non_claims present", bucket, violations)
            add(bool(first_item(registry, name)), f"{name} registry has item", bucket, violations)

    closure = loaded.get("b7_closure_review", {})
    add(set(closure.get("source_bundles", [])) >= {"B1", "B2", "B3", "B4", "B5", "B6"}, "closure review consumes B1-B6", report["closure_review_checks"], violations)
    add(not closure.get("hard_blockers"), "closure review has no hard blockers", report["closure_review_checks"], violations)

    thor = loaded.get("thor_v4_1_2_intake_report", {})
    version_text = json.dumps(thor.get("version_sources", []), sort_keys=True)
    for token in ["README.md", "docs/RELEASE_STATUS.md", "pyproject.toml", "src/thor/__init__.py", "src/thor/capabilities.py", "4.1.2"]:
        add(token in version_text, f"Thor version source includes {token}", report["thor_v4_1_2_intake_checks"], violations)
    release_status = thor.get("release_status", {})
    add(release_status.get("state") == "prepared_not_released", "Thor treated as prepared_not_released", report["thor_v4_1_2_intake_checks"], violations)
    for key, expected in [("tag", "tag_not_verified"), ("github_release", "github_release_not_verified"), ("pypi", "pypi_not_verified"), ("assets", "assets_not_verified")]:
        add(release_status.get(key) == expected, f"Thor external {key} is not verified", report["thor_v4_1_2_intake_checks"], violations)

    pack = loaded.get("thor_pack_intake_evaluation", {})
    add(pack.get("intake_status") in {"shape_valid_static", "shape_invalid_static", "requires_review", "deferred_to_manual_thor_session", "cannot_safely_complete", "not_run"}, "Thor pack status is allowed", report["thor_pack_intake_checks"], violations)
    add(EXPECTED_THOR_PACK_FILES.issubset(set(pack.get("expected_thor_pack_files", []))), "Thor expected pack files listed", report["thor_pack_intake_checks"], violations)
    add(pack.get("pack_artifacts_committed") is False, "no Thor pack artifacts committed by contract", report["thor_pack_intake_checks"], violations)
    add(pack.get("thor_session_artifacts_committed") is False, "no .thor artifacts committed by contract", report["thor_pack_intake_checks"], violations)

    policy = loaded.get("provider_runtime_evaluation_policy", {})
    for field in ["network_allowed", "remote_allowed", "api_key_allowed", "hidden_remote_fallback_allowed", "actual_provider_execution_allowed_in_this_pr"]:
        add(policy.get(field) is False, f"provider runtime policy {field} false", report["provider_runtime_policy_checks"], violations)
    for field in ["requires_receipt_guard", "requires_local_only", "requires_explicit_user_or_repo_policy"]:
        add(policy.get(field) is True, f"provider runtime policy {field} true", report["provider_runtime_policy_checks"], violations)
    add("remote_network_request" in policy.get("forbidden_probe_types", []), "remote network request forbidden", report["provider_runtime_policy_checks"], violations)

    guard = loaded.get("provider_runtime_receipt_guard", {})
    add(guard.get("guard_status") in {"guard_pass_static", "guard_warn_static", "guard_block_static", "requires_human_review", "cannot_safely_complete"}, "receipt guard status allowed", report["provider_runtime_receipt_guard_checks"], violations)
    add("authorizes_nothing" in guard.get("claim_boundary", "") or "does_not_authorize_provider_runtime" in json.dumps(guard.get("non_claims", [])), "receipt guard authorizes nothing by itself", report["provider_runtime_receipt_guard_checks"], violations)

    prep = loaded.get("local_provider_runtime_evaluation_prep", {})
    for field in ["actual_inference_run", "actual_benchmark_run", "network_used", "api_key_read"]:
        add(prep.get(field) is False, f"local provider runtime prep {field} false", report["local_provider_runtime_prep_checks"], violations)
    add(prep.get("probe_status") in {"not_run", "static_contract_only", "dry_run_only", "local_presence_check_deferred", "blocked_by_missing_policy", "blocked_by_missing_receipt", "blocked_by_missing_local_only_guard", "requires_human_review", "cannot_safely_complete"}, "local provider runtime prep status allowed", report["local_provider_runtime_prep_checks"], violations)

    security = loaded.get("security_review_separation", {})
    add("security_certification" in json.dumps(security.get("excluded_from_b7_claims", [])), "security certification separated", report["security_separation_checks"], violations)
    target = loaded.get("target_host_runtime_separation", {})
    add("target_host_runtime_proof" in json.dumps(target.get("excluded_from_b7_claims", [])), "target-host proof separated", report["target_host_separation_checks"], violations)

    eval_report = loaded.get("b7_evaluation_report", {})
    report["known_gaps"] = list(eval_report.get("known_gaps", []))
    report["deferred_items"] = list(eval_report.get("deferred_items", []))
    report["next_recommendations"] = list(eval_report.get("next_recommendations", []))
    add(bool(report["known_gaps"]), "B7 evaluation report known gaps non-empty", report["closure_review_checks"], violations)
    add(bool(report["deferred_items"]), "B7 evaluation report deferred items non-empty", report["closure_review_checks"], violations)
    add(bool(report["next_recommendations"]), "B7 evaluation report next recommendations non-empty", report["closure_review_checks"], violations)

    for rel, path in all_repo_files(root):
        if rel.startswith(".thor/") or "/.thor/" in rel:
            violations.append(f".thor artifact present in repository tree: {rel}")
        if rel.startswith("Thor-Agent-Kit/") or "/Thor-Agent-Kit/" in rel:
            violations.append(f"Thor-Agent-Kit file present in repository tree: {rel}")
        if rel.startswith(".thor/exports/") or "/.thor/exports/" in rel:
            violations.append(f"Thor pack artifact committed from Thor export tree: {rel}")
        if path.suffix == ".py" and ("b7_closure_thor_provider_eval" in rel or rel == "odin/cli.py"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(token in text for token in FORBIDDEN_IMPORT_TOKENS):
                violations.append(f"forbidden provider SDK/network import token in {rel}")
    b7_relevant = []
    for rel, path in all_repo_files(root):
        if path.suffix not in {".json", ".md", ".py"}:
            continue
        if "b7" in rel.lower() or "PR_33" in rel or rel == "odin/cli.py":
            b7_relevant.append(path.read_text(encoding="utf-8", errors="ignore").lower())
    text_blob = "\n".join(b7_relevant)
    forbidden_pairs = [("final gate", "apply gate"), ("receipt ledger", "absolute truth"), ("receipt ledger", "as absolute truth")]
    for left, right in forbidden_pairs:
        phrase = left + " " + right
        add(phrase not in text_blob, f"no {left}/{right} elevation", report["closure_review_checks"], violations)

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", required=True)
    args = parser.parse_args(argv)
    root = Path(args.repo_root).resolve()
    report = validate(root, args.generated_at_utc)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not report["hard_violations"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
