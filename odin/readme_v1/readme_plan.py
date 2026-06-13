"""FINAL-PR-13: README v1 Plan.

Claim boundary: readme_v1_public_surface_documents_candidate_release_without_overclaiming
candidate_only: true
"""
from __future__ import annotations

CLAIM_BOUNDARY = "readme_v1_public_surface_documents_candidate_release_without_overclaiming"

_REQUIRED_SECTIONS = [
    "# Odin Agent Shell",
    "## Current Status",
    "## What Odin Is",
    "## What Odin Is Not",
    "## Why Odin Exists",
    "## Who Odin Is For",
    "## Core Idea",
    "## Quick Start",
    "## Basic Usage",
    "## Main Workflows",
    "## Command Overview",
    "## Documentation Map",
    "## v1.0 Candidate Release Truth",
    "## Safety / Claim Boundaries",
    "## What Odin Does Not Claim",
    "## Root / Repository Map",
    "## Support, Donations, and License",
    "## Danke / Thank You",
]


def build_readme_v1_plan(
    *,
    generated_at_utc: str = "2026-01-01T00:00:00Z",
) -> dict:
    return {
        "artifact_kind": "odin_final_pr_13_readme_v1_plan",
        "candidate_only": True,
        "claim_boundary": CLAIM_BOUNDARY,
        "generated_at_utc": generated_at_utc,
        "required_sections": _REQUIRED_SECTIONS,
        "content_requirements": [
            "public-facing",
            "first-time-reader friendly",
            "concise but complete",
            "local-first",
            "candidate-only",
            "app-owned apply",
            "no model/network calls by default",
            "no provider execution by default",
            "no external release claim",
            "no production readiness claim",
            "no security certification claim",
            "no model superiority claim",
            "no real benchmark claim",
            "links DONATIONS.md",
            "exact Thor-Agent-Kit Danke / Thank You block",
        ],
        "not_proven": [
            "production_readiness",
            "live_model_inference",
            "app_state_mutation",
            "external_send_authority",
        ],
    }
