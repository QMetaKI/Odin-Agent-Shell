from __future__ import annotations

from typing import Any, Dict


def build_shadow_trace_record(work: Dict[str, Any], trace_id: str | None = None) -> Dict[str, Any]:
    trace_id = trace_id or work.get("trace_id") or f"TRACE-{work.get('work_id', 'UNKNOWN')}"
    return {
        "artifact_kind": "odin_shadow_trace_record",
        "protocol_version": "7.1-shadow",
        "trace_id": trace_id,
        "work_id": work.get("work_id"),
        "tables_touched": ["universal_works", "semantic_bus_events", "candidate_artifacts", "trace_entries"],
        "retention_class": "redacted_trace",
        "receipt_candidate": {
            "status": "candidate_only",
            "external_verification": False,
        },
        "boundary": "trace_candidate_only_no_runtime_receipt_claim",
    }
