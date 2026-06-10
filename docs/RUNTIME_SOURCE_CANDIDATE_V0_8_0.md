# v0.8.0 Direct Master Architecture Runtime Source Candidate

This lock materializes the v7.1 master architecture as executable local source as far as this environment can honestly prepare it.

## Built source layers

- Universal Work runtime engine.
- Caller Manifest and app-owned apply boundary validation.
- QIRC local event ledger and digest.
- App Seed Pack compiler and security certification.
- Pattern Mine / Flow Pack intake compiler.
- Worklet / Work Atom micro-op runtime.
- Model route selection with mock candidate workers.
- Candidate Artifact, Candidate Tournament, Final Gate, Why Trace and Response Packet.
- Local HTTP API skeleton.
- Odin Hub static control-surface skeleton.
- Diagnostics support bundle candidate.
- Safe-mode plan candidate.

## Claim boundary

This source candidate does not assert host behavior, live model inference, Windows service behavior, installer behavior, code signing, external network operation, or app-side application. It gives Codex and later host runs a real executable body instead of a pure documentation shell.

## Canonical local flow

```text
Caller Manifest
→ Universal Work
→ Binding Gate
→ Seed Pack Compiler
→ Pattern Mine / Flow Pack Compiler
→ Work Atom Plan and Execution
→ QIRC Event Ledger
→ Model Route / Mock Worker Projection
→ Candidate Artifact
→ Final Gate
→ Why Trace
→ Response Packet
→ App-owned Apply
```

## Required local commands

```text
python -m odin.cli validate-all
python -m odin.cli doctor
python -m odin.cli run-work examples/runtime/universal_work_full.valid.json --seed-pack examples/runtime/app_seed_pack_full.valid.json --pattern-mine examples/runtime/pattern_mine_full.valid.json
python -m odin.cli compile-seed-pack examples/runtime/app_seed_pack_full.valid.json
python -m odin.cli compile-pattern-mine examples/runtime/pattern_mine_full.valid.json
python -m odin.cli build-hub --out .odin_runtime/hub/index.html
python -m odin.cli emit-support-bundle --out .odin_runtime/support
```

## Senior reviewer note

The important shift is not breadth-by-label. The important shift is that every main v7.1 layer now has at least one concrete local source path, one candidate artifact shape, and one testable boundary.
