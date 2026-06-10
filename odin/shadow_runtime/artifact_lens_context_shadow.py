from __future__ import annotations

from typing import Any, Dict, List

DEFAULT_LENS_BY_TYPE = {
    "markdown": "text_lens",
    "plain_text": "text_lens",
    "document_excerpt": "document_lens",
    "repo_context": "code_lens",
    "diff": "code_lens",
    "error_log": "log_lens",
    "event_digest": "event_lens",
    "workflow_state": "workflow_lens",
    "game_state_digest": "game_state_lens",
    "app_qirc_bridge_digest": "event_lens",
}


def select_shadow_lenses(work: Dict[str, Any]) -> List[str]:
    """Return deterministic lens ids for the given Universal Work.

    Shadow contract: pure, local, no model call, no app state mutation.
    """
    lenses: List[str] = []
    for artifact in work.get("input_artifacts", []) or []:
        typ = artifact.get("artifact_type", "")
        lens = DEFAULT_LENS_BY_TYPE.get(typ, "generic_artifact_lens")
        if lens not in lenses:
            lenses.append(lens)
    if work.get("domain") == "wedding_speech" and "wedding_speech_lens" not in lenses:
        lenses.append("wedding_speech_lens")
    return lenses or ["generic_artifact_lens"]


def build_shadow_context_distillation_plan(work: Dict[str, Any]) -> Dict[str, Any]:
    lenses = select_shadow_lenses(work)
    return {
        "artifact_kind": "odin_shadow_context_distillation_plan",
        "protocol_version": "7.1-shadow",
        "work_id": work.get("work_id"),
        "active_lenses": lenses,
        "bus_channels": ["#lens.select", "#context.distill", "#context.capsule"],
        "context_budget": {
            "strategy": "current_moment_capsule",
            "max_context_tokens": 1800,
            "raw_state_allowed": False,
        },
        "boundary": "context_plan_only_no_app_state_authority",
    }
