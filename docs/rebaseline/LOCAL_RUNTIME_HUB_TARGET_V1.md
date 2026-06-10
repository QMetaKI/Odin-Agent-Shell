# Odin Local Runtime Hub Target v1

Odin Local Runtime Hub is the new practical product target for the next build ladder. It preserves Master Architecture v7.1 as the semantic and technical baseline while replacing “Windows App first” as the immediate execution target. The Windows app remains a later optional shell.

## Definition

Odin as a portable local runtime, localhost-only API, browser-based Odin Hub/local webapp surface, SDK Bridge for YNode and other apps, easy start/stop/check flow, candidate-only Odin behavior, and app-owned apply/state/external send.

## Required end-user behavior

1. User downloads/clones repo or release package.
2. User runs one start command.
3. Odin validates itself.
4. Odin starts a localhost-only runtime API.
5. Browser Hub opens or is available locally.
6. Hub shows health, providers, sessions, candidates, bus events, worklets, proof gaps.
7. YNode and other apps connect via SDK Bridge.
8. Apps send Universal Work.
9. Odin returns Candidate Artifacts / Response Packets.
10. Apps own apply, state, external send and domain authority.

## Explicit non-goals

- No production readiness proof by default.
- No Windows service/tray/installer proof yet.
- No signed installer proof yet.
- No live model proof unless configured and receipted.
- No remote provider credentials by default.
- No app-state mutation by Odin.
- No external send by Odin.
- No WAN/LAN API by default.

## Evidence and claim labels

This rebaseline uses these evidence labels only:

- **Verified now** = command run in this workspace.
- **Repo-grounded** = current file content inspected.
- **Diff-grounded** = current PR diff.
- **Prior-context** = handoff/source-chat memory, not reverified.
- **Inference** = architecture inference, not proof.

Proof boundaries: no production readiness proof, no Windows app proof, no Windows service/tray/installer proof, no live model inference proof, no model quality proof, no security certification proof, no external send proof, no app-state mutation proof.

