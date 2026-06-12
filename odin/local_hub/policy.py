"""Localhost-only policy for Simple Local Hub — FINAL-PR-01.

Claim boundary: simple_local_hub_localhost_only_candidate_no_app_apply_no_external_send
"""
from __future__ import annotations

ALLOWED_HOSTS: frozenset[str] = frozenset({"127.0.0.1", "localhost", "::1"})
BLOCKED_HOSTS: frozenset[str] = frozenset({"0.0.0.0", "::", ""})

CLAIM_BOUNDARY = "simple_local_hub_localhost_only_candidate_no_app_apply_no_external_send"


def check_host(host: str) -> tuple[bool, str]:
    """Return (ok, reason). Rejects wildcard and public bind addresses."""
    if host in BLOCKED_HOSTS:
        return False, f"host {host!r} is in blocked list — public or wildcard bind rejected"
    if host not in ALLOWED_HOSTS:
        return False, f"host {host!r} is not an allowed localhost address"
    return True, "ok"
