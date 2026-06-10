from odin.runtime.engine import OdinRuntime
from odin_app_sdk import build_app_manifest, build_universal_work


def run_demo() -> dict:
    manifest = build_app_manifest("codex.handoff.mock", "Codex Handoff Mock")
    work = build_universal_work("codex.handoff.mock", "Prepare a bounded patch-plan candidate", tags=["codex", "patchplan"])
    return OdinRuntime().run_universal_work(work, caller_manifest=manifest)
