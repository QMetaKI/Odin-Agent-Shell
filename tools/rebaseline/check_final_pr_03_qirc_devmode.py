"""Validator: FINAL-PR-03 QIRC Core Dev Mode.

Claim boundary: final_pr_03_validator_candidate_only_no_provider_no_app_apply

Run:
  python tools/rebaseline/check_final_pr_03_qirc_devmode.py \\
    --repo-root . \\
    --out reports/final_pr_03_qirc_devmode_report.json \\
    --generated-at-utc 2026-06-12T00:00:00Z
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
        "odin/qirc_core/__init__.py",
        "odin/qirc_core/policy.py",
        "odin/qirc_core/channels.py",
        "odin/qirc_core/bus.py",
        "odin/qirc_core/events.py",
        "odin/local_hub/surface_registry.py",
        "docs/codex/handoffs/FINAL_PR_03_HUB_SURFACE_CONVERGENCE_DECISION.md",
        "reports/final_pr_03_hub_surface_conflict_report.json",
        "schemas/final_pr_03_qirc_devmode_proof_packet.schema.json",
        "reports/final_pr_03_qirc_devmode_proof_packet.json",
        "examples/final_pr_03/qirc_devmode_proof_packet.example.json",
        "tests/test_final_pr_03_qirc_devmode.py",
    ]
    for rel in required_files:
        if not (repo / rel).exists():
            errors.append(f"missing required file: {rel}")

    # --- surface_registry checks ---
    registry_path = repo / "odin" / "local_hub" / "surface_registry.py"
    if registry_path.exists():
        try:
            sys.path.insert(0, str(repo))
            from odin.local_hub.surface_registry import SURFACES, check_conflicts, get_canonical_entry
            ports = {s["port"] for s in SURFACES}
            for required_port in [8765, 8877, 8878]:
                if required_port not in ports:
                    errors.append(f"surface_registry missing port: {required_port}")
            # Check 8765 is canonical
            try:
                canonical = get_canonical_entry()
                if canonical.get("port") != 8765:
                    errors.append("surface_registry: 8765 must be canonical entry")
            except Exception as exc:
                errors.append(f"surface_registry get_canonical_entry() failed: {exc}")
            # Check conflict check returns ok
            try:
                result = check_conflicts()
                if result.get("status") != "ok":
                    errors.append(f"surface_registry conflict check not ok: {result.get('status')}")
            except Exception as exc:
                errors.append(f"surface_registry check_conflicts() failed: {exc}")
        except Exception as exc:
            errors.append(f"surface_registry import failed: {exc}")
    else:
        errors.append("odin/local_hub/surface_registry.py missing")

    # --- qirc_core.policy checks ---
    policy_path = repo / "odin" / "qirc_core" / "policy.py"
    if policy_path.exists():
        try:
            from odin.qirc_core.policy import DEFAULT_POLICY
            if not DEFAULT_POLICY.is_safe():
                errors.append(f"DEFAULT_POLICY.is_safe() returned False: {DEFAULT_POLICY.check()}")
        except Exception as exc:
            errors.append(f"qirc_core.policy import/check failed: {exc}")
    else:
        errors.append("odin/qirc_core/policy.py missing")

    # --- qirc_core.channels checks ---
    channels_path = repo / "odin" / "qirc_core" / "channels.py"
    if channels_path.exists():
        try:
            from odin.qirc_core.channels import REQUIRED_CHANNELS
            required = [
                "#odin.runtime",
                "#odin.activity",
                "#odin.trace",
                "#odin.receipt",
                "#odin.handoff",
                "#odin.dev",
                "#odin.warning",
            ]
            for ch in required:
                if ch not in REQUIRED_CHANNELS:
                    errors.append(f"REQUIRED_CHANNELS missing: {ch}")
        except Exception as exc:
            errors.append(f"qirc_core.channels import failed: {exc}")
    else:
        errors.append("odin/qirc_core/channels.py missing")

    # --- server.py endpoint checks ---
    server_path = repo / "odin" / "local_hub" / "server.py"
    if server_path.exists():
        server_text = server_path.read_text(encoding="utf-8", errors="ignore")
        required_endpoints = [
            "/activity.json",
            "/qirc/channels.json",
            "/qirc/events.json",
            "/traces.json",
            "/receipts.json",
            "/dev/status.json",
        ]
        for ep in required_endpoints:
            if ep not in server_text:
                errors.append(f"server.py missing endpoint: {ep}")
    else:
        errors.append("odin/local_hub/server.py missing")

    # --- ui.py REQUIRED_IDS check ---
    ui_path = repo / "odin" / "local_hub" / "ui.py"
    if ui_path.exists():
        ui_text = ui_path.read_text(encoding="utf-8", errors="ignore")
        required_dev_ids = [
            "qirc-channel-viewer",
            "qirc-event-viewer",
            "activity-timeline",
            "trace-viewer",
            "receipt-viewer",
            "handoff-chain-viewer",
            "surface-map-viewer",
            "proof-gap-viewer",
        ]
        for id_ in required_dev_ids:
            if id_ not in ui_text:
                errors.append(f"ui.py REQUIRED_IDS missing: {id_}")
    else:
        errors.append("odin/local_hub/ui.py missing")

    # --- proof packet JSON checks ---
    proof_json_path = repo / "reports" / "final_pr_03_qirc_devmode_proof_packet.json"
    if proof_json_path.exists():
        try:
            packet = json.loads(proof_json_path.read_text(encoding="utf-8"))
            if packet.get("candidate_only") is not True:
                errors.append("proof packet: candidate_only must be true")
            if not packet.get("claim_boundary"):
                errors.append("proof packet: claim_boundary required")
            if not packet.get("not_proven"):
                errors.append("proof packet: not_proven list required")
        except Exception as exc:
            errors.append(f"proof packet JSON invalid: {exc}")

    # --- example file checks ---
    example_path = repo / "examples" / "final_pr_03" / "qirc_devmode_proof_packet.example.json"
    if example_path.exists():
        try:
            ex = json.loads(example_path.read_text(encoding="utf-8"))
            if ex.get("candidate_only") is not True:
                errors.append("example: candidate_only must be true")
            if not ex.get("claim_boundary"):
                errors.append("example: claim_boundary required")
        except Exception as exc:
            errors.append(f"example JSON invalid: {exc}")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FINAL-PR-03 QIRC Core Dev Mode validator")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--out", required=True, help="Output JSON report path")
    parser.add_argument("--generated-at-utc", default="2026-06-12T00:00:00Z")
    args = parser.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    errors, warnings = _check(repo)

    report = {
        "report_id": "odin.final_pr_03_qirc_devmode_check",
        "status": "ok" if not errors else "failed",
        "generated_at_utc": args.generated_at_utc,
        "repo_root": str(repo),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "candidate_only": True,
        "claim_boundary": "final_pr_03_validator_candidate_only_no_provider_no_app_apply",
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
