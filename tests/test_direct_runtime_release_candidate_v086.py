import json
from pathlib import Path
from odin.runtime.config import OdinRuntimeConfig, load_runtime_config
from odin.runtime.store import RuntimeStore
from odin.runtime.session import WorkSession
from odin.runtime.engine import run_universal_work_file
from odin.models.providers.registry import list_provider_cards, get_provider
from odin.hub.static_hub import write_static_hub
from odin.recovery.safe_mode import build_safe_mode_plan
from odin_app_sdk import build_app_manifest, build_universal_work

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_config_and_store(tmp_path):
    cfg = OdinRuntimeConfig(runtime_dir=str(tmp_path / "rt"))
    assert cfg.to_dict()["app_apply_owned"] is True
    store = RuntimeStore(tmp_path / "rt")
    path = store.write_session({"response_id": "R1", "candidates": [{"candidate_id": "C1"}]})
    assert path.exists()
    assert store.status()["session_count"] == 1
    assert store.status()["candidate_count"] == 1


def test_work_session_state_machine():
    session = WorkSession("WORK1", "APP1")
    session.mark("bound", "ok")
    session.mark("emitted", "done")
    doc = session.to_dict()
    assert doc["state"] == "emitted"
    assert len(doc["transitions"]) >= 3


def test_app_sdk_builds_valid_work():
    manifest = build_app_manifest("sdk.demo", "SDK Demo")
    work = build_universal_work("sdk.demo", "Make a candidate", tags=["sdk"])
    assert manifest["apply_boundary"]["app_owned"] is True
    assert work["artifact_kind"] == "odin_universal_work"
    assert work["output_contract"]["candidate_only"] is True


def test_golden_flow_runtime_response_contains_session_and_store_boundary():
    result = run_universal_work_file(
        ROOT / "examples/runtime/universal_work_full.valid.json",
        seed_pack_path=ROOT / "examples/runtime/app_seed_pack_full.valid.json",
        pattern_mine_path=ROOT / "examples/runtime/pattern_mine_full.valid.json",
        caller_manifest_path=ROOT / "examples/runtime/app_caller_manifest.valid.json",
    )
    assert result["runtime_status"] == "candidate_generated"
    assert result["work_session"]["state"] == "emitted"
    assert result["qirc_digest"]["event_count"] >= 8
    assert result["runtime_config"]["runtime_candidate_version"] == "0.8.6"


def test_provider_cards_are_candidate_only():
    cards = list_provider_cards()
    ids = {c["provider_id"] for c in cards}
    assert "mock_provider" in ids
    assert "ollama_provider_stub" in ids
    for card in cards:
        assert card["allowed_role"] == "candidate_worker"
        assert "apply_executor" in card["forbidden_roles"]
    result = get_provider("mock").generate("hello", route="3b_7b_8b_hybrid").to_dict()
    assert result["candidate_only"] is True
    assert result["model_inference_verified"] is False


def test_static_hub_and_safe_mode(tmp_path):
    hub_path = write_static_hub(tmp_path / "hub" / "index.html")
    assert hub_path.exists()
    text = hub_path.read_text(encoding="utf-8")
    assert "Odin Hub" in text
    plan = build_safe_mode_plan("test")
    assert "disable_remote_workers" in plan["actions"]
    assert plan["claim_boundary"].startswith("safe_mode_plan")


def test_direct_runtime_release_candidate_registry_paths_exist():
    registry = json.loads((ROOT / "registries/direct_runtime_release_candidate_registry.json").read_text(encoding="utf-8"))
    assert registry["version"] == "0.8.6"
    assert "no_app_apply_by_odin" in registry["proof_boundaries"]
    for module in registry["modules"]:
        assert module["candidate_only"] is True
        for rel in module["paths"]:
            assert (ROOT / rel).exists(), rel
