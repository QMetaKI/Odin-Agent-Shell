"""Validator: FINAL-PR-01 Simple Local Hub.

Claim boundary: simple_local_hub_validator_candidate_only_no_app_apply_no_external_send

Run: python tools/rebaseline/check_simple_local_hub.py --repo-root . --out <path> --generated-at-utc <iso>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _check(repo: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # --- Required implementation files ---
    required_files = [
        "odin/local_hub/__init__.py",
        "odin/local_hub/server.py",
        "odin/local_hub/ui.py",
        "odin/local_hub/proof.py",
        "odin/local_hub/policy.py",
        "tools/rebaseline/check_simple_local_hub.py",
        "tests/test_simple_local_hub.py",
        "docs/rebaseline/FINAL_PR_01_SIMPLE_LOCAL_HUB.md",
        "docs/codex/audits/FINAL_PR_01_SIMPLE_LOCAL_HUB_AUDIT.md",
        "docs/codex/reports/FINAL_PR_01_SIMPLE_LOCAL_HUB_RETURN_REPORT.md",
        "reports/final_pr_01_simple_local_hub_report.json",
        "schemas/final_pr_01_simple_local_hub_proof_packet.schema.json",
        "registries/final_pr_01_simple_local_hub_registry.json",
        "examples/final_pr_01/simple_local_hub_proof_packet.example.json",
        "docs/codex/handoffs/FINAL_PR_01_REPO_COGNITION_SUMMARY.md",
        "docs/codex/handoffs/FINAL_PR_01_THOR_Y_HANDOFF_REQUEST.md",
        "docs/codex/handoffs/FINAL_PR_01_COMPILED_THOR_Y_HANDOFF.md",
        "docs/codex/handoffs/FINAL_PR_01_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
        "docs/codex/handoffs/FINAL_PR_01_Y_MJOLNIR_PROFILE_NOTES.md",
        "docs/codex/audits/FINAL_PR_01_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md",
        "reports/final_pr_01_thor_odin_y_effectiveness_audit.json",
    ]
    for rel in required_files:
        if not (repo / rel).exists():
            errors.append(f"missing required file: {rel}")

    # --- Required CLI commands in odin/cli.py ---
    cli_path = repo / "odin" / "cli.py"
    if cli_path.exists():
        cli_text = cli_path.read_text(encoding="utf-8", errors="ignore")
        for cmd in ["start-local-hub", "status-local-hub", "open-hub",
                    "validate-simple-local-hub", "prove-simple-local-hub"]:
            if f'"{cmd}"' not in cli_text and f"'{cmd}'" not in cli_text:
                errors.append(f"CLI command missing from cli.py: {cmd}")
        # validate-simple-local-hub must be in validate_all
        if "validate_simple_local_hub" not in cli_text:
            errors.append("validate_simple_local_hub not referenced in cli.py")
    else:
        errors.append("odin/cli.py not found")

    # --- UI markers in ui.py ---
    ui_path = repo / "odin" / "local_hub" / "ui.py"
    if ui_path.exists():
        ui_text = ui_path.read_text(encoding="utf-8", errors="ignore")
        required_ids = [
            "hub-title", "runtime-status", "local-api-status", "model-status",
            "connected-apps-status", "activity-status", "warnings-proof-gaps",
            "qirc-status", "handoff-first-status", "dev-mode-entry", "normal-user-help",
        ]
        for id_ in required_ids:
            if f'id="{id_}"' not in ui_text:
                errors.append(f"UI missing stable id: {id_}")
        # Normal-user copy
        required_copy = [
            "Odin is running locally.",
            "Odin returns candidates; apps decide what to apply.",
            "No model is active yet.",
            "No apps are connected yet.",
            "QIRC core is planned for a later final slice.",
            "Handoff-First prepares work before Universal Work.",
            "Dev Mode contains traces, receipts, proof gaps, validators, and handoff details.",
        ]
        for copy in required_copy:
            if copy not in ui_text:
                errors.append(f"UI missing required copy: {copy!r}")
        # QIRC placeholder must be non-authoritative
        if "non-authoritative" not in ui_text:
            errors.append("UI QIRC placeholder missing 'non-authoritative' marker")
        # Dev Mode handoff viewer placeholder
        if "handoff-viewer" not in ui_text and "handoff viewer" not in ui_text.lower():
            errors.append("UI Dev Mode missing handoff viewer placeholder")
    else:
        errors.append("odin/local_hub/ui.py not found")

    # --- Localhost policy ---
    policy_path = repo / "odin" / "local_hub" / "policy.py"
    if policy_path.exists():
        policy_text = policy_path.read_text(encoding="utf-8", errors="ignore")
        if "127.0.0.1" not in policy_text:
            errors.append("policy.py missing 127.0.0.1 in ALLOWED_HOSTS")
        if "0.0.0.0" not in policy_text:
            errors.append("policy.py missing 0.0.0.0 in BLOCKED_HOSTS")
        if "check_host" not in policy_text:
            errors.append("policy.py missing check_host function")
    else:
        errors.append("odin/local_hub/policy.py not found")

    # --- Runtime policy check via import ---
    try:
        sys.path.insert(0, str(repo))
        from odin.local_hub.policy import check_host
        ok, _ = check_host("127.0.0.1")
        if not ok:
            errors.append("policy: check_host rejects 127.0.0.1 — should accept")
        ok, _ = check_host("0.0.0.0")
        if ok:
            errors.append("policy: check_host accepts 0.0.0.0 — should reject")
        ok, _ = check_host("evil.example.com")
        if ok:
            errors.append("policy: check_host accepts public host — should reject")
    except Exception as exc:
        errors.append(f"policy import check failed: {exc}")

    # --- Proof schema and example ---
    schema_path = repo / "schemas" / "final_pr_01_simple_local_hub_proof_packet.schema.json"
    if schema_path.exists():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            if schema.get("title") != "OdinSimpleLocalHubProofPacket":
                warnings.append("proof schema title mismatch")
        except Exception as exc:
            errors.append(f"proof schema invalid JSON: {exc}")
    else:
        errors.append("proof schema missing: schemas/final_pr_01_simple_local_hub_proof_packet.schema.json")

    example_path = repo / "examples" / "final_pr_01" / "simple_local_hub_proof_packet.example.json"
    if example_path.exists():
        try:
            ex = json.loads(example_path.read_text(encoding="utf-8"))
            if not ex.get("candidate_only"):
                errors.append("example proof packet missing candidate_only: true")
            if "claim_boundary" not in ex:
                errors.append("example proof packet missing claim_boundary")
        except Exception as exc:
            errors.append(f"example proof packet invalid JSON: {exc}")
    else:
        errors.append("example proof packet missing: examples/final_pr_01/simple_local_hub_proof_packet.example.json")

    # --- Proof packet report ---
    report_path = repo / "reports" / "final_pr_01_simple_local_hub_report.json"
    if report_path.exists():
        try:
            rpt = json.loads(report_path.read_text(encoding="utf-8"))
            if not rpt.get("candidate_only"):
                errors.append("final_pr_01 report missing candidate_only: true")
        except Exception as exc:
            errors.append(f"final_pr_01 report invalid JSON: {exc}")

    # --- Overclaim guard: new docs must not claim provider/model/runtime proof ---
    guarded_docs = [
        "docs/rebaseline/FINAL_PR_01_SIMPLE_LOCAL_HUB.md",
        "docs/codex/audits/FINAL_PR_01_SIMPLE_LOCAL_HUB_AUDIT.md",
        "docs/codex/reports/FINAL_PR_01_SIMPLE_LOCAL_HUB_RETURN_REPORT.md",
        "docs/codex/handoffs/FINAL_PR_01_COMPILED_THOR_Y_HANDOFF.md",
        "docs/codex/handoffs/FINAL_PR_01_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
    ]
    overclaim_phrases = [
        "production_ready", "model_inference_verified", "runtime_verified",
        "host_validated", "security_verified", "deploy_verified",
    ]
    for rel in guarded_docs:
        p = repo / rel
        if p.exists():
            text = p.read_text(encoding="utf-8", errors="ignore")
            for phrase in overclaim_phrases:
                if phrase in text:
                    errors.append(f"{rel}: overclaim phrase found: {phrase!r}")

    # --- SYSTEM_MAP and FILE_MANIFEST include new files ---
    system_map = repo / "SYSTEM_MAP.json"
    if system_map.exists():
        sm_text = system_map.read_text(encoding="utf-8", errors="ignore")
        if "simple_local_hub" not in sm_text and "local_hub" not in sm_text:
            warnings.append("SYSTEM_MAP.json may not reference simple_local_hub")

    file_manifest = repo / "FILE_MANIFEST.json"
    if file_manifest.exists():
        fm_text = file_manifest.read_text(encoding="utf-8", errors="ignore")
        if "local_hub" not in fm_text:
            warnings.append("FILE_MANIFEST.json may not reference odin/local_hub/")

    return errors, warnings


def build_report(repo_root: Path, generated_at_utc: str) -> dict:
    errors, warnings = _check(repo_root)
    return {
        "report_id": "odin.final_pr_01_simple_local_hub_check",
        "generated_at_utc": generated_at_utc,
        "repo_root": str(repo_root),
        "status": "ok" if not errors else "failed",
        "errors": errors,
        "warnings": warnings,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "candidate_only": True,
        "claim_boundary": "simple_local_hub_validator_candidate_only_no_app_apply_no_external_send",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check_simple_local_hub")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default=None)
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    report = build_report(repo, args.generated_at_utc)
    output = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")

    print(output)
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
