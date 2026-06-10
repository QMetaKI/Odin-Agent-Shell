from __future__ import annotations

import os
import signal
from typing import Any

from odin.local_runtime.config import (
    PortableRuntimeConfig,
    load_config_from_dict,
    validate_config,
    ALLOWED_HOSTS,
    DEFAULT_HOST,
    DEFAULT_PORT,
    LOCAL_RUNTIME_CLAIM_BOUNDARY,
)
from odin.local_runtime.lockfile import (
    write_lockfile,
    read_lockfile,
    remove_lockfile,
    lockfile_exists,
    is_process_alive,
)
from odin.local_runtime.ports import check_port_in_use

STARTER_CLAIM_BOUNDARY = "local_runtime_starter_candidate_only_no_app_apply_no_external_send"


def _blocked_result(message: str, code: str = "blocked") -> dict[str, Any]:
    return {
        "artifact_kind": "odin_local_runtime_status",
        "status": "blocked",
        "error": message,
        "error_code": code,
        "candidate_only": True,
        "claim_boundary": STARTER_CLAIM_BOUNDARY,
    }


def start_portable_runtime(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    *,
    _blocking: bool = True,
) -> dict[str, Any]:
    cfg_data = {"host": host, "port": port, "candidate_only": True, "app_owned_apply": True}
    errors = validate_config(cfg_data)
    if errors:
        return _blocked_result("; ".join(errors), "config_invalid")

    port_status = check_port_in_use(host, port)
    if port_status["status"] == "in_use":
        return _blocked_result(port_status["error"], "port_in_use")

    if lockfile_exists():
        lock = read_lockfile()
        if lock and is_process_alive(lock.get("pid", -1)):
            return _blocked_result(
                f"runtime already running at {lock.get('host')}:{lock.get('port')} (pid {lock.get('pid')})",
                "already_running",
            )
        remove_lockfile()

    write_lockfile(pid=os.getpid(), host=host, port=port)

    if not _blocking:
        return {
            "artifact_kind": "odin_local_runtime_status",
            "status": "ready",
            "host": host,
            "port": port,
            "pid": os.getpid(),
            "runtime_mode": "portable_local",
            "candidate_only": True,
            "claim_boundary": STARTER_CLAIM_BOUNDARY,
        }

    from odin.daemon.local_api import run_local_api
    try:
        run_local_api(host=host, port=port, once_smoke=False)
    finally:
        remove_lockfile()

    return {
        "artifact_kind": "odin_local_runtime_status",
        "status": "stopped",
        "host": host,
        "port": port,
        "candidate_only": True,
        "claim_boundary": STARTER_CLAIM_BOUNDARY,
    }


def stop_portable_runtime() -> dict[str, Any]:
    if not lockfile_exists():
        return {
            "artifact_kind": "odin_local_runtime_status",
            "status": "not_running",
            "candidate_only": True,
            "claim_boundary": STARTER_CLAIM_BOUNDARY,
        }

    lock = read_lockfile()
    if lock is None:
        remove_lockfile()
        return {
            "artifact_kind": "odin_local_runtime_status",
            "status": "not_running",
            "note": "stale lockfile removed",
            "candidate_only": True,
            "claim_boundary": STARTER_CLAIM_BOUNDARY,
        }

    pid = lock.get("pid", -1)
    if not is_process_alive(pid):
        remove_lockfile()
        return {
            "artifact_kind": "odin_local_runtime_status",
            "status": "not_running",
            "note": f"process pid={pid} was not alive; lockfile cleaned",
            "candidate_only": True,
            "claim_boundary": STARTER_CLAIM_BOUNDARY,
        }

    try:
        os.kill(pid, signal.SIGTERM)
    except (OSError, ProcessLookupError) as exc:
        return _blocked_result(f"failed to send SIGTERM to pid={pid}: {exc}", "stop_failed")

    remove_lockfile()
    return {
        "artifact_kind": "odin_local_runtime_status",
        "status": "stopped",
        "pid": pid,
        "candidate_only": True,
        "claim_boundary": STARTER_CLAIM_BOUNDARY,
    }


def check_portable_runtime(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "artifact_kind": "odin_local_runtime_check",
        "candidate_only": True,
        "claim_boundary": STARTER_CLAIM_BOUNDARY,
    }

    cfg_errors = validate_config({"host": host, "port": port})
    result["config_valid"] = len(cfg_errors) == 0
    if cfg_errors:
        result["config_errors"] = cfg_errors

    lock = read_lockfile()
    result["lockfile_present"] = lock is not None
    if lock:
        pid = lock.get("pid", -1)
        result["lockfile_pid"] = pid
        result["lockfile_host"] = lock.get("host")
        result["lockfile_port"] = lock.get("port")
        result["process_alive"] = is_process_alive(pid)
    else:
        result["process_alive"] = False

    port_status = check_port_in_use(host, port)
    result["port_status"] = port_status["status"]

    if result["process_alive"] and port_status["status"] == "in_use":
        result["status"] = "running"
    elif lock is not None and not result["process_alive"]:
        result["status"] = "stale_lockfile"
    else:
        result["status"] = "not_running"

    return result
