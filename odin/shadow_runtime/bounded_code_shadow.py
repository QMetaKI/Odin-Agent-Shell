from __future__ import annotations

from typing import Any, Dict


def build_shadow_bounded_code_plan(work: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "artifact_kind": "odin_shadow_bounded_code_plan",
        "protocol_version": "7.1-shadow",
        "work_id": work.get("work_id"),
        "allowed_outputs": ["patchplan_candidate", "review_candidate", "debug_hypothesis_candidate", "test_plan_candidate"],
        "forbidden_claims": ["patch_applied", "tests_passed", "runtime_verified", "security_verified", "production_ready"],
        "required_steps": ["repo_context_digest", "scope_boundary", "patchplan_candidate", "verification_plan_candidate"],
        "boundary": "bounded_code_candidate_only_no_file_mutation",
    }
