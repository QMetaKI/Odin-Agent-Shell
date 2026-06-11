"""Neutral External App Bridge — Read Candidate Artifact Example.

Claim boundary: neutral_external_app_bridge_candidate_only_no_app_apply_no_external_send_no_credentials

This example shows how a neutral host app can read a Candidate Artifact from a locally running Odin instance.
The candidate is not applied truth. The host app owns apply, state, and external send.

Boundary policy:
- Candidate artifact read target is localhost only (no public network default).
- Odin returns a Candidate Artifact only — not applied truth.
- The host app decides whether and how to use the candidate result.
- Odin does not apply host app state. Odin does not send externally.
- No credentials are required or accepted.
- Displaying a candidate artifact does not apply it or mutate host state.
- This is not a hosted bridge. This is not a public gateway.
- This does not prove production readiness or security certification.

Known non-proofs:
- production_readiness
- live_model_inference
- app_state_mutation
- external_send_authority
- security_certification
- real_external_app_integration
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

ODIN_BASE_URL = "http://127.0.0.1:8877"
_FIXTURE_DIR = Path(__file__).parent

CLAIM_BOUNDARY = (
    "neutral_external_app_bridge_read_candidate_candidate_only_"
    "no_app_apply_no_external_send_no_credentials_localhost_only"
)


def host_read_candidate(
    candidate_id: str,
    base_url: str = ODIN_BASE_URL,
) -> dict:
    """Read a Candidate Artifact by ID from local Odin.

    Returns candidate-only result. NOT applied truth. Host app owns apply.
    Odin does not mutate host app state when this is called.
    """
    _assert_localhost(base_url)
    url = base_url.rstrip("/") + f"/v1/candidates/{candidate_id}"
    try:
        with urlopen(url, timeout=10) as resp:
            candidate = json.loads(resp.read().decode("utf-8"))
            return _wrap_candidate(candidate)
    except URLError as exc:
        fixture = _FIXTURE_DIR / "neutral_candidate_artifact_response.valid.json"
        if fixture.exists():
            candidate = json.loads(fixture.read_text(encoding="utf-8"))
            return {
                "status": "fixture_fallback",
                "note": f"Odin not reachable ({exc}). Returning fixture candidate for demonstration.",
                **_wrap_candidate(candidate),
            }
        return {
            "status": "unreachable",
            "error": str(exc),
            "candidate_only": True,
            "applied_truth": False,
            "host_app_owns_apply": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }


def host_read_candidate_from_fixture() -> dict:
    """Read the fixture Candidate Artifact for demonstration (no live Odin needed).

    Returns candidate-only result. NOT applied truth. Host app owns apply.
    """
    fixture = _FIXTURE_DIR / "neutral_candidate_artifact_response.valid.json"
    if fixture.exists():
        candidate = json.loads(fixture.read_text(encoding="utf-8"))
        return _wrap_candidate(candidate)
    return {
        "status": "fixture_missing",
        "candidate_only": True,
        "applied_truth": False,
        "host_app_owns_apply": True,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _wrap_candidate(candidate: dict) -> dict:
    return {
        "status": "candidate_read",
        "candidate_artifact": candidate,
        "candidate_only": True,
        "applied_truth": False,
        "app_state_mutated": False,
        "host_app_owns_apply": True,
        "host_app_owns_state": True,
        "host_app_owns_external_send": True,
        "note": (
            "Candidate artifact read. This is NOT applied truth. "
            "Displaying this candidate does not apply it or mutate host app state. "
            "Host app decides whether to use this result."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _assert_localhost(url: str) -> None:
    from urllib.parse import urlparse
    hostname = (urlparse(url).hostname or "").lower().strip("[]")
    if hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError(
            f"Neutral bridge base_url must be localhost (got {hostname!r}). "
            "This bridge does not support public or LAN network access by default."
        )


if __name__ == "__main__":
    result = host_read_candidate_from_fixture()
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    print()
    print("--- Boundary Notice ---")
    print("Candidate artifact read. This is NOT applied truth.")
    print("Displaying this candidate does NOT apply it or mutate host app state.")
    print("Host app owns apply, state, and external send.")
    print("Odin does not apply host app state. Odin does not send externally.")
    print("This is not a hosted bridge. This is not a public network gateway.")
    print("This does not prove production readiness or security certification.")
