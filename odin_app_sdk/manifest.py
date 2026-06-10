from __future__ import annotations
from odin.runtime.ids import stable_id


def build_app_manifest(app_id: str, app_name: str, *, permissions: list[str] | None = None) -> dict:
    return {
        "caller_id": app_id,
        "app_name": app_name,
        "protocol_version": "7.1",
        "permissions": permissions or ["submit_work", "receive_candidate", "provide_seed_pack", "provide_flow_pack"],
        "apply_boundary": {"app_owned": True, "odin_may_apply": False, "external_send_by_app_only": True},
        "qirc_digest_mode": "digest_only",
    }


def build_universal_work(app_id: str, goal: str, *, tags: list[str] | None = None, output_type: str = "candidate_markdown") -> dict:
    tags = tags or ["general"]
    return {
        "artifact_kind": "odin_universal_work",
        "protocol_version": "7.1",
        "work_id": stable_id("WORK", {"app_id": app_id, "goal": goal, "tags": tags}, 12),
        "caller_id": app_id,
        "binding_ref": {"caller_manifest_required": True, "app_apply_owned": True},
        "input_artifacts": [{"kind": "text", "value": goal, "privacy_class": "local_candidate"}],
        "work_intent": {"goal": goal, "tags": tags, "requires_model": True},
        "output_contract": {"type": output_type, "candidate_only": True, "requires_why_trace": True},
        "constraints": {"forbidden": ["apply directly", "send externally", "mutate app state"], "actions": []},
        "model_policy": {"resource_profile": "standard_local", "latency_mode": "interactive", "quality_target": "standard", "requires_model": True},
        "claim_boundary": {"claims": ["candidate_generated"], "forbidden_claims": ["runtime_verified", "model_inference_verified", "production_ready"]},
    }
