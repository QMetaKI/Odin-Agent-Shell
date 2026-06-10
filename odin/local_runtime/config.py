from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

LOCAL_RUNTIME_CLAIM_BOUNDARY = "local_runtime_candidate_only_localhost_no_app_apply_no_external_send"

ALLOWED_HOSTS: frozenset[str] = frozenset({"127.0.0.1", "localhost", "::1"})
BLOCKED_HOSTS: frozenset[str] = frozenset({"0.0.0.0", "::", ""})

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8877
DEFAULT_RUNTIME_MODE = "portable_local"


@dataclass
class PortableRuntimeConfig:
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    runtime_mode: str = DEFAULT_RUNTIME_MODE
    candidate_only: bool = True
    app_owned_apply: bool = True
    external_send_default: bool = False
    claim_boundary: str = LOCAL_RUNTIME_CLAIM_BOUNDARY


def validate_config(cfg: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    host = cfg.get("host", DEFAULT_HOST)
    if host in BLOCKED_HOSTS:
        errors.append(f"host '{host}' is blocked by default; only localhost binds are allowed")
    elif host not in ALLOWED_HOSTS:
        errors.append(f"host '{host}' is not a recognized localhost address; use 127.0.0.1 or localhost")

    port = cfg.get("port", DEFAULT_PORT)
    if not isinstance(port, int) or not (1024 <= port <= 65535):
        errors.append(f"port {port!r} must be an integer between 1024 and 65535")

    if cfg.get("candidate_only") is False:
        errors.append("candidate_only must be true; Odin runtime is candidate-only")
    if cfg.get("app_owned_apply") is False:
        errors.append("app_owned_apply must be true; app owns apply")
    if cfg.get("external_send_default") is True:
        errors.append("external_send_default must be false; no external send by default")

    return errors


def load_config_from_dict(data: dict[str, Any]) -> tuple[PortableRuntimeConfig | None, list[str]]:
    errors = validate_config(data)
    if errors:
        return None, errors
    cfg = PortableRuntimeConfig(
        host=data.get("host", DEFAULT_HOST),
        port=int(data.get("port", DEFAULT_PORT)),
        runtime_mode=data.get("runtime_mode", DEFAULT_RUNTIME_MODE),
        candidate_only=data.get("candidate_only", True),
        app_owned_apply=data.get("app_owned_apply", True),
        external_send_default=data.get("external_send_default", False),
        claim_boundary=data.get("claim_boundary", LOCAL_RUNTIME_CLAIM_BOUNDARY),
    )
    return cfg, []


def load_config_from_file(path: Path) -> tuple[PortableRuntimeConfig | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return None, [f"failed to read config file {path}: {exc}"]
    if not isinstance(data, dict):
        return None, ["config file must be a JSON object"]
    return load_config_from_dict(data)
