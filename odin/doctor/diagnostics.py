from __future__ import annotations

from typing import Any

from odin.doctor.checks import (
    DOCTOR_CLAIM_BOUNDARY,
    check_python_version,
    check_package_imports,
    check_runtime_dir,
    check_lockfile,
    check_config_file,
    check_host_safety,
    check_port_availability,
    check_local_api_health,
)

DOCTOR_REPORT_CLAIM = "doctor_report_read_only_candidate_not_production_readiness_proof"

KNOWN_NON_PROOFS = [
    "not_production_readiness_certification",
    "not_windows_service_tray_installer_proof",
    "not_provider_live_model_proof",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_security_certification",
]


def run_doctor(
    host: str = "127.0.0.1",
    port: int = 8877,
    *,
    include_api_health: bool = True,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    checks.append(check_python_version())
    checks.append(check_package_imports())
    checks.append(check_runtime_dir())
    checks.append(check_lockfile())
    checks.append(check_config_file())
    checks.append(check_host_safety(host))
    checks.append(check_port_availability(host, port))

    if include_api_health:
        checks.append(check_local_api_health(host, port))

    failures = [c for c in checks if c["status"] == "fail"]
    warnings = [c for c in checks if c["status"] == "warn"]
    skipped = [c for c in checks if c["status"] == "skip"]

    if failures:
        overall = "fail"
    elif warnings:
        overall = "warn"
    else:
        overall = "ok"

    failure_reasons = [c["failure_reason"] for c in failures if c.get("failure_reason")]

    report: dict[str, Any] = {
        "artifact_kind": "odin_doctor_report",
        "status": overall,
        "host": host,
        "port": port,
        "checks": checks,
        "failure_count": len(failures),
        "warning_count": len(warnings),
        "skip_count": len(skipped),
        "failure_reasons": failure_reasons,
        "candidate_only": True,
        "read_only": True,
        "state_mutated": False,
        "claim_boundary": DOCTOR_REPORT_CLAIM,
        "known_non_proofs": KNOWN_NON_PROOFS,
    }

    return report
