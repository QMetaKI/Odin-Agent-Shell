"""Thor Handoff Compiler v0 — FINAL-PR-11.

Claim boundary: thor_handoff_compiler_v0_compiles_worker_packets_not_thor_runtime
candidate_only: true

Compiles agent operator work packets from structured input contracts.
Does NOT claim Thor runtime execution.
Does NOT grant agent autonomy.
Does NOT apply app state.
"""
from odin.thor_handoff_compiler.input_contract import build_handoff_input_contract
from odin.thor_handoff_compiler.compiler import (
    compile_agent_operator_work_packet,
    compile_acceptance_matrix,
    compile_validator_plan,
    compile_pr_body_skeleton,
    compile_thor_handoff_bundle,
)

__all__ = [
    "build_handoff_input_contract",
    "compile_agent_operator_work_packet",
    "compile_acceptance_matrix",
    "compile_validator_plan",
    "compile_pr_body_skeleton",
    "compile_thor_handoff_bundle",
]
