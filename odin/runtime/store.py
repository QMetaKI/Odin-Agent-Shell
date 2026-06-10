from __future__ import annotations
from pathlib import Path
import json
from typing import Any
from odin.runtime.ids import stable_id, utc_stamp


class RuntimeStore:
    def __init__(self, root: str | Path = ".odin_runtime"):
        self.root = Path(root)
        self.candidates = self.root / "candidates"
        self.sessions = self.root / "sessions"
        self.qirc = self.root / "qirc"
        self.bus_events = self.root / "bus_events"
        self.traces = self.root / "traces"
        self.support = self.root / "support"
        for folder in [self.candidates, self.sessions, self.qirc, self.bus_events, self.traces, self.support]:
            folder.mkdir(parents=True, exist_ok=True)

    def _write_json_record(self, folder: Path, record_id: str, payload: dict) -> Path:
        path = folder / f"{record_id}.json"
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        return path

    def _read_json_record(self, folder: Path, record_id: str) -> dict:
        path = folder / f"{record_id}.json"
        if not path.exists():
            return {"status": "missing", "record_id": record_id, "error": "record_not_found", "claim_boundary": "missing_record_is_not_app_apply_receipt"}
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            return {"status": "error", "record_id": record_id, "error": str(exc), "claim_boundary": "stored_record_error_no_apply_authority"}
        payload.setdefault("status", "ok")
        return payload

    def _list_ids(self, folder: Path) -> list[str]:
        return sorted(p.stem for p in folder.glob("*.json"))

    def write_candidate(self, candidate: dict) -> Path:
        cid = candidate.get("candidate_id") or stable_id("CAND", candidate, 12)
        payload = dict(candidate)
        payload.setdefault("artifact_kind", "odin_runtime_candidate_record")
        payload.setdefault("candidate_id", cid)
        payload.setdefault("stored_at", utc_stamp())
        payload.setdefault("candidate_only", True)
        payload.setdefault("claim_boundary", "stored_candidate_has_no_app_apply_authority")
        return self._write_json_record(self.candidates, cid, payload)

    def read_candidate(self, candidate_id: str) -> dict:
        return self._read_json_record(self.candidates, candidate_id)

    def list_candidate_ids(self) -> list[str]:
        return self._list_ids(self.candidates)

    def write_session(self, response: dict) -> Path:
        sid = response.get("response_id") or response.get("session_id") or stable_id("SESSION", response, 12)
        payload = dict(response)
        payload.setdefault("artifact_kind", "odin_runtime_session_record")
        payload.setdefault("session_id", sid)
        payload.setdefault("stored_at", utc_stamp())
        payload.setdefault("candidate_only", True)
        payload.setdefault("claim_boundary", "stored_session_is_local_candidate_record_not_receipt")
        path = self._write_json_record(self.sessions, sid, payload)
        for candidate in response.get("candidates", []):
            self.write_candidate(candidate)
        if response.get("why_trace"):
            self.write_trace(response["why_trace"])
        return path

    def read_session(self, session_id: str) -> dict:
        return self._read_json_record(self.sessions, session_id)

    def list_session_ids(self) -> list[str]:
        return self._list_ids(self.sessions)

    def write_bus_event(self, event: dict) -> Path:
        eid = event.get("event_id") or stable_id("BUS", event, 16)
        payload = dict(event)
        payload.setdefault("artifact_kind", "odin_runtime_bus_event_record")
        payload.setdefault("event_id", eid)
        payload.setdefault("stored_at", utc_stamp())
        payload.setdefault("candidate_only", True)
        payload.setdefault("local_only", True)
        payload.setdefault("claim_boundary", "stored_bus_event_is_local_trace_record_not_apply_receipt")
        return self._write_json_record(self.bus_events, eid, payload)

    def read_bus_event(self, event_id: str) -> dict:
        return self._read_json_record(self.bus_events, event_id)

    def list_bus_event_ids(self) -> list[str]:
        return self._list_ids(self.bus_events)

    def list_bus_events(self) -> list[dict]:
        return [self.read_bus_event(event_id) for event_id in self.list_bus_event_ids()]

    def write_trace(self, trace: dict[str, Any]) -> Path:
        tid = trace.get("trace_id") or stable_id("TRACE", trace, 12)
        payload = dict(trace)
        payload.setdefault("artifact_kind", "odin_runtime_trace_record")
        payload.setdefault("trace_id", tid)
        payload.setdefault("stored_at", utc_stamp())
        payload.setdefault("candidate_only", True)
        payload.setdefault("claim_boundary", "stored_trace_record_is_not_external_receipt")
        return self._write_json_record(self.traces, tid, payload)

    def status(self) -> dict:
        return {
            "artifact_kind": "odin_runtime_store_status",
            "protocol_version": "7.1",
            "root": str(self.root),
            "candidate_count": len(self.list_candidate_ids()),
            "session_count": len(self.list_session_ids()),
            "bus_event_count": len(self.list_bus_event_ids()),
            "qirc_trace_count": len(list(self.qirc.glob("*.jsonl"))),
            "trace_count": len(self._list_ids(self.traces)),
            "claim_boundary": "status_reports_local_store_shape_not_host_proof_or_app_apply_receipt",
        }
