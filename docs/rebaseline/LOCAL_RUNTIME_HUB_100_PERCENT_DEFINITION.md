# Local Runtime Hub 100 Percent Definition

At 100 percent for this target:

- Odin can be started locally with one clear command/script.
- Odin validates itself before starting.
- Odin exposes a localhost-only API.
- Odin Hub local webapp opens in browser.
- Hub shows runtime status, sessions, candidates, events, worklets, providers, proof gaps.
- YNode can connect via SDK Bridge.
- Any app can submit Universal Work.
- Odin returns Candidate Artifacts.
- Odin never applies app state.
- Odin never sends externally.
- Provider/live model use remains explicit, disabled by default and receipted.
- Proof gaps are visible.
- Support bundle can be emitted.
- Full test and CI command set reports OK in the accepting environment.
- Portable ZIP/release package can be created.
- Windows App remains optional later shell, not required for local functionality.

## Not included

- Production security certification.
- Signed Windows installer proof.
- Windows service/tray proof.
- Live model quality proof.
- Enterprise deployment proof.
- Public network API proof.

## Evidence and claim labels

This rebaseline uses these evidence labels only:

- **Verified now** = command run in this workspace.
- **Repo-grounded** = current file content inspected.
- **Diff-grounded** = current PR diff.
- **Prior-context** = handoff/source-chat memory, not reverified.
- **Inference** = architecture inference, not proof.

Proof boundaries: no production readiness proof, no Windows app proof, no Windows service/tray/installer proof, no live model inference proof, no model quality proof, no security certification proof, no external send proof, no app-state mutation proof.

