from __future__ import annotations

def select_maria_michael_profile(intent_family: str = "general", risk: str = "normal") -> dict:
    if intent_family in {"code", "validator", "runtime_pack", "claim_boundary"}:
        profile = ("papa_qstar_refined_20_80", 20, 80)
    elif risk in {"incident", "debug", "conflict"}:
        profile = ("contingency_michael_35_65", 35, 65)
    elif intent_family in {"story", "intake", "fairy"}:
        profile = ("ritual_story_maria_85_15", 85, 15)
    else:
        profile = ("mama_qooo_refined_80_20", 80, 20)
    return {"artifact_kind":"odin_maria_michael_profile","protocol_version":"7.1","profile_id":profile[0],"maria":profile[1],"michael":profile[2],"collapse_rule":"preserve_center_then_cut_invalid_paths"}
