"""FINAL-PR-13: Manual Release Actions.

Claim boundary: release_artifact_boundary_lists_manual_release_actions_not_external_release
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "release_artifact_boundary_lists_manual_release_actions_not_external_release"

_MANUAL_ACTIONS = [
    {
        "action": "create git tag",
        "manual_only": True,
        "claimed_by_pr13": False,
        "required_evidence_if_done_later": "git tag output showing tag name and commit hash",
        "safe_wording": "A maintainer may separately create a git tag after this PR is merged.",
        "forbidden_wording": "FINAL-PR-13 creates a git tag.",
    },
    {
        "action": "create GitHub Release",
        "manual_only": True,
        "claimed_by_pr13": False,
        "required_evidence_if_done_later": "GitHub Release URL and release notes confirming publication",
        "safe_wording": "A maintainer may separately create a GitHub Release after this PR is merged.",
        "forbidden_wording": "FINAL-PR-13 creates a GitHub Release.",
    },
    {
        "action": "publish to PyPI",
        "manual_only": True,
        "claimed_by_pr13": False,
        "required_evidence_if_done_later": "PyPI package page URL and version confirmation",
        "safe_wording": "A maintainer may separately publish to PyPI after this PR is merged.",
        "forbidden_wording": "FINAL-PR-13 publishes to PyPI.",
    },
    {
        "action": "upload release assets",
        "manual_only": True,
        "claimed_by_pr13": False,
        "required_evidence_if_done_later": "GitHub Release asset URLs confirming upload",
        "safe_wording": "A maintainer may separately upload release assets after this PR is merged.",
        "forbidden_wording": "FINAL-PR-13 uploads release assets.",
    },
    {
        "action": "verify external release state",
        "manual_only": True,
        "claimed_by_pr13": False,
        "required_evidence_if_done_later": "External verification receipts confirming live release state",
        "safe_wording": "A maintainer may separately verify external release state after this PR is merged.",
        "forbidden_wording": "FINAL-PR-13 verifies external release state.",
    },
    {
        "action": "publish release notes externally",
        "manual_only": True,
        "claimed_by_pr13": False,
        "required_evidence_if_done_later": "Published release notes URL or distribution confirmation",
        "safe_wording": "A maintainer may separately publish release notes externally after this PR is merged.",
        "forbidden_wording": "FINAL-PR-13 publishes release notes externally.",
    },
]


def build_manual_release_actions(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_final_pr_13_manual_release_actions",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "manual_actions": _MANUAL_ACTIONS,
        "all_actions_manual_only": True,
        "all_actions_claimed_by_pr13": False,
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }
