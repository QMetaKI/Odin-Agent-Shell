"""FINAL-PR Ladder templates — FINAL-PR-05.

Claim boundary: final_pr_ladder_scaffold_not_full_prompt_compiler
"""
from __future__ import annotations

WORKER_PACKET_SECTIONS = [
    "repo_cognition",
    "handoff_request",
    "compiled_handoff",
    "work_packet",
    "acceptance_gates",
    "proof_commands",
    "return_report_contract",
]

SECTION_DESCRIPTIONS = {
    "repo_cognition": "Summarize current repo state, base SHA, and relevant surfaces.",
    "handoff_request": "Thor/Y handoff request with profiles and scope constraints.",
    "compiled_handoff": "Compiled handoff from Thor/Y — files to touch, forbidden scope.",
    "work_packet": "Odin Agent Operator work packet — candidate_only, forbidden_actions.",
    "acceptance_gates": "List of acceptance gates the PR must pass.",
    "proof_commands": "CLI commands that prove the PR deliverables.",
    "return_report_contract": "Structure of the return report to be produced.",
}
