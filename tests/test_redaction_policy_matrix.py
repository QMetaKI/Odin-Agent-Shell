"""Tests for redaction policy test matrix (LRH-PR-18).

Claim boundary: redaction_policy_test_matrix_not_security_certification
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registries" / "redaction_policy_test_matrix_v1.json"
EXAMPLES = ROOT / "examples" / "redaction_policy"

REQUIRED_CATEGORIES = ["api_keys", "passwords", "private_keys", "tokens", "connection_strings"]


def _data() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


class TestRedactionPolicyRegistryStructure:
    def test_registry_exists(self):
        assert REGISTRY.exists()

    def test_registry_valid_json(self):
        data = _data()
        assert isinstance(data, dict)

    def test_has_registry_id(self):
        assert "registry_id" in _data()

    def test_has_version(self):
        assert "version" in _data()

    def test_has_redaction_categories(self):
        data = _data()
        assert "redaction_categories" in data
        assert len(data["redaction_categories"]) > 0

    def test_has_not_proven(self):
        data = _data()
        assert "not_proven" in data
        assert "redaction_guarantee" in data["not_proven"]

    def test_has_proof_boundaries(self):
        data = _data()
        assert "proof_boundaries" in data
        assert "not_redaction_guarantee" in data["proof_boundaries"]
        assert "not_security_certification" in data["proof_boundaries"]

    def test_candidate_only(self):
        assert _data().get("candidate_only") is True

    def test_local_only(self):
        assert _data().get("local_only") is True


class TestRequiredCategoriesPresent:
    def test_required_category_ids_present(self):
        data = _data()
        cat_ids = [c["id"] for c in data["redaction_categories"]]
        for req in REQUIRED_CATEGORIES:
            assert req in cat_ids, f"Missing required category: {req}"


class TestCategoryStructure:
    def test_each_category_has_id(self):
        for cat in _data()["redaction_categories"]:
            assert "id" in cat

    def test_each_category_has_policy(self):
        for cat in _data()["redaction_categories"]:
            assert "redaction_policy" in cat

    def test_api_keys_always_redact(self):
        cats = {c["id"]: c for c in _data()["redaction_categories"]}
        assert cats["api_keys"]["redaction_policy"] == "always_redact"

    def test_passwords_always_redact(self):
        cats = {c["id"]: c for c in _data()["redaction_categories"]}
        assert cats["passwords"]["redaction_policy"] == "always_redact"


class TestBoundaryPhrases:
    def test_no_secret_guarantee_claim(self):
        data = _data()
        assert "redaction_guarantee" in data["not_proven"]

    def test_no_security_certification_claim(self):
        data = _data()
        assert "security_certification" in data["not_proven"]

    def test_no_secret_leakage_impossible_claim(self):
        data = _data()
        assert "secret_leakage_impossible" in data["not_proven"]

    def test_no_production_security_claim(self):
        data = _data()
        assert "production_security_proof" in data["not_proven"]


class TestSupportBundleRedactionPolicy:
    def test_support_bundle_policy_present(self):
        data = _data()
        assert "support_bundle_redaction_policy" in data

    def test_support_bundle_redacts_api_key(self):
        policy = _data()["support_bundle_redaction_policy"]
        assert "api_key" in policy.get("redact_keys", [])

    def test_support_bundle_redacts_password(self):
        policy = _data()["support_bundle_redaction_policy"]
        assert "password" in policy.get("redact_keys", [])


class TestExampleFixtures:
    def test_redaction_example_dir_exists(self):
        assert EXAMPLES.exists()

    def test_api_key_example_exists(self):
        assert (EXAMPLES / "api_key_redaction.example.json").exists()

    def test_api_key_example_valid_json(self):
        data = json.loads((EXAMPLES / "api_key_redaction.example.json").read_text())
        assert isinstance(data, dict)

    def test_api_key_example_candidate_only(self):
        data = json.loads((EXAMPLES / "api_key_redaction.example.json").read_text())
        assert data.get("candidate_only") is True

    def test_api_key_example_no_real_key(self):
        text = (EXAMPLES / "api_key_redaction.example.json").read_text()
        assert "[REDACTED]" in text

    def test_api_key_example_has_claim_boundary(self):
        data = json.loads((EXAMPLES / "api_key_redaction.example.json").read_text())
        assert "claim_boundary" in data

    def test_api_key_example_not_proven_list(self):
        data = json.loads((EXAMPLES / "api_key_redaction.example.json").read_text())
        assert "not_proven" in data
        assert "redaction_guarantee" in data["not_proven"]
