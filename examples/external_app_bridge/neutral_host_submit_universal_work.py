"""Neutral External App Bridge — Submit Universal Work Example.

Claim boundary: neutral_external_app_bridge_candidate_only_no_app_apply_no_external_send_no_credentials

This example shows how a neutral host app can submit Universal Work to a locally running Odin instance
and receive a Candidate Artifact. The host app owns apply, state, and external send.

Boundary policy:
- Work submission target is localhost only (no public network default).
- Odin returns a Candidate Artifact only — not applied truth.
- The host app decides whether and how to use the candidate result.
- Odin does not apply host app state. Odin does not send externally.
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
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

ODIN_BASE_URL = "http://127.0.0.1:8877"
_FIXTURE_DIR = Path(__file__).parent

CLAIM_BOUNDARY = (
    "neutral_external_app_bridge_submit_universal_work_candidate_only_"
    "no_app_apply_no_external_send_no_credentials_localhost_only"
)


def build_neutral_universal_work_request() -> dict:
    """Build a neutral Universal Work request for bridge demonstration.

    Returns a candidate-only work packet. The host app populates real work fields.
    """
    fixture_path = _FIXTURE_DIR / "neutral_universal_work_request.valid.json"
    if fixture_path.exists():
        return json.loads(fixture_path.read_text(encoding="utf-8"))
    return {
        "candidate_only": True,
        "local_only": True,
        "external_send": False,
        "app_apply": False,
        "host_app_owns_apply": True,
        "host_app_owns_state": True,
        "host_app_owns_external_send": True,
        "arbitrary_shell_execution": False,
        "provider_execution": False,
        "credential_required": False,
        "work": {"kind": "neutral_bridge_demo", "description": "Example neutral work request."},
        "claim_boundary": CLAIM_BOUNDARY,
    }


def host_submit_universal_work(
    work_request: dict | None = None,
    base_url: str = ODIN_BASE_URL,
) -> dict:
    """Submit Universal Work to local Odin. Returns Candidate Artifact (candidate-only).

    The candidate result is NOT applied truth. The host app decides what to do with it.
    Odin does not apply host app state. Odin does not send externally.
    """
    _assert_localhost(base_url)

    if work_request is None:
        work_request = build_neutral_universal_work_request()

    payload = json.dumps({"work": work_request.get("work", work_request)}).encode("utf-8")
    url = base_url.rstrip("/") + "/v1/universal-work"
    req = Request(url, data=payload, method="POST", headers={"Content-Type": "application/json"})

    try:
        with urlopen(req, timeout=10) as resp:
            candidate = json.loads(resp.read().decode("utf-8"))
            return {
                "status": "candidate_received",
                "candidate_artifact": candidate,
                "candidate_only": True,
                "applied_truth": False,
                "host_app_owns_apply": True,
                "host_app_owns_state": True,
                "host_app_owns_external_send": True,
                "note": (
                    "Candidate artifact received. This is not applied truth. "
                    "Host app decides whether to use this result."
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
    except URLError as exc:
        return {
            "status": "simulated_candidate",
            "note": "Odin local runtime not reachable. Returning simulated fixture as demonstration.",
            "candidate_artifact": {
                "candidate_only": True,
                "applied_truth": False,
                "app_state_mutated": False,
                "external_send": False,
                "artifact": {"kind": "neutral_bridge_demo_candidate", "result": "Simulated candidate output."},
            },
            "candidate_only": True,
            "applied_truth": False,
            "host_app_owns_apply": True,
            "host_app_owns_state": True,
            "host_app_owns_external_send": True,
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
    work_request = build_neutral_universal_work_request()
    result = host_submit_universal_work(work_request)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    print()
    print("--- Boundary Notice ---")
    print("Candidate artifact received. This is NOT applied truth.")
    print("Host app owns apply, state, and external send.")
    print("Odin does not apply host app state. Odin does not send externally.")
    print("This is not a hosted bridge. This is not a public network gateway.")
    print("This does not prove production readiness or security certification.")
