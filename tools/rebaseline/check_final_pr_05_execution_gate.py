"""FINAL-PR-05 Execution Gate Validator.

Claim boundary: final_pr_05_validator_candidate_only_no_provider_no_app_apply
candidate_only: true
local_only: true
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CLAIM_BOUNDARY = "final_pr_05_validator_candidate_only_no_provider_no_app_apply"

REQUIRED_EXECUTION_GATE_FILES = [
    "odin/execution_gate/__init__.py",
    "odin/execution_gate/policy.py",
    "odin/execution_gate/gateway.py",
    "odin/execution_gate/mock_provider.py",
    "odin/execution_gate/local_candidate_policy.py",
    "odin/execution_gate/proof.py",
]

REQUIRED_PROOF_CHAIN_FILES = [
    "odin/proof_chain/__init__.py",
    "odin/proof_chain/registry.py",
    "odin/proof_chain/builder.py",
]

REQUIRED_LADDER_FILES = [
    "odin/final_pr_ladder/__init__.py",
    "odin/final_pr_ladder/compiler.py",
    "odin/final_pr_ladder/templates.py",
    "odin/final_pr_ladder/proof.py",
]

REQUIRED_SCHEMA_FILES = [
    "schemas/final_pr_05_execution_gate_proof_packet.schema.json",
    "schemas/final_pr_ladder_worker_packet_scaffold.schema.json",
]

REQUIRED_REGISTRY_FILES = [
    "registries/final_pr_05_execution_gate_registry.json",
]

REQUIRED_EXAMPLE_FILES = [
    "examples/final_pr_05/execution_gate_proof_packet.example.json",
    "examples/final_pr_05/final_pr_ladder_worker_packet_scaffold.example.json",
]

REQUIRED_UI_IDS = [
    "execution-gate-status",
    "mock-execution-panel",
    "mock-execution-result",
    "local-candidate-policy-status",
    "execution-boundary-status",
    "proof-chain-status",
    "final-pr-ladder-scaffold-status",
    "model-execution-warning",
]

REQUIRED_ENDPOINTS = [
    "/execution-gate/status.json",
    "/execution-gate/mock",
    "/execution-gate/proof-chain.json",
    "/final-pr-ladder/scaffold.json",
]

REQUIRED_COPY_FRAGMENTS = [
    "Mock execution is local and deterministic.",
    "Mock execution is not model inference.",
    "No real model is executed by default.",
    "Local candidate execution is disabled by default.",
    "Remote providers and API keys are not used.",
    "Proof chain links receipts but does not prove production readiness.",
    "FINAL-PR Ladder scaffold is not a full Thor replacement.",
]

REQUIRED_AUDIT_FILES = [
    "docs/codex/audits/FINAL_PR_05_EXECUTION_GATE_AUDIT.md",
    "docs/codex/audits/FINAL_PR_05_THOR_EFFECTIVENESS_AUDIT.md",
    "docs/codex/audits/FINAL_PR_05_ODIN_EFFECTIVENESS_AUDIT.md",
]

REQUIRED_HANDOFF_FILES = [
    "docs/codex/handoffs/FINAL_PR_05_REPO_COGNITION_SUMMARY.md",
    "docs/codex/handoffs/FINAL_PR_05_THOR_Y_HANDOFF_REQUEST.md",
    "docs/codex/handoffs/FINAL_PR_05_COMPILED_THOR_Y_HANDOFF.md",
    "docs/codex/handoffs/FINAL_PR_05_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
    "docs/codex/handoffs/FINAL_PR_05_HANDOFF_QUALITY_GATE.md",
]

REQUIRED_REPORT_DOC_FILES = [
    "docs/codex/reports/FINAL_PR_05_EXECUTION_GATE_RETURN_REPORT.md",
    "docs/rebaseline/FINAL_PR_05_EXECUTION_GATE_LADDER.md",
]

# Forbidden markers — scanned in execution gate source only
FORBIDDEN_MARKERS = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "ollama generate",
    "ollama run",
    "ollama chat",
    "ollama embed",
    "llama-cli -m",
    "requests.post(",
    "requests.get(",
    "httpx.",
]

# Forbidden boolean flags that should never be True in production code
FORBIDDEN_POLICY_FLAGS = [
    "remote_execution_allowed=True",
    "api_key_reads_allowed=True",
    "external_network_allowed=True",
    "app_apply_allowed=True",
    "external_send_allowed=True",
]

# Scanned dirs for forbidden markers
SCAN_DIRS = ["odin/execution_gate"]

# Exception files (contain marker strings as documentation)
SCAN_EXCEPTION_FILES = {
    "tools/rebaseline/check_final_pr_05_execution_gate.py",
}


def _check_files_exist(root: Path, file_list: list[str]) -> list[str]:
    errors = []
    for rel in file_list:
        if not (root / rel).exists():
            errors.append(f"missing file: {rel}")
    return errors


def _check_mock_execution_determinism(root: Path) -> list[str]:
    errors = []
    try:
        sys.path.insert(0, str(root))
        from odin.execution_gate.mock_provider import MockProvider
        mp = MockProvider()
        r1 = mp.execute(input_text="test-determinism-check")
        r2 = mp.execute(input_text="test-determinism-check")
        if r1.get("candidate_text") != r2.get("candidate_text"):
            errors.append("mock execution is not deterministic: same input produced different output")
        if r1.get("mock_execution") is not True:
            errors.append("mock execution response missing mock_execution: true")
        if r1.get("model_inference") is not False:
            errors.append("mock execution response must have model_inference: false")
        if r1.get("real_provider_execution") is not False:
            errors.append("mock execution response must have real_provider_execution: false")
        if r1.get("candidate_only") is not True:
            errors.append("mock execution response must have candidate_only: true")
        if r1.get("local_only") is not True:
            errors.append("mock execution response must have local_only: true")
        if r1.get("app_apply") is not False:
            errors.append("mock execution response must have app_apply: false")
    except Exception as exc:
        errors.append(f"mock execution determinism check failed: {exc}")
    return errors


def _check_gateway_policy(root: Path) -> list[str]:
    errors = []
    try:
        sys.path.insert(0, str(root))
        from odin.execution_gate.gateway import ExecutionGateway
        from odin.execution_gate.policy import DEFAULT_EXECUTION_GATE_POLICY as p
        if p.local_candidate_execution_allowed:
            errors.append("policy: local_candidate_execution_allowed must be False by default")
        if p.remote_execution_allowed:
            errors.append("policy: remote_execution_allowed must be False")
        if p.api_key_reads_allowed:
            errors.append("policy: api_key_reads_allowed must be False")
        if p.external_network_allowed:
            errors.append("policy: external_network_allowed must be False")
        if p.app_apply_allowed:
            errors.append("policy: app_apply_allowed must be False")
        if p.external_send_allowed:
            errors.append("policy: external_send_allowed must be False")
        if not p.mock_execution_allowed:
            errors.append("policy: mock_execution_allowed must be True")
        if not p.candidate_only:
            errors.append("policy: candidate_only must be True")
        # Test gateway blocks local candidate
        gw = ExecutionGateway()
        for pid in ("ollama_candidate", "llama_cpp_candidate"):
            result = gw.execute(input_text="test", provider_id=pid)
            if result.get("gate_decision") != "blocked":
                errors.append(f"gateway: {pid} must be blocked by default")
            if result.get("model_inference") is not False:
                errors.append(f"gateway: {pid} blocked response must have model_inference: false")
        # Test gateway blocks remote
        result = gw.execute(input_text="test", provider_id="openai")
        if result.get("gate_decision") != "blocked":
            errors.append("gateway: unknown/remote provider must be blocked")
    except Exception as exc:
        errors.append(f"gateway policy check failed: {exc}")
    return errors


def _check_proof_chain(root: Path) -> list[str]:
    errors = []
    try:
        sys.path.insert(0, str(root))
        from odin.proof_chain.builder import build_proof_chain
        from odin.proof_chain.registry import PROOF_CHAIN_REGISTRY
        chain = build_proof_chain()
        for pr_key in ("final_pr_01", "final_pr_02", "final_pr_03", "final_pr_04", "final_pr_05"):
            if pr_key not in PROOF_CHAIN_REGISTRY:
                errors.append(f"proof_chain: missing entry for {pr_key}")
        if chain.get("candidate_only") is not True:
            errors.append("proof_chain: candidate_only must be True")
        if not chain.get("not_proven"):
            errors.append("proof_chain: must have not_proven list")
        for required in ("production_readiness", "live_model_inference"):
            if required not in chain.get("not_proven", []):
                errors.append(f"proof_chain: not_proven must include {required}")
    except Exception as exc:
        errors.append(f"proof chain check failed: {exc}")
    return errors


def _check_ladder_scaffold(root: Path) -> list[str]:
    errors = []
    try:
        sys.path.insert(0, str(root))
        from odin.final_pr_ladder.compiler import compile_worker_packet_scaffold
        scaffold = compile_worker_packet_scaffold(target_pr_id="FINAL-PR-06")
        if scaffold.get("candidate_only") is not True:
            errors.append("ladder: scaffold must have candidate_only: true")
        if scaffold.get("claim_boundary") != "final_pr_ladder_scaffold_not_full_prompt_compiler":
            errors.append("ladder: wrong claim_boundary in scaffold")
        required_sections = [
            "repo_cognition", "handoff_request", "compiled_handoff",
            "work_packet", "acceptance_gates", "proof_commands", "return_report_contract"
        ]
        for s in required_sections:
            if s not in scaffold.get("sections", []):
                errors.append(f"ladder: scaffold missing section: {s}")
        if "thor_runtime_replacement" not in scaffold.get("not_proven", []):
            errors.append("ladder: scaffold must list thor_runtime_replacement as not_proven")
    except Exception as exc:
        errors.append(f"ladder scaffold check failed: {exc}")
    return errors


def _check_qirc_events(root: Path) -> list[str]:
    errors = []
    try:
        sys.path.insert(0, str(root))
        from odin.qirc_core.bus import clear_bus, list_events
        from odin.execution_gate.gateway import execute_candidate
        clear_bus()
        execute_candidate(input_text="qirc-smoke-test", provider_id="mock")
        events = list_events("#odin.model")
        if len(events) == 0:
            errors.append("QIRC: no #odin.model events emitted during mock execution")
        kinds = {e.get("kind") for e in events}
        for expected in ("execution_gate_checked", "mock_execution_allowed", "mock_execution_completed"):
            if expected not in kinds:
                errors.append(f"QIRC: missing expected event kind: {expected}")
    except Exception as exc:
        errors.append(f"QIRC events check failed: {exc}")
    return errors


def _scan_forbidden_markers(root: Path) -> list[str]:
    errors = []
    for scan_dir in SCAN_DIRS:
        d = root / scan_dir
        if not d.exists():
            continue
        for py_file in sorted(d.rglob("*.py")):
            rel = str(py_file.relative_to(root))
            if rel in SCAN_EXCEPTION_FILES:
                continue
            try:
                content = py_file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for line_no, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                for marker in FORBIDDEN_MARKERS:
                    if marker in line:
                        errors.append(f"forbidden marker in {rel}:{line_no}: {marker}")
                for flag in FORBIDDEN_POLICY_FLAGS:
                    if flag in line:
                        errors.append(f"forbidden policy flag in {rel}:{line_no}: {flag}")
    return errors


def _check_ui_ids(root: Path) -> list[str]:
    errors = []
    try:
        sys.path.insert(0, str(root))
        from odin.local_hub.ui import REQUIRED_IDS, REQUIRED_COPY
        for uid in REQUIRED_UI_IDS:
            if uid not in REQUIRED_IDS:
                errors.append(f"UI: missing required ID: {uid}")
        for copy_fragment in REQUIRED_COPY_FRAGMENTS:
            if copy_fragment not in REQUIRED_COPY:
                errors.append(f"UI: missing required copy: {copy_fragment!r}")
    except Exception as exc:
        errors.append(f"UI ID check failed: {exc}")
    return errors


def _check_endpoints(root: Path) -> list[str]:
    errors = []
    try:
        server_path = root / "odin" / "local_hub" / "server.py"
        content = server_path.read_text(encoding="utf-8", errors="replace")
        for endpoint in REQUIRED_ENDPOINTS:
            if endpoint not in content:
                errors.append(f"server: missing endpoint: {endpoint}")
    except Exception as exc:
        errors.append(f"endpoint check failed: {exc}")
    return errors


def _check_example_schema(root: Path) -> list[str]:
    errors = []
    # Check example files have required fields
    example_path = root / "examples/final_pr_05/execution_gate_proof_packet.example.json"
    if example_path.exists():
        try:
            data = json.loads(example_path.read_text(encoding="utf-8"))
            if data.get("candidate_only") is not True:
                errors.append("example: execution_gate_proof_packet must have candidate_only: true")
            if data.get("claim_boundary") != "final_pr_05_execution_gate_mock_only_not_model_quality_not_production":
                errors.append("example: wrong claim_boundary in proof packet example")
        except Exception as exc:
            errors.append(f"example JSON parse failed: {exc}")
    ladder_example = root / "examples/final_pr_05/final_pr_ladder_worker_packet_scaffold.example.json"
    if ladder_example.exists():
        try:
            data = json.loads(ladder_example.read_text(encoding="utf-8"))
            if data.get("candidate_only") is not True:
                errors.append("example: ladder scaffold must have candidate_only: true")
            if data.get("claim_boundary") != "final_pr_ladder_scaffold_not_full_prompt_compiler":
                errors.append("example: wrong claim_boundary in ladder scaffold example")
        except Exception as exc:
            errors.append(f"ladder example JSON parse failed: {exc}")
    return errors


def _check_runtime_security_extension(root: Path) -> list[str]:
    errors = []
    try:
        smoke_path = root / "odin" / "runtime_security" / "smoke.py"
        content = smoke_path.read_text(encoding="utf-8", errors="replace")
        if "odin/execution_gate" not in content:
            errors.append("runtime_security/smoke.py: missing odin/execution_gate in SCAN_DIRS")
        if "_check_execution_gate_policy_boundaries" not in content:
            errors.append("runtime_security/smoke.py: missing _check_execution_gate_policy_boundaries function")
    except Exception as exc:
        errors.append(f"runtime security extension check failed: {exc}")
    return errors


def run_checks(root: Path) -> tuple[list[str], list[str]]:
    errors = []
    warnings = []

    # File existence checks
    errors.extend(_check_files_exist(root, REQUIRED_EXECUTION_GATE_FILES))
    errors.extend(_check_files_exist(root, REQUIRED_PROOF_CHAIN_FILES))
    errors.extend(_check_files_exist(root, REQUIRED_LADDER_FILES))
    errors.extend(_check_files_exist(root, REQUIRED_SCHEMA_FILES))
    errors.extend(_check_files_exist(root, REQUIRED_REGISTRY_FILES))
    errors.extend(_check_files_exist(root, REQUIRED_EXAMPLE_FILES))
    errors.extend(_check_files_exist(root, REQUIRED_AUDIT_FILES))
    errors.extend(_check_files_exist(root, REQUIRED_HANDOFF_FILES))
    errors.extend(_check_files_exist(root, REQUIRED_REPORT_DOC_FILES))

    # Functional checks
    errors.extend(_check_mock_execution_determinism(root))
    errors.extend(_check_gateway_policy(root))
    errors.extend(_check_proof_chain(root))
    errors.extend(_check_ladder_scaffold(root))
    errors.extend(_check_qirc_events(root))
    errors.extend(_scan_forbidden_markers(root))
    errors.extend(_check_ui_ids(root))
    errors.extend(_check_endpoints(root))
    errors.extend(_check_example_schema(root))
    errors.extend(_check_runtime_security_extension(root))

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FINAL-PR-05 Execution Gate Validator")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve()
    errors, warnings = run_checks(root)

    report = {
        "report_id": "odin.final_pr_05_execution_gate_check",
        "status": "ok" if not errors else "fail",
        "generated_at_utc": args.generated_at_utc,
        "repo_root": str(root),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
