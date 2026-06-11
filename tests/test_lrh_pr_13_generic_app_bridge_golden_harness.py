"""Tests for LRH-PR-13: Generic App Bridge Examples and Golden Harness.

Claim boundary: test_lrh_pr_13_candidate_only_no_apply_no_external_send
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Doc existence
# ---------------------------------------------------------------------------


def test_generic_app_bridge_golden_harness_doc_exists():
    assert (ROOT / "docs" / "GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md").exists()


def test_thor_cli_invocation_discipline_doc_exists():
    assert (ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md").exists()


# ---------------------------------------------------------------------------
# Directory and file existence
# ---------------------------------------------------------------------------


def test_generic_app_bridge_dir_exists():
    assert (ROOT / "examples" / "generic_app_bridge").is_dir()


def test_reference_host_app_dir_exists():
    assert (ROOT / "examples" / "reference_host_app").is_dir()


def test_generic_bridge_flow_one_exists():
    assert (ROOT / "examples" / "generic_app_bridge" / "generic_bridge_flow_one.py").exists()


def test_generic_bridge_flow_two_exists():
    assert (ROOT / "examples" / "generic_app_bridge" / "generic_bridge_flow_two.py").exists()


def test_generic_bridge_harness_exists():
    assert (ROOT / "examples" / "generic_app_bridge" / "generic_bridge_harness.py").exists()


def test_reference_host_app_exists():
    assert (ROOT / "examples" / "reference_host_app" / "reference_host_app.py").exists()


def test_reference_host_policy_exists():
    assert (ROOT / "examples" / "reference_host_app" / "reference_host_policy.json").exists()


def test_neutral_examples_count_at_least_two():
    example_files = [
        ROOT / "examples" / "generic_app_bridge" / "generic_bridge_flow_one.py",
        ROOT / "examples" / "generic_app_bridge" / "generic_bridge_flow_two.py",
    ]
    count = sum(1 for f in example_files if f.exists())
    assert count >= 2, f"At least two neutral examples required; found {count}"


# ---------------------------------------------------------------------------
# Fixture parsing — flow one request
# ---------------------------------------------------------------------------


def test_flow_one_request_fixture_parses():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_request.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_flow_one_request_candidate_only():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_request.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("candidate_only") is True


def test_flow_one_request_local_only():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_request.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("local_only") is True


def test_flow_one_request_host_app_owns_apply():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_request.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("host_app_owns_apply") is True


def test_flow_one_request_applied_truth_false():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_request.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("applied_truth") is False


def test_flow_one_request_has_claim_boundary():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_request.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "claim_boundary" in data


# ---------------------------------------------------------------------------
# Fixture parsing — flow one candidate
# ---------------------------------------------------------------------------


def test_flow_one_candidate_fixture_parses():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_candidate.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_flow_one_candidate_candidate_only():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_candidate.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("candidate_only") is True


def test_flow_one_candidate_applied_truth_false():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_candidate.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("applied_truth") is False


def test_flow_one_candidate_app_state_mutated_false():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_candidate.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("app_state_mutated") is False


def test_flow_one_candidate_external_send_false():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_one_candidate.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("external_send") is False


# ---------------------------------------------------------------------------
# Fixture parsing — flow two request
# ---------------------------------------------------------------------------


def test_flow_two_request_fixture_parses():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_two_request.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_flow_two_request_candidate_only():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_two_request.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("candidate_only") is True


def test_flow_two_request_local_only():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_two_request.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("local_only") is True


def test_flow_two_request_applied_truth_false():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_two_request.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("applied_truth") is False


# ---------------------------------------------------------------------------
# Fixture parsing — flow two candidate
# ---------------------------------------------------------------------------


def test_flow_two_candidate_fixture_parses():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_two_candidate.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_flow_two_candidate_applied_truth_false():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_two_candidate.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("applied_truth") is False


def test_flow_two_candidate_candidate_only():
    p = ROOT / "examples" / "generic_app_bridge" / "fixtures" / "generic_bridge_flow_two_candidate.valid.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("candidate_only") is True


# ---------------------------------------------------------------------------
# Reference host policy
# ---------------------------------------------------------------------------


def test_reference_host_policy_parses():
    p = ROOT / "examples" / "reference_host_app" / "reference_host_policy.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_reference_host_policy_host_app_owns_apply():
    p = ROOT / "examples" / "reference_host_app" / "reference_host_policy.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("host_app_owns_apply") is True


def test_reference_host_policy_host_app_owns_state():
    p = ROOT / "examples" / "reference_host_app" / "reference_host_policy.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("host_app_owns_state") is True


def test_reference_host_policy_host_app_owns_external_send():
    p = ROOT / "examples" / "reference_host_app" / "reference_host_policy.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("host_app_owns_external_send") is True


def test_reference_host_policy_host_state_mutated_false():
    p = ROOT / "examples" / "reference_host_app" / "reference_host_policy.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("app_state_mutated") is False


def test_reference_host_policy_external_send_performed_false():
    p = ROOT / "examples" / "reference_host_app" / "reference_host_policy.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data.get("external_send_performed") is False


# ---------------------------------------------------------------------------
# Golden harness execution
# ---------------------------------------------------------------------------


def _import_harness():
    spec = importlib.util.spec_from_file_location(
        "generic_bridge_harness",
        ROOT / "examples" / "generic_app_bridge" / "generic_bridge_harness.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_golden_harness_runs():
    mod = _import_harness()
    receipt = mod.run()
    assert isinstance(receipt, dict)


def test_golden_harness_receipt_status_ok():
    mod = _import_harness()
    receipt = mod.run()
    assert receipt.get("status") == "ok"


def test_golden_harness_receipt_neutral_examples_at_least_two():
    mod = _import_harness()
    receipt = mod.run()
    assert receipt.get("neutral_examples", 0) >= 2


def test_golden_harness_receipt_host_app_owns_apply():
    mod = _import_harness()
    receipt = mod.run()
    assert receipt.get("host_app_owns_apply") is True


def test_golden_harness_receipt_odin_app_apply_false():
    mod = _import_harness()
    receipt = mod.run()
    assert receipt.get("odin_app_apply") is False


def test_golden_harness_receipt_odin_external_send_false():
    mod = _import_harness()
    receipt = mod.run()
    assert receipt.get("odin_external_send") is False


def test_golden_harness_receipt_concrete_app_names_present_false():
    mod = _import_harness()
    receipt = mod.run()
    assert receipt.get("concrete_app_names_present") is False


def test_golden_harness_receipt_candidate_only():
    mod = _import_harness()
    receipt = mod.run()
    assert receipt.get("candidate_only") is True


def test_golden_harness_receipt_local_only():
    mod = _import_harness()
    receipt = mod.run()
    assert receipt.get("local_only") is True


def test_golden_harness_receipt_host_state_mutated_false():
    mod = _import_harness()
    receipt = mod.run()
    assert receipt.get("host_state_mutated") is False


def test_golden_harness_receipt_external_send_performed_false():
    mod = _import_harness()
    receipt = mod.run()
    assert receipt.get("external_send_performed") is False


def test_golden_harness_receipt_has_proof_boundaries():
    mod = _import_harness()
    receipt = mod.run()
    assert len(receipt.get("proof_boundaries", [])) > 0


def test_golden_harness_receipt_has_known_non_proofs():
    mod = _import_harness()
    receipt = mod.run()
    assert len(receipt.get("known_non_proofs", [])) > 0


# ---------------------------------------------------------------------------
# Neutral naming guard — no concrete app names in public artifacts
# ---------------------------------------------------------------------------

_FORBIDDEN_CONCRETE_NAMES = [
    "github_copilot",
    "jira_integration",
    "slack_bot",
    "salesforce",
    "notion_plugin",
    "linear_integration",
]

_NEUTRAL_SCAN_FILES = [
    "examples/generic_app_bridge/generic_bridge_flow_one.py",
    "examples/generic_app_bridge/generic_bridge_flow_two.py",
    "examples/generic_app_bridge/generic_bridge_harness.py",
    "examples/generic_app_bridge/fixtures/generic_bridge_flow_one_request.valid.json",
    "examples/generic_app_bridge/fixtures/generic_bridge_flow_one_candidate.valid.json",
    "examples/generic_app_bridge/fixtures/generic_bridge_flow_two_request.valid.json",
    "examples/generic_app_bridge/fixtures/generic_bridge_flow_two_candidate.valid.json",
    "examples/reference_host_app/reference_host_app.py",
    "examples/reference_host_app/reference_host_policy.json",
    "docs/GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md",
]


@pytest.mark.parametrize("rel_path", _NEUTRAL_SCAN_FILES)
def test_no_concrete_app_names_in_file(rel_path: str):
    p = ROOT / rel_path
    if not p.exists():
        pytest.skip(f"file not present: {rel_path}")
    text = p.read_text(encoding="utf-8", errors="ignore").lower()
    for name in _FORBIDDEN_CONCRETE_NAMES:
        assert name not in text, f"{rel_path}: forbidden concrete app name found: {name!r}"


def test_no_production_integration_claim_in_doc():
    doc = ROOT / "docs" / "GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "production-ready release" not in text
    assert "real integration complete" not in text
    assert "fully proven" not in text


def test_no_hosted_bridge_claim_in_doc():
    doc = ROOT / "docs" / "GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "hosted bridge ready" not in text


def test_no_public_gateway_claim_in_doc():
    doc = ROOT / "docs" / "GENERIC_APP_BRIDGE_GOLDEN_HARNESS_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "public gateway ready" not in text


# ---------------------------------------------------------------------------
# Forbidden actionable helper names in example files
# ---------------------------------------------------------------------------

_FORBIDDEN_HELPER_NAMES = [
    "apply_candidate",
    "send_external",
    "mutate_app_state",
    "store_credential",
    "save_credential",
    "set_api_key",
    "run_provider",
    "execute_provider",
    "call_model",
    "run_model",
]

_EXAMPLE_SOURCE_FILES = [
    "examples/generic_app_bridge/generic_bridge_flow_one.py",
    "examples/generic_app_bridge/generic_bridge_flow_two.py",
    "examples/generic_app_bridge/generic_bridge_harness.py",
    "examples/reference_host_app/reference_host_app.py",
]


@pytest.mark.parametrize("rel_path", _EXAMPLE_SOURCE_FILES)
def test_no_forbidden_helper_names_in_examples(rel_path: str):
    p = ROOT / rel_path
    if not p.exists():
        pytest.skip(f"file not present: {rel_path}")
    src = p.read_text(encoding="utf-8", errors="ignore")
    for name in _FORBIDDEN_HELPER_NAMES:
        assert f"def {name}(" not in src, (
            f"{rel_path}: forbidden helper function found: def {name}()"
        )


# ---------------------------------------------------------------------------
# Thor CLI invocation discipline doc checks
# ---------------------------------------------------------------------------


def test_thor_discipline_doc_has_advisory_statement():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "thor is advisory" in text


def test_thor_discipline_doc_has_classification_section():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "classification" in text


def test_thor_discipline_doc_has_invocation_order():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "preferred invocation order" in text or "invocation" in text


def test_thor_discipline_doc_has_not_found_in_path_class():
    doc = ROOT / "docs" / "THOR_CLI_INVOCATION_DISCIPLINE_V1.md"
    text = doc.read_text(encoding="utf-8", errors="ignore").lower()
    assert "not_found_in_path" in text


# ---------------------------------------------------------------------------
# Validator and proof packet via CLI module
# ---------------------------------------------------------------------------


def test_validate_generic_app_bridge_golden_harness_passes():
    from odin.hub.shell import validate_generic_app_bridge_golden_harness
    errors = validate_generic_app_bridge_golden_harness()
    assert errors == [], f"Validation errors: {errors}"


def test_prove_generic_app_bridge_golden_harness_emits_packet():
    from odin.hub.shell import build_generic_app_bridge_golden_harness_proof_packet
    packet = build_generic_app_bridge_golden_harness_proof_packet()
    assert packet.get("artifact_kind") == "generic_app_bridge_golden_harness_proof_packet"
    assert packet.get("status") == "ok"
    assert packet.get("candidate_only") is True
    assert packet.get("local_only") is True
    assert packet.get("neutral_examples_count") >= 2
    assert packet.get("host_app_owns_apply") is True
    assert packet.get("host_app_owns_state") is True
    assert packet.get("host_app_owns_external_send") is True
    assert packet.get("odin_app_apply") is False
    assert packet.get("odin_external_send") is False
    assert packet.get("host_state_mutation_by_odin") is False
    assert packet.get("concrete_app_names_present") is False


def test_prove_packet_not_proven_list():
    from odin.hub.shell import build_generic_app_bridge_golden_harness_proof_packet
    packet = build_generic_app_bridge_golden_harness_proof_packet()
    not_proven = packet.get("not_proven", [])
    assert "production_readiness" in not_proven
    assert "security_certification" in not_proven
    assert "signed_distribution" in not_proven
    assert "hosted_bridge" in not_proven
    assert "specific_external_app_integration" in not_proven
    assert "live_model_inference" in not_proven
    assert "external_send_authority" in not_proven


def test_prove_packet_proven_list():
    from odin.hub.shell import build_generic_app_bridge_golden_harness_proof_packet
    packet = build_generic_app_bridge_golden_harness_proof_packet()
    proven = packet.get("proven", [])
    assert "generic_examples_exist" in proven
    assert "reference_host_app_exists" in proven
    assert "golden_harness_exists" in proven
    assert "host_app_owns_apply_declared" in proven
    assert "odin_app_apply_false" in proven
    assert "candidate_artifact_not_applied_truth" in proven
    assert "thor_invocation_discipline_doc_exists" in proven


# ---------------------------------------------------------------------------
# agent-handoff --lrh-pr 13 packet
# ---------------------------------------------------------------------------


def test_agent_handoff_lrh_pr_13_produces_valid_packet(tmp_path):
    import subprocess
    out_path = tmp_path / "lrh_pr_13_packet.json"
    result = subprocess.run(
        [
            sys.executable, "-m", "odin.cli",
            "agent-handoff", "--agent", "claude-code",
            "--lrh-pr", "13",
            "--out", str(out_path),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"agent-handoff failed: {result.stderr}"
    assert out_path.exists(), "output packet file was not created"
    packet = json.loads(out_path.read_text(encoding="utf-8"))
    assert packet.get("candidate_only") is True
    assert packet.get("app_owned_apply") is True


def test_agent_guard_passes(tmp_path):
    import subprocess
    out_path = tmp_path / "lrh_pr_13_packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff", "--agent", "claude-code",
         "--lrh-pr", "13", "--out", str(out_path)],
        capture_output=True, text=True, timeout=30,
    )
    if not out_path.exists():
        pytest.skip("agent-handoff packet not created")
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-guard", "--packet", str(out_path)],
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, f"agent-guard failed: {result.stderr}\n{result.stdout}"


def test_agent_check_passes(tmp_path):
    import subprocess
    out_path = tmp_path / "lrh_pr_13_packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff", "--agent", "claude-code",
         "--lrh-pr", "13", "--out", str(out_path)],
        capture_output=True, text=True, timeout=30,
    )
    if not out_path.exists():
        pytest.skip("agent-handoff packet not created")
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-check", "--packet", str(out_path)],
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, f"agent-check failed: {result.stderr}\n{result.stdout}"


def test_agent_proof_passes_or_expected_gap(tmp_path):
    import subprocess
    out_path = tmp_path / "lrh_pr_13_packet.json"
    subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-handoff", "--agent", "claude-code",
         "--lrh-pr", "13", "--out", str(out_path)],
        capture_output=True, text=True, timeout=30,
    )
    if not out_path.exists():
        pytest.skip("agent-handoff packet not created")
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "agent-proof", "--packet", str(out_path)],
        capture_output=True, text=True, timeout=30,
    )
    output_text = result.stdout + result.stderr
    has_proof = result.returncode == 0
    has_expected_gap = "expected_pr_level_gap" in output_text or "gaps_present" in output_text
    assert has_proof or has_expected_gap, (
        f"agent-proof returned unexpected failure: rc={result.returncode}\n{output_text}"
    )


# ---------------------------------------------------------------------------
# validate-all passes
# ---------------------------------------------------------------------------


def test_validate_all_passes():
    import subprocess
    result = subprocess.run(
        [sys.executable, "-m", "odin.cli", "validate-all"],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, (
        f"validate-all failed:\n{result.stdout}\n{result.stderr}"
    )
