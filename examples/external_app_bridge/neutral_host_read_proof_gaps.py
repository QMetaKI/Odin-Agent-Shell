"""Neutral External App Bridge — Read Proof Gaps Example.

Claim boundary: neutral_external_app_bridge_candidate_only_no_app_apply_no_external_send_no_credentials

This example shows how a neutral host app can read the proof gaps from a locally running Odin instance.
Reading proof gaps does not close them. Known non-proofs remain non-proofs.

Boundary policy:
- Proof gap read target is localhost only (no public network default).
- Odin returns a proof gap summary — known non-proofs remain non-proofs.
- Displaying proof gaps does not close them. They are informational only.
- The host app reads gaps and makes its own decisions about risk/completeness.
- Odin does not apply host app state. Odin does not send externally.
- No credentials are required or accepted.
- This is not a hosted bridge. This is not a public gateway.
- This does not prove production readiness or security certification.

Known non-proofs (always present, never closed by this example):
- production_readiness
- live_model_inference
- app_state_mutation
- external_send_authority
- security_certification
- real_external_app_integration
"""

from __future__ import annotations

import json
from urllib.request import urlopen
from urllib.error import URLError

ODIN_BASE_URL = "http://127.0.0.1:8877"

CLAIM_BOUNDARY = (
    "neutral_external_app_bridge_read_proof_gaps_candidate_only_"
    "no_app_apply_no_external_send_no_credentials_localhost_only"
)

KNOWN_NON_PROOFS = [
    "production_readiness",
    "live_model_inference",
    "app_state_mutation",
    "external_send_authority",
    "security_certification",
    "real_external_app_integration",
    "hosted_bridge",
    "public_gateway",
    "credential_handling",
    "provider_execution",
    "model_quality",
]


def host_read_proof_gaps(base_url: str = ODIN_BASE_URL) -> dict:
    """Read proof gaps from local Odin.

    Displaying proof gaps does NOT close them.
    Known non-proofs remain non-proofs regardless of this call.
    """
    _assert_localhost(base_url)
    url = base_url.rstrip("/") + "/v1/proof-gaps"
    try:
        with urlopen(url, timeout=10) as resp:
            gaps = json.loads(resp.read().decode("utf-8"))
            return _wrap_gaps(gaps, "live")
    except URLError as exc:
        return _wrap_gaps(
            {
                "status": "unreachable",
                "note": f"Odin not reachable ({exc}). Known non-proofs shown from static policy.",
            },
            "static_policy_fallback",
        )


def _wrap_gaps(gaps: dict, source: str) -> dict:
    return {
        "status": "proof_gaps_read",
        "gaps_source": source,
        "odin_response": gaps,
        "known_non_proofs": KNOWN_NON_PROOFS,
        "gaps_closed_by_this_read": False,
        "candidate_only": True,
        "host_app_owns_apply": True,
        "host_app_owns_state": True,
        "host_app_owns_external_send": True,
        "note": (
            "Proof gaps are informational only. "
            "Displaying gaps does not close them. "
            "Known non-proofs remain non-proofs after this read. "
            "Host app decides its own risk posture based on these gaps."
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
    result = host_read_proof_gaps()
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    print()
    print("--- Boundary Notice ---")
    print("Proof gaps are informational only. Displaying gaps does NOT close them.")
    print("Known non-proofs remain non-proofs after this read.")
    print("Host app owns apply, state, and external send.")
    print("Odin does not apply host app state. Odin does not send externally.")
    print("This is not a hosted bridge. This is not a public network gateway.")
    print("This does not prove production readiness or security certification.")
