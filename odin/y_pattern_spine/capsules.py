"""Y Work Capsule — compact context capsule for local worker efficiency.

Claim boundary: work_capsule_is_context_not_authority
candidate_only: true
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

CLAIM_BOUNDARY = "work_capsule_is_context_not_authority"


@dataclass
class YWorkCapsule:
    capsule_id: str
    task_intent: str
    allowed_files: List[str]
    forbidden_files: List[str]
    required_evidence: List[str]
    expected_outputs: List[str]
    validators: List[str]
    proof_commands: List[str]
    token_budget: str
    claim_boundary: str = CLAIM_BOUNDARY
    compile_near_hint: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "capsule_id": self.capsule_id,
            "task_intent": self.task_intent,
            "allowed_files": self.allowed_files,
            "forbidden_files": self.forbidden_files,
            "required_evidence": self.required_evidence,
            "expected_outputs": self.expected_outputs,
            "validators": self.validators,
            "proof_commands": self.proof_commands,
            "token_budget": self.token_budget,
            "compile_near_hint": self.compile_near_hint,
            "claim_boundary": self.claim_boundary,
        }


DEMO_WORK_CAPSULE = YWorkCapsule(
    capsule_id="demo_universal_work_capsule",
    task_intent="Demonstrate Y Pattern Spine route hint and work capsule preparation",
    allowed_files=[
        "odin/local_hub/demo_universal_work.py",
        "odin/local_hub/ui.py",
        "odin/y_pattern_spine/profiles.py",
    ],
    forbidden_files=[
        "provider runtime files",
        "external app runtime files",
    ],
    required_evidence=[
        "repo_route_identified",
        "pattern_selected",
    ],
    expected_outputs=[
        "response packet",
        "proof packet",
    ],
    validators=[
        "validate-y-pattern-spine",
        "validate-all",
    ],
    proof_commands=[
        "python -m odin.cli prove-y-pattern-spine",
        "python -m odin.cli validate-y-pattern-spine",
    ],
    token_budget="minimal",
    compile_near_hint="y_shadow_candidate_graph",
)


def build_work_capsule_demo() -> YWorkCapsule:
    return DEMO_WORK_CAPSULE
