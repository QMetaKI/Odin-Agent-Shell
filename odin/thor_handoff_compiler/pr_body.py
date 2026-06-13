"""PR body skeleton builder — FINAL-PR-11."""
from __future__ import annotations

from odin.thor_handoff_compiler.input_contract import CLAIM_BOUNDARY, _NOT_PROVEN
from odin.thor_handoff_compiler.compiler import compile_pr_body_skeleton

__all__ = ["compile_pr_body_skeleton", "CLAIM_BOUNDARY", "_NOT_PROVEN"]
