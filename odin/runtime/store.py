from __future__ import annotations
from pathlib import Path
import json
from odin.runtime.ids import stable_id, utc_stamp

class RuntimeStore:
    def __init__(self, root: str | Path = ".odin_runtime"):
        self.root = Path(root)
        self.candidates = self.root / "candidates"
        self.sessions = self.root / "sessions"
        self.qirc = self.root / "qirc"
        self.support = self.root / "support"
        for folder in [self.candidates, self.sessions, self.qirc, self.support]:
            folder.mkdir(parents=True, exist_ok=True)

    def write_candidate(self, candidate: dict) -> Path:
        cid = candidate.get("candidate_id") or stable_id("CAND", candidate, 12)
        path = self.candidates / f"{cid}.json"
        payload = dict(candidate)
        payload.setdefault("stored_at", utc_stamp())
        payload.setdefault("claim_boundary", "stored_candidate_has_no_app_apply_authority")
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        return path

    def write_session(self, response: dict) -> Path:
        sid = response.get("response_id") or stable_id("SESSION", response, 12)
        path = self.sessions / f"{sid}.json"
        payload = dict(response)
        payload.setdefault("stored_at", utc_stamp())
        payload.setdefault("claim_boundary", "stored_session_is_local_candidate_record_not_receipt")
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        for candidate in response.get("candidates", []):
            self.write_candidate(candidate)
        return path

    def status(self) -> dict:
        return {
            "artifact_kind": "odin_runtime_store_status",
            "protocol_version": "7.1",
            "root": str(self.root),
            "candidate_count": len(list(self.candidates.glob("*.json"))),
            "session_count": len(list(self.sessions.glob("*.json"))),
            "qirc_trace_count": len(list(self.qirc.glob("*.jsonl"))),
            "claim_boundary": "status_reports_local_store_shape_not_host_proof",
        }
