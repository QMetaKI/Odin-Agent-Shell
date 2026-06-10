# Local Runtime Hub 100 Percent Definition

This is the target definition for the Odin Local Runtime Hub Road to 100 percent. It is a future acceptance target, not a claim that this rebaseline PR implements the target.

## Required end-state

- Odin can be started locally with one clear command/script.
- Odin validates itself before starting.
- Odin exposes a localhost-only API by default.
- Odin Hub local webapp opens in a browser.
- Hub shows runtime status, sessions, candidates, events, worklets, providers and proof gaps.
- External apps can connect via SDK Bridge.
- Any host app can submit Universal Work.
- Odin returns Candidate Artifacts.
- Odin never applies app state.
- Odin never sends externally.
- Provider/live model use remains explicit, disabled by default and receipted.
- Proof gaps are visible.
- Support bundle can be emitted.
- All tests pass.
- CI passes.
- Portable ZIP/release package can be created.
- Windows App remains optional later shell, not required for local functionality.

## Acceptance categories

### A. Startability

- What must work: one clear start/stop/check path works locally.
- Command that proves it: future target `python -m odin.cli prove-local-runtime`.
- Explicitly not proven: Windows service/tray/installer proof, production readiness.

### B. Runtime Health

- What must work: health, status, validation and proof gaps are visible.
- Command that proves it: future target `python -m odin.cli prove-local-runtime`.
- Explicitly not proven: host validation outside local receipts.

### C. Localhost API

- What must work: localhost-only API exposes health/status/providers/universal-work/sessions/candidates/events/proof-gaps.
- Command that proves it: future target `python -m odin.cli prove-sdk-bridge`.
- Explicitly not proven: public network API proof.

### D. Browser Hub

- What must work: local browser Hub shows status and read-only surfaces.
- Command that proves it: future target `python -m odin.cli prove-browser-hub`.
- Explicitly not proven: browser UI production readiness or remote hosting proof.

### E. Agent Operator Mode

- What must work: Codex, Claude Code and generic CLI profiles use packet/permission/proof/return contracts.
- Command that proves it: future target `python -m odin.cli prove-agent-operator-mode`.
- Explicitly not proven: agent autonomy, hidden tool execution, or provider integration.

### F. SDK Bridge

- What must work: SDK can health-check, submit Universal Work and read Candidate Artifacts.
- Command that proves it: future target `python -m odin.cli prove-sdk-bridge`.
- Explicitly not proven: app apply/state/external send authority by Odin.

### G. External App Bridge

- What must work: neutral external app bridge fixtures show host app integration boundaries.
- Command that proves it: future target `python -m odin.cli prove-external-app-bridge`.
- Explicitly not proven: specific external app integration proof.

### H. Universal Work Playground

- What must work: safe local Universal Work demo returns Candidate Artifacts.
- Command that proves it: future target `python -m odin.cli run-golden-flow`.
- Explicitly not proven: live model quality or app apply proof.

### I. Provider / Worker / Pre-LLM Visibility

- What must work: provider cards, worker permissions, route decisions and redaction status are visible.
- Command that proves it: future target `python -m odin.cli validate-provider-worker-boundary`.
- Explicitly not proven: live inference proof unless separately receipted.

### J. Packaging

- What must work: portable ZIP/release package can be created with manifest and checksums.
- Command that proves it: future target `python -m odin.cli prove-portable-package`.
- Explicitly not proven: signed installer or store readiness proof.

### K. Support Bundle

- What must work: diagnostic support bundle can be emitted without secrets.
- Command that proves it: future target `python -m odin.cli emit-support-bundle`.
- Explicitly not proven: security certification or support organization readiness.

### L. Boundary Preservation

- What must work: candidate-only, app-owned apply/state/external send and localhost-only defaults remain enforced.
- Command that proves it: future target `python -m odin.cli validate-all`.
- Explicitly not proven: production security certification.

### M. CI/Test Acceptance

- What must work: all validators and deterministic tests pass in CI/local acceptance environment.
- Command that proves it: future target `validate-all and pytest`.
- Explicitly not proven: deployment certification.

### N. Public Naming Neutrality

- What must work: public LRH artifacts use neutral external app fixtures and do not require concrete external app/product/project names.
- Command that proves it: future target `test_local_runtime_hub_rebaseline.py`.
- Explicitly not proven: specific external app integration proof.

## Not included in 100 percent by default

- Production security certification.
- Signed Windows installer proof.
- Windows service/tray proof.
- Live model quality proof.
- Enterprise deployment proof.
- Public network API proof.
- Specific external app integration proof.

## Public Naming Neutrality

No concrete external app/product/project names are required for Odin’s public Local Runtime Hub architecture. External app examples use neutral fixtures only.

## Evidence and claim labels

- **Verified now** = command run in this workspace.
- **Repo-grounded** = current file content inspected.
- **Diff-grounded** = current PR diff.
- **Prior-context** = handoff/source-chat memory, not reverified.
- **Inference** = architecture inference, not proof.

Proof boundaries: no production readiness proof, no Windows app proof, no Windows service/tray/installer proof, no live model inference proof, no model quality proof, no security certification proof, no external send proof, no app-state mutation proof.
