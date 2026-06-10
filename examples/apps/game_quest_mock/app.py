from odin.runtime.engine import OdinRuntime
from odin_app_sdk import build_app_manifest, build_universal_work

PATTERN_MINE = {
    "artifact_kind": "odin_pattern_mine",
    "mine_id": "quest_pattern_mine",
    "patterns": [{"id": "return_with_cost", "label": "Return with cost", "tags": ["game", "quest"], "operators": ["choice", "consequence"]}],
    "flow_packs": [{"id": "quest_loop", "stages": ["hook", "choice", "cost", "return"], "tags": ["game"]}],
}

def run_demo() -> dict:
    manifest = build_app_manifest("game.quest.mock", "Game Quest Mock")
    work = build_universal_work("game.quest.mock", "Create a candidate quest beat", tags=["game", "quest"])
    return OdinRuntime().run_universal_work(work, caller_manifest=manifest, pattern_mine=PATTERN_MINE)
