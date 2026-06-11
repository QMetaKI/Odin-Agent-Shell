"""Tests for LRH-PR-14 — Local Config, Redaction and Safe Settings UI.

Claim boundary: local_config_safe_settings_candidate_only_local_only_settings_visibility_only

These tests verify:
- Schema, fixture, and doc file existence
- Safe config validates correctly
- Unsafe configs are detected as unsafe
- Redaction fixture matches expected output
- Hub panel elements exist
- No forbidden controls
- CLI commands are available
- validate-all is not broken
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "odin" / "hub" / "static"


# ---------------------------------------------------------------------------
# File existence checks
# ---------------------------------------------------------------------------

def test_schema_exists():
    assert (ROOT / "schemas/v7_1/odin_local_config.schema.json").exists()


def test_safe_config_fixture_exists():
    assert (ROOT / "examples/local_config/safe_local_config.valid.json").exists()


def test_unsafe_network_config_fixture_exists():
    assert (ROOT / "examples/local_config/unsafe_network_config.invalid.json").exists()


def test_unsafe_provider_enabled_fixture_exists():
    assert (ROOT / "examples/local_config/unsafe_provider_enabled.invalid.json").exists()


def test_unsafe_raw_payload_reveal_fixture_exists():
    assert (ROOT / "examples/local_config/unsafe_raw_payload_reveal.invalid.json").exists()


def test_unsafe_redaction_disabled_fixture_exists():
    assert (ROOT / "examples/local_config/unsafe_redaction_disabled.invalid.json").exists()


def test_redaction_fixture_exists():
    assert (ROOT / "examples/local_config/redaction_fixture.valid.json").exists()


def test_redaction_expected_fixture_exists():
    assert (ROOT / "examples/local_config/redaction_expected.valid.json").exists()


def test_doc_exists():
    assert (ROOT / "docs/LOCAL_CONFIG_SAFE_SETTINGS_V1.md").exists()


def test_js_module_exists():
    assert (STATIC_DIR / "local_config_safe_settings.js").exists()


def test_test_file_exists():
    assert (ROOT / "tests/test_lrh_pr_14_local_config_safe_settings.py").exists()


# ---------------------------------------------------------------------------
# Schema file parses as valid JSON
# ---------------------------------------------------------------------------

def test_schema_is_valid_json():
    data = json.loads((ROOT / "schemas/v7_1/odin_local_config.schema.json").read_text(encoding="utf-8"))
    assert data.get("title") == "Odin Local Config"
    assert "properties" in data


# ---------------------------------------------------------------------------
# Safe config fixture checks
# ---------------------------------------------------------------------------

def _load_safe_config():
    return json.loads((ROOT / "examples/local_config/safe_local_config.valid.json").read_text(encoding="utf-8"))


def test_safe_config_parses():
    cfg = _load_safe_config()
    assert isinstance(cfg, dict)


def test_safe_config_localhost_only():
    cfg = _load_safe_config()
    assert cfg["localhost_only"] is True


def test_safe_config_bind_host():
    cfg = _load_safe_config()
    assert cfg["bind_host"] in ("127.0.0.1", "localhost", "::1")


def test_safe_config_public_network_disabled():
    cfg = _load_safe_config()
    assert cfg["public_network_enabled"] is False


def test_safe_config_external_send_disabled():
    cfg = _load_safe_config()
    assert cfg["external_send_enabled"] is False


def test_safe_config_app_apply_disabled():
    cfg = _load_safe_config()
    assert cfg["app_apply_enabled"] is False


def test_safe_config_provider_credentials_disabled():
    cfg = _load_safe_config()
    assert cfg["provider_credentials_enabled"] is False


def test_safe_config_raw_payload_reveal_disabled():
    cfg = _load_safe_config()
    assert cfg["raw_payload_reveal_enabled"] is False


def test_safe_config_redaction_enabled():
    cfg = _load_safe_config()
    assert cfg["redaction_enabled"] is True


def test_safe_config_providers_disabled_by_default():
    cfg = _load_safe_config()
    assert cfg["providers"]["enabled_by_default"] is False


def test_safe_config_candidate_only():
    cfg = _load_safe_config()
    assert cfg["candidate_only"] is True


def test_safe_config_has_claim_boundary():
    cfg = _load_safe_config()
    assert "claim_boundary" in cfg
    assert "safe" in cfg["claim_boundary"] or "local_config" in cfg["claim_boundary"]


# ---------------------------------------------------------------------------
# Unsafe config detection via shell validator
# ---------------------------------------------------------------------------

from odin.hub.shell import _lcss_check_unsafe_config


def test_unsafe_network_config_is_blocked():
    cfg = json.loads((ROOT / "examples/local_config/unsafe_network_config.invalid.json").read_text())
    reasons = _lcss_check_unsafe_config(cfg)
    assert len(reasons) > 0, "Unsafe network config should be detected as blocked"


def test_unsafe_provider_enabled_is_blocked():
    cfg = json.loads((ROOT / "examples/local_config/unsafe_provider_enabled.invalid.json").read_text())
    reasons = _lcss_check_unsafe_config(cfg)
    assert len(reasons) > 0, "Unsafe provider config should be detected as blocked"


def test_unsafe_raw_payload_reveal_is_blocked():
    cfg = json.loads((ROOT / "examples/local_config/unsafe_raw_payload_reveal.invalid.json").read_text())
    reasons = _lcss_check_unsafe_config(cfg)
    assert len(reasons) > 0, "Unsafe raw payload reveal config should be detected as blocked"


def test_unsafe_redaction_disabled_is_blocked():
    cfg = json.loads((ROOT / "examples/local_config/unsafe_redaction_disabled.invalid.json").read_text())
    reasons = _lcss_check_unsafe_config(cfg)
    assert len(reasons) > 0, "Unsafe redaction disabled config should be detected as blocked"


def test_safe_config_is_not_blocked():
    cfg = _load_safe_config()
    reasons = _lcss_check_unsafe_config(cfg)
    assert reasons == [], f"Safe config should not be blocked, got: {reasons}"


# ---------------------------------------------------------------------------
# Unsafe setting block list completeness
# ---------------------------------------------------------------------------

from odin.hub.shell import _LCSS_UNSAFE_BLOCK_LIST


def test_block_list_has_bind_host():
    fields = [item[0] for item in _LCSS_UNSAFE_BLOCK_LIST]
    assert "bind_host" in fields


def test_block_list_has_public_network():
    fields = [item[0] for item in _LCSS_UNSAFE_BLOCK_LIST]
    assert "public_network_enabled" in fields


def test_block_list_has_external_send():
    fields = [item[0] for item in _LCSS_UNSAFE_BLOCK_LIST]
    assert "external_send_enabled" in fields


def test_block_list_has_app_apply():
    fields = [item[0] for item in _LCSS_UNSAFE_BLOCK_LIST]
    assert "app_apply_enabled" in fields


def test_block_list_has_provider_credentials():
    fields = [item[0] for item in _LCSS_UNSAFE_BLOCK_LIST]
    assert "provider_credentials_enabled" in fields


def test_block_list_has_raw_payload_reveal():
    fields = [item[0] for item in _LCSS_UNSAFE_BLOCK_LIST]
    assert "raw_payload_reveal_enabled" in fields


def test_block_list_has_log_secrets():
    fields = [item[0] for item in _LCSS_UNSAFE_BLOCK_LIST]
    assert "log_secrets" in fields


def test_block_list_has_redaction_enabled():
    fields = [item[0] for item in _LCSS_UNSAFE_BLOCK_LIST]
    assert "redaction_enabled" in fields


# ---------------------------------------------------------------------------
# Redaction fixture checks — NOTE: must not print raw sensitive values
# ---------------------------------------------------------------------------

def test_redaction_fixture_contains_sensitive_keys():
    fixture = json.loads((ROOT / "examples/local_config/redaction_fixture.valid.json").read_text())
    sensitive = {"token", "secret", "password", "api_key", "credential", "auth",
                 "private", "raw_payload", "payload_raw", "sensitive"}
    found = set(fixture.keys()) & sensitive
    assert len(found) > 0, "Redaction fixture must contain sensitive-looking keys"


def test_redaction_expected_has_redacted_markers():
    expected = json.loads((ROOT / "examples/local_config/redaction_expected.valid.json").read_text())
    sensitive = {"token", "secret", "password", "api_key", "credential", "auth",
                 "private", "raw_payload", "payload_raw", "sensitive"}
    for key in sensitive:
        if key in expected:
            assert expected[key] == "[REDACTED]", f"Expected fixture: {key} should be [REDACTED]"


def test_redaction_function_produces_expected_output():
    """Apply redaction to fixture and verify output matches expected (no raw values printed)."""
    from odin.doctor.redaction import redact_recursive
    fixture = json.loads((ROOT / "examples/local_config/redaction_fixture.valid.json").read_text())
    expected = json.loads((ROOT / "examples/local_config/redaction_expected.valid.json").read_text())
    redacted = redact_recursive(fixture)
    sensitive = {"token", "secret", "password", "api_key", "credential", "auth",
                 "private", "raw_payload", "payload_raw", "sensitive"}
    for key in sensitive:
        if key in fixture:
            assert redacted.get(key) == "[REDACTED]", f"Key {key!r} was not redacted"
    # Safe fields should not be redacted
    if "host" in fixture:
        assert redacted.get("host") == fixture["host"]
    if "port" in fixture:
        assert redacted.get("port") == fixture["port"]
    # Compare against expected for sensitive keys
    for key in sensitive:
        if key in expected:
            assert redacted.get(key) == expected.get(key), f"Redacted output differs from expected for key {key!r}"


# ---------------------------------------------------------------------------
# Hub panel HTML checks
# ---------------------------------------------------------------------------

def _load_index_html():
    return (STATIC_DIR / "index.html").read_text(encoding="utf-8")


def test_hub_panel_exists():
    html = _load_index_html()
    assert "local-config-safe-settings-panel" in html


def test_hub_panel_has_config_status_surface():
    html = _load_index_html()
    assert "lcss-config-status-content" in html


def test_hub_panel_has_unsafe_block_list_surface():
    html = _load_index_html()
    assert "lcss-unsafe-block-list-content" in html


def test_hub_panel_has_redaction_status_surface():
    html = _load_index_html()
    assert "lcss-redaction-status-content" in html


def test_hub_panel_has_provider_disabled_surface():
    html = _load_index_html()
    assert "lcss-provider-disabled-content" in html


def test_hub_panel_has_proof_boundaries_surface():
    html = _load_index_html()
    assert "lcss-proof-boundaries-content" in html


def test_hub_panel_has_provider_disabled_by_default_phrase():
    html = _load_index_html().lower()
    assert "providers disabled by default" in html or "disabled by default" in html


def test_hub_panel_redaction_status_not_certification():
    html = _load_index_html().lower()
    assert "redaction status is not" in html or "not a security certification" in html


def test_hub_panel_settings_visibility_only():
    html = _load_index_html().lower()
    assert "settings visibility only" in html or "settings-visibility-only" in html


def test_hub_panel_loads_js_module():
    html = _load_index_html()
    assert "local_config_safe_settings.js" in html


def test_hub_panel_no_credential_input():
    html = _load_index_html().lower()
    assert 'type="password"' not in html or 'provider-credential' not in html


def test_hub_panel_no_provider_enable_control():
    html = _load_index_html().lower()
    assert "function enableprovider(" not in html
    assert "function disableprovider(" not in html


def test_hub_panel_no_redaction_bypass():
    html = _load_index_html().lower()
    assert "function bypassredaction(" not in html
    assert "function rawpayloadreveal(" not in html


# ---------------------------------------------------------------------------
# Documentation boundary phrase checks
# ---------------------------------------------------------------------------

def _load_doc():
    return (ROOT / "docs/LOCAL_CONFIG_SAFE_SETTINGS_V1.md").read_text(encoding="utf-8").lower()


def test_doc_no_app_apply_phrase():
    doc = _load_doc()
    assert "does not grant app apply authority" in doc


def test_doc_no_external_send_phrase():
    doc = _load_doc()
    assert "does not send externally" in doc


def test_doc_no_provider_execution():
    doc = _load_doc()
    assert "does not execute providers" in doc


def test_doc_no_credential_storage():
    doc = _load_doc()
    assert "does not store provider credentials" in doc


def test_doc_no_raw_payload():
    doc = _load_doc()
    assert "does not display raw sensitive payloads" in doc


def test_doc_no_production_readiness_claim():
    doc = _load_doc()
    assert "does not prove production readiness" in doc


def test_doc_no_security_certification_claim():
    doc = _load_doc()
    assert "does not prove security certification" in doc


def test_doc_has_proof_boundaries():
    doc = _load_doc()
    assert "proof boundaries" in doc


def test_doc_has_not_proven():
    doc = _load_doc()
    assert "not_production_readiness_certification" in doc


def test_doc_redaction_not_certification():
    doc = _load_doc()
    assert "redaction status is not a security certification" in doc


def test_doc_settings_visibility_only():
    doc = _load_doc()
    assert "settings visibility only" in doc


# ---------------------------------------------------------------------------
# Validator function tests
# ---------------------------------------------------------------------------

from odin.hub.shell import validate_local_config_safe_settings, build_local_config_safe_settings_proof_packet


def test_validate_local_config_safe_settings_passes():
    errors = validate_local_config_safe_settings()
    assert errors == [], f"Validator errors: {errors}"


def test_prove_local_config_safe_settings_status():
    packet = build_local_config_safe_settings_proof_packet()
    assert packet["status"] in ("ok", "partial")
    assert packet["candidate_only"] is True
    assert packet["local_only"] is True
    assert packet["settings_visibility_only"] is True
    assert packet["redaction_status_not_security_certification"] is True
    assert packet["provider_settings_disabled_by_default"] is True


def test_prove_packet_not_proven_list():
    packet = build_local_config_safe_settings_proof_packet()
    required_not_proven = [
        "production_readiness",
        "security_certification",
        "redaction_safety_certification",
        "provider_credential_storage",
        "app_apply_authority",
        "external_send_authority",
        "live_model_inference",
    ]
    for item in required_not_proven:
        assert item in packet["not_proven"], f"not_proven must include {item!r}"


def test_prove_packet_proof_boundaries():
    packet = build_local_config_safe_settings_proof_packet()
    pb = packet["proof_boundaries"]
    assert "not_production_readiness_certification" in pb
    assert "not_security_certification" in pb
    assert "settings_visibility_only" in pb
    assert "redaction_status_not_security_certification" in pb
    assert "provider_settings_disabled_by_default" in pb


# ---------------------------------------------------------------------------
# CLI command registration (via subparser check)
# ---------------------------------------------------------------------------

def test_cli_validate_local_config_safe_settings():
    from odin.cli import main
    rc = main(["validate-local-config-safe-settings"])
    assert rc == 0


def test_cli_prove_local_config_safe_settings():
    from odin.cli import main
    rc = main(["prove-local-config-safe-settings"])
    assert rc == 0


# ---------------------------------------------------------------------------
# Agent handoff --lrh-pr 14 smoke test
# ---------------------------------------------------------------------------

def test_agent_handoff_lrh_pr_14():
    import tempfile
    import os
    from odin.cli import main
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "lrh_pr_14_packet.json")
        rc = main(["agent-handoff", "--agent", "claude-code", "--lrh-pr", "14", "--out", out_path])
        assert rc == 0
        packet = json.loads(Path(out_path).read_text(encoding="utf-8"))
        assert packet.get("candidate_only") is True
        assert packet.get("app_owned_apply") is True
        assert packet.get("external_send_default") is False
        assert packet.get("hidden_tool_execution_allowed") is False


# ---------------------------------------------------------------------------
# Validate-all still green (does not include LRH-PR-14 validator failure)
# ---------------------------------------------------------------------------

def test_validate_all_passes():
    from odin.cli import validate_all
    errors = validate_all()
    assert errors == [], f"validate-all errors: {errors[:10]}"
