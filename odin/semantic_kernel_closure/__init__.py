"""Odin Semantic Kernel Closure — compiles Odin kernel IR and pipeline map.

Claim boundary: semantic_kernel_closure_compiles_odin_kernel_ir_not_runtime_completion
candidate_only: true
app_owned_apply: true
"""
from .ir import build_odin_work_ir
from .pipeline import build_semantic_kernel_pipeline
from .contracts import build_kernel_contract_map
from .receipts import build_kernel_receipt_map
from .reports import build_semantic_kernel_closure_report

__all__ = [
    "build_odin_work_ir",
    "build_semantic_kernel_pipeline",
    "build_kernel_contract_map",
    "build_kernel_receipt_map",
    "build_semantic_kernel_closure_report",
]
