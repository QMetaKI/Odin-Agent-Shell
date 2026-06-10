from odin.shadow_runtime.pre_llm_intelligence_shadow import build_pre_llm_intelligence_shadow
from odin.shadow_runtime.model_work_avoidance_shadow import build_model_work_avoidance_shadow
from odin.shadow_runtime.output_intelligence_composer_shadow import build_output_intelligence_composer_shadow
from odin.shadow_runtime.perceived_intelligence_metrics_shadow import build_perceived_intelligence_metrics_shadow
from odin.shadow_runtime.micro_to_macro_synthesis_shadow import build_micro_to_macro_synthesis_shadow


def test_pre_llm_shadow_allows_candidate_only_flow():
    pkt = build_pre_llm_intelligence_shadow({"work_id": "W065", "forbidden": []})
    assert pkt["ok"] is True
    assert pkt["candidate_only"] is True
    assert "model_work_avoidance" in pkt["steps"]


def test_model_work_avoidance_blocks_direct_apply():
    pkt = build_model_work_avoidance_shadow({"work_id": "W065B", "forbidden": ["direct_apply"]})
    assert pkt["ok"] is False
    assert pkt["decision"] == "block"


def test_output_composition_and_metrics_are_candidate_only():
    for builder in [build_output_intelligence_composer_shadow, build_perceived_intelligence_metrics_shadow, build_micro_to_macro_synthesis_shadow]:
        pkt = builder({"work_id": "W065C", "forbidden": []})
        assert pkt["authority"] == "odin_internal_candidate_only"
        assert pkt["trace"]["app_apply"] == "app_owned"
