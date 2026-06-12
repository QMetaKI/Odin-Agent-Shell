"""Connected apps placeholder data — FINAL-PR-02.

Claim boundary: connected_apps_demo_slots_only_no_real_app_integration_no_app_apply

Connected apps are demo placeholder slots only.
No real external app is connected.
No app state is mutated. No external send happens.
"""
from __future__ import annotations

CONNECTED_APPS_CLAIM_BOUNDARY = (
    "connected_apps_demo_slots_only_no_real_app_integration_no_app_apply"
)

APP_SLOTS: list[dict] = [
    {
        "slot_id": "generic",
        "label": "Generic App Slot",
        "description": "Placeholder for a generic app integration. Not connected.",
        "status": "demo_placeholder_not_connected",
        "app_apply": False,
        "external_send": False,
        "app_state_mutation": False,
        "candidate_only": True,
        "deferred_to": "FINAL-PR-03",
    },
    {
        "slot_id": "browser",
        "label": "Browser Slot",
        "description": "Placeholder for a browser app integration. Not connected.",
        "status": "demo_placeholder_not_connected",
        "app_apply": False,
        "external_send": False,
        "app_state_mutation": False,
        "candidate_only": True,
        "deferred_to": "FINAL-PR-03",
    },
    {
        "slot_id": "file",
        "label": "File Slot",
        "description": "Placeholder for a file-based app integration. Not connected.",
        "status": "demo_placeholder_not_connected",
        "app_apply": False,
        "external_send": False,
        "app_state_mutation": False,
        "candidate_only": True,
        "deferred_to": "FINAL-PR-03",
    },
]

APP_BRIDGE_STATUS: dict = {
    "bridge_active": False,
    "real_app_connected": False,
    "app_apply": False,
    "external_send": False,
    "app_state_mutation": False,
    "status": "demo_placeholder_not_runtime",
    "not_proven": [
        "real_app_bridge_runtime",
        "external_app_connection",
        "app_apply",
        "external_send",
    ],
    "claim_boundary": CONNECTED_APPS_CLAIM_BOUNDARY,
}


def get_app_slots() -> list[dict]:
    """Return connected app placeholder slots. No real app is connected."""
    return APP_SLOTS


def get_app_bridge_status() -> dict:
    """Return app bridge placeholder status. Bridge is not active."""
    return APP_BRIDGE_STATUS


def build_apps_json() -> dict:
    """Build the /apps.json response payload."""
    return {
        "artifact_kind": "odin_connected_apps_status",
        "candidate_only": True,
        "real_app_connected": False,
        "app_apply": False,
        "external_send": False,
        "slots": APP_SLOTS,
        "app_bridge_status": APP_BRIDGE_STATUS,
        "not_proven": [
            "real_app_bridge_runtime",
            "external_app_connection",
            "app_apply",
            "external_send",
        ],
        "claim_boundary": CONNECTED_APPS_CLAIM_BOUNDARY,
    }
