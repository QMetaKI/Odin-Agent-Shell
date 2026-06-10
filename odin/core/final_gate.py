from __future__ import annotations
from odin.core.claim_boundary import blocked_claims


def final_gate(candidate: dict) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if candidate.get("artifact_kind") != "odin_candidate_artifact":
        reasons.append("candidate must use artifact_kind odin_candidate_artifact")
    if candidate.get("candidate_only") is not True:
        reasons.append("candidate_only must be true")
    if candidate.get("app_owned_apply") is not True:
        reasons.append("app_owned_apply must be true")
    if candidate.get("may_apply") is True:
        reasons.append("Odin candidates may not apply")
    blocked = blocked_claims(candidate.get("claims", []))
    if blocked:
        reasons.append("blocked claims: " + ", ".join(blocked))
    if candidate.get("external_send") is True:
        reasons.append("external_send is forbidden")
    return (not reasons), reasons
