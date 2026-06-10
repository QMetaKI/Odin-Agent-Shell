from __future__ import annotations

def build_qirc_ring_radar(pressures: dict[str, float]) -> dict:
    rings = {}
    for ring, pressure in pressures.items():
        status = "active" if pressure >= 0.7 else "watch" if pressure >= 0.35 else "defer"
        rings[ring] = {"pressure": pressure, "status": status}
    return {"artifact_kind": "odin_qirc_ring_radar", "protocol_version": "7.1", "rings": rings, "route_hint": "activate_only_relevant_rings"}
