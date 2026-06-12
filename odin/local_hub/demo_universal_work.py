"""Deterministic demo Universal Work flow — FINAL-PR-02.

Claim boundary: demo_universal_work_candidate_response_not_model_or_provider_execution

This module implements a deterministic demo Universal Work flow.
It does NOT call any model, provider, or external service.
It returns a hard-coded candidate response packet showing the shape of Odin's work.

Flow: raw input → Handoff Context → Universal Work Packet → Candidate Artifact → Response Packet
"""
from __future__ import annotations

import uuid

DEMO_CLAIM_BOUNDARY = (
    "demo_universal_work_candidate_response_not_model_or_provider_execution"
)

DEMO_NOT_PROVEN = [
    "model_inference",
    "provider_execution",
    "real_app_bridge_runtime",
    "external_app_connection",
    "app_apply",
    "external_send",
    "qirc_core_runtime",
]


def build_demo_universal_work_response(input_text: str = "demo input") -> dict:
    """Build a deterministic demo Universal Work response.

    No model is called. No provider is executed. No API key is used.
    The response is hard-coded to show the candidate packet shape.
    """
    work_id = f"demo-uw-{uuid.uuid4().hex[:8]}"

    return {
        "artifact_kind": "odin_demo_universal_work_response_packet",
        "candidate_only": True,
        "local_only": True,
        "model_execution": False,
        "model_inference": False,
        "provider_execution": False,
        "app_apply": False,
        "external_send": False,
        "input": input_text,
        "handoff_context": {
            "profile": "generic",
            "intent": "demo_universal_work",
            "forbidden_actions": [
                "provider_execution",
                "model_inference",
                "app_apply",
                "external_send",
            ],
        },
        "universal_work": {
            "work_id": work_id,
            "kind": "demo",
            "status": "compiled",
        },
        "candidate_artifact": {
            "artifact_kind": "demo_candidate",
            "summary": (
                "This is a deterministic demo candidate. "
                "No model was invoked. Odin compiled the work packet and "
                "returned this candidate for the app to review and optionally apply."
            ),
        },
        "response_packet": {
            "status": "ok_with_known_gaps",
        },
        "not_proven": DEMO_NOT_PROVEN,
        "claim_boundary": DEMO_CLAIM_BOUNDARY,
    }


def get_demo_universal_work_json() -> dict:
    """Return the static demo Universal Work GET response."""
    return {
        "artifact_kind": "odin_demo_universal_work_info",
        "candidate_only": True,
        "description": (
            "POST to /demo/universal-work with {\"input\": \"your text\"} "
            "to receive a deterministic candidate response packet. "
            "No model is called. No provider is executed. No app apply."
        ),
        "flow": [
            "raw input",
            "handoff context",
            "universal work packet",
            "candidate artifact",
            "response packet",
        ],
        "demo_response_preview": build_demo_universal_work_response("example demo input"),
        "not_proven": DEMO_NOT_PROVEN,
        "claim_boundary": DEMO_CLAIM_BOUNDARY,
    }
