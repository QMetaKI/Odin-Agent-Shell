from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List
import json


def shadow_registry_consistency_report(root: str | Path) -> Dict[str, Any]:
    base = Path(root)
    registries = base / "registries"
    required = [
        "artifact_types.json",
        "verb_registry.json",
        "output_contract_types.json",
        "semantic_bus_channels.json",
        "model_scale_ladder.json",
        "slot_classes.json",
        "artifact_lenses.json",
        "acceptance_gates.json",
        "failure_states.json",
        "codex_task_registry.json",
        "codex_pr_bundle_registry.json",
        "shadow_runtime_contract_registry.json",
    ]
    missing: List[str] = []
    invalid: List[str] = []
    for name in required:
        path = registries / name
        if not path.exists():
            missing.append(name)
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - diagnostic branch
            invalid.append(f"{name}: {exc}")
    return {
        "artifact_kind": "odin_shadow_registry_consistency_report",
        "protocol_version": "7.1-shadow",
        "required_count": len(required),
        "missing": missing,
        "invalid": invalid,
        "ok": not missing and not invalid,
        "boundary": "registry_report_only_no_runtime_truth_claim",
    }
