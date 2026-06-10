# Windows Implementation Drilldown v7.1

## Purpose

This drilldown converts the Windows product runtime lock into implementable host-level contracts. It remains a specification, not a host-validated claim.

## Process topology

### `odin-host.exe`
Stable launcher and microkernel boundary. It owns startup, shutdown, pack loading, pack validation, single-instance lock and emergency recovery routing.

### `odin-daemon.exe`
Long-running local service for Universal Work, QIRC Gold Spine, runtime packs, app pairings, work queue, storage and model orchestration.

### `odin-tray.exe`
Small status surface. It exposes status, pause, safe mode, restart, open hub and export support bundle.

### `odin-hub.exe`
Control Center. It provides panels for Apps, Work Capsules, Runtime Packs, Seed Packs, Pattern Mines, QIRC, Candidates, Why Trace, Models, Handoffs, Support and Settings.

### `odin-model-runner.exe`
Isolated model provider supervisor. It never owns app state. It returns model projections only.

### `odin-pack-compiler.exe`
AOT and cached capability slice compiler for Runtime Packs. It must never run arbitrary unvalidated code.

## IPC hierarchy

1. Named pipe for trusted local host/daemon/hub/tray communication.
2. Localhost HTTP API for app bridges.
3. WebSocket localhost optional for Hub live updates.
4. LAN disabled by default.
5. WAN forbidden in core.

## App pairing lifecycle

```text
APP_DISCOVERED
→ MANIFEST_SUBMITTED
→ PAIRING_TOKEN_ISSUED
→ CALLER_MANIFEST_VALIDATED
→ PERMISSION_CARDS_ASSIGNED
→ CAPABILITY_SLICE_SELECTED
→ ACTIVE
→ EXPIRED | REVOKED | SUSPENDED
```

## Runtime pack lifecycle

```text
PACK_DISCOVERED
→ MANIFEST_VALIDATED
→ SOURCE_HASH_VERIFIED
→ POLICY_CHECKED
→ TEST_GATES_CHECKED
→ LOADED
→ ACTIVE
→ RETIRED | ROLLED_BACK | BLOCKED
```

## Model runner lifecycle

```text
PROVIDER_DISCOVERED
→ MODEL_PROFILE_LOADED
→ RESOURCE_POSTURE_CHECKED
→ ROUTE_ELIGIBILITY_ASSIGNED
→ IDLE
→ RUNNING_SLOT
→ RETURNED_PROJECTION
→ MINICHECK
→ IDLE | FAILED | QUARANTINED
```

## Safe mode

Safe mode disables:

- remote workers;
- heavy local model routes;
- untrusted seed packs;
- pattern mine intake;
- cached capability compilation;
- developer debug payloads;
- non-essential QIRC channels.

Safe mode keeps:

- app manifest reading;
- claim boundary;
- minimal Universal Work validation;
- support bundle export;
- read-only diagnostics;
- safe rollback.

## Windows implementation gates

Codex must implement Windows code in phases. Host and daemon must exist before Hub richness. App pairing must exist before app actions. Pack validation must exist before pack loading. Support bundle redaction must exist before diagnostics export.
