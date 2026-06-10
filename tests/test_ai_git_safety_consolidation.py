from odin.shadow_runtime.ai_git_safety_shadow import build_shadow_ai_git_safety
from odin.shadow_runtime.autonomy_escalation_gate_shadow import build_shadow_autonomy_escalation_gate
from odin.shadow_runtime.safety_superposition_shadow import build_shadow_safety_superposition
from odin.shadow_runtime.semantic_diff_branch_merge_shadow import build_shadow_semantic_diff_branch_merge
from odin.shadow_runtime.skynet_pattern_boundary_shadow import build_shadow_skynet_pattern_boundary
from odin.shadow_runtime.human_review_apply_boundary_shadow import build_shadow_human_review_apply_boundary


def test_ai_git_safety_allows_candidate():
    pkt = build_shadow_ai_git_safety({"work_id": "W1", "forbidden": []})
    assert pkt.decision == "allow_candidate"
    assert "candidate_only" in pkt.reasons


def test_autonomy_escalation_blocks_direct_apply():
    pkt = build_shadow_autonomy_escalation_gate({"work_id": "W2", "forbidden": ["direct_apply"]})
    assert pkt.decision == "block"
    assert "direct_apply" in pkt.blocked


def test_all_safety_shadow_modules_are_candidate_only():
    builders = [
        build_shadow_safety_superposition,
        build_shadow_semantic_diff_branch_merge,
        build_shadow_skynet_pattern_boundary,
        build_shadow_human_review_apply_boundary,
    ]
    for builder in builders:
        pkt = builder({"work_id": "W3", "forbidden": []})
        assert pkt.trace["authority"] == "odin_internal_candidate_only"
