from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
LOCKFILE_PATH: Path = _REPO_ROOT / ".odin_runtime" / "local_runtime.lock"

LOCKFILE_CLAIM_BOUNDARY = "local_runtime_lockfile_candidate_no_app_apply"


def write_lockfile(
    pid: int,
    host: str,
    port: int,
    *,
    started_by: str = "odin.local_runtime.starter",
    runtime_mode: str = "portable_local",
) -> Path:
    LOCKFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "pid": pid,
        "host": host,
        "port": port,
        "started_by": started_by,
        "runtime_mode": runtime_mode,
        "created_at_policy": "deterministic_fixture",
        "claim_boundary": LOCKFILE_CLAIM_BOUNDARY,
        "candidate_only": True,
    }
    LOCKFILE_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return LOCKFILE_PATH


def read_lockfile() -> dict[str, Any] | None:
    if not LOCKFILE_PATH.exists():
        return None
    try:
        data = json.loads(LOCKFILE_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        return data
    except Exception:
        return None


def remove_lockfile() -> bool:
    if LOCKFILE_PATH.exists():
        LOCKFILE_PATH.unlink()
        return True
    return False


def lockfile_exists() -> bool:
    return LOCKFILE_PATH.exists()


def is_process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False
