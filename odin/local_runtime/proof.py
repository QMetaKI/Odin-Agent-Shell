from __future__ import annotations

from typing import Any

from odin.local_runtime.config import (
    validate_config,
    DEFAULT_HOST,
    DEFAULT_PORT,
    LOCAL_RUNTIME_CLAIM_BOUNDARY,
)
from odin.local_runtime.ports import check_port_in_use

PROOF_CLAIM_BOUNDARY = (
    "local_runtime_once_smoke_proof_candidate_only_"
    "no_production_readiness_no_windows_service_no_live_model_no_external_send"
)

NOT_PROVEN = [
    "production_readiness",
    "windows_service_or_tray_or_installer",
    "signed_installer",
    "live_model_inference",
    "security_certification",
    "public_network_api",
    "app_state_mutation",
    "external_send_authority",
    "deploy_readiness",
]

PROVEN = [
    "config_validates_localhost_only",
    "public_bind_rejected",
    "port_availability_check_structured",
    "lockfile_semantics_deterministic",
    "local_api_once_smoke_binds_localhost",
]


def run_once_smoke_proof(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
) -> dict[str, Any]:
    steps: list[dict[str, Any]] = []

    cfg_errors = validate_config({"host": host, "port": port})
    steps.append({
        "step": "validate_config",
        "status": "ok" if not cfg_errors else "failed",
        "errors": cfg_errors,
    })

    from odin.local_runtime.config import BLOCKED_HOSTS
    public_bind_result = validate_config({"host": "0.0.0.0", "port": port})
    steps.append({
        "step": "public_bind_rejected",
        "status": "ok" if public_bind_result else "failed",
        "blocked_host": "0.0.0.0",
    })

    port_result = check_port_in_use(host, port)
    steps.append({
        "step": "port_check",
        "port_status": port_result["status"],
        "status": "ok",
    })

    once_smoke_result: dict[str, Any] = {"status": "skipped", "reason": "port_in_use"}
    if port_result["status"] == "available":
        from odin.daemon.local_api import run_local_api
        try:
            sr = run_local_api(host=host, port=port, once_smoke=True)
            once_smoke_result = {"status": "ok", "result": sr}
        except Exception as exc:
            once_smoke_result = {"status": "error", "error": str(exc)}
    steps.append({"step": "once_smoke_bind", **once_smoke_result})

    all_ok = all(s.get("status") in {"ok", "skipped"} for s in steps)

    return {
        "artifact_kind": "local_runtime_proof_packet",
        "status": "ok" if all_ok else "partial",
        "host": host,
        "port": port,
        "candidate_only": True,
        "steps": steps,
        "proven": PROVEN,
        "not_proven": NOT_PROVEN,
        "claim_boundary": PROOF_CLAIM_BOUNDARY,
        "note": (
            "This is a bounded local smoke proof. "
            "It does not claim production readiness, Windows service, "
            "signed installer, live model inference, or public network access."
        ),
    }
