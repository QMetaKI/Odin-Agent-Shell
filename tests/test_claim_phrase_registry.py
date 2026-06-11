"""Tests for claim phrase registry (LRH-PR-18).

Claim boundary: claim_phrase_registry_local_wording_policy_not_automated_scanner
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registries" / "claim_phrase_registry_v1.json"


def _data() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


class TestClaimPhraseRegistryStructure:
    def test_registry_exists(self):
        assert REGISTRY.exists()

    def test_registry_valid_json(self):
        data = _data()
        assert isinstance(data, dict)

    def test_has_registry_id(self):
        assert "registry_id" in _data()

    def test_has_version(self):
        assert "version" in _data()

    def test_has_forbidden_positive_overclaims(self):
        data = _data()
        assert "forbidden_positive_overclaims" in data
        assert len(data["forbidden_positive_overclaims"]) > 0

    def test_has_allowed_negated_phrases(self):
        data = _data()
        assert "allowed_negated_phrases" in data
        assert len(data["allowed_negated_phrases"]) > 0

    def test_has_allowed_scoped_phrases(self):
        data = _data()
        assert "allowed_scoped_phrases" in data
        assert len(data["allowed_scoped_phrases"]) > 0


class TestForbiddenPositiveOverclaims:
    def test_fully_proven_is_forbidden(self):
        assert "fully proven" in _data()["forbidden_positive_overclaims"]

    def test_certified_is_forbidden(self):
        assert "certified" in _data()["forbidden_positive_overclaims"]

    def test_production_ready_is_forbidden(self):
        overclaims = _data()["forbidden_positive_overclaims"]
        # Check that some production affirmative phrase is forbidden
        assert any("production" in p for p in overclaims)

    def test_guaranteed_is_forbidden(self):
        assert "guaranteed" in _data()["forbidden_positive_overclaims"]

    def test_security_certified_is_forbidden(self):
        assert "security certified" in _data()["forbidden_positive_overclaims"]

    def test_release_ready_is_forbidden(self):
        assert "release ready" in _data()["forbidden_positive_overclaims"]

    def test_target_host_proven_is_forbidden(self):
        assert "target-host proven" in _data()["forbidden_positive_overclaims"]

    def test_complete_proof_is_forbidden(self):
        assert "complete proof" in _data()["forbidden_positive_overclaims"]


class TestAllowedNegatedPhrases:
    def test_not_production_readiness_allowed(self):
        assert "not production readiness" in _data()["allowed_negated_phrases"]

    def test_not_release_certification_allowed(self):
        assert "not release certification" in _data()["allowed_negated_phrases"]

    def test_not_security_certification_allowed(self):
        assert "not security certification" in _data()["allowed_negated_phrases"]

    def test_not_signed_distribution_allowed(self):
        assert "not signed distribution proof" in _data()["allowed_negated_phrases"]

    def test_not_windows_service_allowed(self):
        assert "not Windows service proof" in _data()["allowed_negated_phrases"]

    def test_retained_gap_allowed(self):
        assert "retained gap" in _data()["allowed_negated_phrases"]

    def test_proof_gap_retained_allowed(self):
        assert "proof gap retained" in _data()["allowed_negated_phrases"]

    def test_non_goal_boundary_allowed(self):
        assert "non-goal boundary" in _data()["allowed_negated_phrases"]


class TestAllowedScopedPhrases:
    def test_green_allowed(self):
        assert "green" in _data()["allowed_scoped_phrases"]

    def test_passed_locally_allowed(self):
        assert "passed locally" in _data()["allowed_scoped_phrases"]

    def test_local_receipt_allowed(self):
        assert "local receipt" in _data()["allowed_scoped_phrases"]

    def test_candidate_only_allowed(self):
        assert "candidate-only" in _data()["allowed_scoped_phrases"]

    def test_ok_with_known_gaps_allowed(self):
        assert "ok_with_known_gaps" in _data()["allowed_scoped_phrases"]


class TestContextAwareRules:
    def test_context_aware_rules_present(self):
        data = _data()
        assert "context_aware_rules" in data

    def test_scripts_code_is_strict(self):
        rules = _data()["context_aware_rules"]
        assert "scripts_and_code" in rules
        assert "strict" in rules["scripts_and_code"].lower()

    def test_docs_allow_negated_phrases(self):
        rules = _data()["context_aware_rules"]
        assert "docs" in rules
        assert "negated" in rules["docs"].lower() or "allow" in rules["docs"].lower()

    def test_examples_safe_placeholders(self):
        rules = _data()["context_aware_rules"]
        assert "examples" in rules

    def test_no_false_positive_conflict_with_boundary_docs(self):
        data = _data()
        overclaims = set(data.get("forbidden_positive_overclaims", []))
        allowed_negated = set(data.get("allowed_negated_phrases", []))
        conflicts = overclaims & allowed_negated
        assert len(conflicts) == 0, f"Conflict between forbidden and allowed: {conflicts}"
