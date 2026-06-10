from __future__ import annotations

CANDIDATE_ONLY = True
APP_OWNS_APPLY = True
SEMANTIC_BUS_LOCAL_ONLY = True
MODEL_OUTPUT_PROJECTION_ONLY = True
DEFAULT_ROUTE = "3b_7b_8b_hybrid"

FORBIDDEN_ACTION_KINDS = {
    "apply_direct",
    "send_external",
    "mutate_app_state",
    "network_publish",
}

FORBIDDEN_BUS_REQUESTS = {
    "public_irc",
    "lan_mesh",
    "federation",
    "external_relay",
}

REQUIRED_CHANNELS = [
    "#work.received",
    "#work.validate",
    "#context.distill",
    "#worklet.graph",
    "#slot.forge",
    "#model.route",
    "#candidate.compose",
    "#candidate.ready",
]
