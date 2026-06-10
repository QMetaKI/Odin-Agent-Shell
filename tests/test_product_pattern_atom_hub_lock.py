from pathlib import Path
import json

from odin.shadow_runtime.windows_product_runtime_shadow import run_windows_product_runtime_shadow
from odin.shadow_runtime.pattern_mine_intake_shadow import run_pattern_mine_intake_shadow
from odin.shadow_runtime.work_atom_runtime_shadow import run_work_atom_runtime_shadow
from odin.shadow_runtime.odin_hub_operational_center_shadow import run_odin_hub_operational_center_shadow

ROOT = Path(__file__).resolve().parents[1]


def test_windows_product_runtime_shadow_candidate():
    packet = json.loads((ROOT / "examples/windows/windows_product_runtime_manifest.valid.json").read_text())
    result = run_windows_product_runtime_shadow(packet)
    assert result["ok"] is True
    assert result["decision"] == "candidate"


def test_pattern_mine_executable_is_blocked():
    packet = json.loads((ROOT / "examples/pattern_mines/pattern_mine_executable.invalid.json").read_text())
    result = run_pattern_mine_intake_shadow(packet)
    assert result["ok"] is False
    assert result["decision"] == "block"


def test_work_atom_apply_is_blocked():
    packet = json.loads((ROOT / "examples/work_atoms/work_atom_apply.invalid.json").read_text())
    result = run_work_atom_runtime_shadow(packet)
    assert result["ok"] is False
    assert result["claim_boundary"] == "candidate_only_not_runtime"


def test_odin_hub_surface_is_operational_candidate():
    packet = json.loads((ROOT / "examples/odin_hub/odin_hub_surface.valid.json").read_text())
    result = run_odin_hub_operational_center_shadow(packet)
    assert result["ok"] is True
    assert result["candidate_type"] == "odin_hub_candidate"


def test_new_registries_present():
    for name in ["windows_process_registry.json", "pattern_mine_type_registry.json", "work_atom_type_registry.json", "odin_hub_panel_registry.json"]:
        data = json.loads((ROOT / "registries" / name).read_text())
        assert data["registry_id"]
        assert data["version"] == "0.7.4"
