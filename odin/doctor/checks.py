from __future__ import annotations

import importlib
import socket
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]

DOCTOR_CLAIM_BOUNDARY = "doctor_checks_read_only_no_state_mutation_no_host_proof"

REQUIRED_PACKAGES = [
    "odin",
    "odin.runtime",
    "odin.local_runtime",
    "odin.agent_operator",
    "odin.doctor",
    "odin.bootstrap",
]

LOCALHOST_SAFE_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
BLOCKED_HOSTS = frozenset({"0.0.0.0", "::", ""})


def _check_result(name: str, status: str, detail: str = "", failure_reason: str = "") -> dict[str, Any]:
    result: dict[str, Any] = {
        "check": name,
        "status": status,
        "detail": detail,
    }
    if failure_reason:
        result["failure_reason"] = failure_reason
    return result


def check_python_version() -> dict[str, Any]:
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        return _check_result(
            "python_version",
            "fail",
            detail=version_str,
            failure_reason=f"Python 3.9+ required, found {version_str}",
        )
    return _check_result("python_version", "ok", detail=version_str)


def check_package_imports() -> dict[str, Any]:
    failed: list[str] = []
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
        except ImportError as exc:
            failed.append(f"{pkg}: {exc}")
    if failed:
        return _check_result(
            "package_imports",
            "fail",
            detail=str(failed),
            failure_reason="required packages not importable",
        )
    return _check_result("package_imports", "ok", detail=f"checked {len(REQUIRED_PACKAGES)} packages")


def check_runtime_dir() -> dict[str, Any]:
    runtime_dir = _REPO_ROOT / ".odin_runtime"
    if not runtime_dir.exists():
        return _check_result(
            "runtime_dir",
            "warn",
            detail=str(runtime_dir),
            failure_reason="runtime dir absent — will be created on first start",
        )
    return _check_result("runtime_dir", "ok", detail=str(runtime_dir))


def check_lockfile() -> dict[str, Any]:
    try:
        from odin.local_runtime.lockfile import LOCKFILE_PATH, read_lockfile, is_process_alive
    except ImportError as exc:
        return _check_result("lockfile", "fail", failure_reason=f"lockfile module not importable: {exc}")

    if not LOCKFILE_PATH.exists():
        return _check_result("lockfile", "ok", detail="no lockfile — runtime not running")

    lock = read_lockfile()
    if lock is None:
        return _check_result(
            "lockfile",
            "warn",
            detail=str(LOCKFILE_PATH),
            failure_reason="lockfile present but unreadable",
        )

    pid = lock.get("pid", -1)
    alive = is_process_alive(pid)
    if not alive:
        return _check_result(
            "lockfile",
            "warn",
            detail=f"pid={pid}",
            failure_reason="stale lockfile — process not alive",
        )
    return _check_result("lockfile", "ok", detail=f"pid={pid} alive")


def check_config_file() -> dict[str, Any]:
    config_path = _REPO_ROOT / ".odin_runtime" / "local_runtime_config.json"
    if not config_path.exists():
        return _check_result(
            "config_file",
            "warn",
            detail=str(config_path),
            failure_reason="config absent — run first-run-bootstrap to create safe default",
        )
    try:
        import json
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return _check_result("config_file", "fail", detail=str(config_path), failure_reason=f"config unreadable: {exc}")

    try:
        from odin.local_runtime.config import validate_config
        errs = validate_config(data)
    except ImportError as exc:
        return _check_result("config_file", "fail", failure_reason=f"config module not importable: {exc}")

    if errs:
        combined = "; ".join(errs)
        return _check_result("config_file", "fail", detail=combined, failure_reason=combined)

    host = data.get("host", "")
    if host in BLOCKED_HOSTS:
        return _check_result(
            "config_file",
            "fail",
            detail=f"host={host}",
            failure_reason=f"config has blocked host {host!r}; only localhost binds allowed",
        )
    return _check_result("config_file", "ok", detail=f"host={host}")


def check_host_safety(host: str) -> dict[str, Any]:
    if host in BLOCKED_HOSTS:
        return _check_result(
            "host_safety",
            "fail",
            detail=host,
            failure_reason=f"host {host!r} is blocked; only localhost allowed",
        )
    if host not in LOCALHOST_SAFE_HOSTS:
        return _check_result(
            "host_safety",
            "fail",
            detail=host,
            failure_reason=f"host {host!r} not recognized as localhost; only 127.0.0.1/localhost/::1 allowed",
        )
    return _check_result("host_safety", "ok", detail=host)


def check_port_availability(host: str = "127.0.0.1", port: int = 8877) -> dict[str, Any]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((host, port))
        if result == 0:
            return _check_result(
                "port_availability",
                "warn",
                detail=f"{host}:{port}",
                failure_reason=f"port {port} appears in use on {host}",
            )
        return _check_result("port_availability", "ok", detail=f"{host}:{port} available")
    except Exception as exc:
        return _check_result("port_availability", "warn", detail=str(exc), failure_reason=f"port check error: {exc}")


def check_local_api_health(host: str = "127.0.0.1", port: int = 8877) -> dict[str, Any]:
    try:
        import urllib.request
        url = f"http://{host}:{port}/health"
        with urllib.request.urlopen(url, timeout=1.0) as resp:
            status = resp.status
        return _check_result("local_api_health", "ok", detail=f"http {status}")
    except Exception:
        return _check_result(
            "local_api_health",
            "skip",
            detail=f"{host}:{port}",
            failure_reason="local API not reachable — runtime may not be running",
        )
