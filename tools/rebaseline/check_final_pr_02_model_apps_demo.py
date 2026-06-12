"""Validator: FINAL-PR-02 Model Picker + Connected Apps + Demo Universal Work.

Claim boundary: final_pr_02_validator_candidate_only_no_provider_no_app_apply

Run:
  python tools/rebaseline/check_final_pr_02_model_apps_demo.py \\
    --repo-root . \\
    --out reports/final_pr_02_model_apps_demo_report.json \\
    --generated-at-utc 2026-01-01T00:00:00Z
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
        "odin/local_hub/proof_pr02.py",
        "odin/local_hub/policy.py",
        "odin/local_hub/model_picker.py",
        "odin/local_hub/connected_apps.py",
        "odin/local_hub/demo_universal_work.py",
        "tools/rebaseline/check_final_pr_02_model_apps_demo.py",
        "tests/test_final_pr_02_model_apps_demo.py",
        "docs/rebaseline/FINAL_PR_02_MODEL_APPS_DEMO.md",
        "docs/codex/audits/FINAL_PR_02_MODEL_APPS_DEMO_AUDIT.md",
        "docs/codex/reports/FINAL_PR_02_MODEL_APPS_DEMO_RETURN_REPORT.md",
        "reports/final_pr_02_model_apps_demo_report.json",
        "schemas/final_pr_02_demo_universal_work_response_packet.schema.json",
        "registries/final_pr_02_model_apps_demo_registry.json",
        "examples/final_pr_02/demo_universal_work_response_packet.example.json",
        "docs/codex/handoffs/FINAL_PR_02_REPO_COGNITION_SUMMARY.md",
        "docs/codex/handoffs/FINAL_PR_02_HUB_SURFACE_DECISION.md",
        "docs/codex/handoffs/FINAL_PR_02_THOR_Y_HANDOFF_REQUEST.md",
        "docs/codex/handoffs/FINAL_PR_02_COMPILED_THOR_Y_HANDOFF.md",
        "docs/codex/handoffs/FINAL_PR_02_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
        "docs/codex/audits/FINAL_PR_02_THOR_EFFECTIVENESS_AUDIT.md",
        "docs/codex/audits/FINAL_PR_02_ODIN_EFFECTIVENESS_AUDIT.md",
        "reports/final_pr_02_thor_effectiveness_audit.json",
        "reports/final_pr_02_odin_effectiveness_audit.json",
    ]
    for rel in required_files:
        if not (repo / rel).exists():
            errors.append(f"missing required file: {rel}")

    # --- Required CLI commands in odin/cli.py ---
    cli_path = repo / "odin" / "cli.py"
    if cli_path.exists():
        cli_text = cli_path.read_text(encoding="utf-8", errors="ignore")
        for cmd in [
            "validate-final-pr-02-model-apps-demo",
            "prove-final-pr-02-demo-universal-work",
        ]:
            if f'"{cmd}"' not in cli_text and f"'{cmd}'" not in cli_text:
                errors.append(f"CLI command missing from cli.py: {cmd}")
        if "validate_final_pr_02_model_apps_demo" not in cli_text:
            errors.append("validate_final_pr_02_model_apps_demo not referenced in cli.py")
        if "validate_final_pr_02_model_apps_demo" not in cli_text or \
                "validate_all" not in cli_text:
            pass  # Already checked above
        # validate-final-pr-02 must be called in validate_all
        if "validate_final_pr_02_model_apps_demo()" not in cli_text:
            errors.append("validate_final_pr_02_model_apps_demo() not called in validate_all()")
    else:
        errors.append("odin/cli.py not found")

    # --- UI markers in ui.py ---
    ui_path = repo / "odin" / "local_hub" / "ui.py"
    if ui_path.exists():
        ui_text = ui_path.read_text(encoding="utf-8", errors="ignore")
        # FINAL-PR-01 IDs (must still be present)
        pr01_ids = [
            "hub-title", "runtime-status", "local-api-status", "model-status",
            "connected-apps-status", "activity-status", "warnings-proof-gaps",
            "qirc-status", "handoff-first-status", "dev-mode-entry", "normal-user-help",
        ]
        for id_ in pr01_ids:
            if f'id="{id_}"' not in ui_text:
                errors.append(f"UI missing FINAL-PR-01 stable id: {id_}")
        # FINAL-PR-02 IDs
        pr02_ids = [
            "model-picker-section",
            "model-option-none",
            "model-option-mock",
            "model-option-local-candidate",
            "provider-status-panel",
            "connected-apps-section",
            "connected-app-slot-generic",
            "connected-app-slot-browser",
            "connected-app-slot-file",
            "app-bridge-status",
            "demo-universal-work-section",
            "demo-work-input",
            "demo-submit-placeholder",
            "demo-response-packet",
            "demo-candidate-artifact",
            "demo-handoff-context",
            "demo-universal-work-packet",
            "demo-proof-gap-status",
        ]
        for id_ in pr02_ids:
            if f'id="{id_}"' not in ui_text:
                errors.append(f"UI missing FINAL-PR-02 stable id: {id_}")
        # Normal-user copy (FINAL-PR-02 additions)
        required_copy = [
            "Choose how Odin should prepare work.",
            "No model inference runs in this PR.",
            "Mock mode returns deterministic demo candidates.",
            "Local candidate provider is listed but not executed yet.",
            "Connected apps are demo slots only.",
            "Odin can accept a demo Universal Work request and return a candidate response packet.",
            "Apps still decide what to apply.",
        ]
        for copy in required_copy:
            if copy not in ui_text:
                errors.append(f"UI missing required FINAL-PR-02 copy: {copy!r}")
        # Dev Mode copy
        if "No provider execution" not in ui_text and "No provider execution." not in ui_text:
            errors.append("UI Dev Mode missing 'No provider execution'")
        if "No model inference" not in ui_text:
            errors.append("UI Dev Mode missing 'No model inference'")
        if "No app apply" not in ui_text:
            errors.append("UI Dev Mode missing 'No app apply'")
        if "No external send" not in ui_text:
            errors.append("UI Dev Mode missing 'No external send'")
    else:
        errors.append("odin/local_hub/ui.py not found")

    # --- No model/provider execution in server.py ---
    server_path = repo / "odin" / "local_hub" / "server.py"
    if server_path.exists():
        server_text = server_path.read_text(encoding="utf-8", errors="ignore")
        forbidden_in_server = [
            "import openai", "import anthropic", "import ollama",
            "requests.post", "requests.get",
            "subprocess.run", "subprocess.Popen",
            "os.environ.get(\"OPENAI", "os.environ.get(\"ANTHROPIC",
        ]
        for marker in forbidden_in_server:
            if marker in server_text:
                errors.append(f"server.py contains forbidden marker: {marker!r}")
    else:
        errors.append("odin/local_hub/server.py not found")

    # --- Demo response schema checks ---
    example_path = repo / "examples" / "final_pr_02" / "demo_universal_work_response_packet.example.json"
    if example_path.exists():
        try:
            example = json.loads(example_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"demo example JSON invalid: {exc}")
            example = {}
        if example.get("candidate_only") is not True:
            errors.append("demo example: candidate_only must be true")
        if example.get("model_execution") is not False and example.get("model_inference") is not False:
            errors.append("demo example: model_execution/model_inference must be false")
        if example.get("provider_execution") is not False:
            errors.append("demo example: provider_execution must be false")
        if example.get("app_apply") is not False:
            errors.append("demo example: app_apply must be false")
        if example.get("external_send") is not False:
            errors.append("demo example: external_send must be false")
        if not example.get("not_proven"):
            errors.append("demo example: not_proven list required")
        if not example.get("claim_boundary"):
            errors.append("demo example: claim_boundary required")
        if not example.get("handoff_context"):
            errors.append("demo example: handoff_context required")
        if not example.get("universal_work"):
            errors.append("demo example: universal_work required")
        if not example.get("candidate_artifact"):
            errors.append("demo example: candidate_artifact required")
        if not example.get("response_packet"):
            errors.append("demo example: response_packet required")
    else:
        errors.append("demo example missing: examples/final_pr_02/demo_universal_work_response_packet.example.json")

    # --- Registry check ---
    registry_path = repo / "registries" / "final_pr_02_model_apps_demo_registry.json"
    if registry_path.exists():
        try:
            reg = json.loads(registry_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"registry JSON invalid: {exc}")
            reg = {}
        if "registry_id" not in reg:
            errors.append("registry missing registry_id")
        if "version" not in reg:
            errors.append("registry missing version")
    else:
        errors.append("registry missing: registries/final_pr_02_model_apps_demo_registry.json")

    # --- Proof packet module checks ---
    proof_path = repo / "odin" / "local_hub" / "proof_pr02.py"
    if proof_path.exists():
        proof_text = proof_path.read_text(encoding="utf-8", errors="ignore")
        for field in [
            "model_picker_visible", "connected_apps_visible", "demo_universal_work_visible",
            "response_packet_visible", "candidate_artifact_visible", "handoff_context_visible",
            "universal_work_packet_visible", "provider_execution", "model_inference",
            "app_apply", "external_send", "qirc_core_runtime", "candidate_only",
        ]:
            if field not in proof_text:
                errors.append(f"proof_pr02.py missing field: {field}")
    else:
        errors.append("odin/local_hub/proof_pr02.py missing")

    # --- Fail-closed checks ---
    demo_module_path = repo / "odin" / "local_hub" / "demo_universal_work.py"
    if demo_module_path.exists():
        demo_text = demo_module_path.read_text(encoding="utf-8", errors="ignore")
        # Must not claim model execution
        for bad in ["inference_result", "model_output =", "provider.run("]:
            if bad in demo_text:
                errors.append(f"demo_universal_work.py contains provider/model execution marker: {bad!r}")
        # Must claim candidate_only
        if '"candidate_only": True' not in demo_text and "'candidate_only': True" not in demo_text:
            errors.append("demo_universal_work.py must include candidate_only: True in response")
    else:
        errors.append("odin/local_hub/demo_universal_work.py missing")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FINAL-PR-02 Model Picker / Apps / Demo validator")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--out", required=True, help="Output JSON report path")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    errors, warnings = _check(repo)

    report = {
        "report_id": "odin.final_pr_02_model_apps_demo_check",
        "status": "ok" if not errors else "fail",
        "generated_at_utc": args.generated_at_utc,
        "repo_root": str(repo),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "candidate_only": True,
        "claim_boundary": "final_pr_02_validator_candidate_only_no_provider_no_app_apply",
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
