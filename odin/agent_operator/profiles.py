"""Agent profile registry loader for Odin Agent Operator Mode."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
_REGISTRY_PATH = _ROOT / "registries" / "agent_operator_profile_registry.json"


def load_profile_registry() -> dict[str, Any]:
    """Load the agent operator profile registry from disk."""
    with _REGISTRY_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_profile(profile_id: str) -> dict[str, Any] | None:
    """Return a single agent profile by ID, or None if not found."""
    registry = load_profile_registry()
    for profile in registry.get("profiles", []):
        if profile.get("profile_id") == profile_id:
            return profile
    return None


def list_profile_ids() -> list[str]:
    """Return all registered profile IDs."""
    registry = load_profile_registry()
    return [p.get("profile_id", "") for p in registry.get("profiles", [])]
