from __future__ import annotations

from typing import Any, Dict


def validate_shadow_sdk_template(template_name: str, files: list[str]) -> Dict[str, Any]:
    required_markers = ["caller_manifest", "odin_connector", "event_digest_builder", "candidate_renderer", "apply_gate_bridge"]
    present = {marker: any(marker in f for f in files) for marker in required_markers}
    return {
        "artifact_kind": "odin_shadow_sdk_template_validation",
        "protocol_version": "7.1-shadow",
        "template_name": template_name,
        "required_markers": present,
        "ok": all(present.values()),
        "no_llm_in_app_required": True,
        "boundary": "template_validation_only_no_app_runtime_claim",
    }
