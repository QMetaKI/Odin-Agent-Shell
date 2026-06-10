from __future__ import annotations

from typing import Any

REPAIR_CLAIM_BOUNDARY = (
    "repair_plan_only_no_apply_no_state_mutation_no_external_send_"
    "explicit_apply_gate_required_for_any_real_repair"
)

REPAIR_KNOWN_NON_PROOFS = [
    "not_applied",
    "not_production_readiness_proof",
    "not_automatic_repair",
    "not_app_state_mutation",
    "not_external_send",
    "not_windows_service_tray_installer_proof",
    "not_provider_live_model_proof",
]

FAILURE_REASON_CATALOG: dict[str, str] = {
    "stale lockfile — process not alive": (
        "Remove the stale lockfile at .odin_runtime/local_runtime.lock "
        "after confirming no runtime is running."
    ),
    "config absent — run first-run-bootstrap to create safe default": (
        "Run: python -m odin.cli first-run-bootstrap "
        "to create a safe localhost-only default config."
    ),
    "config validation failed": (
        "Edit .odin_runtime/local_runtime_config.json to fix the listed errors. "
        "Ensure host is 127.0.0.1 or localhost."
    ),
    "config has blocked host": (
        "Update config host to 127.0.0.1 or localhost. "
        "Public binds (0.0.0.0, ::) are not allowed."
    ),
    "port appears in use": (
        "Check what process is using the configured port. "
        "Change port in config or stop the conflicting process."
    ),
    "required packages not importable": (
        "Run: python -m pip install -e . "
        "to install missing Odin packages."
    ),
    "Python 3.9+ required": (
        "Upgrade Python to 3.9 or later."
    ),
    "runtime dir absent": (
        "The .odin_runtime/ directory will be created automatically on first start. "
        "No action required unless start also fails."
    ),
}


def _suggest_fix(failure_reason: str) -> str:
    for key, suggestion in FAILURE_REASON_CATALOG.items():
        if key.lower() in failure_reason.lower():
            return suggestion
    return f"Investigate failure: {failure_reason}"


def build_repair_plan(doctor_report: dict[str, Any]) -> dict[str, Any]:
    checks = doctor_report.get("checks", [])
    failure_reasons = doctor_report.get("failure_reasons", [])

    failed_checks = [c for c in checks if c.get("status") == "fail"]
    warned_checks = [c for c in checks if c.get("status") == "warn"]

    plan_items: list[dict[str, Any]] = []
    for check in failed_checks:
        reason = check.get("failure_reason", "unknown failure")
        plan_items.append({
            "check": check.get("check"),
            "severity": "fail",
            "failure_reason": reason,
            "suggested_fix": _suggest_fix(reason),
            "plan_only": True,
            "apply_gate_required": True,
        })

    for check in warned_checks:
        reason = check.get("failure_reason", "warning")
        plan_items.append({
            "check": check.get("check"),
            "severity": "warn",
            "failure_reason": reason,
            "suggested_fix": _suggest_fix(reason),
            "plan_only": True,
            "apply_gate_required": True,
        })

    if not plan_items:
        overall = "no_repairs_needed"
    elif any(i["severity"] == "fail" for i in plan_items):
        overall = "repairs_suggested"
    else:
        overall = "improvements_suggested"

    return {
        "artifact_kind": "odin_repair_plan",
        "status": overall,
        "plan_items": plan_items,
        "plan_item_count": len(plan_items),
        "failure_count": len(failed_checks),
        "warning_count": len(warned_checks),
        "applied": False,
        "plan_only": True,
        "apply_gate_required": True,
        "candidate_only": True,
        "state_mutated": False,
        "claim_boundary": REPAIR_CLAIM_BOUNDARY,
        "known_non_proofs": REPAIR_KNOWN_NON_PROOFS,
    }
