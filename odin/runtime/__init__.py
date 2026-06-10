"""Executable Odin v7.1 runtime candidate layer.

This package materializes the master architecture as a local, deterministic,
candidate-only runtime body. It intentionally does not prove Windows host
behavior, live model inference, deployment, or external network operation.
"""
from .engine import OdinRuntime, run_universal_work_file

__all__ = ["OdinRuntime", "run_universal_work_file"]
