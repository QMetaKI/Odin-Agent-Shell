"""Executable Odin v7.1 runtime candidate layer.

This package materializes the master architecture as a local, deterministic,
candidate-only runtime body. It intentionally does not prove Windows host
behavior, live model inference, deployment, or external network operation.
"""

__all__ = ["OdinRuntime", "run_universal_work_file"]


def __getattr__(name: str):
    if name in __all__:
        from .engine import OdinRuntime, run_universal_work_file
        return {"OdinRuntime": OdinRuntime, "run_universal_work_file": run_universal_work_file}[name]
    raise AttributeError(name)
