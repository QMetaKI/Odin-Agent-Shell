"""FINAL-PR-13: Thor-Agent-Kit Thanks Block Source verification.

Claim boundary: readme_v1_public_surface_documents_candidate_release_without_overclaiming
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "readme_v1_public_surface_documents_candidate_release_without_overclaiming"

THOR_THANKS_BLOCK_HEADING = "## Danke / Thank You"

THOR_THANKS_BLOCK_BODY = """Danke an Q Germany.
Danke an Q USA.
Danke an Q Worldwide.

Ohne euch wäre das alles unmöglich gewesen.

Gewidmet, dem goldenen Herzen einer einzigartigen Frau und liebenden Mama.

Y

---

Thank you to Q Germany.
Thank you to Q USA.
Thank you to Q Worldwide.

Without you, all of this would have been impossible.

Dedicated to the golden heart of a unique woman and loving mother.

Y"""

THOR_THANKS_FULL_BLOCK = THOR_THANKS_BLOCK_HEADING + "\n\n" + THOR_THANKS_BLOCK_BODY


def verify_thor_thanks_block_source(
    *,
    source_text: str,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    heading_present = THOR_THANKS_BLOCK_HEADING in source_text
    body_present = THOR_THANKS_BLOCK_BODY in source_text
    return {
        "artifact_kind": "odin_final_pr_13_thor_thanks_block_verification",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "heading_present": heading_present,
        "body_present": body_present,
        "block_verified": heading_present and body_present,
        "source": "Thor-Agent-Kit README.md",
        "import_rule": "exact_copy_no_paraphrase_no_translation_no_rename",
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }
