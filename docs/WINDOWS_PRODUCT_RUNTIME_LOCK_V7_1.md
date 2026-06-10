# Windows Product Runtime Lock v7.1

## Purpose
This document defines Odin as a real Windows product target, not only an architecture/specification repo. It converts the existing v7.1 canon into a product runtime contract: process model, IPC posture, installer modes, update and rollback, recovery, diagnostics, support bundle, runtime pack loading and Control Center behavior.

## Product identity
Odin on Windows is a local-first LLM/agent work operating shell. It provides a stable host for compiled runtime packs, QIRC Gold Spine, Universal Work, Handoff Compiler, App Seed Pack Compiler, Pattern Mine Intake, Work Atom Runtime, Model Worker routing and Candidate rendering. The Windows app does not own app state. It owns only Odin's local runtime boundary.

## Process Responsibilities
Each Windows process has one responsibility and one authority boundary. Host coordinates lifecycle; daemon handles work; tray displays state; Control Center exposes Odin Hub; model runner isolates inference; pack compiler prepares packs; diagnostics exports redacted state.

## Required process model
- `odin-host.exe`: stable product entrypoint, single-instance lock, lifecycle manager, service discovery, safe-mode entry.
- `odin-daemon.exe`: local work queue, Universal Work runtime, QIRC Gold Spine, runtime pack loader, model route scheduling.
- `odin-tray.exe`: status, quick actions, safe-mode toggle, start/stop/restart, model availability, active work count.
- `odin-control-center.exe`: Odin Hub surface, apps, models, runtime packs, seed packs, pattern mines, traces, support bundles.
- `odin-model-runner.exe`: supervised model-worker process boundary, local provider child process management.
- `odin-pack-compiler.exe`: AOT/cached runtime pack, capability slice, seed pack and pattern flow compilation.
- `odin-diagnostics.exe`: support bundle, doctor, repair, logs, redaction and environment snapshot.

## IPC policy
Preferred local privileged IPC is a named pipe. App bridge integration may use localhost HTTP/WebSocket under pairing-token and capability-card rules. WAN is forbidden. LAN is disabled by default. Every app receives a scoped capability token tied to Caller Manifest, Permission Card and App-owned Apply Boundary. IPC must not expose apply, external-send or app-state mutation commands.

## Runtime modes
- `minimal`: no model provider, schema/registry validation, Control Center minimal, QIRC disabled or light.
- `low_memory_strict`: semantic bus light, Work Atoms, 1B/2B/3B micro slots, short trace retention.
- `standard_local`: 3B + 7B/8B hybrid sweet spot, QIRC Gold Spine, full Universal Work.
- `quality_local`: 13B/14B quality escalation where hardware allows.
- `heavy_local_batch`: 22B/32B or larger batch/offload, not interactive default.
- `verification_only`: validators, pack checks, no model calls.
- `safe_mode`: last-known-good runtime pack only, all external/remote routes blocked.

## Installer modes
- Portable ZIP: no registry requirement, local data path selectable, developer-friendly.
- MSIX candidate: signed desktop packaging, update channel possible, no overclaim.
- Winget candidate: later distribution channel after runtime proof exists.
- Developer editable install: only for Codex/build mode.

## Update and rollback
Every update must preserve: prior pack manifest, prior schema/registry snapshot, prior app pairings, prior seed-pack state, prior support-bundle redaction policy. Runtime pack update is staged, validated, loaded, health-checked and only then promoted. On failure, rollback to last-known-good pack. Pack validation failure forces safe mode.

## Control Center / Odin Hub product panels
Home, Apps, Work Capsules, Capability Packs, Seed Packs, Pattern Mines, Flow Packs, Work Atoms, QIRC Gold Spine, Models, Runtime Packs, Handoffs, Candidate Canvas, Why Trace, Diagnostics, Support Bundle, Settings, License/Notices.

## Windows failure modes
- `daemon_not_running`
- `named_pipe_denied`
- `localhost_port_blocked`
- `app_pairing_expired`
- `runtime_pack_invalid`
- `seed_pack_blocked`
- `pattern_mine_intake_failed`
- `work_atom_budget_exceeded`
- `qirc_event_backlog`
- `model_runner_crashed`
- `disk_cache_full`
- `low_memory_strict_forced`
- `support_bundle_redaction_failed`

## Required DoD
A future Codex PR implementing this lock must add process contracts, IPC contracts, product state schemas, support-bundle CLI stubs, safe-mode behavior, rollback fixtures, diagnostics tests and no network-by-default verification. Runtime proof remains a future target and must not be claimed by this preparation layer.
