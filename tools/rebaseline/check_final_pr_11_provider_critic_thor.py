"""FINAL-PR-11 validator: Local Provider Receipt Harness + Critic Runtime Binding + Thor Handoff Compiler v0.

Claim boundary: final_pr_11_provider_receipt_critic_thor_compiler_not_release_closure
stdlib only, no external dependencies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

CLAIM_BOUNDARY = "final_pr_11_provider_receipt_critic_thor_compiler_not_release_closure"

_REQUIRED_MODULE_FILES = [
    "odin/local_provider_receipts/__init__.py",
    "odin/local_provider_receipts/provider_ids.py",
    "odin/local_provider_receipts/readiness.py",
    "odin/local_provider_receipts/request_packet.py",
    "odin/local_provider_receipts/receipt.py",
    "odin/local_provider_receipts/executor.py",
    "odin/local_provider_receipts/reports.py",
    "odin/critic_runtime/__init__.py",
    "odin/critic_runtime/critic_packet.py",
    "odin/critic_runtime/deterministic_critic.py",
    "odin/critic_runtime/cascade.py",
    "odin/critic_runtime/reports.py",
    "odin/thor_handoff_compiler/__init__.py",
    "odin/thor_handoff_compiler/input_contract.py",
    "odin/thor_handoff_compiler/compiler.py",
    "odin/thor_handoff_compiler/acceptance_matrix.py",
    "odin/thor_handoff_compiler/validator_plan.py",
    "odin/thor_handoff_compiler/pr_body.py",
    "odin/thor_handoff_compiler/reports.py",
    "odin/route_evaluation/__init__.py",
    "odin/route_evaluation/fixtures.py",
    "odin/route_evaluation/evaluator.py",
    "odin/route_evaluation/receipt.py",
    "odin/route_evaluation/reports.py",
]

_REQUIRED_DOCS = [
    "docs/rebaseline/FINAL_PR_11_PROVIDER_CRITIC_THOR.md",
    "docs/release/FINAL_PR_11_RELEASE_SEQUENCE_TRANSITION.md",
    "docs/release/FINAL_PR_11_LOCAL_PROVIDER_RECEIPT_HARNESS.md",
    "docs/release/FINAL_PR_11_CRITIC_RUNTIME_BINDING.md",
    "docs/release/FINAL_PR_11_ROUTE_EVALUATION_RECEIPTS.md",
    "docs/release/FINAL_PR_11_THOR_HANDOFF_COMPILER_V0.md",
    "docs/release/FINAL_PR_11_PREFLIGHT_AFTER_PR11.md",
    "docs/codex/handoffs/FINAL_PR_11_REPO_COGNITION_SUMMARY.md",
    "docs/codex/handoffs/FINAL_PR_11_THOR_STYLE_PROVIDER_CRITIC_HANDOFF.md",
    "docs/codex/handoffs/FINAL_PR_11_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
    "docs/codex/audits/FINAL_PR_11_PROVIDER_CRITIC_THOR_AUDIT.md",
    "docs/codex/audits/FINAL_PR_11_SENIOR_REVIEW.md",
    "docs/codex/audits/FINAL_PR_11_CODE_REVIEW.md",
    "docs/codex/audits/FINAL_PR_11_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md",
    "docs/codex/reports/FINAL_PR_11_PROVIDER_CRITIC_THOR_RETURN_REPORT.md",
]

_REQUIRED_EXAMPLES = [
    "examples/final_pr_11/provider_readiness_receipt.example.json",
    "examples/final_pr_11/provider_execution_unavailable_receipt.example.json",
    "examples/final_pr_11/provider_execution_scoped_receipt.example.json",
    "examples/final_pr_11/critic_packet.example.json",
    "examples/final_pr_11/critic_cascade.example.json",
    "examples/final_pr_11/route_evaluation_receipt.example.json",
    "examples/final_pr_11/thor_handoff_input_contract.example.json",
    "examples/final_pr_11/thor_handoff_bundle.example.json",
    "examples/final_pr_11/release_sequence_transition.example.json",
    "examples/final_pr_11/preflight_after_pr11.example.json",
]

_REQUIRED_REPORTS = [
    "reports/final_pr_11_provider_receipt_harness_report.json",
    "reports/final_pr_11_critic_runtime_binding_report.json",
    "reports/final_pr_11_route_evaluation_receipt_report.json",
    "reports/final_pr_11_thor_handoff_compiler_report.json",
    "reports/final_pr_11_release_sequence_transition_report.json",
    "reports/final_pr_11_preflight_after_pr11_report.json",
    "reports/final_pr_11_provider_critic_thor_proof_packet.json",
]

_REQUIRED_REGISTRIES = [
    "registries/final_pr_11_provider_critic_thor_registry.json",
    "registries/final_pr_11_provider_receipt_registry.json",
    "registries/final_pr_11_critic_runtime_registry.json",
    "registries/final_pr_11_thor_handoff_compiler_registry.json",
    "registries/final_pr_11_route_evaluation_registry.json",
    "registries/final_pr_11_release_sequence_registry.json",
]

_REQUIRED_SCHEMAS = [
    "schemas/final_pr_11_provider_receipt.schema.json",
    "schemas/final_pr_11_critic_packet.schema.json",
    "schemas/final_pr_11_thor_handoff_bundle.schema.json",
    "schemas/final_pr_11_route_evaluation_receipt.schema.json",
]

_REQUIRED_CLI_COMMANDS = [
    "validate-local-provider-receipt-harness",
    "local-provider-doctor",
    "run-local-provider-receipt",
    "explain-provider-receipt-claims",
    "validate-critic-runtime-binding",
    "run-critic-cascade",
    "explain-critic-cascade",
    "validate-route-evaluation-receipts",
    "run-route-evaluation",
    "explain-route-evaluation-claims",
    "validate-thor-handoff-compiler",
    "compile-thor-handoff",
    "explain-thor-handoff-compiler",
    "validate-final-pr-11-provider-critic-thor",
]

_REQUIRED_HUB_ENDPOINTS = [
    "/provider-receipts/status.json",
    "/provider-receipts/demo.json",
    "/provider-receipts/claims.json",
    "/critic-runtime/status.json",
    "/critic-runtime/demo.json",
    "/route-evaluation/status.json",
    "/route-evaluation/demo.json",
    "/thor-handoff-compiler/status.json",
    "/thor-handoff-compiler/demo.json",
    "/release/sequence-transition.json",
    "/release/preflight-after-pr11.json",
]

_REQUIRED_UI_SECTIONS = [
    "provider-receipt-harness-section",
    "critic-runtime-binding-section",
    "thor-handoff-compiler-section",
    "release-sequence-transition-section",
]

_FORBIDDEN_NETWORK_PATTERNS = [
    "urllib.request.urlopen",
    "requests.get",
    "requests.post",
    "socket.connect",
    "http.client.HTTPConnection",
]


def _load_json(path: Path) -> tuple[dict | list | None, str | None]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f), None
    except Exception as exc:
        return None, str(exc)


def _check_required_files(root: Path, file_list: list[str], label: str) -> list[str]:
    errors = []
    for rel in file_list:
        p = root / rel
        if not p.exists():
            errors.append(f"[{label}] missing: {rel}")
    return errors


def _check_json_files(root: Path, file_list: list[str]) -> list[str]:
    errors = []
    for rel in file_list:
        p = root / rel
        if not p.exists():
            continue
        obj, err = _load_json(p)
        if err:
            errors.append(f"invalid JSON in {rel}: {err}")
    return errors


def _check_no_eval_exec(root: Path) -> list[str]:
    errors = []
    new_modules = [
        root / "odin/local_provider_receipts",
        root / "odin/critic_runtime",
        root / "odin/route_evaluation",
        root / "odin/thor_handoff_compiler",
    ]
    for module_dir in new_modules:
        if not module_dir.exists():
            continue
        for py_file in module_dir.glob("*.py"):
            text = py_file.read_text(encoding="utf-8", errors="ignore")
            for bad in ["eval(", "exec("]:
                if bad in text:
                    errors.append(f"forbidden {bad!r} in {py_file.relative_to(root)}")
    return errors


def _check_no_public_network_in_modules(root: Path) -> list[str]:
    errors = []
    new_modules = [
        root / "odin/local_provider_receipts",
        root / "odin/critic_runtime",
        root / "odin/route_evaluation",
        root / "odin/thor_handoff_compiler",
    ]
    executor_path = root / "odin/local_provider_receipts/executor.py"
    for module_dir in new_modules:
        if not module_dir.exists():
            continue
        for py_file in module_dir.glob("*.py"):
            # executor.py is allowed subprocess but not public network
            text = py_file.read_text(encoding="utf-8", errors="ignore")
            for pattern in _FORBIDDEN_NETWORK_PATTERNS:
                if pattern in text and py_file != executor_path:
                    errors.append(f"forbidden public network call {pattern!r} in {py_file.relative_to(root)}")
    return errors


def _check_executor_no_shell_true(root: Path) -> list[str]:
    errors = []
    executor = root / "odin/local_provider_receipts/executor.py"
    if not executor.exists():
        return []
    text = executor.read_text(encoding="utf-8", errors="ignore")
    if "shell=True" in text:
        errors.append("executor.py must not use shell=True")
    return errors


def _check_provider_execution_disabled_by_default(root: Path) -> list[str]:
    errors = []
    receipt_path = root / "odin/local_provider_receipts/receipt.py"
    if not receipt_path.exists():
        return ["receipt.py missing"]
    text = receipt_path.read_text(encoding="utf-8", errors="ignore")
    if "allow_local_provider_execution: bool = False" not in text:
        errors.append("receipt.py: default allow_local_provider_execution must be False")
    return errors


def _check_cli_commands(root: Path) -> list[str]:
    errors = []
    cli_path = root / "odin/cli.py"
    if not cli_path.exists():
        return ["odin/cli.py missing"]
    text = cli_path.read_text(encoding="utf-8", errors="ignore")
    for cmd in _REQUIRED_CLI_COMMANDS:
        if cmd not in text:
            errors.append(f"CLI command not registered: {cmd}")
    if "validate_final_pr_11_provider_critic_thor" not in text:
        errors.append("validate_all() does not call validate_final_pr_11_provider_critic_thor")
    return errors


def _check_local_hub_endpoints(root: Path) -> list[str]:
    errors = []
    server_path = root / "odin/local_hub/server.py"
    if not server_path.exists():
        return ["odin/local_hub/server.py missing"]
    text = server_path.read_text(encoding="utf-8", errors="ignore")
    for endpoint in _REQUIRED_HUB_ENDPOINTS:
        if endpoint not in text:
            errors.append(f"Local Hub endpoint not registered: {endpoint}")
    return errors


def _check_ui_sections(root: Path) -> list[str]:
    errors = []
    ui_path = root / "odin/local_hub/ui.py"
    if not ui_path.exists():
        return ["odin/local_hub/ui.py missing"]
    text = ui_path.read_text(encoding="utf-8", errors="ignore")
    for section in _REQUIRED_UI_SECTIONS:
        if section not in text:
            errors.append(f"REQUIRED_IDS missing section: {section}")
    return errors


def _check_system_map(root: Path) -> list[str]:
    errors = []
    sm = root / "SYSTEM_MAP.json"
    if not sm.exists():
        return ["SYSTEM_MAP.json missing"]
    text = sm.read_text(encoding="utf-8", errors="ignore")
    if "final_pr_11_provider_critic_thor" not in text:
        errors.append("SYSTEM_MAP.json missing final_pr_11_provider_critic_thor entry")
    return errors


def _check_file_manifest(root: Path) -> list[str]:
    errors = []
    fm = root / "FILE_MANIFEST.json"
    if not fm.exists():
        return ["FILE_MANIFEST.json missing"]
    text = fm.read_text(encoding="utf-8", errors="ignore")
    all_required = (
        _REQUIRED_MODULE_FILES
        + _REQUIRED_DOCS
        + _REQUIRED_EXAMPLES
        + _REQUIRED_REPORTS
        + _REQUIRED_REGISTRIES
        + _REQUIRED_SCHEMAS
        + ["tests/test_final_pr_11_provider_critic_thor.py",
           "tools/rebaseline/check_final_pr_11_provider_critic_thor.py"]
    )
    for rel in all_required:
        if rel not in text:
            errors.append(f"FILE_MANIFEST.json missing entry for {rel}")
    return errors


def _check_release_sequence_transition(root: Path) -> list[str]:
    errors = []
    report = root / "reports/final_pr_11_release_sequence_transition_report.json"
    if not report.exists():
        return ["release sequence transition report missing"]
    obj, err = _load_json(report)
    if err:
        return [f"invalid JSON in release sequence transition report: {err}"]
    if obj.get("recommended_next_pr") != "FINAL-PR-12":
        errors.append("release sequence transition: recommended_next_pr must be FINAL-PR-12")
    if not obj.get("final_pr_12_remains_deferred"):
        errors.append("release sequence transition: final_pr_12_remains_deferred must be true")
    return errors


def _check_preflight_after_pr11(root: Path) -> list[str]:
    errors = []
    report = root / "reports/final_pr_11_preflight_after_pr11_report.json"
    if not report.exists():
        return ["preflight after PR11 report missing"]
    obj, err = _load_json(report)
    if err:
        return [f"invalid JSON in preflight after PR11 report: {err}"]
    if obj.get("recommended_next_pr") != "FINAL-PR-12":
        errors.append("preflight after PR11: recommended_next_pr must be FINAL-PR-12")
    if not obj.get("final_pr_12_remains_deferred"):
        errors.append("preflight after PR11: final_pr_12_remains_deferred must be true")
    return errors


def _check_proof_packet(root: Path) -> list[str]:
    errors = []
    p = root / "reports/final_pr_11_provider_critic_thor_proof_packet.json"
    if not p.exists():
        return ["proof packet missing"]
    obj, err = _load_json(p)
    if err:
        return [f"invalid JSON in proof packet: {err}"]
    if not obj.get("candidate_only"):
        errors.append("proof packet: candidate_only must be true")
    if not obj.get("app_owned_apply"):
        errors.append("proof packet: app_owned_apply must be true")
    if obj.get("claim_boundary") != CLAIM_BOUNDARY:
        errors.append(f"proof packet: claim_boundary mismatch")
    required_proven = [
        "local_provider_receipt_harness_exists",
        "provider_execution_disabled_by_default",
        "critic_runtime_binding_exists",
        "thor_handoff_compiler_v0_exists",
        "release_closure_moved_to_final_pr_12",
        "final_pr_12_remains_deferred",
    ]
    proven = obj.get("proven", [])
    for item in required_proven:
        if item not in proven:
            errors.append(f"proof packet: missing proven item: {item}")
    required_not_proven = ["production_readiness", "security_certification", "release_certification"]
    not_proven = obj.get("not_proven", [])
    for item in required_not_proven:
        if item not in not_proven:
            errors.append(f"proof packet: missing not_proven item: {item}")
    return errors


def _check_evidence_class_in_receipts(root: Path) -> list[str]:
    errors = []
    for rel in _REQUIRED_EXAMPLES:
        p = root / rel
        if not p.exists():
            continue
        obj, err = _load_json(p)
        if err or obj is None:
            continue
        if isinstance(obj, dict) and "artifact_kind" in obj:
            if "receipt" in obj.get("artifact_kind", "") or "packet" in obj.get("artifact_kind", ""):
                if "evidence_class" not in obj:
                    errors.append(f"{rel}: missing evidence_class field")
    return errors


def _functional_check_provider_receipts() -> list[str]:
    errors = []
    try:
        from odin.local_provider_receipts.readiness import build_provider_readiness_receipt
        r = build_provider_readiness_receipt("ollama_candidate")
        if r.get("candidate_only") is not True:
            errors.append("readiness receipt: candidate_only must be True")
        if r.get("execution_performed") is not False:
            errors.append("readiness receipt: execution_performed must be False")
        if r.get("evidence_class") != "structural_evidence":
            errors.append("readiness receipt: evidence_class must be structural_evidence")
    except Exception as exc:
        errors.append(f"provider readiness receipt import/call failed: {exc}")

    try:
        from odin.local_provider_receipts.receipt import run_local_provider_receipt
        r = run_local_provider_receipt("ollama_candidate", "test", allow_local_provider_execution=False)
        if r.get("execution_performed") is not False:
            errors.append("default receipt: execution_performed must be False")
        if r.get("model_inference") is not False:
            errors.append("default receipt: model_inference must be False")
    except Exception as exc:
        errors.append(f"run_local_provider_receipt failed: {exc}")
    return errors


def _functional_check_critic(root: Path) -> list[str]:
    errors = []
    try:
        from odin.critic_runtime.deterministic_critic import run_deterministic_critic
        candidate = {"candidate_only": True, "claim_boundary": "test", "not_proven": ["x"]}
        r = run_deterministic_critic(candidate)
        if r.get("not_authority") is not True:
            errors.append("critic: not_authority must be True")
        if r.get("final_gate_required") is not True:
            errors.append("critic: final_gate_required must be True")
        if r.get("evidence_class") != "structural_evidence":
            errors.append("critic: evidence_class must be structural_evidence")
        # Test critic detects app_apply=True
        bad = {"candidate_only": True, "claim_boundary": "test", "not_proven": ["x"], "app_apply": True}
        r2 = run_deterministic_critic(bad)
        if not r2.get("errors"):
            errors.append("critic: should detect app_apply=True as error")
    except Exception as exc:
        errors.append(f"critic functional check failed: {exc}")
    return errors


def _functional_check_route_eval() -> list[str]:
    errors = []
    try:
        from odin.route_evaluation.receipt import run_route_evaluation_receipt
        r = run_route_evaluation_receipt()
        if r.get("not_a_model_quality_benchmark") is not True:
            errors.append("route eval: not_a_model_quality_benchmark must be True")
        if r.get("no_superiority_claim") is not True:
            errors.append("route eval: no_superiority_claim must be True")
        if r.get("routes_evaluated", 0) < 4:
            errors.append(f"route eval: must evaluate at least 4 routes, got {r.get('routes_evaluated')}")
    except Exception as exc:
        errors.append(f"route evaluation functional check failed: {exc}")
    return errors


def _functional_check_thor_compiler() -> list[str]:
    errors = []
    try:
        from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
        from odin.thor_handoff_compiler.compiler import compile_thor_handoff_bundle
        ic = build_handoff_input_contract(
            objective="test",
            repo_evidence=["file.py"],
            allowed_edits=["odin/"],
            forbidden_edits=[],
            acceptance_gates=["validate OK"],
            claim_boundary="test_boundary",
        )
        bundle = compile_thor_handoff_bundle(ic)
        if bundle.get("thor_runtime_execution") is not False:
            errors.append("thor compiler: thor_runtime_execution must be False")
        if bundle.get("agent_autonomy") is not False:
            errors.append("thor compiler: agent_autonomy must be False")
        for key in ["agent_operator_work_packet", "acceptance_matrix", "validator_plan", "pr_body_skeleton"]:
            if key not in bundle:
                errors.append(f"thor compiler bundle missing: {key}")
    except Exception as exc:
        errors.append(f"thor compiler functional check failed: {exc}")
    return errors


def run_checks(root: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    checked_files: list[str] = []

    # File existence checks
    for rel in _REQUIRED_MODULE_FILES:
        checked_files.append(rel)
    for rel in _REQUIRED_DOCS:
        checked_files.append(rel)

    errors.extend(_check_required_files(root, _REQUIRED_MODULE_FILES, "module"))
    errors.extend(_check_required_files(root, _REQUIRED_DOCS, "doc"))
    errors.extend(_check_required_files(root, _REQUIRED_EXAMPLES, "example"))
    errors.extend(_check_required_files(root, _REQUIRED_REPORTS, "report"))
    errors.extend(_check_required_files(root, _REQUIRED_REGISTRIES, "registry"))
    errors.extend(_check_required_files(root, _REQUIRED_SCHEMAS, "schema"))
    errors.extend(_check_required_files(root, ["tests/test_final_pr_11_provider_critic_thor.py"], "test"))
    errors.extend(_check_required_files(root, ["tools/rebaseline/check_final_pr_11_provider_critic_thor.py"], "validator"))

    # JSON validity
    errors.extend(_check_json_files(root, _REQUIRED_EXAMPLES))
    errors.extend(_check_json_files(root, _REQUIRED_REPORTS))
    errors.extend(_check_json_files(root, _REQUIRED_REGISTRIES))
    errors.extend(_check_json_files(root, _REQUIRED_SCHEMAS))

    # Code safety
    errors.extend(_check_no_eval_exec(root))
    errors.extend(_check_no_public_network_in_modules(root))
    errors.extend(_check_executor_no_shell_true(root))
    errors.extend(_check_provider_execution_disabled_by_default(root))

    # CLI integration
    errors.extend(_check_cli_commands(root))

    # Local Hub integration
    errors.extend(_check_local_hub_endpoints(root))
    errors.extend(_check_ui_sections(root))

    # Metadata
    errors.extend(_check_system_map(root))
    errors.extend(_check_file_manifest(root))

    # Release sequence
    errors.extend(_check_release_sequence_transition(root))
    errors.extend(_check_preflight_after_pr11(root))

    # Proof packet
    errors.extend(_check_proof_packet(root))

    # Evidence class presence
    errors.extend(_check_evidence_class_in_receipts(root))

    # Functional checks (require module imports)
    try:
        errors.extend(_functional_check_provider_receipts())
        errors.extend(_functional_check_critic(root))
        errors.extend(_functional_check_route_eval())
        errors.extend(_functional_check_thor_compiler())
    except Exception as exc:
        errors.append(f"functional check block failed: {exc}")

    status = "ok" if not errors else "error"
    return {
        "status": status,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "checked_files": checked_files,
        "errors": errors,
        "warnings": warnings,
        "generated_at_utc": "2026-01-01T00:00:00Z",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_final_pr_11_provider_critic_thor",
        description="Validate FINAL-PR-11 Local Provider Receipt Harness + Critic Runtime Binding + Thor Handoff Compiler v0",
    )
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    parser.add_argument("--out", required=True, help="Output report JSON path")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve()
    report = run_checks(root)
    report["generated_at_utc"] = args.generated_at_utc

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    if report["errors"]:
        for err in report["errors"]:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
