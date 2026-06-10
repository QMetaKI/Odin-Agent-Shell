from pathlib import Path
import json

from odin.shadow_runtime.shadow_narrative_shadow import run_shadow_narrative_shadow
from odin.shadow_runtime.loki_mediation_shadow import run_loki_mediation_shadow
from odin.shadow_runtime.shadow_narrative_to_gate_shadow import run_shadow_narrative_to_gate_shadow

ROOT = Path(__file__).resolve().parents[1]


def test_shadow_narrative_valid_fixture_maps_to_candidate():
    fixture = json.loads((ROOT / "examples/shadow_narrative/shadow_narrative_helpful_tyrant.valid.json").read_text())
    result = run_shadow_narrative_shadow(fixture)
    assert result["ok"] is True
    assert result["decision"] == "candidate"


def test_loki_cannot_grant_authority():
    fixture = json.loads((ROOT / "examples/shadow_narrative/loki_authority_escalation.invalid.json").read_text())
    result = run_loki_mediation_shadow(fixture)
    assert result["ok"] is False
    assert result["decision"] == "block"


def test_shadow_to_gate_is_candidate_only():
    result = run_shadow_narrative_to_gate_shadow({"anti_pattern_id": "seed_hydra"})
    assert result["claim_boundary"] == "candidate_only_not_runtime"


def test_shadow_narrative_registries_exist():
    for name in ["shadow_narrative_registry.json", "anti_fairy_pattern_registry.json", "loki_mediation_registry.json", "shadow_to_gate_registry.json"]:
        data = json.loads((ROOT / "registries" / name).read_text())
        assert data["registry_id"]
        assert data["version"] == "0.7.0"
