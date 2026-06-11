"""Thor CLI Probe — Discover and classify Thor CLI availability.

Usage:
    python tools/dev/thor_cli_probe.py
    python tools/dev/thor_cli_probe.py --json

Optional (requires network):
    python tools/dev/thor_cli_probe.py --attempt-install --json

Read-only by default. Does not mutate the repo. Does not require network unless
--attempt-install is passed.

Claim boundary: thor_cli_probe_read_only_diagnostic_only_advisory
"""

from __future__ import annotations

import importlib.util
import json
import os
import pkgutil
import shutil
import subprocess
import sys
from pathlib import Path


def check_path() -> str:
    return os.environ.get("PATH", "")


def check_cwd() -> str:
    return str(Path.cwd())


def check_command_v_thor() -> str | None:
    return shutil.which("thor")


def check_module(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except (ModuleNotFoundError, ValueError):
        return False


def check_pip_show(package: str) -> str:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except Exception:
        return ""


def discover_thor_like_modules() -> list[str]:
    return [m.name for m in pkgutil.iter_modules() if "thor" in m.name.lower()]


def check_tmp_thor_agent_kit() -> bool:
    return Path("/tmp/thor-agent-kit").is_dir()


def run_thor_help() -> str:
    thor_path = check_command_v_thor()
    if not thor_path:
        return ""
    try:
        result = subprocess.run(
            ["thor", "--help"], capture_output=True, text=True, timeout=10
        )
        return result.stdout[:200] if result.returncode == 0 else ""
    except Exception:
        return ""


def classify_failure(
    thor_in_path: bool,
    module_found: bool,
    pip_found: bool,
    tmp_found: bool,
) -> str:
    if thor_in_path:
        return "thor_available"
    if pip_found and not thor_in_path:
        return "entrypoint_missing_after_install"
    if not pip_found and not thor_in_path and module_found:
        return "module_not_importable_after_install"
    if tmp_found and not thor_in_path:
        return "not_found_in_PATH"
    return "not_found_in_PATH"


def attempt_install(dry_run: bool = False) -> dict:
    """Attempt to install Thor from /tmp/thor-agent-kit or clone.

    Only runs when --attempt-install flag is passed.
    Requires network for fresh clone.
    """
    if dry_run:
        return {"attempted": False, "reason": "dry_run"}

    if check_tmp_thor_agent_kit():
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", ".[dev]", "-q"],
                cwd="/tmp/thor-agent-kit",
                capture_output=True,
                text=True,
                timeout=120,
            )
            return {
                "attempted": True,
                "source": "existing_/tmp/thor-agent-kit",
                "returncode": result.returncode,
                "stdout": result.stdout[:200],
            }
        except Exception as e:
            return {"attempted": True, "source": "existing_/tmp/thor-agent-kit", "error": str(e)}
    else:
        try:
            clone_result = subprocess.run(
                ["git", "clone", "--depth=1",
                 "https://github.com/QMetaKI/Thor-Agent-Kit.git",
                 "/tmp/thor-agent-kit"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if clone_result.returncode != 0:
                return {
                    "attempted": True,
                    "source": "clone",
                    "classification": "clone_unavailable",
                    "stderr": clone_result.stderr[:200],
                }
            install_result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", ".[dev]", "-q"],
                cwd="/tmp/thor-agent-kit",
                capture_output=True,
                text=True,
                timeout=120,
            )
            return {
                "attempted": True,
                "source": "fresh_clone",
                "returncode": install_result.returncode,
            }
        except Exception as e:
            return {"attempted": True, "source": "clone", "error": str(e)}


def probe(do_install: bool = False) -> dict:
    thor_path = check_command_v_thor()
    thor_in_path = thor_path is not None
    module_found = check_module("thor_agent_kit") or check_module("thor")
    pip_show = check_pip_show("thor-agent-kit") or check_pip_show("thor_agent_kit")
    pip_found = bool(pip_show)
    tmp_found = check_tmp_thor_agent_kit()
    thor_modules = discover_thor_like_modules()
    thor_help = run_thor_help() if thor_in_path else ""

    install_result = None
    if do_install:
        install_result = attempt_install()
        thor_path_after = check_command_v_thor()
        thor_in_path = thor_path_after is not None

    classification = classify_failure(thor_in_path, module_found, pip_found, tmp_found)

    return {
        "artifact_kind": "thor_cli_probe_result",
        "advisory_only": True,
        "cwd": check_cwd(),
        "path": check_path(),
        "thor_in_path": thor_in_path,
        "thor_path": thor_path,
        "module_found": module_found,
        "pip_show_found": pip_found,
        "pip_show_snippet": pip_show[:100] if pip_show else "",
        "tmp_thor_agent_kit_exists": tmp_found,
        "thor_like_modules": thor_modules,
        "thor_help_snippet": thor_help,
        "classification": classification,
        "install_attempted": install_result,
        "claim_boundary": "thor_cli_probe_read_only_diagnostic_only_advisory",
        "note": "Thor is advisory only. Odin repo validators remain authority.",
    }


def main() -> None:
    args = sys.argv[1:]
    as_json = "--json" in args
    do_install = "--attempt-install" in args

    result = probe(do_install=do_install)

    if as_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"classification: {result['classification']}")
        print(f"thor_in_path:   {result['thor_in_path']}")
        print(f"thor_path:      {result['thor_path']}")
        print(f"module_found:   {result['module_found']}")
        print(f"pip_found:      {result['pip_show_found']}")
        print(f"tmp_kit_exists: {result['tmp_thor_agent_kit_exists']}")
        if result["thor_like_modules"]:
            print(f"thor_modules:   {result['thor_like_modules']}")
        print(f"note:           {result['note']}")


if __name__ == "__main__":
    main()
