from __future__ import annotations

FORBIDDEN_WORK_ACTIONS = {
    "direct_apply", "apply_directly", "mutate_app_state", "external_send",
    "network_send", "grant_permission", "issue_receipt", "claim_runtime_verified",
    "claim_model_inference_verified", "claim_production_ready",
}

FORBIDDEN_OUTPUT_CLAIMS = {
    "runtime_verified", "host_validated", "model_inference_verified",
    "network_verified", "security_verified", "production_ready",
    "deploy_verified", "patch_applied", "full_implementation_complete",
}

REQUIRED_CANDIDATE_MARKERS = {
    "candidate_only": True,
    "app_owned_apply": True,
}

def scan_forbidden_markers(value: object) -> list[str]:
    text = str(value).lower()
    hits = []
    for marker in sorted(FORBIDDEN_WORK_ACTIONS | FORBIDDEN_OUTPUT_CLAIMS):
        if marker.replace('_', ' ') in text or marker in text:
            hits.append(marker)
    return hits

def enforce_candidate_output(output_contract: dict) -> list[str]:
    errors: list[str] = []
    if output_contract.get("candidate_only") is not True:
        errors.append("output_contract.candidate_only must be true")
    if output_contract.get("app_owned_apply", True) is not True:
        errors.append("output_contract.app_owned_apply must remain true")
    if output_contract.get("may_apply") is True:
        errors.append("output_contract.may_apply is forbidden for Odin")
    return errors
