from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH: Path = _REPO_ROOT / ".odin_runtime" / "local_runtime_config.json"

BOOTSTRAP_CLAIM_BOUNDARY = (
    "first_run_bootstrap_local_config_only_no_app_apply_no_external_send_"
    "localhost_safe_default_not_production_readiness_proof"
)

SAFE_DEFAULT_CONFIG: dict[str, Any] = {
    "host": "127.0.0.1",
    "port": 8877,
    "runtime_mode": "portable",
    "candidate_only": True,
    "app_owned_apply": True,
    "public_bind": False,
    "external_send_default": False,
    "provider_live_default": False,
    "claim_boundary": "local_config_is_not_production_readiness_proof",
}

BOOTSTRAP_KNOWN_NON_PROOFS = [
    "not_production_readiness_proof",
    "not_windows_service_tray_installer_proof",
    "not_provider_live_model_proof",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
]

BLOCKED_HOSTS = frozenset({"0.0.0.0", "::", ""})


def _validate_safe_config(cfg: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    host = cfg.get("host", "127.0.0.1")
    if host in BLOCKED_HOSTS:
        errors.append(f"blocked host {host!r} — public bind not allowed in safe default config")
    if cfg.get("public_bind") is True:
        errors.append("public_bind must not be true in safe default config")
    if cfg.get("external_send_default") is True:
        errors.append("external_send_default must not be true in safe default config")
    if cfg.get("provider_live_default") is True:
        errors.append("provider_live_default must not be true in safe default config")
    if cfg.get("candidate_only") is False:
        errors.append("candidate_only must be true in safe default config")
    if cfg.get("app_owned_apply") is False:
        errors.append("app_owned_apply must be true in safe default config")
    return errors


def run_first_run_bootstrap(
    config_path: Path = CONFIG_PATH,
    *,
    force: bool = False,
) -> dict[str, Any]:
    if config_path.exists() and not force:
        return {
            "artifact_kind": "odin_bootstrap_report",
            "status": "skipped",
            "reason": "config already exists — idempotent, no overwrite",
            "config_path": str(config_path),
            "candidate_only": True,
            "state_mutated": False,
            "claim_boundary": BOOTSTRAP_CLAIM_BOUNDARY,
            "known_non_proofs": BOOTSTRAP_KNOWN_NON_PROOFS,
        }

    guard_errors = _validate_safe_config(SAFE_DEFAULT_CONFIG)
    if guard_errors:
        return {
            "artifact_kind": "odin_bootstrap_report",
            "status": "blocked",
            "reason": "safe default config failed internal guard",
            "guard_errors": guard_errors,
            "candidate_only": True,
            "state_mutated": False,
            "claim_boundary": BOOTSTRAP_CLAIM_BOUNDARY,
            "known_non_proofs": BOOTSTRAP_KNOWN_NON_PROOFS,
        }

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(SAFE_DEFAULT_CONFIG, indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "artifact_kind": "odin_bootstrap_report",
        "status": "created",
        "config_path": str(config_path),
        "config_written": SAFE_DEFAULT_CONFIG,
        "candidate_only": True,
        "state_mutated": True,
        "mutation_scope": "local_config_file_only",
        "claim_boundary": BOOTSTRAP_CLAIM_BOUNDARY,
        "known_non_proofs": BOOTSTRAP_KNOWN_NON_PROOFS,
    }
