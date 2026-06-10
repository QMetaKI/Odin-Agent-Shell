import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_semantic_bus_channels_cover_core_families():
    channels = {c["name"] for c in load("registries/semantic_bus_channels.json")["channels"]}
    for ch in ["#work.received", "#context.distill", "#slot.forge", "#critic.claim", "#candidate.compose", "#response.packet"]:
        assert ch in channels


def test_model_ladder_has_default_and_escalations():
    ladder = load("registries/model_scale_ladder.json")
    assert ladder["default"] == "3b_7b_8b_hybrid"
    levels = set(ladder["levels"])
    assert "3b_7b_8b_hybrid" in levels
    assert "3b_13b_14b_quality_hybrid" in levels
    assert "70b_class_batch" in levels
    assert "remote_optional_explicit" in levels
