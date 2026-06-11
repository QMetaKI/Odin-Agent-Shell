"""Tests for forbidden control pattern registry (LRH-PR-18).

Claim boundary: forbidden_control_pattern_registry_schema_not_automated_enforcement
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registries" / "forbidden_control_pattern_registry_v1.json"

REQUIRED_CATEGORIES = [
    "app_apply",
    "external_send",
    "hidden_tool_execution",
    "public_network_bind",
    "provider_model_execution",
    "windows_service_install",
    "tray_launch",
    "installer_creation",
    "code_signing",
    "credential_exfiltration",
    "unredacted_support_bundle",
]


def _data() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


class TestForbiddenControlRegistryStructure:
    def test_registry_exists(self):
        assert REGISTRY.exists()

    def test_registry_valid_json(self):
        data = _data()
        assert isinstance(data, dict)

    def test_has_registry_id(self):
        assert "registry_id" in _data()

    def test_has_version(self):
        assert "version" in _data()

    def test_has_categories(self):
        data = _data()
        assert "categories" in data
        assert isinstance(data["categories"], dict)
        assert len(data["categories"]) > 0

    def test_has_context_rules(self):
        assert "context_rules" in _data()

    def test_has_false_positive_prevention(self):
        assert "false_positive_prevention" in _data()


class TestRequiredCategoriesPresent:
    @pytest.mark.parametrize("cat", REQUIRED_CATEGORIES)
    def test_category_present(self, cat):
        assert cat in _data()["categories"]


class TestCategoryStructure:
    def test_each_category_has_description(self):
        cats = _data()["categories"]
        for name, cat in cats.items():
            assert "description" in cat, f"{name}: missing description"

    def test_each_category_has_forbidden_in(self):
        cats = _data()["categories"]
        for name, cat in cats.items():
            assert "forbidden_in" in cat, f"{name}: missing forbidden_in"

    def test_each_category_has_patterns(self):
        cats = _data()["categories"]
        for name, cat in cats.items():
            assert "patterns" in cat, f"{name}: missing patterns"
            assert len(cat["patterns"]) > 0, f"{name}: empty patterns list"

    def test_docs_allow_negated_in_app_apply(self):
        cats = _data()["categories"]
        assert "allowed_negated_in" in cats["app_apply"]
        assert "docs" in cats["app_apply"]["allowed_negated_in"]

    def test_docs_allow_negated_in_external_send(self):
        cats = _data()["categories"]
        assert "allowed_negated_in" in cats["external_send"]
        assert "docs" in cats["external_send"]["allowed_negated_in"]

    def test_scripts_code_strict_for_app_apply(self):
        cats = _data()["categories"]
        assert "scripts" in cats["app_apply"]["forbidden_in"]
        assert "code" in cats["app_apply"]["forbidden_in"]

    def test_credential_exfiltration_strict_for_examples(self):
        cats = _data()["categories"]
        assert "examples" in cats["credential_exfiltration"]["forbidden_in"]


class TestContextRules:
    def test_scripts_code_rule_strict(self):
        rules = _data()["context_rules"]
        assert "scripts_code" in rules
        assert "strict" in rules["scripts_code"].lower()

    def test_docs_rule_allows_negated(self):
        rules = _data()["context_rules"]
        assert "docs" in rules
        assert "negated" in rules["docs"].lower() or "allow" in rules["docs"].lower()


class TestFalsePositivePrevention:
    def test_safe_negation_markers_present(self):
        fpp = _data()["false_positive_prevention"]
        assert "safe_negation_markers" in fpp
        markers = fpp["safe_negation_markers"]
        assert any("not" in m for m in markers)

    def test_no_broad_brittle_rule(self):
        fpp = _data()["false_positive_prevention"]
        assert "note" in fpp
        note = fpp["note"].lower()
        assert "negated" in note or "not" in note
