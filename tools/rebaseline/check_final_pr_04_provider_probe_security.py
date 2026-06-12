"""FINAL-PR-04 validator: Provider Probe + Provider Policy + Runtime Security Smoke.

Claim boundary: final_pr_04_validator_candidate_only_no_provider_no_app_apply
candidate_only: true
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLAIM_BOUNDARY = "final_pr_04_validator_candidate_only_no_provider_no_app_apply"
REQUIRED_PROVIDER_IDS = ["none", "mock", "ollama_candidate", "llama_cpp_candidate"]
REQUIRED_UI_IDS = [
    "provider-policy-status",
    "provider-probe-panel",
    "provider-probe-results",
    "provider-execution-boundary",
    "runtime-security-smoke-status",
    "secret-scan-status",
    "network-boundary-status",
    "qirc-provider-events-status",
]
REQUIRED_COPY_FRAGMENTS = [
    "Provider probe checks readiness only.",
    "No model is executed.",
    "No API keys are read.",
    "No external network is used.",
    "Provider execution remains disabled by default.",
]
REQUIRED_ENDPOINTS = [
    "/providers.json",
    "/providers/probe.json",
    "/security/runtime-smoke.json",
]
REQUIRED_POST_ENDPOINTS = [
    "/providers/probe",
]
FORBIDDEN_MARKERS = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "ollama run",
    "ollama generate",
    "ollama chat",
    "allow_public_network=True",
    "allow_federation=True",
]


def check_provider_policy(root: Path, errors: list[str], warnings: list[str]) -> None:
    policy_path = root / "odin" / "providers" / "policy.py"
    if not policy_path.exists():
        errors.append("missing odin/providers/policy.py")
        return
    try:
        from odin.providers.policy import PROVIDER_POLICIES
        for pid in REQUIRED_PROVIDER_IDS:
            if pid not in PROVIDER_POLICIES:
                errors.append(f"provider policy missing provider_id: {pid}")
                continue
            p = PROVIDER_POLICIES[pid]
            if getattr(p, "execution_allowed", True):
                errors.append(f"provider {pid}: execution_allowed must be False")
            if not getattr(p, "candidate_only", False):
                errors.append(f"provider {pid}: candidate_only must be True")
            if pid in ("ollama_candidate", "llama_cpp_candidate"):
                if getattr(p, "remote", True):
                    errors.append(f"provider {pid}: remote must be False")
                if getattr(p, "requires_api_key", True):
                    errors.append(f"provider {pid}: requires_api_key must be False")
    except Exception as exc:
        errors.append(f"error loading provider policy: {exc}")


def check_provider_registry(root: Path, errors: list[str], warnings: list[str]) -> None:
    reg_path = root / "odin" / "providers" / "registry.py"
    if not reg_path.exists():
        errors.append("missing odin/providers/registry.py")
        return
    try:
        from odin.providers.registry import PROVIDER_REGISTRY
        for pid in REQUIRED_PROVIDER_IDS:
            if pid not in PROVIDER_REGISTRY:
                errors.append(f"registry missing provider_id: {pid}")
            else:
                entry = PROVIDER_REGISTRY[pid]
                if entry.get("execution_allowed", True):
                    errors.append(f"registry {pid}: execution_allowed must be False")
    except Exception as exc:
        errors.append(f"error loading provider registry: {exc}")


def check_provider_probe(root: Path, errors: list[str], warnings: list[str]) -> None:
    probe_path = root / "odin" / "providers" / "probe.py"
    if not probe_path.exists():
        errors.append("missing odin/providers/probe.py")
        return
    content = probe_path.read_text(encoding="utf-8")
    for fn in ["list_provider_candidates", "probe_provider", "probe_all_providers", "build_provider_status_packet"]:
        if f"def {fn}" not in content:
            errors.append(f"odin/providers/probe.py missing function: {fn}")
    # Check forbidden patterns absent
    for marker in ["ollama run", "ollama generate", "ollama chat", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]:
        if marker in content:
            errors.append(f"odin/providers/probe.py contains forbidden marker: {marker}")

    # Actually run the probe and verify shape
    try:
        from odin.providers.probe import probe_all_providers
        results = probe_all_providers()
        for r in results:
            if r.get("execution_allowed", True):
                errors.append(f"probe result for {r.get('provider_id')}: execution_allowed must be False")
            if not r.get("candidate_only", False):
                errors.append(f"probe result for {r.get('provider_id')}: candidate_only must be True")
            if not r.get("local_only", False):
                errors.append(f"probe result for {r.get('provider_id')}: local_only must be True")
            if r.get("model_inference", True):
                errors.append(f"probe result for {r.get('provider_id')}: model_inference must be False")
            if r.get("provider_execution", True):
                errors.append(f"probe result for {r.get('provider_id')}: provider_execution must be False")
            if r.get("requires_api_key", True):
                errors.append(f"probe result for {r.get('provider_id')}: requires_api_key must be False or absent")
        # Verify missing binary results in not_found not error
        ollama_result = next((r for r in results if r["provider_id"] == "ollama_candidate"), None)
        if ollama_result and ollama_result.get("status") not in ("available", "not_found", "disabled", "blocked"):
            errors.append(f"ollama_candidate probe status unexpected: {ollama_result.get('status')}")
    except Exception as exc:
        errors.append(f"error running probe_all_providers: {exc}")


def check_runtime_security_smoke(root: Path, errors: list[str], warnings: list[str]) -> None:
    smoke_path = root / "odin" / "runtime_security" / "smoke.py"
    if not smoke_path.exists():
        errors.append("missing odin/runtime_security/smoke.py")
        return
    try:
        import sys
        if "odin.runtime_security.smoke" not in sys.modules:
            import importlib
            importlib.import_module("odin.runtime_security.smoke")
        from odin.runtime_security.smoke import run_runtime_security_smoke, scan_content
        result = run_runtime_security_smoke(root)
        d = result.as_dict()
        if d.get("provider_execution_default", True):
            errors.append("runtime smoke: provider_execution_default must be False")
        if d.get("model_inference_default", True):
            errors.append("runtime smoke: model_inference_default must be False")
        # Verify synthetic detection works
        synthetic = "OPENAI_API_KEY"
        findings = scan_content(synthetic, "synthetic_test")
        if not findings:
            errors.append("runtime smoke: scan_content failed to detect OPENAI_API_KEY in synthetic input")
    except Exception as exc:
        errors.append(f"error running runtime security smoke: {exc}")


def check_qirc_model_channel(root: Path, errors: list[str], warnings: list[str]) -> None:
    channels_path = root / "odin" / "qirc_core" / "channels.py"
    if not channels_path.exists():
        errors.append("missing odin/qirc_core/channels.py")
        return
    content = channels_path.read_text(encoding="utf-8")
    if "#odin.model" not in content:
        errors.append("qirc_core/channels.py missing #odin.model channel")


def check_hub_endpoints(root: Path, errors: list[str], warnings: list[str]) -> None:
    server_path = root / "odin" / "local_hub" / "server.py"
    if not server_path.exists():
        errors.append("missing odin/local_hub/server.py")
        return
    content = server_path.read_text(encoding="utf-8")
    for ep in REQUIRED_ENDPOINTS:
        if ep not in content:
            errors.append(f"server.py missing endpoint: GET {ep}")
    for ep in REQUIRED_POST_ENDPOINTS:
        if ep not in content:
            errors.append(f"server.py missing endpoint: POST {ep}")


def check_ui_ids(root: Path, errors: list[str], warnings: list[str]) -> None:
    ui_path = root / "odin" / "local_hub" / "ui.py"
    if not ui_path.exists():
        errors.append("missing odin/local_hub/ui.py")
        return
    content = ui_path.read_text(encoding="utf-8")
    for uid in REQUIRED_UI_IDS:
        if uid not in content:
            errors.append(f"ui.py missing required ID: {uid}")
    for copy_frag in REQUIRED_COPY_FRAGMENTS:
        if copy_frag not in content:
            errors.append(f"ui.py missing required copy: {copy_frag!r}")


def check_proof_packet(root: Path, errors: list[str], warnings: list[str]) -> None:
    proof_path = root / "odin" / "providers" / "proof.py"
    if not proof_path.exists():
        errors.append("missing odin/providers/proof.py")
        return
    try:
        from odin.providers.proof import build_proof_packet
        packet = build_proof_packet()
        if packet.get("provider_execution", True):
            errors.append("proof packet: provider_execution must be False")
        if packet.get("model_inference", True):
            errors.append("proof packet: model_inference must be False")
        if packet.get("api_key_reads", True):
            errors.append("proof packet: api_key_reads must be False")
        if packet.get("external_network", True):
            errors.append("proof packet: external_network must be False")
        if not packet.get("candidate_only", False):
            errors.append("proof packet: candidate_only must be True")
        not_proven = packet.get("not_proven", [])
        for expected in ["production_readiness", "security_certification", "actual_model_inference"]:
            if expected not in not_proven:
                errors.append(f"proof packet: missing not_proven entry: {expected}")
    except Exception as exc:
        errors.append(f"error building proof packet: {exc}")


def check_report_persisted(root: Path, errors: list[str], warnings: list[str]) -> None:
    proof_report = root / "reports" / "final_pr_04_provider_probe_security_proof_packet.json"
    if not proof_report.exists():
        warnings.append("proof packet report not yet persisted (run prove-final-pr-04-provider-probe-security)")


def check_schema_and_examples(root: Path, errors: list[str], warnings: list[str]) -> None:
    schema_path = root / "schemas" / "final_pr_04_provider_probe_security_proof_packet.schema.json"
    if not schema_path.exists():
        errors.append("missing schemas/final_pr_04_provider_probe_security_proof_packet.schema.json")
    example_path = root / "examples" / "final_pr_04" / "provider_probe_security_proof_packet.example.json"
    if not example_path.exists():
        errors.append("missing examples/final_pr_04/provider_probe_security_proof_packet.example.json")
    registry_path = root / "registries" / "final_pr_04_provider_probe_security_registry.json"
    if not registry_path.exists():
        errors.append("missing registries/final_pr_04_provider_probe_security_registry.json")


def check_handoff_and_audit_docs(root: Path, errors: list[str], warnings: list[str]) -> None:
    required_docs = [
        "docs/codex/handoffs/FINAL_PR_04_REPO_COGNITION_SUMMARY.md",
        "docs/codex/handoffs/FINAL_PR_04_THOR_Y_HANDOFF_REQUEST.md",
        "docs/codex/handoffs/FINAL_PR_04_COMPILED_THOR_Y_HANDOFF.md",
        "docs/codex/handoffs/FINAL_PR_04_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
        "docs/codex/handoffs/FINAL_PR_04_HANDOFF_QUALITY_GATE.md",
        "docs/codex/audits/FINAL_PR_04_PROVIDER_PROBE_SECURITY_AUDIT.md",
        "docs/codex/audits/FINAL_PR_04_THOR_EFFECTIVENESS_AUDIT.md",
        "docs/codex/audits/FINAL_PR_04_ODIN_EFFECTIVENESS_AUDIT.md",
        "docs/codex/reports/FINAL_PR_04_PROVIDER_PROBE_SECURITY_RETURN_REPORT.md",
        "docs/rebaseline/FINAL_PR_04_PROVIDER_PROBE_SECURITY.md",
    ]
    for d in required_docs:
        if not (root / d).exists():
            errors.append(f"missing doc: {d}")


_FORBIDDEN_SCAN_EXCEPTIONS = {
    "odin/runtime_security/smoke.py",  # defines markers as string constants, not actual usage
}


def check_forbidden_api_key_reads(root: Path, errors: list[str], warnings: list[str]) -> None:
    provider_dir = root / "odin" / "providers"
    security_dir = root / "odin" / "runtime_security"
    for d in [provider_dir, security_dir]:
        if not d.exists():
            continue
        for py_file in d.rglob("*.py"):
            rel = str(py_file.relative_to(root))
            if rel in _FORBIDDEN_SCAN_EXCEPTIONS:
                continue
            content = py_file.read_text(encoding="utf-8", errors="replace")
            for marker in FORBIDDEN_MARKERS:
                if marker in content:
                    errors.append(f"forbidden marker '{marker}' in {rel}")


def check_cli_commands(root: Path, errors: list[str], warnings: list[str]) -> None:
    cli_path = root / "odin" / "cli.py"
    if not cli_path.exists():
        errors.append("missing odin/cli.py")
        return
    content = cli_path.read_text(encoding="utf-8")
    for cmd in [
        "validate-final-pr-04-provider-probe-security",
        "prove-final-pr-04-provider-probe-security",
        "provider-status",
        "provider-probe",
        "runtime-security-smoke",
    ]:
        if cmd not in content:
            errors.append(f"cli.py missing command: {cmd}")
    if "validate_final_pr_04_provider_probe_security" not in content:
        errors.append("cli.py missing validate_final_pr_04_provider_probe_security in validate_all")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FINAL-PR-04 validator")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    check_provider_policy(root, errors, warnings)
    check_provider_registry(root, errors, warnings)
    check_provider_probe(root, errors, warnings)
    check_runtime_security_smoke(root, errors, warnings)
    check_qirc_model_channel(root, errors, warnings)
    check_hub_endpoints(root, errors, warnings)
    check_ui_ids(root, errors, warnings)
    check_proof_packet(root, errors, warnings)
    check_report_persisted(root, errors, warnings)
    check_schema_and_examples(root, errors, warnings)
    check_handoff_and_audit_docs(root, errors, warnings)
    check_forbidden_api_key_reads(root, errors, warnings)
    check_cli_commands(root, errors, warnings)

    report = {
        "report_id": "odin.final_pr_04_provider_probe_security_check",
        "status": "ok" if not errors else "errors",
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
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
