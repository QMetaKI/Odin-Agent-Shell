"""Tests for LRH-PR-02 Odin Agent Operator Mode.

No network. No time-sensitive assertions. No dependency on Claude Code or Thor installation.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "agent_operator"
REGISTRIES = ROOT / "registries"
SCHEMAS = ROOT / "schemas" / "v7_1"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Profile Registry
# ---------------------------------------------------------------------------

class TestAgentProfileRegistry:
    def test_registry_exists_and_is_valid_json(self):
        path = REGISTRIES / "agent_operator_profile_registry.json"
        assert path.exists(), "agent_operator_profile_registry.json missing"
        data = load_json(path)
        assert "registry_id" in data
        assert "version" in data
        assert "profiles" in data

    def test_required_profiles_exist(self):
        data = load_json(REGISTRIES / "agent_operator_profile_registry.json")
        ids = {p["profile_id"] for p in data["profiles"]}
        for required in ["codex", "claude-code", "generic-cli-agent", "thor-compatible", "future-local-agent"]:
            assert required in ids, f"Profile missing: {required}"

    def test_codex_profile_has_pr_diff_test_workflow(self):
        data = load_json(REGISTRIES / "agent_operator_profile_registry.json")
        codex = next(p for p in data["profiles"] if p["profile_id"] == "codex")
        workflow = codex.get("recommended_workflow", [])
        assert any("edit" in s or "plan" in s for s in workflow), "Codex workflow must include planning/editing"
        assert codex.get("primary_surface") == "github_pr_workflow"
        assert "candidate_patch" in codex.get("allowed_outputs", [])
        assert "return_report" in codex.get("allowed_outputs", [])

    def test_claude_code_profile_has_explore_plan_implement(self):
        data = load_json(REGISTRIES / "agent_operator_profile_registry.json")
        cc = next(p for p in data["profiles"] if p["profile_id"] == "claude-code")
        workflow = cc.get("recommended_workflow", [])
        workflow_str = " ".join(workflow)
        assert "explore" in workflow_str, "Claude Code workflow must include explore"
        assert "plan" in workflow_str, "Claude Code workflow must include plan"
        cc_specific = cc.get("claude_code_specific", {})
        assert cc_specific.get("claude_md_support") is True
        assert cc_specific.get("hooks_support") is True
        assert cc_specific.get("subagent_review_boundaries") is True
        assert cc_specific.get("requires_claude_code_installed") is False
        assert cc_specific.get("requires_provider_api") is False

    def test_generic_profile_is_tool_neutral(self):
        data = load_json(REGISTRIES / "agent_operator_profile_registry.json")
        generic = next(p for p in data["profiles"] if p["profile_id"] == "generic-cli-agent")
        assert generic.get("allowed_tools_policy") == "deterministic_cli_and_file_edit_only"
        assert generic.get("context_strategy") == "minimal_tool_neutral"

    def test_future_local_agent_is_candidate_only_and_permission_card_bound(self):
        data = load_json(REGISTRIES / "agent_operator_profile_registry.json")
        future = next(p for p in data["profiles"] if p["profile_id"] == "future-local-agent")
        perm = future.get("default_permission_card", {})
        assert perm.get("may_apply_app_state") is False
        assert perm.get("may_send_external") is False
        assert perm.get("may_call_provider_api") is False
        assert perm.get("may_use_hidden_tools") is False
        assert perm.get("may_mutate_domain_state") is False
        assert future.get("future_only") is True

    def test_all_profiles_have_hard_forbidden_actions(self):
        data = load_json(REGISTRIES / "agent_operator_profile_registry.json")
        required_forbidden = {
            "app_state_apply",
            "external_send",
            "hidden_tool_execution",
            "domain_state_mutation",
        }
        for profile in data["profiles"]:
            declared = set(profile.get("forbidden_actions", []))
            missing = required_forbidden - declared
            assert not missing, f"Profile {profile['profile_id']!r} missing forbidden actions: {missing}"

    def test_all_profiles_have_hard_permission_defaults_false(self):
        data = load_json(REGISTRIES / "agent_operator_profile_registry.json")
        hard_false_fields = [
            "may_apply_app_state",
            "may_send_external",
            "may_call_provider_api",
            "may_use_hidden_tools",
            "may_mutate_domain_state",
        ]
        for profile in data["profiles"]:
            perm = profile.get("default_permission_card", {})
            for field in hard_false_fields:
                assert perm.get(field) is False, (
                    f"Profile {profile['profile_id']!r} permission card must have {field}=false"
                )


# ---------------------------------------------------------------------------
# Thor Compatibility Registry
# ---------------------------------------------------------------------------

class TestThorCompatibilityRegistry:
    def test_registry_exists_and_is_valid_json(self):
        path = REGISTRIES / "thor_compatibility_registry.json"
        assert path.exists(), "thor_compatibility_registry.json missing"
        data = load_json(path)
        assert "registry_id" in data
        assert "version" in data
        assert "mappings" in data

    def test_all_mappings_have_evidence_and_gap_labels(self):
        data = load_json(REGISTRIES / "thor_compatibility_registry.json")
        for m in data["mappings"]:
            assert "thor_concept" in m, f"Mapping missing thor_concept: {m}"
            assert "odin_concept" in m, f"Mapping missing odin_concept: {m}"
            assert "status" in m, f"Mapping missing status: {m}"
            assert "evidence_label" in m, f"Mapping missing evidence_label: {m}"
            assert "gap" in m, f"Mapping missing gap: {m}"
            assert "claim_boundary" in m, f"Mapping missing claim_boundary: {m}"
            assert m["status"] in {"verified", "partial", "conceptual", "gap", "unsupported"}, (
                f"Invalid status {m['status']!r} in mapping for {m['thor_concept']!r}"
            )

    def test_required_thor_concepts_mapped(self):
        data = load_json(REGISTRIES / "thor_compatibility_registry.json")
        mapped = {m["thor_concept"] for m in data["mappings"]}
        required = [
            "thor handoff",
            "thor plan",
            "thor guard",
            "thor expected",
            "thor return-plan",
            "thor pack --agent codex",
            "thor repo cognition",
            "thor repo intent",
            "thor repo semantic-inputs",
        ]
        for concept in required:
            assert concept in mapped, f"Thor concept not mapped: {concept!r}"

    def test_no_mapping_claims_full_thor_support(self):
        data = load_json(REGISTRIES / "thor_compatibility_registry.json")
        for m in data["mappings"]:
            cb = m.get("claim_boundary", "")
            assert "full_thor_protocol" not in cb or "not" in cb, (
                f"Mapping {m['thor_concept']!r} must not claim full Thor protocol support"
            )


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class TestSchemas:
    def test_agent_work_packet_schema_exists(self):
        assert (SCHEMAS / "odin_agent_work_packet.schema.json").exists()

    def test_agent_return_report_schema_exists(self):
        assert (SCHEMAS / "odin_agent_return_report.schema.json").exists()

    def test_agent_operator_permission_card_schema_exists(self):
        assert (SCHEMAS / "odin_agent_operator_permission_card.schema.json").exists()

    def test_schemas_are_valid_json(self):
        for name in [
            "odin_agent_work_packet.schema.json",
            "odin_agent_return_report.schema.json",
            "odin_agent_operator_permission_card.schema.json",
        ]:
            data = load_json(SCHEMAS / name)
            assert "$schema" in data or "title" in data, f"Schema {name} missing $schema or title"


# ---------------------------------------------------------------------------
# Valid Examples
# ---------------------------------------------------------------------------

class TestValidExamples:
    def _load_valid(self, name: str) -> dict:
        return load_json(EXAMPLES / name)

    def test_codex_packet_has_required_invariants(self):
        p = self._load_valid("codex_work_packet.valid.json")
        assert p["artifact_kind"] == "odin_agent_work_packet"
        assert p["candidate_only"] is True
        assert p["app_owned_apply"] is True
        assert p["external_send_default"] is False
        assert p["network_transport_default"] is False
        assert p["hidden_tool_execution_allowed"] is False
        assert "app_state_apply" in p["forbidden_actions"]

    def test_claude_code_packet_has_required_invariants(self):
        p = self._load_valid("claude_code_work_packet.valid.json")
        assert p["artifact_kind"] == "odin_agent_work_packet"
        assert p["candidate_only"] is True
        assert p["app_owned_apply"] is True
        assert p["external_send_default"] is False
        assert p["hidden_tool_execution_allowed"] is False
        assert p["agent_profile_id"] == "claude-code"

    def test_generic_agent_packet_has_required_invariants(self):
        p = self._load_valid("generic_cli_agent_work_packet.valid.json")
        assert p["candidate_only"] is True
        assert p["app_owned_apply"] is True
        assert p["agent_profile_id"] == "generic-cli-agent"

    def test_future_local_agent_packet_is_candidate_only(self):
        p = self._load_valid("future_local_agent_work_packet.valid.json")
        assert p["candidate_only"] is True
        assert p["app_owned_apply"] is True
        assert p["external_send_default"] is False
        assert p["hidden_tool_execution_allowed"] is False
        assert p["agent_profile_id"] == "future-local-agent"
        assert "implementation_future_target" in p.get("future_target_flags", [])

    def test_thor_compatible_packet_has_gap_labels(self):
        p = self._load_valid("thor_compatible_packet.valid.json")
        assert p["agent_profile_id"] == "thor-compatible"
        thor = p.get("thor_compatibility", {})
        assert thor.get("status") in {"partial", "conceptual"}
        assert len(thor.get("gaps", [])) > 0


# ---------------------------------------------------------------------------
# Invalid Examples
# ---------------------------------------------------------------------------

class TestInvalidExamples:
    def test_hidden_apply_example_fails_guard_check(self):
        from odin.agent_operator.guards import check_forbidden_actions
        packet = load_json(EXAMPLES / "agent_work_packet.invalid.hidden_apply.json")
        result = check_forbidden_actions(packet)
        assert result["status"] == "blocked", (
            f"Expected blocked for hidden_apply invalid example, got: {result}"
        )
        violations = result.get("violations", [])
        assert any("hidden_tool_execution_allowed" in v or "app_owned_apply" in v for v in violations), (
            f"Expected violation for hidden_tool_execution_allowed or app_owned_apply, got: {violations}"
        )

    def test_external_send_example_fails_guard_check(self):
        from odin.agent_operator.guards import check_forbidden_actions
        packet = load_json(EXAMPLES / "agent_work_packet.invalid.external_send.json")
        result = check_forbidden_actions(packet)
        assert result["status"] == "blocked", (
            f"Expected blocked for external_send invalid example, got: {result}"
        )
        violations = result.get("violations", [])
        assert any("external_send_default" in v for v in violations), (
            f"Expected external_send_default violation, got: {violations}"
        )

    def test_provider_api_permission_card_fails_validate(self):
        from odin.agent_operator.guards import validate_permission_card
        card = load_json(EXAMPLES / "agent_permission_card.invalid.provider_api.json")
        result = validate_permission_card(card)
        assert result["status"] == "blocked", (
            f"Expected blocked for provider_api invalid card, got: {result}"
        )
        violations = result.get("violations", [])
        assert any("may_call_provider_api" in v for v in violations), (
            f"Expected may_call_provider_api violation, got: {violations}"
        )

    def test_hidden_apply_example_fails_packet_validation(self):
        from odin.agent_operator.packets import validate_agent_work_packet
        packet = load_json(EXAMPLES / "agent_work_packet.invalid.hidden_apply.json")
        result = validate_agent_work_packet(packet)
        assert result["status"] == "invalid"


# ---------------------------------------------------------------------------
# Permission Card Hard Defaults
# ---------------------------------------------------------------------------

class TestPermissionCardDefaults:
    def _valid_card(self) -> dict:
        return load_json(EXAMPLES / "codex_work_packet.valid.json").get("permission_card") or {
            "artifact_kind": "odin_agent_operator_permission_card",
            "schema_version": "1.0",
            "permission_card_id": "PC-TEST-001",
            "agent_profile_id": "codex",
            "may_read_files": True,
            "may_edit_files": True,
            "may_run_commands": True,
            "may_create_pr": True,
            "may_apply_app_state": False,
            "may_send_external": False,
            "may_call_provider_api": False,
            "may_use_hidden_tools": False,
            "may_mutate_domain_state": False,
            "allowed_file_patterns": [],
            "forbidden_file_patterns": [],
            "allowed_command_patterns": [],
            "forbidden_command_patterns": [],
            "required_approval_for": [],
            "proof_boundary": "candidate_only",
            "claim_boundary": "test_card",
        }

    def test_valid_card_passes(self):
        from odin.agent_operator.guards import validate_permission_card
        card = self._valid_card()
        result = validate_permission_card(card)
        assert result["status"] == "ok"

    def test_app_apply_denied(self):
        from odin.agent_operator.guards import validate_permission_card
        card = self._valid_card()
        card["may_apply_app_state"] = True
        result = validate_permission_card(card)
        assert result["status"] == "blocked"

    def test_external_send_denied(self):
        from odin.agent_operator.guards import validate_permission_card
        card = self._valid_card()
        card["may_send_external"] = True
        result = validate_permission_card(card)
        assert result["status"] == "blocked"

    def test_provider_api_denied(self):
        from odin.agent_operator.guards import validate_permission_card
        card = self._valid_card()
        card["may_call_provider_api"] = True
        result = validate_permission_card(card)
        assert result["status"] == "blocked"

    def test_hidden_tools_denied(self):
        from odin.agent_operator.guards import validate_permission_card
        card = self._valid_card()
        card["may_use_hidden_tools"] = True
        result = validate_permission_card(card)
        assert result["status"] == "blocked"

    def test_domain_state_denied(self):
        from odin.agent_operator.guards import validate_permission_card
        card = self._valid_card()
        card["may_mutate_domain_state"] = True
        result = validate_permission_card(card)
        assert result["status"] == "blocked"


# ---------------------------------------------------------------------------
# Return Report
# ---------------------------------------------------------------------------

class TestReturnReport:
    def test_skeleton_has_required_fields(self):
        from odin.agent_operator.returns import build_return_report_skeleton
        report = build_return_report_skeleton("AWP-TEST-001", "codex")
        assert report["artifact_kind"] == "odin_agent_return_report"
        assert report["schema_version"] == "1.0"
        assert report["packet_id"] == "AWP-TEST-001"
        assert report["agent_profile_id"] == "codex"
        assert report["ready_for_review"] is False
        assert len(report["proof_boundaries"]) > 0
        assert "no_app_apply_by_agent" in report["proof_boundaries"]

    def test_skeleton_validates_ok(self):
        from odin.agent_operator.returns import build_return_report_skeleton, validate_return_report
        report = build_return_report_skeleton("AWP-TEST-002", "claude-code")
        result = validate_return_report(report)
        assert result["status"] == "ok", f"Skeleton validation failed: {result}"

    def test_return_report_rejects_missing_proof_boundaries(self):
        from odin.agent_operator.returns import validate_return_report
        report = {
            "artifact_kind": "odin_agent_return_report",
            "schema_version": "1.0",
            "packet_id": "AWP-TEST-003",
            "agent_profile_id": "codex",
            "implemented": [],
            "changed_files": [],
            "commands_run": [],
            "results": {},
            "skipped": [],
            "blocked": [],
            "proof_boundaries": [],
            "senior_reviewer_simulation": {
                "architecture": "x", "scope": "x", "risks": [], "verdict": "not_ready"
            },
            "senior_code_reviewer_simulation": {
                "code_repo": "x", "tests": "x", "fixes_applied": [], "verdict": "not_ready"
            },
            "ready_for_review": False,
            "claim_boundary": "test",
        }
        result = validate_return_report(report)
        assert result["status"] == "invalid"
        assert any("proof_boundaries" in e for e in result["errors"])


# ---------------------------------------------------------------------------
# CLI scaffold tests
# ---------------------------------------------------------------------------

class TestCLI:
    def test_agent_handoff_codex_emits_valid_packet(self):
        import subprocess, sys
        r = subprocess.run(
            [sys.executable, "-m", "odin.cli", "agent-handoff",
             "--agent", "codex", "--task", "README.md"],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        assert r.returncode == 0, f"agent-handoff failed:\n{r.stdout}\n{r.stderr}"
        data = json.loads(r.stdout)
        assert data.get("artifact_kind") == "odin_agent_work_packet"
        assert data.get("candidate_only") is True
        assert data.get("app_owned_apply") is True
        assert data.get("hidden_tool_execution_allowed") is False

    def test_agent_handoff_claude_code_emits_valid_packet(self):
        import subprocess, sys
        r = subprocess.run(
            [sys.executable, "-m", "odin.cli", "agent-handoff",
             "--agent", "claude-code", "--task", "README.md"],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        assert r.returncode == 0, f"agent-handoff claude-code failed:\n{r.stdout}\n{r.stderr}"
        data = json.loads(r.stdout)
        assert data.get("agent_profile_id") == "claude-code"
        assert data.get("candidate_only") is True

    def test_agent_guard_blocks_invalid_packet(self):
        import subprocess, sys, tempfile, os
        packet_path = str(EXAMPLES / "agent_work_packet.invalid.hidden_apply.json")
        r = subprocess.run(
            [sys.executable, "-m", "odin.cli", "agent-guard", "--packet", packet_path],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        assert r.returncode != 0 or "blocked" in r.stdout, (
            f"agent-guard should block invalid packet:\n{r.stdout}\n{r.stderr}"
        )

    def test_agent_proof_reports_missing_receipts(self):
        import subprocess, sys
        packet_path = str(EXAMPLES / "future_local_agent_work_packet.valid.json")
        r = subprocess.run(
            [sys.executable, "-m", "odin.cli", "agent-proof", "--packet", packet_path],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        assert r.returncode == 0, f"agent-proof failed:\n{r.stdout}\n{r.stderr}"
        data = json.loads(r.stdout)
        assert "claim_boundary" in data

    def test_agent_return_emits_skeleton(self):
        import subprocess, sys
        packet_path = str(EXAMPLES / "codex_work_packet.valid.json")
        r = subprocess.run(
            [sys.executable, "-m", "odin.cli", "agent-return", "--packet", packet_path],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        assert r.returncode == 0, f"agent-return failed:\n{r.stdout}\n{r.stderr}"
        data = json.loads(r.stdout)
        assert data.get("artifact_kind") == "odin_agent_return_report"
        assert data.get("ready_for_review") is False

    def test_validate_agent_operator_mode_passes(self):
        import subprocess, sys
        r = subprocess.run(
            [sys.executable, "-m", "odin.cli", "validate-agent-operator-mode"],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        assert r.returncode == 0, (
            f"validate-agent-operator-mode failed:\n{r.stdout}\n{r.stderr}"
        )
