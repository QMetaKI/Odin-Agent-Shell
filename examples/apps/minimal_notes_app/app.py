from odin.runtime.engine import OdinRuntime
from odin_app_sdk import build_app_manifest, build_universal_work


def run_demo() -> dict:
    manifest = build_app_manifest("minimal.notes", "Minimal Notes")
    work = build_universal_work("minimal.notes", "Turn this rough note into a candidate checklist", tags=["notes", "checklist"])
    result = OdinRuntime().run_universal_work(work, caller_manifest=manifest)
    return {
        "app": "minimal_notes_app",
        "candidate_count": len(result.get("candidates", [])),
        "apply_boundary": "app_must_review_before_saving_note",
        "runtime_status": result.get("runtime_status"),
    }

if __name__ == "__main__":
    import json
    print(json.dumps(run_demo(), indent=2, sort_keys=True))
