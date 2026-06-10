from __future__ import annotations
from pathlib import Path
import json, html

PANELS = [
    "Home", "Apps", "Work Queue", "Candidates", "QIRC", "Seed Packs", "Pattern Mines",
    "Flow Packs", "Work Atoms", "Models", "Why Trace", "Diagnostics", "Recovery", "Settings",
]

def build_hub_snapshot(status: dict | None = None) -> dict:
    return {
        "artifact_kind": "odin_hub_snapshot",
        "protocol_version": "7.1",
        "runtime_candidate_version": "0.8.6",
        "panels": PANELS,
        "status": status or {"runtime": "candidate", "host_scope": "local_dev"},
        "quick_actions": ["run_golden_flow", "compile_seed_pack", "compile_pattern_mine", "emit_support_bundle", "safe_mode_plan"],
        "claim_boundary": "hub_snapshot_is_local_control_surface_candidate",
    }

def write_static_hub(path: Path, snapshot: dict | None = None) -> Path:
    snapshot = snapshot or build_hub_snapshot()
    panel_cards = "\n".join(f"<section><h2>{html.escape(panel)}</h2><p>Candidate panel for {html.escape(panel.lower())}.</p></section>" for panel in snapshot["panels"])
    doc = """<!doctype html><html><head><meta charset='utf-8'><title>Odin Hub</title>
<style>body{{font-family:system-ui;margin:2rem;background:#111;color:#eee}}section{{border:1px solid #444;border-radius:12px;padding:1rem;margin:.75rem 0}}code,pre{{background:#222;padding:.75rem;display:block;overflow:auto}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.5rem}}</style></head>
<body><h1>Odin Hub</h1><p>Runtime release candidate control surface. App apply remains app-owned.</p>
<div class='grid'>{panel_cards}</div><h2>Snapshot</h2><pre>{snapshot}</pre></body></html>""".format(
        panel_cards=panel_cards,
        snapshot=html.escape(json.dumps(snapshot, indent=2, ensure_ascii=False, sort_keys=True)),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding='utf-8')
    return path
