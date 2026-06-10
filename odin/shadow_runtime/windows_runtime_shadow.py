from __future__ import annotations

from typing import Any, Dict


def build_shadow_windows_runtime_plan(mode: str = "standard_local") -> Dict[str, Any]:
    return {
        "artifact_kind": "odin_shadow_windows_runtime_plan",
        "protocol_version": "7.1-shadow",
        "mode": mode,
        "processes": ["odin-daemon", "odin-tray", "odin-control-center", "odin-worker-process"],
        "optional_processes": ["odin-semantic-bus", "odin-model-runner"],
        "startup_states": ["CONFIG_INIT", "DB_MIGRATE", "DAEMON_START", "HEALTH_CHECK", "MODEL_DISCOVERY", "NORMAL_OPERATION"],
        "localhost_only": True,
        "boundary": "runtime_plan_only_no_host_validation_claim",
    }
