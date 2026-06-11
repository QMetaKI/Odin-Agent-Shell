"""LRH-PR-18: Consolidated Proof Governance, Gap Closure & Release Boundary Pack.

Claim boundary: consolidated_proof_governance_local_receipt_not_production_not_release_certification
Candidate-only. Local-only. Deterministic.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REGISTRIES = ROOT / "registries"
DOCS = ROOT / "docs"
EXAMPLES = ROOT / "examples"


# ── Registry existence ────────────────────────────────────────────────────────

class TestNewRegistryExistence:
    def test_post_lrh_proof_governance_registry_exists(self):
        assert (REGISTRIES / "post_lrh_proof_governance_registry_v1.json").exists()

    def test_agent_proof_boundary_registry_exists(self):
        assert (REGISTRIES / "agent_proof_boundary_registry_v1.json").exists()

    def test_thor_hermetic_ci_artifact_contract_exists(self):
        assert (REGISTRIES / "thor_hermetic_ci_artifact_contract_v1.json").exists()

    def test_claim_phrase_registry_exists(self):
        assert (REGISTRIES / "claim_phrase_registry_v1.json").exists()

    def test_claim_boundary_registry_exists(self):
        assert (REGISTRIES / "claim_boundary_registry_v1.json").exists()

    def test_forbidden_control_pattern_registry_exists(self):
        assert (REGISTRIES / "forbidden_control_pattern_registry_v1.json").exists()

    def test_runtime_backend_coverage_matrix_exists(self):
        assert (REGISTRIES / "runtime_backend_coverage_matrix_v1.json").exists()

    def test_redaction_policy_test_matrix_exists(self):
        assert (REGISTRIES / "redaction_policy_test_matrix_v1.json").exists()

    def test_release_readiness_boundary_exists(self):
        assert (REGISTRIES / "release_readiness_boundary_v1.json").exists()

    def test_windows_target_host_receipt_contract_exists(self):
        assert (REGISTRIES / "windows_target_host_receipt_contract_v1.json").exists()


# ── Registry valid JSON ───────────────────────────────────────────────────────

def _load(name: str) -> dict:
    return json.loads((REGISTRIES / name).read_text(encoding="utf-8"))


class TestRegistryValidJSON:
    def test_post_lrh_proof_governance_valid_json(self):
        data = _load("post_lrh_proof_governance_registry_v1.json")
        assert isinstance(data, dict)

    def test_agent_proof_boundary_valid_json(self):
        data = _load("agent_proof_boundary_registry_v1.json")
        assert isinstance(data, dict)

    def test_thor_hermetic_ci_valid_json(self):
        data = _load("thor_hermetic_ci_artifact_contract_v1.json")
        assert isinstance(data, dict)

    def test_claim_phrase_valid_json(self):
        data = _load("claim_phrase_registry_v1.json")
        assert isinstance(data, dict)

    def test_claim_boundary_valid_json(self):
        data = _load("claim_boundary_registry_v1.json")
        assert isinstance(data, dict)

    def test_forbidden_control_valid_json(self):
        data = _load("forbidden_control_pattern_registry_v1.json")
        assert isinstance(data, dict)

    def test_runtime_backend_coverage_valid_json(self):
        data = _load("runtime_backend_coverage_matrix_v1.json")
        assert isinstance(data, dict)

    def test_redaction_policy_valid_json(self):
        data = _load("redaction_policy_test_matrix_v1.json")
        assert isinstance(data, dict)

    def test_release_readiness_boundary_valid_json(self):
        data = _load("release_readiness_boundary_v1.json")
        assert isinstance(data, dict)

    def test_windows_target_host_valid_json(self):
        data = _load("windows_target_host_receipt_contract_v1.json")
        assert isinstance(data, dict)


# ── Registry required fields ──────────────────────────────────────────────────

class TestRegistryRequiredFields:
    def test_post_lrh_has_registry_id(self):
        assert "registry_id" in _load("post_lrh_proof_governance_registry_v1.json")

    def test_post_lrh_has_version(self):
        assert "version" in _load("post_lrh_proof_governance_registry_v1.json")

    def test_post_lrh_has_closed_gaps(self):
        data = _load("post_lrh_proof_governance_registry_v1.json")
        assert "closed_gaps" in data
        assert len(data["closed_gaps"]) > 0

    def test_post_lrh_has_retained_gaps(self):
        data = _load("post_lrh_proof_governance_registry_v1.json")
        assert "retained_gaps" in data
        assert len(data["retained_gaps"]) > 0

    def test_post_lrh_has_not_proven(self):
        data = _load("post_lrh_proof_governance_registry_v1.json")
        assert "not_proven" in data
        assert "production_readiness" in data["not_proven"]

    def test_post_lrh_candidate_only(self):
        data = _load("post_lrh_proof_governance_registry_v1.json")
        assert data.get("candidate_only") is True

    def test_post_lrh_local_only(self):
        data = _load("post_lrh_proof_governance_registry_v1.json")
        assert data.get("local_only") is True

    def test_agent_proof_has_receipts(self):
        data = _load("agent_proof_boundary_registry_v1.json")
        assert "receipts" in data
        receipts = data["receipts"]
        assert "no_app_apply_by_agent_receipt" in receipts
        assert "no_external_send_by_agent_receipt" in receipts
        assert "no_hidden_tool_execution_receipt" in receipts

    def test_agent_proof_receipts_are_closed(self):
        receipts = _load("agent_proof_boundary_registry_v1.json")["receipts"]
        assert receipts["no_app_apply_by_agent_receipt"]["status"] == "closed"
        assert receipts["no_external_send_by_agent_receipt"]["status"] == "closed"
        assert receipts["no_hidden_tool_execution_receipt"]["status"] == "closed"

    def test_agent_proof_has_not_proven(self):
        data = _load("agent_proof_boundary_registry_v1.json")
        assert "not_proven" in data
        assert "production_readiness" in data["not_proven"]

    def test_agent_proof_has_proof_boundaries(self):
        data = _load("agent_proof_boundary_registry_v1.json")
        assert "proof_boundaries" in data
        assert "not_agent_authority_expansion" in data["proof_boundaries"]

    def test_runtime_backend_has_coverage_categories(self):
        data = _load("runtime_backend_coverage_matrix_v1.json")
        assert "coverage_categories" in data
        assert len(data["coverage_categories"]) > 0

    def test_runtime_backend_has_not_proven(self):
        data = _load("runtime_backend_coverage_matrix_v1.json")
        assert "not_proven" in data
        assert "production_runtime_coverage" in data["not_proven"]

    def test_redaction_has_redaction_categories(self):
        data = _load("redaction_policy_test_matrix_v1.json")
        assert "redaction_categories" in data
        assert len(data["redaction_categories"]) > 0

    def test_redaction_has_not_proven(self):
        data = _load("redaction_policy_test_matrix_v1.json")
        assert "not_proven" in data
        assert "redaction_guarantee" in data["not_proven"]

    def test_release_has_future_receipt_requirements(self):
        data = _load("release_readiness_boundary_v1.json")
        assert "future_receipt_requirements" in data
        assert len(data["future_receipt_requirements"]) > 0

    def test_release_has_not_proven(self):
        data = _load("release_readiness_boundary_v1.json")
        assert "not_proven" in data
        assert "signed_distribution" in data["not_proven"]

    def test_windows_has_future_receipt_requirements(self):
        data = _load("windows_target_host_receipt_contract_v1.json")
        assert "future_receipt_requirements" in data
        assert len(data["future_receipt_requirements"]) > 0

    def test_windows_has_not_proven(self):
        data = _load("windows_target_host_receipt_contract_v1.json")
        assert "not_proven" in data
        assert "windows_service_proof" in data["not_proven"]


# ── Doc existence ─────────────────────────────────────────────────────────────

class TestNewDocExistence:
    def test_consolidated_pg_doc_exists(self):
        assert (DOCS / "CONSOLIDATED_PROOF_GOVERNANCE_GAP_CLOSURE_RELEASE_BOUNDARY_V1.md").exists()

    def test_agent_proof_boundary_doc_exists(self):
        assert (DOCS / "AGENT_PROOF_BOUNDARY_CLOSURE_V1.md").exists()

    def test_thor_hermetic_doc_exists(self):
        assert (DOCS / "THOR_HERMETIC_CI_ARTIFACT_CONTRACT_V1.md").exists()

    def test_claim_scanner_doc_exists(self):
        assert (DOCS / "CLAIM_SCANNER_PHRASE_REGISTRY_V1.md").exists()

    def test_forbidden_control_doc_exists(self):
        assert (DOCS / "FORBIDDEN_CONTROL_PATTERN_REGISTRY_V1.md").exists()

    def test_runtime_backend_coverage_doc_exists(self):
        assert (DOCS / "RUNTIME_BACKEND_COVERAGE_MATRIX_V1.md").exists()

    def test_redaction_policy_doc_exists(self):
        assert (DOCS / "REDACTION_POLICY_TEST_MATRIX_V1.md").exists()

    def test_signed_distribution_doc_exists(self):
        assert (DOCS / "SIGNED_DISTRIBUTION_READINESS_BOUNDARY_V1.md").exists()

    def test_windows_target_host_doc_exists(self):
        assert (DOCS / "WINDOWS_TARGET_HOST_RECEIPT_BOUNDARY_V1.md").exists()


# ── Doc boundary phrase validation ────────────────────────────────────────────

def _doc_text(name: str) -> str:
    return (DOCS / name).read_text(encoding="utf-8").lower()


class TestDocBoundaryPhrases:
    def test_consolidated_pg_doc_has_claim_boundary(self):
        text = _doc_text("CONSOLIDATED_PROOF_GOVERNANCE_GAP_CLOSURE_RELEASE_BOUNDARY_V1.md")
        assert "claim boundary" in text or "claim_boundary" in text

    def test_consolidated_pg_doc_has_not_proven(self):
        text = _doc_text("CONSOLIDATED_PROOF_GOVERNANCE_GAP_CLOSURE_RELEASE_BOUNDARY_V1.md")
        assert "not proven" in text or "not_proven" in text

    def test_consolidated_pg_doc_not_production(self):
        text = _doc_text("CONSOLIDATED_PROOF_GOVERNANCE_GAP_CLOSURE_RELEASE_BOUNDARY_V1.md")
        assert "not production readiness" in text

    def test_consolidated_pg_doc_not_release(self):
        text = _doc_text("CONSOLIDATED_PROOF_GOVERNANCE_GAP_CLOSURE_RELEASE_BOUNDARY_V1.md")
        assert "not release certification" in text

    def test_agent_proof_doc_has_not_proven(self):
        text = _doc_text("AGENT_PROOF_BOUNDARY_CLOSURE_V1.md")
        assert "not proven" in text or "not_proven" in text

    def test_agent_proof_doc_not_authority_expansion(self):
        text = _doc_text("AGENT_PROOF_BOUNDARY_CLOSURE_V1.md")
        assert "not agent authority expansion" in text

    def test_signed_distribution_doc_not_signing(self):
        text = _doc_text("SIGNED_DISTRIBUTION_READINESS_BOUNDARY_V1.md")
        assert "not signed distribution proof" in text or "not signing proof" in text or "no signing performed" in text

    def test_windows_target_host_doc_not_service(self):
        text = _doc_text("WINDOWS_TARGET_HOST_RECEIPT_BOUNDARY_V1.md")
        assert "not windows service proof" in text or "no service" in text


# ── Agent Proof Boundary Closure ──────────────────────────────────────────────

class TestAgentProofBoundaryClosure:
    def test_prove_agent_operator_mode_passes(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert result["status"] in {"ok", "ok_with_known_gaps"}

    def test_prove_agent_operator_mode_candidate_only(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert result["candidate_only"] is True

    def test_prove_agent_operator_mode_local_only(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert result["local_only"] is True

    def test_prove_agent_operator_mode_app_owned_apply(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert result["app_owned_apply"] is True

    def test_prove_agent_operator_mode_external_send_false(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert result["external_send_default"] is False

    def test_prove_agent_operator_mode_hidden_tool_false(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert result["hidden_tool_execution_allowed"] is False

    def test_no_app_apply_receipt_closed(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert result["no_app_apply_by_agent_receipt"] == "closed"

    def test_no_external_send_receipt_closed(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert result["no_external_send_by_agent_receipt"] == "closed"

    def test_no_hidden_tool_receipt_closed(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert result["no_hidden_tool_execution_receipt"] == "closed"

    def test_agent_proof_has_not_proven(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert "production_readiness" in result["not_proven"]
        assert "live_model_inference" in result["not_proven"]

    def test_agent_proof_has_proof_boundaries(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert "not_agent_authority_expansion" in result["proof_boundaries"]
        assert "not_app_apply_proof" in result["proof_boundaries"]

    def test_no_forbidden_action_introduced(self):
        from odin.hub.shell import build_agent_operator_mode_proof_packet
        result = build_agent_operator_mode_proof_packet()
        assert result.get("app_owned_apply") is True
        assert result.get("external_send_default") is False
        assert result.get("hidden_tool_execution_allowed") is False


# ── External App Bridge Proof ─────────────────────────────────────────────────

class TestExternalAppBridgeProof:
    def test_prove_external_app_bridge_passes(self):
        from odin.hub.shell import build_external_app_bridge_proof_packet
        result = build_external_app_bridge_proof_packet()
        assert result["status"] in {"ok", "ok_with_known_gaps"}

    def test_prove_external_app_bridge_candidate_only(self):
        from odin.hub.shell import build_external_app_bridge_proof_packet
        result = build_external_app_bridge_proof_packet()
        assert result["candidate_only"] is True

    def test_prove_external_app_bridge_no_external_send(self):
        from odin.hub.shell import build_external_app_bridge_proof_packet
        result = build_external_app_bridge_proof_packet()
        assert result["external_send"] is False

    def test_prove_external_app_bridge_no_app_apply(self):
        from odin.hub.shell import build_external_app_bridge_proof_packet
        result = build_external_app_bridge_proof_packet()
        assert result["app_apply"] is False

    def test_prove_external_app_bridge_no_public_network(self):
        from odin.hub.shell import build_external_app_bridge_proof_packet
        result = build_external_app_bridge_proof_packet()
        assert result["public_network"] is False

    def test_prove_external_app_bridge_no_specific_app(self):
        from odin.hub.shell import build_external_app_bridge_proof_packet
        result = build_external_app_bridge_proof_packet()
        assert result["specific_app_integration"] is False

    def test_prove_external_app_bridge_not_proven_list(self):
        from odin.hub.shell import build_external_app_bridge_proof_packet
        result = build_external_app_bridge_proof_packet()
        assert "specific_external_app_integration" in result["not_proven"]
        assert "live_external_system_connection" in result["not_proven"]

    def test_prove_external_app_bridge_proof_boundaries(self):
        from odin.hub.shell import build_external_app_bridge_proof_packet
        result = build_external_app_bridge_proof_packet()
        assert "not_specific_external_app_integration_proof" in result["proof_boundaries"]
        assert "generic_neutral_local_receipt_only" in result["proof_boundaries"]


# ── Consolidated Proof Governance Packet ─────────────────────────────────────

class TestConsolidatedProofGovernancePacket:
    def test_validate_consolidated_passes(self):
        from odin.hub.shell import validate_consolidated_proof_governance
        errors = validate_consolidated_proof_governance()
        assert errors == [], f"Unexpected errors: {errors}"

    def test_packet_artifact_kind(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert result["artifact_kind"] == "odin_consolidated_proof_governance_packet"

    def test_packet_lrh_pr(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert result["lrh_pr"] == "LRH-PR-18"

    def test_packet_status_valid(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert result["status"] in {"ok", "ok_with_known_gaps"}

    def test_packet_candidate_only(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert result["candidate_only"] is True

    def test_packet_local_only(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert result["local_only"] is True

    def test_packet_proof_governance_receipt(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert result["proof_governance_receipt"] is True

    def test_packet_agent_proof_boundary_present(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert "agent_proof_boundary" in result
        apb = result["agent_proof_boundary"]
        assert apb.get("no_app_apply_by_agent_receipt") == "closed"
        assert apb.get("no_external_send_by_agent_receipt") == "closed"
        assert apb.get("no_hidden_tool_execution_receipt") == "closed"

    def test_packet_closed_gaps_present(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert "closed_gaps" in result
        assert len(result["closed_gaps"]) > 0

    def test_packet_retained_gaps_present(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert "retained_gaps" in result
        assert len(result["retained_gaps"]) > 0

    def test_packet_not_proven_present(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert "not_proven" in result
        assert "production_readiness" in result["not_proven"]
        assert "release_certification" in result["not_proven"]
        assert "security_certification" in result["not_proven"]
        assert "signed_distribution" in result["not_proven"]
        assert "windows_service" in result["not_proven"]
        assert "windows_tray" in result["not_proven"]
        assert "windows_installer" in result["not_proven"]
        assert "target_host_validation" in result["not_proven"]
        assert "live_model_inference" in result["not_proven"]
        assert "model_quality" in result["not_proven"]

    def test_packet_proof_boundaries_present(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert "proof_boundaries" in result
        pb = result["proof_boundaries"]
        assert "not_production_readiness_certification" in pb
        assert "not_release_certification" in pb
        assert "not_security_certification" in pb
        assert "not_signed_distribution_proof" in pb
        assert "not_windows_service_proof" in pb
        assert "not_target_host_proof" in pb
        assert "candidate_artifact_not_applied_truth" in pb
        assert "host_app_owns_apply_state_external_send" in pb

    def test_packet_no_production_claim(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        forbidden = [
            "production_ready", "certified", "release_certified",
            "fully_proven", "guaranteed", "security_certified"
        ]
        result_str = json.dumps(result)
        for phrase in forbidden:
            assert phrase not in result_str, f"Forbidden claim found: {phrase}"

    def test_packet_thor_hermetic_present(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert "thor_hermetic_contract" in result
        assert result["thor_hermetic_contract"]["advisory_only"] is True

    def test_packet_claim_boundary(self):
        from odin.hub.shell import build_consolidated_proof_governance_packet
        result = build_consolidated_proof_governance_packet()
        assert result["claim_boundary"] == "consolidated_proof_governance_local_receipt_not_production_not_release_certification"


# ── Runtime Backend Coverage ──────────────────────────────────────────────────

class TestRuntimeBackendCoverage:
    def test_prove_runtime_backend_coverage_passes(self):
        from odin.hub.shell import build_runtime_backend_coverage_proof_packet
        result = build_runtime_backend_coverage_proof_packet()
        assert result["status"] in {"ok", "ok_with_known_gaps"}

    def test_runtime_coverage_candidate_only(self):
        from odin.hub.shell import build_runtime_backend_coverage_proof_packet
        result = build_runtime_backend_coverage_proof_packet()
        assert result["candidate_only"] is True

    def test_runtime_coverage_has_covered_backends(self):
        from odin.hub.shell import build_runtime_backend_coverage_proof_packet
        result = build_runtime_backend_coverage_proof_packet()
        assert len(result["covered_backends"]) > 0

    def test_runtime_coverage_has_retained_gaps(self):
        from odin.hub.shell import build_runtime_backend_coverage_proof_packet
        result = build_runtime_backend_coverage_proof_packet()
        assert len(result["retained_gap_backends"]) > 0

    def test_runtime_coverage_not_proven_production(self):
        from odin.hub.shell import build_runtime_backend_coverage_proof_packet
        result = build_runtime_backend_coverage_proof_packet()
        assert "production_runtime_coverage" in result["not_proven"]

    def test_runtime_coverage_not_proven_live_model(self):
        from odin.hub.shell import build_runtime_backend_coverage_proof_packet
        result = build_runtime_backend_coverage_proof_packet()
        assert "live_model_execution" in result["not_proven"]


# ── Example existence ─────────────────────────────────────────────────────────

class TestExampleExistence:
    def test_proof_governance_example_exists(self):
        assert (EXAMPLES / "proof_governance" / "consolidated_proof_governance_packet.example.json").exists()

    def test_redaction_policy_example_exists(self):
        assert (EXAMPLES / "redaction_policy" / "api_key_redaction.example.json").exists()

    def test_release_boundary_example_exists(self):
        assert (EXAMPLES / "release_boundary" / "signed_distribution_boundary.example.json").exists()

    def test_windows_boundary_example_exists(self):
        assert (EXAMPLES / "windows_target_host_boundary" / "windows_target_host_receipt.example.json").exists()

    def test_proof_governance_example_valid_json(self):
        data = json.loads(
            (EXAMPLES / "proof_governance" / "consolidated_proof_governance_packet.example.json")
            .read_text(encoding="utf-8")
        )
        assert data["candidate_only"] is True
        assert data["local_only"] is True

    def test_release_boundary_example_no_signing_claim(self):
        data = json.loads(
            (EXAMPLES / "release_boundary" / "signed_distribution_boundary.example.json")
            .read_text(encoding="utf-8")
        )
        assert data["signing_status"] == "not_performed"
        assert data["certificate_status"] == "not_present"

    def test_windows_boundary_example_no_service_claim(self):
        data = json.loads(
            (EXAMPLES / "windows_target_host_boundary" / "windows_target_host_receipt.example.json")
            .read_text(encoding="utf-8")
        )
        assert data["service_status"] == "not_created"
        assert data["tray_status"] == "not_created"
        assert data["installer_status"] == "not_created"


# ── Validate-all integration ──────────────────────────────────────────────────

class TestValidateAllIntegration:
    def test_validate_all_includes_consolidated_pg(self):
        import inspect
        from odin.cli import validate_all
        source = inspect.getsource(validate_all)
        assert "validate_consolidated_proof_governance" in source

    def test_validate_consolidated_proof_governance_is_green(self):
        from odin.hub.shell import validate_consolidated_proof_governance
        errors = validate_consolidated_proof_governance()
        assert errors == [], f"validate_consolidated_proof_governance errors: {errors}"


# ── Boundary phrase / wording discipline ─────────────────────────────────────

class TestBoundaryPhraseCompliance:
    def test_packet_example_no_production_ready_claim(self):
        data = json.loads(
            (EXAMPLES / "proof_governance" / "consolidated_proof_governance_packet.example.json")
            .read_text(encoding="utf-8")
        )
        s = json.dumps(data).lower()
        for phrase in ["production_ready", "certified", "fully_proven", "release_certified"]:
            assert phrase not in s, f"Forbidden phrase '{phrase}' in example"

    def test_agent_proof_registry_no_authority_expansion(self):
        data = _load("agent_proof_boundary_registry_v1.json")
        s = json.dumps(data).lower()
        forbidden = ["authority_granted", "applies_state", "sends_externally", "executes_hidden"]
        for phrase in forbidden:
            assert phrase not in s, f"Forbidden phrase '{phrase}' in agent_proof_boundary_registry"

    def test_windows_registry_no_service_created_claim(self):
        data = _load("windows_target_host_receipt_contract_v1.json")
        assert data["service_status"] == "not_created"
        assert data["tray_status"] == "not_created"
        assert data["installer_status"] == "not_created"

    def test_release_registry_no_signing_claimed(self):
        data = _load("release_readiness_boundary_v1.json")
        assert data["signing_status"] == "not_performed"
        assert data["certificate_status"] == "not_present"
