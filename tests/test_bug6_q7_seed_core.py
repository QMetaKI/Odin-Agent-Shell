import json
from pathlib import Path
from odin import cli
from odin.shadow_runtime.bug6_q7_invariant_shadow import check_bug6_q7_invariants
from odin.shadow_runtime.y_core_posture_shadow import select_y_core_posture
from odin.shadow_runtime.operational_seed_substrate_shadow import activate_operational_seeds
from odin.shadow_runtime.seed_archetype_synthesis_shadow import synthesize_seed_archetype_roles
from odin.shadow_runtime.fairy_ystar_seed_binding_shadow import bind_fairy_node_to_seeds
from odin.shadow_runtime.shadow_runtime_seed_binding_shadow import build_shadow_seed_binding
ROOT = Path(__file__).resolve().parents[1]
def test_bug6_q7_seed_core_validation_clean():
    assert cli.validate_bug6_q7_seed_core() == []
def test_bug6_q7_valid_and_blocking_flows():
    good = json.loads((ROOT / "examples/shadow_runtime/bug6_q7_seed_core_flow.valid.json").read_text())
    assert check_bug6_q7_invariants(good)["decision"] == "allow"
    bad = json.loads((ROOT / "examples/shadow_runtime/bug6_q7_seed_core_block.invalid.json").read_text())
    assert check_bug6_q7_invariants(bad)["decision"] == "block"
def test_y_core_seed_archetype_fairy_and_shadow_binding():
    posture = select_y_core_posture()
    assert posture["authority_scope"] == "odin_llm_work_only"
    seeds = activate_operational_seeds(["context_clarity", "fairy_ystar_seed_binding"], budget=8)
    assert "children_family_first" in seeds["active_seeds"]
    synth = synthesize_seed_archetype_roles(seeds["active_seeds"])
    assert "boundary_guard" in synth["active_roles"]
    binding = bind_fairy_node_to_seeds("the_gatekeeper_checks_the_keys", "boundary.validate_binding", seeds["active_seeds"])
    assert binding["ok"] is True
    shadow = build_shadow_seed_binding("binding_gate", seeds["active_seeds"], synth["active_roles"])
    assert shadow["bug6_status"] == "preserved"
def test_pr50_to_pr55_and_real_pr16_registered():
    tasks = json.loads((ROOT / "registries/codex_task_registry.json").read_text())["tasks"]
    task_ids = {task["id"] for task in tasks}
    for tid in ["PR-50", "PR-51", "PR-52", "PR-53", "PR-54", "PR-55"]:
        assert tid in task_ids
    bundles = json.loads((ROOT / "registries/codex_pr_bundle_registry.json").read_text())["bundles"]
    assert any(bundle["id"] == "REAL-PR-16" and "PR-55" in bundle["internal_tasks"] for bundle in bundles)
