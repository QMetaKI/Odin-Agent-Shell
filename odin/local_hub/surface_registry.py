"""Hub Surface Registry — FINAL-PR-03.

Defines the canonical surface ownership model for 8765/8877/8878.
No destructive merge. Documents ownership only.

Claim boundary: hub_surface_registry_local_only_no_app_apply_no_external_send
"""
from __future__ import annotations

CLAIM_BOUNDARY = "hub_surface_registry_local_only_no_app_apply_no_external_send"

SURFACES = [
    {
        "port": 8765,
        "role": "canonical_normal_user_entry",
        "description": "Simple Local Runtime Hub — canonical normal-user entry point. FINAL-PR-01+.",
        "owner": "odin.local_hub.server",
        "is_canonical_entry": True,
        "local_only": True,
        "candidate_only": True,
    },
    {
        "port": 8877,
        "role": "local_api_daemon",
        "description": "Local API daemon / backend capability surface. Existing LRH-PR-05.",
        "owner": "odin.daemon.local_api",
        "is_canonical_entry": False,
        "local_only": True,
        "candidate_only": True,
    },
    {
        "port": 8878,
        "role": "browser_hub_shell",
        "description": "Browser hub shell / legacy-or-dev shell surface. Existing LRH-PR-06.",
        "owner": "odin.hub.shell",
        "is_canonical_entry": False,
        "local_only": True,
        "candidate_only": True,
    },
]

_SURFACE_MAP = {s["port"]: s for s in SURFACES}


def get_surface(port: int) -> dict | None:
    return _SURFACE_MAP.get(port)


def list_surfaces() -> list[dict]:
    return list(SURFACES)


def get_canonical_entry() -> dict:
    for s in SURFACES:
        if s.get("is_canonical_entry"):
            return s
    raise RuntimeError("no canonical entry surface defined")


def check_conflicts() -> dict:
    ports = [s["port"] for s in SURFACES]
    seen: set[int] = set()
    duplicates: list[int] = []
    for p in ports:
        if p in seen:
            duplicates.append(p)
        seen.add(p)
    public_bind_risk = []
    for s in SURFACES:
        if not s.get("local_only", True):
            public_bind_risk.append(s["port"])
    return {
        "artifact_kind": "odin_hub_surface_conflict_check",
        "status": "ok" if not duplicates and not public_bind_risk else "conflict",
        "duplicate_ports": duplicates,
        "public_bind_risk": public_bind_risk,
        "surfaces": SURFACES,
        "candidate_only": True,
        "local_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def surface_map_summary() -> dict:
    return {
        "artifact_kind": "odin_hub_surface_map",
        "surfaces": SURFACES,
        "canonical_entry_port": 8765,
        "conflict_check": check_conflicts(),
        "candidate_only": True,
        "local_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }
