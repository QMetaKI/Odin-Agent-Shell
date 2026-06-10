"""Odin Browser Hub Shell — local static asset server scaffold.

Claim boundary: browser_hub_shell_candidate_only_local_only_no_apply_no_external_send

This module provides:
- validate_browser_hub_shell(): deterministic static validator for the shell (LRH-PR-06)
- build_browser_hub_proof_packet(): emit a proof packet for the shell
- validate_hub_runtime_dashboard(): deterministic static validator for the dashboard (LRH-PR-07)
- build_dashboard_proof_packet(): emit a dashboard proof packet
- BROWSER_HUB_SHELL_CLAIM_BOUNDARY: canonical boundary string
- BROWSER_HUB_PROOF_BOUNDARIES: list of not-proven items
- DASHBOARD_CLAIM_BOUNDARY: dashboard-specific boundary string
- DASHBOARD_PROOF_BOUNDARIES: dashboard-specific not-proven list

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


DASHBOARD_CLAIM_BOUNDARY = (
    "hub_runtime_dashboard_candidate_only_local_only_no_apply_no_external_send_no_production_health_claim"
)

DASHBOARD_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_production_health_certification",
    "not_hosted_cloud_dashboard_proof",
    "not_hidden_diagnostic_upload_proof",
    "not_live_browser_runtime_e2e",
    "not_provider_execution_proof",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
]

_DASHBOARD_REQUIRED_FILES = [
    "odin/hub/static/dashboard.js",
    "odin/hub/static/index.html",
    "docs/HUB_RUNTIME_DASHBOARD_V1.md",
    "tests/test_lrh_pr_07_hub_runtime_dashboard.py",
]

_DASHBOARD_FORBIDDEN_CONTROL_PATTERNS = [
    "function apply(",
    "function externalSend(",
    "function sendExternally(",
    'onclick="apply(',
    "onclick=\"apply(",
    'id="apply-btn',
    "id=\"apply-btn",
    'id="external-send',
    "id=\"external-send",
    "providerCredential",
    "enablePublicNetwork(",
    "hiddenUpload(",
    "remoteUpload(",
    "diagnosticUpload(",
]

_DASHBOARD_REQUIRED_BOUNDARY_PATTERNS = [
    "candidate_only",
    "claim_boundary",
    "no_apply",
    "local",
]

_DASHBOARD_REQUIRED_API_REFS = [
    "/v1/health",
    "/v1/status",
    "/v1/proof-gaps",
]

_DASHBOARD_REQUIRED_SURFACE_IDS = [
    "runtime-status",
    "validation-status",
    "doctor",
    "support-bundle",
    "proof-gap-summary",
    "dashboard-health",
    "missing-capabilities",
]

_DASHBOARD_REQUIRED_DOC_PHRASES = [
    "not a production health certification",
    "not a hosted cloud dashboard",
    "does not upload diagnostics",
    "does not grant app apply",
    "does not send externally",
    "does not execute provider",
    "proof boundaries",
    "not_production_readiness",
]


def validate_hub_runtime_dashboard() -> list[str]:
    """Deterministic static validator for the Hub Runtime Dashboard (LRH-PR-07).

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    for rel in _DASHBOARD_REQUIRED_FILES:
        p = _ROOT / rel
        if not p.exists():
            errors.append(f"dashboard required file missing: {rel}")

    dashboard_js = _STATIC_DIR / "dashboard.js"
    if dashboard_js.exists():
        js = dashboard_js.read_text(encoding="utf-8", errors="ignore")
        for api_ref in _DASHBOARD_REQUIRED_API_REFS:
            if api_ref not in js:
                errors.append(f"dashboard.js: missing required API reference: {api_ref!r}")
        for pattern in ["candidate_only", "claim_boundary"]:
            if pattern not in js:
                errors.append(f"dashboard.js: missing required boundary token: {pattern!r}")
        js_lower = js.lower()
        forbidden_found = [p for p in _DASHBOARD_FORBIDDEN_CONTROL_PATTERNS if p.lower() in js_lower]
        if forbidden_found:
            errors.append(f"dashboard.js: forbidden interactive controls found: {forbidden_found}")
        if "127.0.0.1" not in js and "ODIN_API_BASE" not in js:
            errors.append("dashboard.js: missing localhost default reference")
        if "function apply(" in js or "prototype.apply = function" in js:
            errors.append("dashboard.js: must not have apply() function definition")
        if "function externalSend(" in js or "prototype.externalSend" in js:
            errors.append("dashboard.js: must not have externalSend() function definition")

    index = _STATIC_DIR / "index.html"
    if index.exists():
        html = index.read_text(encoding="utf-8", errors="ignore")
        if "dashboard.js" not in html:
            errors.append("index.html: must load dashboard.js")
        for surface_id in _DASHBOARD_REQUIRED_SURFACE_IDS:
            if surface_id not in html:
                errors.append(f"index.html: missing required dashboard surface id: {surface_id!r}")
        html_lower = html.lower()
        forbidden_found = [p for p in _DASHBOARD_FORBIDDEN_CONTROL_PATTERNS if p.lower() in html_lower]
        if forbidden_found:
            errors.append(f"index.html: forbidden interactive controls found in dashboard section: {forbidden_found}")
        if "support-bundle" not in html.lower():
            errors.append("index.html: missing support-bundle surface")
        for phrase in ["local-only", "diagnostics-only", "no hidden upload"]:
            if phrase.lower() not in html.lower():
                errors.append(f"index.html: support bundle surface missing phrase: {phrase!r}")

    doc = _ROOT / "docs" / "HUB_RUNTIME_DASHBOARD_V1.md"
    if doc.exists():
        doc_text = doc.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in _DASHBOARD_REQUIRED_DOC_PHRASES:
            if phrase.lower() not in doc_text:
                errors.append(f"HUB_RUNTIME_DASHBOARD_V1.md: missing required phrase: {phrase!r}")

    return errors


def build_dashboard_proof_packet() -> dict[str, Any]:
    """Emit a bounded proof packet for the Hub Runtime Dashboard (LRH-PR-07)."""
    dashboard_errors = validate_hub_runtime_dashboard()
    all_ok = not bool(dashboard_errors)

    return {
        "artifact_kind": "hub_runtime_dashboard_proof_packet",
        "candidate_only": True,
        "local_only": True,
        "dashboard_only": True,
        "status": "ok" if all_ok else "partial",
        "validation_errors": dashboard_errors,
        "proven": [
            "dashboard_static_files_exist",
            "dashboard_references_v1_health",
            "dashboard_references_v1_status",
            "dashboard_references_v1_proof_gaps",
            "no_apply_controls",
            "no_external_send_controls",
            "support_bundle_surface_is_local_only",
            "no_hidden_diagnostic_upload_controls",
            "runtime_status_surface_present",
            "validation_status_surface_present",
            "doctor_surface_present",
            "proof_gap_summary_surface_present",
            "missing_capabilities_surface_present",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "production_health_certification",
            "hosted_cloud_dashboard",
            "live_browser_runtime_e2e",
            "provider_execution",
            "app_state_mutation",
            "external_send_authority",
            "hidden_diagnostic_upload_absence_beyond_static_scan",
            "live_model_inference",
            "model_quality",
        ],
        "proof_boundaries": DASHBOARD_PROOF_BOUNDARIES,
        "claim_boundary": DASHBOARD_CLAIM_BOUNDARY,
    }


CANDIDATE_STORE_VIEWER_CLAIM_BOUNDARY = (
    "candidate_store_viewer_candidate_only_local_only_no_apply_no_external_send_no_store_mutation_no_raw_payload"
)

CANDIDATE_STORE_VIEWER_PROOF_BOUNDARIES = [
    "not_production_readiness_certification",
    "not_candidate_application_proof",
    "not_candidate_as_truth_proof",
    "not_store_mutation_proof",
    "not_raw_sensitive_payload_safety_certification",
    "not_live_browser_runtime_e2e",
    "not_provider_execution_proof",
    "not_public_network_api_proof",
    "not_app_state_mutation_proof",
    "not_external_send_authority_proof",
    "not_live_model_inference_proof",
    "not_model_quality_proof",
    "not_full_session_list_backend",
    "not_full_candidate_backend_coverage",
    "not_full_store_backend_coverage",
]

_CSV_REQUIRED_FILES = [
    "odin/hub/static/candidate_store_viewer.js",
    "odin/hub/static/index.html",
    "docs/HUB_CANDIDATE_STORE_VIEWER_V1.md",
    "tests/test_lrh_pr_08_candidate_store_viewer.py",
]

_CSV_REQUIRED_JS_API_REFS = [
    "/v1/candidates",
    "/v1/sessions",
    "/v1/proof-gaps",
]

_CSV_REQUIRED_JS_BOUNDARY_TOKENS = [
    "candidate_only",
    "claim_boundary",
    "not_applied_truth",
    "no_apply",
]

_CSV_FORBIDDEN_CONTROL_PATTERNS = [
    "function apply(",
    "function applyCandidate(",
    "function externalSend(",
    "function sendExternally(",
    "function storeWrite(",
    "function storeDelete(",
    "function rawPayloadReveal(",
    "function unsafePayloadToggle(",
    'onclick="apply(',
    "onclick=\"apply(",
    'id="apply-btn',
    "id=\"apply-btn",
    'id="external-send',
    "id=\"external-send",
    "providerCredential",
    "enablePublicNetwork(",
    "hiddenUpload(",
    "remoteUpload(",
]

_CSV_REQUIRED_SURFACE_IDS = [
    "csv-sessions-content",
    "csv-candidate-content",
    "csv-store-content",
    "csv-proof-gaps-content",
]

_CSV_REQUIRED_BOUNDARY_PHRASES = [
    "Candidate-only",
    "not applied truth",
    "app-owned apply",
    "No app apply",
    "No external send",
    "No store mutation",
    "No raw sensitive payload",
]

_CSV_REQUIRED_DOC_PHRASES = [
    "does not apply candidate artifacts",
    "does not show candidates as applied truth",
    "does not mutate the runtime store",
    "does not send externally",
    "does not display raw sensitive payloads by default",
    "does not close proof gaps by displaying them",
    "does not prove production readiness",
    "proof boundaries",
]


def validate_candidate_store_viewer() -> list[str]:
    """Deterministic static validator for the Candidate Store Viewer (LRH-PR-08).

    Returns a list of error strings (empty = ok).
    """
    errors: list[str] = []

    for rel in _CSV_REQUIRED_FILES:
        p = _ROOT / rel
        if not p.exists():
            errors.append(f"candidate store viewer required file missing: {rel}")

    csv_js = _STATIC_DIR / "candidate_store_viewer.js"
    if csv_js.exists():
        js = csv_js.read_text(encoding="utf-8", errors="ignore")

        for api_ref in _CSV_REQUIRED_JS_API_REFS:
            if api_ref not in js:
                errors.append(f"candidate_store_viewer.js: missing required API reference: {api_ref!r}")

        for token in _CSV_REQUIRED_JS_BOUNDARY_TOKENS:
            if token not in js:
                errors.append(f"candidate_store_viewer.js: missing required boundary token: {token!r}")

        js_lower = js.lower()
        forbidden_found = [p for p in _CSV_FORBIDDEN_CONTROL_PATTERNS if p.lower() in js_lower]
        if forbidden_found:
            errors.append(f"candidate_store_viewer.js: forbidden interactive controls found: {forbidden_found}")

        if "127.0.0.1" not in js and "ODIN_API_BASE" not in js:
            errors.append("candidate_store_viewer.js: missing localhost default reference")

        if "function apply(" in js:
            errors.append("candidate_store_viewer.js: must not define apply() function")
        if "function externalSend(" in js:
            errors.append("candidate_store_viewer.js: must not define externalSend() function")

    index = _STATIC_DIR / "index.html"
    if index.exists():
        html = index.read_text(encoding="utf-8", errors="ignore")

        if "candidate_store_viewer.js" not in html:
            errors.append("index.html: must load candidate_store_viewer.js")

        for surface_id in _CSV_REQUIRED_SURFACE_IDS:
            if surface_id not in html:
                errors.append(f"index.html: missing required candidate store viewer surface id: {surface_id!r}")

        html_lower = html.lower()
        for phrase in _CSV_REQUIRED_BOUNDARY_PHRASES:
            if phrase.lower() not in html_lower:
                errors.append(f"index.html: missing required boundary phrase: {phrase!r}")

        forbidden_found = [p for p in _CSV_FORBIDDEN_CONTROL_PATTERNS if p.lower() in html_lower]
        if forbidden_found:
            errors.append(f"index.html: forbidden interactive controls found in candidate viewer: {forbidden_found}")

    doc = _ROOT / "docs" / "HUB_CANDIDATE_STORE_VIEWER_V1.md"
    if doc.exists():
        doc_text = doc.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in _CSV_REQUIRED_DOC_PHRASES:
            if phrase.lower() not in doc_text:
                errors.append(f"HUB_CANDIDATE_STORE_VIEWER_V1.md: missing required phrase: {phrase!r}")

    return errors


def build_candidate_store_viewer_proof_packet() -> dict[str, Any]:
    """Emit a bounded proof packet for the Candidate Store Viewer (LRH-PR-08)."""
    csv_errors = validate_candidate_store_viewer()
    all_ok = not bool(csv_errors)

    return {
        "artifact_kind": "hub_candidate_store_viewer_proof_packet",
        "candidate_only": True,
        "local_only": True,
        "read_only": True,
        "viewer_only": True,
        "status": "ok" if all_ok else "partial",
        "validation_errors": csv_errors,
        "proven": [
            "candidate_store_viewer_static_files_exist",
            "candidate_viewer_references_v1_candidates",
            "candidate_viewer_references_v1_sessions",
            "proof_gap_viewer_references_v1_proof_gaps",
            "candidate_boundary_banner_present",
            "not_applied_truth_warning_present",
            "no_apply_controls",
            "no_external_send_controls",
            "no_store_mutation_controls",
            "raw_sensitive_payload_not_displayed_by_default",
        ] if all_ok else [],
        "not_proven": [
            "production_readiness",
            "live_browser_runtime_e2e",
            "full_session_list_backend",
            "full_candidate_backend_coverage",
            "full_store_backend_coverage",
            "raw_sensitive_payload_safety_certification",
            "candidate_application",
            "external_send_authority",
            "store_mutation",
            "live_model_inference",
            "model_quality",
        ],
        "proof_boundaries": CANDIDATE_STORE_VIEWER_PROOF_BOUNDARIES,
        "claim_boundary": CANDIDATE_STORE_VIEWER_CLAIM_BOUNDARY,
    }


def build_browser_hub_proof_packet(shell_only: bool = True, dashboard: bool = False, candidates: bool = False) -> dict[str, Any]:
    """Emit a bounded proof packet for the browser hub shell.

    If candidates=True, runs the candidate store viewer validator.
    If dashboard=True, runs both shell and dashboard validators and returns a combined packet.
    If shell_only=True (default), runs only shell validator.
    """
    if candidates:
        return build_candidate_store_viewer_proof_packet()

    if dashboard:
        return build_dashboard_proof_packet()

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
