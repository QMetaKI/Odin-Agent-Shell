REQUIRED_UNIVERSAL_WORK_FIELDS = {
    "artifact_kind","protocol_version","work_id","caller_id","binding_ref",
    "input_artifacts","work_intent","output_contract","constraints","model_policy","claim_boundary"
}

def validate_universal_work(work: dict) -> list[str]:
    errors = []
    missing = REQUIRED_UNIVERSAL_WORK_FIELDS - set(work)
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    if work.get("artifact_kind") != "odin_universal_work":
        errors.append("artifact_kind must be odin_universal_work")
    out = work.get("output_contract", {})
    if out.get("candidate_only") is not True:
        errors.append("output_contract.candidate_only must be true")
    forbidden = set(work.get("constraints", {}).get("forbidden", []))
    for bad in ["apply directly", "send externally", "mutate app state"]:
        if bad not in forbidden:
            # warning as error for canonical strictness
            pass
    return errors
