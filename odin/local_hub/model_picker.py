"""Model picker data and policy — FINAL-PR-02.

Claim boundary: model_picker_candidate_only_no_provider_execution_no_model_inference

Model picker shows options only. No model is executed.
No provider binary is called. No API key is read.
"""
from __future__ import annotations

MODEL_PICKER_CLAIM_BOUNDARY = (
    "model_picker_candidate_only_no_provider_execution_no_model_inference"
)

MODEL_OPTIONS: list[dict] = [
    {
        "option_id": "none",
        "label": "None",
        "description": "No model selected. Odin returns deterministic candidates only.",
        "execution_status": "not_executing",
        "candidate_only": True,
        "provider_execution": False,
        "model_inference": False,
        "recommended_for": "demo_and_planning",
    },
    {
        "option_id": "mock",
        "label": "Mock deterministic candidate",
        "description": "Returns hard-coded deterministic demo candidate. No model binary is called.",
        "execution_status": "mock_only_not_executing",
        "candidate_only": True,
        "provider_execution": False,
        "model_inference": False,
        "recommended_for": "demo_universal_work_flow",
    },
    {
        "option_id": "local_candidate",
        "label": "Local candidate provider (planned, not executed)",
        "description": "Local candidate provider is listed for future activation. Not executed in this PR.",
        "execution_status": "planned_not_executed",
        "candidate_only": True,
        "provider_execution": False,
        "model_inference": False,
        "recommended_for": "future_final_pr_04",
        "deferred_to": "FINAL-PR-04",
    },
]

PROVIDER_STATUS: dict = {
    "active_provider": None,
    "model_inference": False,
    "provider_execution": False,
    "api_key_in_use": False,
    "local_binary_running": False,
    "remote_provider_enabled": False,
    "status": "no_provider_active",
    "not_proven": [
        "model_inference",
        "provider_execution",
        "live_inference_verified",
    ],
    "claim_boundary": MODEL_PICKER_CLAIM_BOUNDARY,
}


def get_model_options() -> list[dict]:
    """Return available model picker options. No model is executed."""
    return MODEL_OPTIONS


def get_provider_status() -> dict:
    """Return provider status. No provider is active or executing."""
    return PROVIDER_STATUS


def build_models_json() -> dict:
    """Build the /models.json response payload."""
    return {
        "artifact_kind": "odin_model_picker_status",
        "candidate_only": True,
        "model_inference": False,
        "provider_execution": False,
        "api_key_in_use": False,
        "options": MODEL_OPTIONS,
        "provider_status": PROVIDER_STATUS,
        "not_proven": [
            "model_inference",
            "provider_execution",
            "live_inference_verified",
        ],
        "claim_boundary": MODEL_PICKER_CLAIM_BOUNDARY,
    }
