"""FINAL-PR-13 v1.0 Release Closure Validator.

Claim boundary: final_pr_13_v1_candidate_release_closure_not_external_release
candidate_only: true
stdlib only — no external dependencies.

Usage:
  python tools/rebaseline/check_final_pr_13_v1_release_closure.py \\
    --repo-root . \\
    --out reports/final_pr_13_v1_release_closure_report.json \\
    --generated-at-utc 2026-01-01T00:00:00Z
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CLAIM_BOUNDARY = "final_pr_13_v1_candidate_release_closure_not_external_release"

_REQUIRED_MODULE_FILES = [
    "odin/v1_release_closure/__init__.py",
    "odin/v1_release_closure/closure_matrix.py",
    "odin/v1_release_closure/release_truth.py",
    "odin/v1_release_closure/proof_packet.py",
    "odin/v1_release_closure/reports.py",
    "odin/root_public_surface/__init__.py",
    "odin/root_public_surface/root_inventory.py",
    "odin/root_public_surface/root_hygiene.py",
    "odin/root_public_surface/root_index.py",
    "odin/root_public_surface/reports.py",
    "odin/readme_v1/__init__.py",
    "odin/readme_v1/readme_plan.py",
    "odin/readme_v1/thanks_block_source.py",
    "odin/readme_v1/reports.py",
    "odin/donation_surface/__init__.py",
    "odin/donation_surface/donations_plan.py",
    "odin/donation_surface/reports.py",
    "odin/release_artifact_boundary/__init__.py",
    "odin/release_artifact_boundary/artifact_boundary.py",
    "odin/release_artifact_boundary/manual_release_actions.py",
    "odin/release_artifact_boundary/reports.py",
]

_REQUIRED_EXAMPLES = [
    "examples/final_pr_13/v1_release_closure_matrix.example.json",
    "examples/final_pr_13/v1_release_truth.example.json",
    "examples/final_pr_13/root_inventory.example.json",
    "examples/final_pr_13/root_hygiene_report.example.json",
    "examples/final_pr_13/readme_v1_plan.example.json",
    "examples/final_pr_13/donations_plan.example.json",
    "examples/final_pr_13/release_artifact_boundary.example.json",
    "examples/final_pr_13/release_sequence_after_pr13.example.json",
]

_REQUIRED_REPORTS = [
    "reports/final_pr_13_v1_release_closure_matrix.json",
    "reports/final_pr_13_v1_release_truth.json",
    "reports/final_pr_13_root_inventory.json",
    "reports/final_pr_13_root_hygiene_report.json",
    "reports/final_pr_13_readme_v1_report.json",
    "reports/final_pr_13_donation_surface_report.json",
    "reports/final_pr_13_release_artifact_boundary.json",
    "reports/final_pr_13_release_sequence_after_pr13.json",
    "reports/final_pr_13_v1_release_closure_proof_packet.json",
]

_REQUIRED_REGISTRIES = [
    "registries/final_pr_13_v1_release_closure_registry.json",
    "registries/final_pr_13_root_public_surface_registry.json",
    "registries/final_pr_13_readme_v1_registry.json",
    "registries/final_pr_13_donation_surface_registry.json",
    "registries/final_pr_13_release_artifact_boundary_registry.json",
]

_REQUIRED_SCHEMAS = [
    "schemas/final_pr_13_v1_release_closure.schema.json",
    "schemas/final_pr_13_root_public_surface.schema.json",
    "schemas/final_pr_13_readme_v1.schema.json",
    "schemas/final_pr_13_release_artifact_boundary.schema.json",
]

_REQUIRED_DOCS = [
    "docs/rebaseline/FINAL_PR_13_V1_RELEASE_CLOSURE.md",
    "docs/release/FINAL_PR_13_V1_RELEASE_TRUTH.md",
    "docs/release/FINAL_PR_13_ROOT_PUBLIC_SURFACE.md",
    "docs/release/FINAL_PR_13_README_V1.md",
    "docs/release/FINAL_PR_13_DONATION_SURFACE.md",
    "docs/release/FINAL_PR_13_RELEASE_ARTIFACT_BOUNDARY.md",
    "docs/release/FINAL_PR_13_RELEASE_SEQUENCE_AFTER_PR13.md",
    "docs/codex/handoffs/FINAL_PR_13_REPO_COGNITION_SUMMARY.md",
    "docs/codex/handoffs/FINAL_PR_13_THOR_STYLE_RELEASE_CLOSURE_HANDOFF.md",
    "docs/codex/handoffs/FINAL_PR_13_ODIN_AGENT_OPERATOR_WORK_PACKET.md",
    "docs/codex/audits/FINAL_PR_13_RELEASE_CLOSURE_AUDIT.md",
    "docs/codex/audits/FINAL_PR_13_SENIOR_REVIEW.md",
    "docs/codex/audits/FINAL_PR_13_CODE_REVIEW.md",
    "docs/codex/audits/FINAL_PR_13_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md",
    "docs/codex/reports/FINAL_PR_13_V1_RELEASE_CLOSURE_RETURN_REPORT.md",
]

_REQUIRED_README_SECTIONS = [
    "# Odin Agent Shell",
    "## Current Status",
    "## What Odin Is",
    "## What Odin Is Not",
    "## Quick Start",
    "## Documentation Map",
    "## v1.0 Candidate Release Truth",
    "## Safety / Claim Boundaries",
    "## Support, Donations, and License",
    "## Danke / Thank You",
]

_THOR_THANKS_HEADING = "## Danke / Thank You"
_THOR_THANKS_BODY_FRAGMENT = "Danke an Q Germany"
_PAYPAL_ADDRESS = "QMetaKI@gmail.com"

_FORBIDDEN_README_PHRASES = [
    "available on pypi",
    "published to pypi",
    "github release exists",
    "is production_ready",
    "security certified",
    "superior model",
    "released on pypi",
]

_REQUIRED_CLI_COMMANDS = [
    "validate-v1-release-closure",
    "build-v1-release-closure-matrix",
    "build-v1-release-truth",
    "explain-v1-release-closure",
    "validate-root-public-surface",
    "build-root-inventory",
    "build-root-hygiene-report",
    "explain-root-public-surface",
    "validate-readme-v1",
    "build-readme-v1-plan",
    "explain-readme-v1",
    "validate-donation-surface",
    "build-donations-plan",
    "explain-donation-surface",
    "validate-release-artifact-boundary",
    "build-release-artifact-boundary",
    "explain-release-artifact-boundary",
    "validate-final-pr-13-v1-release-closure",
]

_REQUIRED_HUB_ENDPOINTS = [
    "/v1-release-closure/status.json",
    "/v1-release-closure/matrix.json",
    "/v1-release-closure/truth.json",
    "/root-public-surface/inventory.json",
    "/root-public-surface/hygiene.json",
    "/readme-v1/plan.json",
    "/donation-surface/plan.json",
    "/release-artifact-boundary/index.json",
    "/release/sequence-after-pr13.json",
]

_REQUIRED_UI_IDS = [
    "v1-release-closure-section",
    "root-public-surface-section",
    "readme-v1-section",
    "donation-surface-section",
    "release-artifact-boundary-section",
    "final-pr-13-closure-section",
]

_FORBIDDEN_MODULE_PATTERNS = [
    "eval(",
    "exec(",
    "subprocess",
    "__import__",
]

_FORBIDDEN_NETWORK_PATTERNS = [
    "urllib.request.urlopen",
    "http.client.HTTPConnection",
    "socket.connect",
    "requests.get",
    "httpx.",
    "aiohttp.",
]


def _load_json(path: Path) -> tuple[dict | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:
        return None, str(exc)


def _check_new_module_files(root: Path, errors: list[str]) -> None:
    new_module_dirs = [
        "odin/v1_release_closure",
        "odin/root_public_surface",
        "odin/readme_v1",
        "odin/donation_surface",
        "odin/release_artifact_boundary",
    ]
    for rel_dir in new_module_dirs:
        module_dir = root / rel_dir
        if not module_dir.exists():
            continue
        for py_file in sorted(module_dir.glob("*.py")):
            text = py_file.read_text(encoding="utf-8", errors="ignore")
            for pattern in _FORBIDDEN_MODULE_PATTERNS:
                if pattern in text:
                    errors.append(f"forbidden pattern '{pattern}' in {py_file.relative_to(root)}")
            for pattern in _FORBIDDEN_NETWORK_PATTERNS:
                if pattern in text:
                    errors.append(f"forbidden network pattern '{pattern}' in {py_file.relative_to(root)}")
            if "app_state" in text and "mutation" in text and "app_state_mutation = True" in text:
                errors.append(f"app state mutation in {py_file.relative_to(root)}")
            if "external_send = True" in text:
                errors.append(f"external send in {py_file.relative_to(root)}")
            if "production_ready = True" in text or '"production_ready": true' in text.lower():
                errors.append(f"production readiness claim in {py_file.relative_to(root)}")


def run_checks(repo_root: str, generated_at_utc: str) -> dict:
    root = Path(repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    checked_files: list[str] = []

    # Check required module files
    for rel in _REQUIRED_MODULE_FILES:
        p = root / rel
        checked_files.append(rel)
        if not p.exists():
            errors.append(f"missing required module file: {rel}")

    # Check examples (must parse as JSON and include candidate_only: true)
    for rel in _REQUIRED_EXAMPLES:
        p = root / rel
        checked_files.append(rel)
        if not p.exists():
            errors.append(f"missing required example: {rel}")
            continue
        data, err = _load_json(p)
        if data is None:
            errors.append(f"example does not parse as JSON: {rel} — {err}")
            continue
        if data.get("candidate_only") is not True:
            errors.append(f"example missing candidate_only: true — {rel}")

    # Check reports (must parse as JSON)
    for rel in _REQUIRED_REPORTS:
        p = root / rel
        checked_files.append(rel)
        if not p.exists():
            errors.append(f"missing required report: {rel}")
            continue
        data, err = _load_json(p)
        if data is None:
            errors.append(f"report does not parse as JSON: {rel} — {err}")

    # Check registries
    for rel in _REQUIRED_REGISTRIES:
        p = root / rel
        checked_files.append(rel)
        if not p.exists():
            errors.append(f"missing required registry: {rel}")
            continue
        data, err = _load_json(p)
        if data is None:
            errors.append(f"registry does not parse as JSON: {rel} — {err}")

    # Check schemas
    for rel in _REQUIRED_SCHEMAS:
        p = root / rel
        checked_files.append(rel)
        if not p.exists():
            errors.append(f"missing required schema: {rel}")
            continue
        data, err = _load_json(p)
        if data is None:
            errors.append(f"schema does not parse as JSON: {rel} — {err}")

    # Check docs
    for rel in _REQUIRED_DOCS:
        p = root / rel
        checked_files.append(rel)
        if not p.exists():
            errors.append(f"missing required doc: {rel}")

    # Check README
    readme_path = root / "README.md"
    checked_files.append("README.md")
    if not readme_path.exists():
        errors.append("README.md missing")
    else:
        readme_text = readme_path.read_text(encoding="utf-8")
        for section in _REQUIRED_README_SECTIONS:
            if section not in readme_text:
                errors.append(f"README.md missing section: {section}")
        if "DONATIONS.md" not in readme_text:
            errors.append("README.md does not link DONATIONS.md")
        if _THOR_THANKS_HEADING not in readme_text:
            errors.append("README.md missing Danke / Thank You heading")
        if _THOR_THANKS_BODY_FRAGMENT not in readme_text:
            errors.append("README.md missing exact Thor-Agent-Kit Thank You body")
        readme_lower = readme_text.lower()
        for phrase in _FORBIDDEN_README_PHRASES:
            if phrase in readme_lower:
                errors.append(f"README.md contains forbidden phrase: '{phrase}'")

    # Check DONATIONS.md
    donations_path = root / "DONATIONS.md"
    checked_files.append("DONATIONS.md")
    if not donations_path.exists():
        errors.append("DONATIONS.md missing at root")
    else:
        donations_text = donations_path.read_text(encoding="utf-8")
        if "Odin" not in donations_text:
            errors.append("DONATIONS.md does not reference Odin")
        if _PAYPAL_ADDRESS not in donations_text:
            errors.append(f"DONATIONS.md missing PayPal address: {_PAYPAL_ADDRESS}")
        if "optional" not in donations_text.lower():
            errors.append("DONATIONS.md missing optional donation framing")
        if "support obligation" not in donations_text.lower():
            errors.append("DONATIONS.md missing no-support-obligation statement")
        if "licensing" not in donations_text.lower():
            errors.append("DONATIONS.md missing no-licensing statement")

    # Check CLI
    cli_path = root / "odin" / "cli.py"
    checked_files.append("odin/cli.py")
    if not cli_path.exists():
        errors.append("odin/cli.py missing")
    else:
        cli_text = cli_path.read_text(encoding="utf-8")
        for cmd in _REQUIRED_CLI_COMMANDS:
            if f'"{cmd}"' not in cli_text:
                errors.append(f"CLI missing command: {cmd}")
        if "validate_final_pr_13_v1_release_closure" not in cli_text:
            errors.append("CLI missing validate_final_pr_13_v1_release_closure function")
        if "validate_final_pr_13_v1_release_closure()" not in cli_text:
            errors.append("validate-all does not call PR13 validator")

    # Check Local Hub server
    server_path = root / "odin" / "local_hub" / "server.py"
    checked_files.append("odin/local_hub/server.py")
    if not server_path.exists():
        errors.append("odin/local_hub/server.py missing")
    else:
        server_text = server_path.read_text(encoding="utf-8")
        for endpoint in _REQUIRED_HUB_ENDPOINTS:
            if endpoint not in server_text:
                errors.append(f"Local Hub missing endpoint: {endpoint}")

    # Check UI REQUIRED_IDS
    ui_path = root / "odin" / "local_hub" / "ui.py"
    checked_files.append("odin/local_hub/ui.py")
    if not ui_path.exists():
        errors.append("odin/local_hub/ui.py missing")
    else:
        ui_text = ui_path.read_text(encoding="utf-8")
        for section_id in _REQUIRED_UI_IDS:
            if f'"{section_id}"' not in ui_text:
                errors.append(f"REQUIRED_IDS missing: {section_id}")

    # Check for forbidden patterns in new modules
    _check_new_module_files(root, errors)

    # Check release artifact boundary report
    rab_path = root / "reports" / "final_pr_13_release_artifact_boundary.json"
    if rab_path.exists():
        data, _ = _load_json(rab_path)
        if data:
            if data.get("external_release_claimed") is not False:
                errors.append("release artifact boundary report: external_release_claimed must be false")
            if data.get("tag_creation_claimed") is not False:
                errors.append("release artifact boundary report: tag_creation_claimed must be false")
            manual_actions = data.get("manual_actions", [])
            action_names = [a.get("action", "") for a in manual_actions]
            for required_action in ["create git tag", "create GitHub Release", "publish to PyPI", "upload release assets"]:
                if required_action not in action_names:
                    errors.append(f"release artifact boundary missing manual action: {required_action}")

    # Check v1 release truth
    truth_path = root / "reports" / "final_pr_13_v1_release_truth.json"
    if truth_path.exists():
        data, _ = _load_json(truth_path)
        if data:
            if data.get("external_release_claimed") is not False:
                errors.append("v1 release truth: external_release_claimed must be false")
            if data.get("tag_creation_claimed") is not False:
                errors.append("v1 release truth: tag_creation_claimed must be false")
            if data.get("github_release_claimed") is not False:
                errors.append("v1 release truth: github_release_claimed must be false")
            if data.get("pypi_publication_claimed") is not False:
                errors.append("v1 release truth: pypi_publication_claimed must be false")

    return {
        "status": "ok" if not errors else "fail",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "checked_files": checked_files,
        "errors": errors,
        "warnings": warnings,
        "not_proven": [
            "production_readiness",
            "security_certification",
            "external_release_certification",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_final_pr_13_v1_release_closure",
        description="Validate FINAL-PR-13 v1.0 Release Closure artifacts.",
    )
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    parser.add_argument("--out", default="reports/final_pr_13_v1_release_closure_report.json",
                        help="Output report path")
    parser.add_argument("--generated-at-utc", default="2026-01-01T00:00:00Z",
                        dest="generated_at_utc")
    args = parser.parse_args(argv)

    report = run_checks(args.repo_root, args.generated_at_utc)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True),
                        encoding="utf-8")

    if report["errors"]:
        for err in report["errors"]:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"check_final_pr_13_v1_release_closure: OK ({report['error_count']} errors, "
          f"{report['warning_count']} warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
