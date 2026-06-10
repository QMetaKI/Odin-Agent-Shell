from __future__ import annotations
from pathlib import Path
import json
from odin.runtime.ids import stable_id, utc_stamp


def emit_support_bundle(root: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    files = [str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '.git' not in p.parts]
    payload = {
        "artifact_kind": "odin_support_bundle",
        "protocol_version": "7.1",
        "bundle_id": stable_id("SUPPORT", files, 12),
        "created_at": utc_stamp(),
        "file_count": len(files),
        "redaction": "paths_only_no_secret_payloads",
        "claim_boundary": "support_bundle_is_diagnostic_candidate_not_security_certification",
    }
    path = out_dir / f"{payload['bundle_id']}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding='utf-8')
    return path
