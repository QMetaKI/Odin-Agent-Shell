"""Agent Operator Mode Presets — defines bounded worker presets for Claude Code / Codex workflows.

Claim boundary: agent_operator_modes_define_bounded_worker_presets_not_agent_autonomy
candidate_only: true
app_owned_apply: true
agent_autonomy: false
"""
from .modes import list_agent_operator_modes, get_agent_operator_mode
from .presets import AGENT_OPERATOR_MODES
from .reports import build_agent_operator_mode_matrix

__all__ = [
    "list_agent_operator_modes",
    "get_agent_operator_mode",
    "AGENT_OPERATOR_MODES",
    "build_agent_operator_mode_matrix",
]
