# Windows Direct Source Handoff v0.8.0

This file translates the direct source candidate into the later Windows build lane.

## Current local source body

- Python CLI runtime candidate.
- Local HTTP API skeleton.
- Static Odin Hub page generator.
- Support bundle candidate emitter.
- Windows launcher scripts.

## Later Windows-real work

- Replace localhost skeleton with hardened Windows host API and named-pipe lane where appropriate.
- Build tray process and control center shell.
- Bind model runner process lifecycle.
- Add installer/update/rollback implementation.
- Add host receipts from a real Windows target.

## Non-claims

No Windows service behavior, tray behavior, installer behavior, code signing, model inference, or host IPC behavior is proven by this artifact alone.
