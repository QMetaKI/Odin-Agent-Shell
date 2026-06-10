"""Odin Browser Hub Shell — local static asset server scaffold.

Claim boundary: browser_hub_shell_candidate_only_local_only_no_apply_no_external_send

This module provides:
- validate_browser_hub_shell(): deterministic static validator
- build_browser_hub_proof_packet(): emit a proof packet for the shell
- BROWSER_HUB_SHELL_CLAIM_BOUNDARY: canonical boundary string
- BROWSER_HUB_PROOF_BOUNDARIES: list of not-proven items

Runtime serve is scaffold only — no live listen loop is claimed in LRH-PR-06.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
_HUB_DIR = Path(__file__).resolve().parent
_STATIC_DIR = _HUB_DIR / "static"
_API_CLIENT_PATH = _HUB_DIR / "api_client.js"

BROWSER_HUB_SHELL_CLAIM_BOUNDARY = (
    "browser_hub_shell_candidate_only_local_only_no_apply_no_external_send_no_provider_execution"
)

BROWSER_HUB_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_hosted_cloud_ui_proof",
    "not_auth_security_certification",
    "not_live_browser_runtime_e2e",
    "not_provider_execution_proof",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
]

# Patterns that must NOT appear as interactive controls
_FORBIDDEN_CONTROL_PATTERNS = [
    "onclick=\"apply(",
    'onclick="apply(',
    "id=\"apply-btn",
    'id="apply-btn',
    "id=\"external-send",
    'id="external-send',
    "function apply()",
    "function externalSend()",
    "function sendExternally()",
    "providerCredential",
    "enablePublicNetwork()",
]

# Patterns that must be present in index.html
_REQUIRED_BOUNDARY_PATTERNS = [
    "Localhost only",
    "Candidate-only",
    "No app apply",
    "No external send",
    "No provider execution",
]

_REQUIRED_NAV_ITEMS = [
    "health",
    "status",
    "proof-gap",
]

_DEFAULT_API_BASE = "http://127.0.0.1:8877"


def validate_browser_hub_shell() -> list[str]:
    """Deterministic static validator for the browser hub shell.

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    # File existence checks
    required_files = [
        _STATIC_DIR / "index.html",
        _STATIC_DIR / "styles.css",
        _STATIC_DIR / "app.js",
        _API_CLIENT_PATH,
        _HUB_DIR / "shell.py",
        _ROOT / "docs" / "BROWSER_ODIN_HUB_SHELL_V1.md",
        _ROOT / "tests" / "test_lrh_pr_06_browser_hub_shell.py",
    ]
    for p in required_files:
        if not p.exists():
            errors.append(f"browser hub shell file missing: {p.relative_to(_ROOT)}")

    index = _STATIC_DIR / "index.html"
    if index.exists():
        html = index.read_text(encoding="utf-8", errors="ignore")

        # Boundary banner required patterns
        for pattern in _REQUIRED_BOUNDARY_PATTERNS:
            if pattern not in html:
                errors.append(f"index.html: missing required boundary text: {pattern!r}")

        # Navigation items
        for nav in _REQUIRED_NAV_ITEMS:
            if nav not in html.lower():
                errors.append(f"index.html: missing navigation item: {nav!r}")

        # Universal Work Playground placeholder must be present
        if "universal" not in html.lower() and "playground" not in html.lower():
            errors.append("index.html: missing Universal Work Playground placeholder")

        # Forbidden interactive controls
        html_lower = html.lower()
        forbidden_found = [p for p in _FORBIDDEN_CONTROL_PATTERNS if p.lower() in html_lower]
        if forbidden_found:
            errors.append(f"index.html: forbidden interactive controls found: {forbidden_found}")

    api_client = _API_CLIENT_PATH
    if api_client.exists():
        js = api_client.read_text(encoding="utf-8", errors="ignore")

        # Must reference localhost default
        if "127.0.0.1" not in js:
            errors.append("api_client.js: missing 127.0.0.1 default base URL")

        # Must reference /v1 paths
        for path in ["/v1/health", "/v1/status", "/v1/proof-gaps"]:
            if path not in js:
                errors.append(f"api_client.js: missing required path reference: {path!r}")

        # Must NOT have apply or externalSend as callable methods
        if "function apply(" in js or ".prototype.apply = function" in js:
            errors.append("api_client.js: must not have apply() method")
        if "function externalSend(" in js or "prototype.externalSend" in js or "prototype.external_send" in js:
            errors.append("api_client.js: must not have externalSend() method")

        # Must NOT default to non-localhost URL
        if "0.0.0.0" in js:
            errors.append("api_client.js: must not reference 0.0.0.0")

    # Docs boundary checks
    doc = _ROOT / "docs" / "BROWSER_ODIN_HUB_SHELL_V1.md"
    if doc.exists():
        doc_text = doc.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in [
            "not a hosted cloud ui",
            "not a public network api",
            "does not grant app apply",
            "does not send externally",
            "does not execute provider",
            "proof boundaries",
            "not_production_readiness",
        ]:
            if phrase not in doc_text:
                errors.append(f"BROWSER_ODIN_HUB_SHELL_V1.md: missing required phrase: {phrase!r}")

    return errors


def build_browser_hub_proof_packet(shell_only: bool = True) -> dict[str, Any]:
    """Emit a bounded proof packet for the browser hub shell."""
    errors = validate_browser_hub_shell()
    all_ok = not bool(errors)

    return {
        "artifact_kind": "browser_hub_shell_proof_packet",
        "candidate_only": True,
        "local_only": True,
        "shell_only": shell_only,
        "status": "ok" if all_ok else "partial",
        "validation_errors": errors,
        "proven": [
            "static_shell_files_exist",
            "local_api_client_references_v1_contract",
            "no_apply_controls",
            "no_external_send_controls",
            "boundary_banner_present",
            "navigation_shell_present",
            "localhost_default_enforced",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "hosted_cloud_ui",
            "auth_security_certification",
            "live_browser_runtime_e2e",
            "provider_execution",
            "app_state_mutation",
            "external_send_authority",
            "live_model_inference",
            "model_quality",
        ],
        "proof_boundaries": BROWSER_HUB_PROOF_BOUNDARIES,
        "claim_boundary": BROWSER_HUB_SHELL_CLAIM_BOUNDARY,
    }
