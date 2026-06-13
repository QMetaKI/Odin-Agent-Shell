"""ReceiptLink for FINAL-PR-08 Projection Candidate Spine."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

CLAIM_BOUNDARY = "projection_candidate_spine_prepares_candidates_not_runtime_execution"


@dataclass
class ReceiptLink:
    link_id: str
    candidate_node_id: str
    trace_record_ref: str
    qirc_event_ref: str | None
    bound_at_utc: str
    candidate_only: bool = True
    claim_boundary: str = CLAIM_BOUNDARY

    def to_dict(self) -> dict:
        return {
            "link_id": self.link_id,
            "candidate_node_id": self.candidate_node_id,
            "trace_record_ref": self.trace_record_ref,
            "qirc_event_ref": self.qirc_event_ref,
            "bound_at_utc": self.bound_at_utc,
            "candidate_only": self.candidate_only,
            "claim_boundary": self.claim_boundary,
        }


def _deterministic_link_id(candidate_node_id: str, trace_record_ref: str, bound_at_utc: str) -> str:
    payload = json.dumps(
        {"candidate_node_id": candidate_node_id, "trace_record_ref": trace_record_ref, "bound_at_utc": bound_at_utc},
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"receipt_link_{digest}"


def build_receipt_link(
    candidate_node_id: str,
    trace_record_ref: str,
    qirc_event_ref: str | None = None,
    bound_at_utc: str = "2026-01-01T00:00:00Z",
) -> ReceiptLink:
    """Build a ReceiptLink.

    bound_at_utc must be present. No QIRC emit. No runtime proof.
    """
    link_id = _deterministic_link_id(candidate_node_id, trace_record_ref, bound_at_utc)
    return ReceiptLink(
        link_id=link_id,
        candidate_node_id=candidate_node_id,
        trace_record_ref=trace_record_ref,
        qirc_event_ref=qirc_event_ref,
        bound_at_utc=bound_at_utc,
    )
