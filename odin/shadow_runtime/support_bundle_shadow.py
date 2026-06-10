from __future__ import annotations

from typing import Any, Dict, List


def build_shadow_support_bundle_manifest(work_id: str, files: List[str] | None = None) -> Dict[str, Any]:
    files = files or ["SYSTEM_MAP.json", "FILE_MANIFEST.json", "runtime/traces/redacted.trace.json"]
    return {
        "artifact_kind": "odin_shadow_support_bundle_manifest",
        "protocol_version": "7.1-shadow",
        "work_id": work_id,
        "files": files,
        "redaction_required": True,
        "forbidden_contents": ["secrets", "raw_app_state", "model_provider_tokens"],
        "boundary": "support_bundle_manifest_only_no_upload_no_external_send",
    }
