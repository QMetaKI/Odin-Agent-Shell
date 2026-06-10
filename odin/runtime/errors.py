from __future__ import annotations

class OdinRuntimeError(Exception):
    """Base exception for bounded Odin runtime candidate failures."""

class OdinValidationError(OdinRuntimeError):
    """Raised when an input cannot become candidate work."""
