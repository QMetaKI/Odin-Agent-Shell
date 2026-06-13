"""Acceptance matrix builder — FINAL-PR-11."""
from __future__ import annotations

from odin.thor_handoff_compiler.input_contract import CLAIM_BOUNDARY, _NOT_PROVEN
from odin.thor_handoff_compiler.compiler import compile_acceptance_matrix

__all__ = ["compile_acceptance_matrix", "CLAIM_BOUNDARY", "_NOT_PROVEN"]
