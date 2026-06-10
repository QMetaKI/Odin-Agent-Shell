from __future__ import annotations

REPAIR_HINTS = {
    "caller_manifest missing fields": "Add caller_id, app_name, protocol_version, permissions and apply_boundary.",
    "apply_boundary.app_owned must be true": "Keep apply in the calling app; Odin may only return candidates.",
    "seed pack must contain": "Provide at least one seed or seed_unit, or omit the seed pack.",
    "pattern mine must contain": "Provide patterns or flow_packs, or omit the pattern mine.",
    "direct_apply": "Remove direct_apply and return an app-owned candidate action instead.",
}

def build_repair_suggestions(errors: list[str] | str) -> list[dict]:
    if isinstance(errors, str):
        errors = [errors]
    suggestions = []
    for err in errors:
        matched = None
        for needle, hint in REPAIR_HINTS.items():
            if needle in err:
                matched = hint
                break
        suggestions.append({
            "error": err,
            "suggestion": matched or "Review the relevant schema, registry and claim boundary before retrying.",
            "candidate_only": True,
        })
    return suggestions
