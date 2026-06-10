from __future__ import annotations
from odin.quality.boundaries import FORBIDDEN_OUTPUT_CLAIMS

FORBIDDEN_CLAIMS = set(FORBIDDEN_OUTPUT_CLAIMS) | {
    "tests_passed", "app_state_mutated", "external_send_complete", "model_truth",
}


def normalize_claims(claims: list[str] | None) -> list[str]:
    return [str(c).strip().lower() for c in (claims or []) if str(c).strip()]


def blocked_claims(claims: list[str] | None) -> list[str]:
    normalized = normalize_claims(claims)
    return sorted({c for c in normalized if c in FORBIDDEN_CLAIMS})


def filter_claims(claims: list[str] | None) -> tuple[list[str], list[str]]:
    normalized = normalize_claims(claims)
    blocked = set(blocked_claims(normalized))
    allowed = [c for c in normalized if c not in blocked]
    return allowed, sorted(blocked)
