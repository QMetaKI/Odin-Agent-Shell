"""LRH-PR-17: Full Acceptance, E2E Golden Flows and User Start Proof — deterministic tests.

Claim boundary: lrh_pr_17_test_full_acceptance_local_only_no_network_no_live_model_no_app_apply

All tests are deterministic, local-only, no target-host assumption, no public network,
no live model requirement, no app-specific integration.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# 9.1 Required file existence
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rel", [
    "docs/rebaseline/ROAD_TO_100_ACCEPTANCE_HARNESS_V1.md",
    "registries/road_to_100_acceptance_harness_v1.json",
    "docs/FULL_ACCEPTANCE_E2E_GOLDEN_FLOWS_V1.md",
    "tests/test_lrh_pr_17_full_acceptance.py",
    "examples/full_acceptance/final_acceptance_report.example.json",
    "examples/full_acceptance/remaining_proof_gaps.example.json",
    "examples/full_acceptance/e2e_golden_flow_receipt.example.json",
    "examples/full_acceptance/support_bundle_receipt.example.json",
])
def test_required_file_exists(rel: str) -> None:
    assert (ROOT / rel).exists(), f"required file missing: {rel}"


# ---------------------------------------------------------------------------
# 9.2 Ladder source tests
# ---------------------------------------------------------------------------

def _load_ladder() -> dict:
    path = ROOT / "registries" / "local_runtime_hub_build_ladder_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_lrh_pr_17_exists_in_ladder() -> None:
    ladder = _load_ladder()
    ids = [entry["id"] for entry in ladder.get("ladder", [])]
    assert "LRH-PR-17" in ids, "LRH-PR-17 must be present in the ladder"


def test_lrh_pr_17_title() -> None:
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-17")
    assert entry["title"] == "Full Acceptance, E2E Golden Flows and User Start Proof"


def test_lrh_pr_17_depends_on_all_prior() -> None:
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-17")
    depends_on = entry.get("depends_on", [])
    for i in range(1, 17):
        pr_id = f"LRH-PR-{i:02d}"
        assert pr_id in depends_on, f"LRH-PR-17 must depend on {pr_id}"


def test_lrh_pr_17_target_files() -> None:
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-17")
    target_files = entry.get("target_files", [])
    for required in [
        "docs/rebaseline/ROAD_TO_100_ACCEPTANCE_HARNESS_V1.md",
        "registries/road_to_100_acceptance_harness_v1.json",
        "tests/test_lrh_pr_17_full_acceptance.py",
        "docs/FULL_ACCEPTANCE_E2E_GOLDEN_FLOWS_V1.md",
    ]:
        assert required in target_files, f"LRH-PR-17 target_files must include {required!r}"


def test_lrh_pr_17_forbidden_scope() -> None:
    ladder = _load_ladder()
    entry = next(e for e in ladder["ladder"] if e["id"] == "LRH-PR-17")
    forbidden = entry.get("forbidden_scope", [])
    assert any("production readiness" in f for f in forbidden), \
        "forbidden scope must include 'no production readiness claim'"
    assert any("release certification" in f for f in forbidden), \
        "forbidden scope must include 'no release certification claim'"
    assert any("live model" in f for f in forbidden), \
        "forbidden scope must include 'no live model quality claim'"
    assert any("external app" in f.lower() for f in forbidden), \
        "forbidden scope must include 'no external app-specific integration claim'"
    assert any("public network" in f for f in forbidden), \
        "forbidden scope must include 'no public network API proof claim'"


# ---------------------------------------------------------------------------
# 9.3 Acceptance harness registry tests
# ---------------------------------------------------------------------------

def _load_harness_registry() -> dict:
    path = ROOT / "registries" / "road_to_100_acceptance_harness_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_harness_registry_is_valid_json() -> None:
    path = ROOT / "registries" / "road_to_100_acceptance_harness_v1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_harness_registry_artifact_kind() -> None:
    reg = _load_harness_registry()
    assert reg.get("artifact_kind") == "odin_road_to_100_acceptance_harness"


def test_harness_registry_claim_boundary_present() -> None:
    reg = _load_harness_registry()
    assert reg.get("claim_boundary"), "claim_boundary must be present and non-empty"


def test_harness_registry_command_matrix_present() -> None:
    reg = _load_harness_registry()
    matrix = reg.get("command_matrix", [])
    assert len(matrix) > 0, "command_matrix must be non-empty"


def test_harness_registry_command_entries_shape() -> None:
    reg = _load_harness_registry()
    for cmd in reg.get("command_matrix", []):
        for key in ("command", "status", "proof_boundary", "known_non_proof"):
            assert key in cmd, f"command entry missing {key!r}: {cmd.get('command', '?')}"


def test_harness_registry_missing_commands_not_checked_locally() -> None:
    reg = _load_harness_registry()
    for cmd in reg.get("command_matrix", []):
        if cmd.get("status") == "missing_command":
            assert cmd.get("checked_locally") is not True, \
                f"missing_command must not have checked_locally=true: {cmd.get('command')}"


def test_harness_registry_known_non_proofs_retained() -> None:
    reg = _load_harness_registry()
    known_nps = reg.get("known_non_proofs", [])
    required = [
        "production_readiness",
        "release_certification",
        "security_certification",
        "signed_distribution",
        "windows_service_tray_installer",
        "target_host_validation",
        "public_network_api",
        "specific_external_app_integration",
        "live_model_inference",
        "model_quality",
        "app_apply_authority",
        "app_state_mutation",
        "external_send_authority",
        "agent_proof_boundary_closure",
        "thor_hermetic_ci_artifact",
    ]
    for np in required:
        assert np in known_nps, f"known_non_proofs must include {np!r}"


def test_harness_registry_remaining_gaps_non_empty() -> None:
    reg = _load_harness_registry()
    gaps = reg.get("remaining_proof_gaps", [])
    assert len(gaps) > 0, "remaining_proof_gaps must be non-empty"


def test_harness_registry_proof_boundaries_present() -> None:
    reg = _load_harness_registry()
    boundaries = reg.get("proof_boundaries", [])
    required = [
        "not_production_readiness_certification",
        "not_release_certification",
        "not_security_certification",
        "not_signed_distribution_proof",
        "not_windows_service_tray_installer_proof",
        "not_target_host_proof",
        "not_public_network_api_proof",
        "not_specific_external_app_integration_proof",
        "not_live_model_inference_proof",
        "not_model_quality_proof",
        "not_app_apply_proof",
        "not_app_state_mutation_proof",
        "not_external_send_authority_proof",
        "candidate_artifact_not_applied_truth",
        "host_app_owns_apply_state_external_send",
    ]
    for b in required:
        assert b in boundaries, f"proof_boundaries must include {b!r}"


# ---------------------------------------------------------------------------
# 9.4 Proof command registration tests
# ---------------------------------------------------------------------------

def test_validate_full_acceptance_cli() -> None:
    from odin.hub.shell import validate_full_acceptance
    errors = validate_full_acceptance()
    assert errors == [], f"validate_full_acceptance returned errors: {errors}"


def test_prove_full_acceptance_cli() -> None:
    from odin.hub.shell import build_full_acceptance_proof_packet
    packet = build_full_acceptance_proof_packet()
    assert packet.get("status") in {"ok", "ok_with_known_gaps"}, \
        f"prove-full-acceptance status must be ok or ok_with_known_gaps, got {packet.get('status')}"
    assert packet.get("candidate_only") is True
    assert packet.get("local_only") is True
    assert packet.get("full_acceptance_local_receipt") is True
    assert "commands_checked" in packet
    assert "commands_green_locally" in packet
    assert "commands_missing" in packet
    assert "remaining_proof_gaps" in packet
    assert "not_proven" in packet
    assert "proof_boundaries" in packet
    # Must NOT claim production readiness
    forbidden_status = {"complete", "certified", "production_ready", "release_ready", "fully_proven", "guaranteed"}
    assert packet["status"] not in forbidden_status, \
        f"prove-full-acceptance must not use forbidden status: {packet['status']}"


def test_prove_full_acceptance_not_proven_entries() -> None:
    from odin.hub.shell import build_full_acceptance_proof_packet
    packet = build_full_acceptance_proof_packet()
    not_proven = packet.get("not_proven", [])
    required = [
        "production_readiness",
        "release_certification",
        "security_certification",
        "signed_distribution",
        "windows_service_tray_installer",
        "target_host_validation",
        "public_network_api",
        "specific_external_app_integration",
        "live_model_inference",
        "model_quality",
        "app_apply_authority",
        "app_state_mutation",
        "external_send_authority",
        "agent_proof_boundary_closure",
        "thor_hermetic_ci_artifact",
    ]
    for np in required:
        assert np in not_proven, f"not_proven must include {np!r}"


def test_prove_full_acceptance_proof_boundaries() -> None:
    from odin.hub.shell import build_full_acceptance_proof_packet
    packet = build_full_acceptance_proof_packet()
    boundaries = packet.get("proof_boundaries", [])
    required = [
        "not_production_readiness_certification",
        "not_release_certification",
        "not_security_certification",
        "not_signed_distribution_proof",
        "not_windows_service_tray_installer_proof",
        "not_target_host_proof",
        "not_public_network_api_proof",
        "not_specific_external_app_integration_proof",
        "not_live_model_inference_proof",
        "not_model_quality_proof",
        "not_app_apply_proof",
        "not_app_state_mutation_proof",
        "not_external_send_authority_proof",
        "candidate_artifact_not_applied_truth",
        "host_app_owns_apply_state_external_send",
    ]
    for b in required:
        assert b in boundaries, f"proof_boundaries must include {b!r}"


# ---------------------------------------------------------------------------
# 9.5 Prior proof command gap tests
# ---------------------------------------------------------------------------

def test_prove_agent_operator_mode_listed_as_missing() -> None:
    # LRH-PR-17: was missing_command. LRH-PR-18: implemented_now.
    reg = _load_harness_registry()
    match = next(
        (c for c in reg["command_matrix"] if "prove-agent-operator-mode" in c["command"]),
        None,
    )
    assert match is not None, "prove-agent-operator-mode must be in command_matrix"
    assert match.get("status") in {"missing_command", "implemented_now"}, \
        f"prove-agent-operator-mode status must be missing_command or implemented_now, got {match.get('status')}"


def test_prove_external_app_bridge_listed_as_missing() -> None:
    # LRH-PR-17: was missing_command. LRH-PR-18: implemented_now (generic neutral).
    reg = _load_harness_registry()
    match = next(
        (c for c in reg["command_matrix"] if "prove-external-app-bridge" in c["command"]),
        None,
    )
    assert match is not None, "prove-external-app-bridge must be in command_matrix"
    assert match.get("status") in {"missing_command", "implemented_now"}, \
        f"prove-external-app-bridge status must be missing_command or implemented_now, got {match.get('status')}"


@pytest.mark.parametrize("cmd_substr", [
    "prove-local-runtime",
    "prove-sdk-bridge",
    "prove-browser-hub",
    "prove-portable-package",
    "prove-windows-convenience-layer",
    "emit-support-bundle",
    "run-golden-flow",
])
def test_implemented_proof_commands_in_matrix(cmd_substr: str) -> None:
    reg = _load_harness_registry()
    match = next(
        (c for c in reg["command_matrix"] if cmd_substr in c["command"]),
        None,
    )
    assert match is not None, f"{cmd_substr} must be in command_matrix"
    assert match.get("status") == "implemented_now", \
        f"{cmd_substr} must have status=implemented_now"


def test_missing_commands_in_remaining_gaps() -> None:
    # LRH-PR-17: commands were missing, so they appeared in remaining_proof_gaps.
    # LRH-PR-18: commands are implemented_now; remaining_proof_gaps updated accordingly.
    # Test now verifies remaining_proof_gaps is non-empty (some gaps always remain).
    reg = _load_harness_registry()
    gaps = reg.get("remaining_proof_gaps", [])
    assert len(gaps) > 0, "remaining_proof_gaps must be non-empty (some gaps always remain)"


# ---------------------------------------------------------------------------
# 9.6 Boundary phrase tests
# ---------------------------------------------------------------------------

def _harness_doc_text() -> str:
    return (ROOT / "docs" / "rebaseline" / "ROAD_TO_100_ACCEPTANCE_HARNESS_V1.md").read_text(
        encoding="utf-8", errors="ignore"
    ).lower()


def _golden_doc_text() -> str:
    return (ROOT / "docs" / "FULL_ACCEPTANCE_E2E_GOLDEN_FLOWS_V1.md").read_text(
        encoding="utf-8", errors="ignore"
    ).lower()


@pytest.mark.parametrize("phrase", [
    "full acceptance local receipt",
    "e2e golden flow",
    "candidate-only",
    "local-only",
    "app-owned apply",
    "not production readiness",
    "not release certification",
    "not security certification",
    "not signed distribution proof",
    "not windows service/tray/installer proof",
    "not target-host proof",
    "not public network api proof",
    "not live model inference proof",
    "not model quality proof",
    "not specific external app integration proof",
    "remaining proof gaps are retained",
])
def test_harness_doc_required_phrases(phrase: str) -> None:
    text = _harness_doc_text()
    assert phrase in text, \
        f"ROAD_TO_100_ACCEPTANCE_HARNESS_V1.md must contain phrase: {phrase!r}"


@pytest.mark.parametrize("phrase", [
    "full acceptance local receipt",
    "e2e golden flow",
    "candidate-only",
    "local-only",
    "app-owned apply",
    "not production readiness",
    "not release certification",
    "not security certification",
    "not signed distribution proof",
    "not windows service/tray/installer proof",
    "not target-host proof",
    "not public network api proof",
    "not live model inference proof",
    "not model quality proof",
    "not specific external app integration proof",
    "remaining proof gaps are retained",
])
def test_golden_doc_required_phrases(phrase: str) -> None:
    text = _golden_doc_text()
    assert phrase in text, \
        f"FULL_ACCEPTANCE_E2E_GOLDEN_FLOWS_V1.md must contain phrase: {phrase!r}"


def test_prove_full_acceptance_remaining_gaps_non_empty() -> None:
    from odin.hub.shell import build_full_acceptance_proof_packet
    packet = build_full_acceptance_proof_packet()
    gaps = packet.get("remaining_proof_gaps", [])
    assert len(gaps) > 0, "remaining_proof_gaps must be non-empty in proof packet"


# ---------------------------------------------------------------------------
# 9.7 Public naming neutrality tests
# ---------------------------------------------------------------------------

_PUBLIC_NAMING_FORBIDDEN = [
    "wordpress",
    "obsidian",
    "notion",
    "vscode",
    "cursor",
    "jetbrains",
    "microsoft store",
    "apple store",
    "github copilot",
]

@pytest.mark.parametrize("rel", [
    "docs/FULL_ACCEPTANCE_E2E_GOLDEN_FLOWS_V1.md",
    "docs/rebaseline/ROAD_TO_100_ACCEPTANCE_HARNESS_V1.md",
    "registries/road_to_100_acceptance_harness_v1.json",
    "examples/full_acceptance/final_acceptance_report.example.json",
    "examples/full_acceptance/remaining_proof_gaps.example.json",
    "examples/full_acceptance/e2e_golden_flow_receipt.example.json",
    "examples/full_acceptance/support_bundle_receipt.example.json",
])
@pytest.mark.parametrize("forbidden_name", _PUBLIC_NAMING_FORBIDDEN)
def test_public_naming_neutrality(rel: str, forbidden_name: str) -> None:
    p = ROOT / rel
    if not p.exists():
        pytest.skip(f"{rel} does not exist")
    text_lower = p.read_text(encoding="utf-8", errors="ignore").lower()
    assert forbidden_name not in text_lower, \
        f"{rel}: public naming violation — found {forbidden_name!r}"


# ---------------------------------------------------------------------------
# 9.8 Claim scanner / overclaim tests
# ---------------------------------------------------------------------------

_FA_FORBIDDEN_DOC_CLAIMS = [
    "guaranteed secure",
    "windows service proven",
    "tray proven",
    "installer proven",
    "live model quality proven",
]

@pytest.mark.parametrize("rel", [
    "docs/FULL_ACCEPTANCE_E2E_GOLDEN_FLOWS_V1.md",
    "docs/rebaseline/ROAD_TO_100_ACCEPTANCE_HARNESS_V1.md",
])
@pytest.mark.parametrize("forbidden_claim", _FA_FORBIDDEN_DOC_CLAIMS)
def test_no_overclaim_in_docs(rel: str, forbidden_claim: str) -> None:
    p = ROOT / rel
    if not p.exists():
        pytest.skip(f"{rel} does not exist")
    text_lower = p.read_text(encoding="utf-8", errors="ignore").lower()
    assert forbidden_claim not in text_lower, \
        f"{rel}: forbidden overclaim phrase found: {forbidden_claim!r}"


# ---------------------------------------------------------------------------
# 9.9 Validate-all integration
# ---------------------------------------------------------------------------

def test_validate_full_acceptance_integrated_in_validate_all() -> None:
    import inspect
    from odin import cli
    source = inspect.getsource(cli.validate_all)
    assert "validate_full_acceptance" in source, \
        "validate_full_acceptance must be called in validate_all()"


# ---------------------------------------------------------------------------
# Example fixture shape tests
# ---------------------------------------------------------------------------

def test_final_acceptance_report_example_shape() -> None:
    p = ROOT / "examples" / "full_acceptance" / "final_acceptance_report.example.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("artifact_kind") == "odin_full_acceptance_proof_packet"
    assert data.get("candidate_only") is True
    assert data.get("local_only") is True
    assert data.get("full_acceptance_local_receipt") is True
    assert data.get("status") == "ok_with_known_gaps"
    assert "not_proven" in data
    assert "proof_boundaries" in data
    assert "remaining_proof_gaps" in data
    assert len(data.get("not_proven", [])) > 0
    assert len(data.get("remaining_proof_gaps", [])) > 0


def test_e2e_golden_flow_receipt_example_shape() -> None:
    p = ROOT / "examples" / "full_acceptance" / "e2e_golden_flow_receipt.example.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("artifact_kind") == "odin_e2e_golden_flow_receipt"
    assert data.get("candidate_only") is True
    assert data.get("local_only") is True
    assert data.get("claim_boundary") is not None
    assert "not_proven" in data
    assert "proof_boundaries" in data


def test_support_bundle_receipt_example_shape() -> None:
    p = ROOT / "examples" / "full_acceptance" / "support_bundle_receipt.example.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("artifact_kind") == "odin_support_bundle_receipt"
    assert data.get("redaction_applied") is True
    assert data.get("external_send") is False
    assert data.get("local_diagnostics_only") is True
    assert data.get("claim_boundary") is not None


def test_remaining_proof_gaps_example_shape() -> None:
    p = ROOT / "examples" / "full_acceptance" / "remaining_proof_gaps.example.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("candidate_only") is True
    assert data.get("claim_boundary") is not None
    gaps = data.get("gaps", [])
    assert len(gaps) > 0
    # All gaps should have required fields
    for gap in gaps:
        assert "gap" in gap
        assert "status" in gap
        assert "reason" in gap


# ---------------------------------------------------------------------------
# Candidate / app-owned boundary tests
# ---------------------------------------------------------------------------

def test_prove_full_acceptance_candidate_only() -> None:
    from odin.hub.shell import build_full_acceptance_proof_packet
    packet = build_full_acceptance_proof_packet()
    assert packet.get("candidate_only") is True, "candidate_only must be true"
    assert packet.get("local_only") is True, "local_only must be true"


def test_prove_full_acceptance_no_app_apply() -> None:
    from odin.hub.shell import build_full_acceptance_proof_packet
    packet = build_full_acceptance_proof_packet()
    # The packet must not contain app_apply or external_send claims
    text = json.dumps(packet)
    assert '"app_owned_apply": false' not in text
    assert '"may_apply": true' not in text
    assert '"external_send": true' not in text


def test_harness_registry_candidate_only() -> None:
    reg = _load_harness_registry()
    assert reg.get("candidate_only") is True
    assert reg.get("local_only") is True


def test_harness_registry_full_acceptance_local_receipt() -> None:
    reg = _load_harness_registry()
    assert reg.get("full_acceptance_local_receipt") is True
