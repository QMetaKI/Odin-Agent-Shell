"""Neutral External App Bridge — Health Check Example.

Claim boundary: neutral_external_app_bridge_candidate_only_no_app_apply_no_external_send_no_credentials

This example shows how a neutral host app can health-check a locally running Odin instance.

Boundary policy:
- Odin runs locally on localhost only (no public network default).
- Odin returns a candidate-only health/status response.
- The host app reads the health response and decides what to do.
- Odin does not apply app state. Odin does not send externally.
- No credentials are required or accepted.
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
import sys
from urllib.request import urlopen
from urllib.error import URLError

ODIN_BASE_URL = "http://127.0.0.1:8877"

CLAIM_BOUNDARY = (
    "neutral_external_app_bridge_health_check_candidate_only_"
    "no_app_apply_no_external_send_no_credentials_localhost_only"
)


def host_health_check(base_url: str = ODIN_BASE_URL) -> dict:
    """Health-check local Odin. Returns candidate-only status dict.

    The host app reads this result and decides its own next action.
    Odin does not apply app state. Odin does not send externally.
    """
    _assert_localhost(base_url)
    try:
        url = base_url.rstrip("/") + "/v1/health"
        with urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "status": "reached",
                "odin_response": data,
                "candidate_only": True,
                "host_app_owns_apply": True,
                "host_app_owns_state": True,
                "host_app_owns_external_send": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
    except URLError as exc:
        return {
            "status": "unreachable",
            "error": str(exc),
            "note": "Odin local runtime not reachable. This is expected if Odin is not running.",
            "candidate_only": True,
            "host_app_owns_apply": True,
            "host_app_owns_state": True,
            "host_app_owns_external_send": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }


def _assert_localhost(url: str) -> None:
    """Refuse non-localhost URLs — bridge is localhost-only by default."""
    from urllib.parse import urlparse
    hostname = (urlparse(url).hostname or "").lower().strip("[]")
    if hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError(
            f"Neutral bridge base_url must be localhost (got {hostname!r}). "
            "This bridge does not support public or LAN network access by default."
        )


if __name__ == "__main__":
    result = host_health_check()
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    print()
    print("--- Boundary Notice ---")
    print("Candidate-only health check. This is not applied truth.")
    print("Host app owns apply, state, and external send.")
    print("Odin does not apply host app state. Odin does not send externally.")
    print("This is not a hosted bridge. This is not a public network gateway.")
    print("This does not prove production readiness or security certification.")
