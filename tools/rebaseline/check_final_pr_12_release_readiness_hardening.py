#!/usr/bin/env python3
"""FINAL-PR-12 Release Readiness Hardening Validator.

Claim boundary: final_pr_12_release_readiness_hardening_not_release_closure
candidate_only: true
stdlib only
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

CLAIM_BOUNDARY = "final_pr_12_release_readiness_hardening_not_release_closure"

REQUIRED_MODULE_FILES = [
    "odin/release_readiness_hardening/__init__.py",
    "odin/release_readiness_hardening/readiness_matrix.py",
    "odin/release_readiness_hardening/risk_register.py",
    "odin/release_readiness_hardening/hardening_plan.py",
    "odin/release_readiness_hardening/reports.py",
    "odin/evidence_closure_dry_run/__init__.py",
    "odin/evidence_closure_dry_run/evidence_plan.py",
    "odin/evidence_closure_dry_run/dry_run.py",
    "odin/evidence_closure_dry_run/receipt_classifier.py",
    "odin/evidence_closure_dry_run/reports.py",
    "odin/packaging_boundary_prep/__init__.py",
    "odin/packaging_boundary_prep/inventory.py",
    "odin/packaging_boundary_prep/boundary.py",
    "odin/packaging_boundary_prep/manifest_plan.py",
    "odin/packaging_boundary_prep/reports.py",
    "odin/command_surface_closure/__init__.py",
    "odin/command_surface_closure/command_index.py",
    "odin/command_surface_closure/alias_policy.py",
    "odin/command_surface_closure/coverage.py",
    "odin/command_surface_closure/reports.py",
    "odin/docs_readiness/__init__.py",
    "odin/docs_readiness/doc_index.py",
    "odin/docs_readiness/start_here_plan.py",
    "odin/docs_readiness/readme_plan.py",
    "odin/docs_readiness/reports.py",
    "odin/final_pr_13_input_bundle/__init__.py",
    "odin/final_pr_13_input_bundle/bundle.py",
    "odin/final_pr_13_input_bundle/prompt_inputs.py",
    "odin/final_pr_13_input_bundle/reports.py",
]

REQUIRED_DOCS = [
    "docs/rebaseline/FINAL_PR_12_RELEASE_READINESS_HARDENING.md",
    "docs/release/FINAL_PR_12_RELEASE_READINESS_MATRIX.md",
    "docs/release/FINAL_PR_12_EVIDENCE_CLOSURE_DRY_RUN.md",
    "docs/release/FINAL_PR_12_PACKAGING_BOUNDARY_PREP.md",
    "docs/release/FINAL_PR_12_COMMAND_SURFACE_CLOSURE.md",
    "docs/release/FINAL_PR_12_DOCS_READINESS.md",
    "docs/release/FINAL_PR_12_FINAL_PR_13_INPUT_BUNDLE.md",
    "docs/release/FINAL_PR_12_RELEASE_SEQUENCE_AFTER_PR12.md",
    "docs/codex/handoffs/FINAL_PR_12_REPO_COGNITION_SUMMARY.md",
    "docs/codex/handoffs/FINAL_PR_12_THOR_STYLE_RELEASE_READINESS_HANDOFF.md",
    "docs/codex/handoffs/FINAL_PR_12_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
    "docs/codex/audits/FINAL_PR_12_RELEASE_READINESS_AUDIT.md",
    "docs/codex/audits/FINAL_PR_12_SENIOR_REVIEW.md",
    "docs/codex/audits/FINAL_PR_12_CODE_REVIEW.md",
    "docs/codex/audits/FINAL_PR_12_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md",
    "docs/codex/reports/FINAL_PR_12_RELEASE_READINESS_RETURN_REPORT.md",
]

REQUIRED_EXAMPLES = [
    "examples/final_pr_12/release_readiness_matrix.example.json",
    "examples/final_pr_12/evidence_closure_dry_run.example.json",
    "examples/final_pr_12/packaging_boundary_inventory.example.json",
    "examples/final_pr_12/command_surface_index.example.json",
    "examples/final_pr_12/docs_readiness_index.example.json",
    "examples/final_pr_12/final_pr_13_input_bundle.example.json",
    "examples/final_pr_12/release_sequence_after_pr12.example.json",
]

REQUIRED_REPORTS = [
    "reports/final_pr_12_release_readiness_matrix.json",
    "reports/final_pr_12_release_risk_register.json",
    "reports/final_pr_12_evidence_closure_dry_run.json",
    "reports/final_pr_12_packaging_boundary_inventory.json",
    "reports/final_pr_12_command_surface_index.json",
    "reports/final_pr_12_docs_readiness_index.json",
    "reports/final_pr_12_final_pr_13_input_bundle.json",
    "reports/final_pr_12_release_sequence_after_pr12.json",
    "reports/final_pr_12_release_readiness_proof_packet.json",
]

REQUIRED_REGISTRIES = [
    "registries/final_pr_12_release_readiness_registry.json",
    "registries/final_pr_12_evidence_closure_dry_run_registry.json",
    "registries/final_pr_12_packaging_boundary_registry.json",
    "registries/final_pr_12_command_surface_registry.json",
    "registries/final_pr_12_docs_readiness_registry.json",
    "registries/final_pr_12_final_pr_13_input_bundle_registry.json",
]

REQUIRED_SCHEMAS = [
    "schemas/final_pr_12_release_readiness_matrix.schema.json",
    "schemas/final_pr_12_evidence_closure_dry_run.schema.json",
    "schemas/final_pr_12_packaging_boundary.schema.json",
    "schemas/final_pr_12_final_pr_13_input_bundle.schema.json",
]

REQUIRED_CLI_COMMANDS = [
    "validate-release-readiness-hardening",
    "build-release-readiness-matrix",
    "build-release-risk-register",
    "explain-release-readiness-hardening",
    "validate-evidence-closure-dry-run",
    "run-evidence-closure-dry-run",
    "explain-evidence-closure-dry-run",
    "validate-packaging-boundary-prep",
    "build-packaging-boundary",
    "explain-packaging-boundary",
    "validate-command-surface-closure",
    "build-command-surface-index",
    "explain-command-surface",
    "validate-docs-readiness",
    "build-docs-readiness-index",
    "explain-docs-readiness",
    "validate-final-pr-13-input-bundle",
    "build-final-pr-13-input-bundle",
    "explain-final-pr-13-input-bundle",
    "validate-final-pr-12-release-readiness-hardening",
]

REQUIRED_HUB_ENDPOINTS = [
    "/release-readiness/status.json",
    "/release-readiness/matrix.json",
    "/release-readiness/risk-register.json",
    "/evidence-closure/dry-run.json",
    "/packaging-boundary/inventory.json",
    "/command-surface/index.json",
    "/docs-readiness/index.json",
    "/final-pr-13/input-bundle.json",
    "/release/sequence-after-pr12.json",
]

REQUIRED_UI_IDS = [
    "release-readiness-hardening-section",
    "evidence-closure-dry-run-section",
    "packaging-boundary-prep-section",
    "command-surface-closure-section",
    "docs-readiness-section",
    "final-pr-13-input-bundle-section",
]

FORBIDDEN_TERMS = [
    "production_readiness_certified",
    "security_certified",
    "release_certified",
    "model_superiority_proven",
    "real_model_benchmark_proven",
]


def check_file_exists(root: Path, path: str) -> str | None:
    if not (root / path).exists():
        return f"missing file: {path}"
    return None


def check_json_parseable(root: Path, path: str) -> str | None:
    p = root / path
    if not p.exists():
        return f"missing JSON file: {path}"
    try:
        json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"JSON parse error in {path}: {exc}"
    return None


def check_candidate_only_in_json(root: Path, path: str) -> str | None:
    p = root / path
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not data.get("candidate_only"):
        return f"candidate_only not true in {path}"
    return None


def check_no_forbidden_code(root: Path, path: str) -> list[str]:
    p = root / path
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8")
    errors = []
    if "eval(" in text and "# allow" not in text:
        errors.append(f"eval() found in {path}")
    if "exec(" in text and "# allow" not in text:
        errors.append(f"exec() found in {path}")
    if "subprocess" in text:
        errors.append(f"subprocess found in {path}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check_final_pr_12_release_readiness_hardening")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", required=True)
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z")
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []

    # Check required module files
    for path in REQUIRED_MODULE_FILES:
        checked.append(path)
        err = check_file_exists(root, path)
        if err:
            errors.append(err)
        else:
            errs = check_no_forbidden_code(root, path)
            errors.extend(errs)

    # Check required docs
    for path in REQUIRED_DOCS:
        checked.append(path)
        err = check_file_exists(root, path)
        if err:
            errors.append(err)

    # Check examples parse as JSON and have candidate_only
    for path in REQUIRED_EXAMPLES:
        checked.append(path)
        err = check_json_parseable(root, path)
        if err:
            errors.append(err)
        else:
            err2 = check_candidate_only_in_json(root, path)
            if err2:
                errors.append(err2)

    # Check reports parse as JSON
    for path in REQUIRED_REPORTS:
        checked.append(path)
        err = check_json_parseable(root, path)
        if err:
            errors.append(err)

    # Check registries
    for path in REQUIRED_REGISTRIES:
        checked.append(path)
        err = check_json_parseable(root, path)
        if err:
            errors.append(err)

    # Check schemas
    for path in REQUIRED_SCHEMAS:
        checked.append(path)
        err = check_json_parseable(root, path)
        if err:
            errors.append(err)

    # Check proof packet
    proof_path = root / "reports/final_pr_12_release_readiness_proof_packet.json"
    if proof_path.exists():
        try:
            pp = json.loads(proof_path.read_text(encoding="utf-8"))
            if not pp.get("candidate_only"):
                errors.append("proof packet missing candidate_only: true")
            not_proven = pp.get("not_proven", [])
            for required_np in ["production_readiness", "security_certification", "release_certification", "final_pr_13_release_closure"]:
                if required_np not in not_proven:
                    errors.append(f"proof packet missing {required_np} in not_proven")
        except Exception as exc:
            errors.append(f"proof packet parse error: {exc}")

    # Check CLI commands registered in cli.py
    cli_path = root / "odin/cli.py"
    if cli_path.exists():
        cli_text = cli_path.read_text(encoding="utf-8")
        for cmd in REQUIRED_CLI_COMMANDS:
            if f'"{cmd}"' not in cli_text and f"'{cmd}'" not in cli_text:
                errors.append(f"CLI command not registered: {cmd}")
        if "validate_final_pr_12_release_readiness_hardening" not in cli_text:
            errors.append("validate_final_pr_12_release_readiness_hardening not in cli.py")
        if "validate_all" in cli_text and "validate_final_pr_12_release_readiness_hardening" in cli_text:
            # Check it's called in validate_all
            import re
            va_match = re.search(r"def validate_all\(\)(.*?)^def ", cli_text, re.DOTALL | re.MULTILINE)
            if va_match:
                va_body = va_match.group(1)
                if "validate_final_pr_12_release_readiness_hardening" not in va_body:
                    errors.append("validate_final_pr_12_release_readiness_hardening not called in validate_all()")

    # Check local hub server has endpoints
    server_path = root / "odin/local_hub/server.py"
    if server_path.exists():
        server_text = server_path.read_text(encoding="utf-8")
        for ep in REQUIRED_HUB_ENDPOINTS:
            if ep not in server_text:
                errors.append(f"local hub endpoint not registered: {ep}")

    # Check UI REQUIRED_IDS
    ui_path = root / "odin/local_hub/ui.py"
    if ui_path.exists():
        ui_text = ui_path.read_text(encoding="utf-8")
        for uid in REQUIRED_UI_IDS:
            if uid not in ui_text:
                errors.append(f"REQUIRED_IDS missing: {uid}")

    # Check release sequence points to FINAL-PR-13
    seq_path = root / "reports/final_pr_12_release_sequence_after_pr12.json"
    if seq_path.exists():
        try:
            seq = json.loads(seq_path.read_text(encoding="utf-8"))
            if seq.get("next_pr") != "FINAL-PR-13":
                errors.append("release sequence after PR12 does not point to FINAL-PR-13")
            if not seq.get("final_pr_13_remains_deferred"):
                errors.append("release sequence missing final_pr_13_remains_deferred: true")
        except Exception as exc:
            errors.append(f"release sequence parse error: {exc}")

    # Check evidence closure dry run does not close release
    ecd_path = root / "reports/final_pr_12_evidence_closure_dry_run.json"
    if ecd_path.exists():
        try:
            ecd = json.loads(ecd_path.read_text(encoding="utf-8"))
            if not ecd.get("dry_run_is_not_release_closure"):
                errors.append("evidence closure dry run missing dry_run_is_not_release_closure: true")
            if not ecd.get("final_pr_13_remains_deferred"):
                errors.append("evidence closure dry run missing final_pr_13_remains_deferred: true")
        except Exception as exc:
            errors.append(f"evidence closure parse error: {exc}")

    # Check packaging inventory does not claim signed distribution
    pkg_path = root / "reports/final_pr_12_packaging_boundary_inventory.json"
    if pkg_path.exists():
        try:
            pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
            not_proven = pkg.get("not_proven", [])
            for claim in ["signed_distribution", "installer_proof", "distribution_proof"]:
                if claim not in not_proven:
                    errors.append(f"packaging inventory missing {claim} in not_proven")
        except Exception as exc:
            errors.append(f"packaging inventory parse error: {exc}")

    # Check SYSTEM_MAP
    sysmap_path = root / "SYSTEM_MAP.json"
    if sysmap_path.exists():
        try:
            sysmap = json.loads(sysmap_path.read_text(encoding="utf-8"))
            if "final_pr_12_release_readiness_hardening" not in sysmap:
                errors.append("SYSTEM_MAP missing final_pr_12_release_readiness_hardening")
        except Exception as exc:
            errors.append(f"SYSTEM_MAP parse error: {exc}")

    # Check FILE_MANIFEST contains PR12 files
    manifest_path = root / "FILE_MANIFEST.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            files_in_manifest = {f["path"] for f in manifest.get("files", [])}
            for path in REQUIRED_MODULE_FILES[:5]:  # spot-check first 5
                if path not in files_in_manifest:
                    errors.append(f"FILE_MANIFEST missing: {path}")
        except Exception as exc:
            errors.append(f"FILE_MANIFEST parse error: {exc}")

    report = {
        "status": "ok" if not errors else "fail",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": args.generated_at_utc,
        "checked_files": checked,
        "errors": errors,
        "warnings": warnings,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("check_final_pr_12_release_readiness_hardening: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
