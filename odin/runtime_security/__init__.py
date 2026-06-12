"""Runtime security smoke checks — FINAL-PR-04.

Claim boundary: runtime_security_smoke_not_security_certification
candidate_only: true
"""
from __future__ import annotations

from .smoke import run_runtime_security_smoke, RuntimeSecuritySmokeResult

__all__ = ["run_runtime_security_smoke", "RuntimeSecuritySmokeResult"]
