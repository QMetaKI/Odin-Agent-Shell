from __future__ import annotations

def build_qirc_capability_slice_channels(profile: str, app_kind: str = "generic") -> dict:
    base = ["#core.ingress", "#core.admissibility", "#context.hot_window", "#seed.activate", "#slot.forge", "#model.route", "#candidate.compose", "#why.route"]
    if profile != "low_memory_strict":
        base += ["#candidate.tournament", "#critic.style", "#critic.claim"]
    if app_kind == "code":
        base += ["#critic.schema", "#runtime_pack.validate"]
    return {"artifact_kind": "odin_qirc_capability_slice_channels", "protocol_version": "7.1", "profile": profile, "qirc_channels": base, "excluded_channels": ["#model.heavy"] if profile == "low_memory_strict" else []}
