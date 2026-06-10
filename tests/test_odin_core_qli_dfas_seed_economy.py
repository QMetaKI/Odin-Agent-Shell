from __future__ import annotations
import json
from pathlib import Path
from odin.shadow_runtime.qli_master_interface_shadow import run_qli_master_shadow
from odin.shadow_runtime.maria_michael_superposition_shadow import select_maria_michael_profile

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT / "examples" / "shadow_runtime" / name).read_text(encoding="utf-8"))

def test_qli_master_shadow_valid_flow_has_center_seed_route_and_why_trace():
    work = load("odin_core_qli_flow.valid.json")
    result = run_qli_master_shadow(work)
    assert result["ok"] is True
    assert result["centerline_packet"]["final_gate_required"] is True
    assert result["centerline_packet"]["candidate_only"] is True
    assert result["admissibility"]["decision"] == "continue"
    assert result["seed_packet"]["active_seeds"]
    assert "boundary_guard" in result["archetype_role_packet"]["active_roles"]
    assert result["route_score"]["selected_route"] == "3b_7b_8b_hybrid"
    assert result["why_trace"]["selected_route"] == "3b_7b_8b_hybrid"
    assert result["ring_activation_map"]["rings"]


def test_qli_master_shadow_blocks_non_candidate_contract():
    work = load("odin_core_policy_block.invalid.json")
    result = run_qli_master_shadow(work)
    assert result["ok"] is False
    assert result["admissibility"]["decision"] == "block"
    assert "output_contract_not_candidate_only" in result["admissibility"]["reasons"]


def test_maria_michael_profiles_are_operational_not_persona():
    default = select_maria_michael_profile("general")
    code = select_maria_michael_profile("code")
    risk = select_maria_michael_profile("general", risk="debug")
    assert default["maria"] == 80 and default["michael"] == 20
    assert code["maria"] == 20 and code["michael"] == 80
    assert risk["profile_id"] == "contingency_michael_35_65"


def test_pr38_to_pr44_and_real_pr14_registered():
    tasks = json.loads((ROOT / "registries" / "codex_task_registry.json").read_text(encoding="utf-8"))["tasks"]
    task_ids = {t["id"] for t in tasks}
    for tid in [f"PR-{i:02d}" for i in range(38,45)]:
        assert tid in task_ids
    bundles = json.loads((ROOT / "registries" / "codex_pr_bundle_registry.json").read_text(encoding="utf-8"))["bundles"]
    real14 = next(b for b in bundles if b["id"] == "REAL-PR-14")
    for tid in [f"PR-{i:02d}" for i in range(38,45)]:
        assert tid in real14["internal_tasks"]


def test_new_registries_exist_and_have_entries():
    for rel in ["seed_registry.json","archetype_role_registry.json","resonance_band_registry.json","centerline_gate_registry.json","qmath_score_registry.json","maria_michael_profile_registry.json","qfoundation_system_palette_registry.json"]:
        data = json.loads((ROOT / "registries" / rel).read_text(encoding="utf-8"))
        assert data["registry_id"]
        assert data["version"] == "7.1"
