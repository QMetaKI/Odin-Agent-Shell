from odin.runtime.engine import OdinRuntime
from odin_app_sdk import build_app_manifest, build_universal_work

SEED_PACK = {
    "artifact_kind": "odin_app_seed_pack",
    "pack_id": "wedding_studio_seed_pack",
    "seeds": [
        {"id": "dignified_warmth", "purpose": "calm wedding wording", "activation_tags": ["wedding", "always"], "weight": 1.2},
        {"id": "no_fake_claims", "purpose": "avoid invented vendor or legal claims", "activation_tags": ["wedding"], "weight": 1.0},
    ],
}

def run_demo() -> dict:
    manifest = build_app_manifest("wedding.studio.mock", "Wedding Studio Mock")
    work = build_universal_work("wedding.studio.mock", "Draft candidate structure for a ceremony paragraph", tags=["wedding", "writing"])
    return OdinRuntime().run_universal_work(work, caller_manifest=manifest, seed_pack=SEED_PACK)
