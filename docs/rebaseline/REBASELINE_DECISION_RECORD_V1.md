# Rebaseline Decision Record v1

## Decision

Adopt Odin Local Runtime Hub as the immediate practical product target while preserving Master Architecture v7.1 and the v0.8.7 handoff as baseline history.

## Rationale

The current repo has runtime, API, bus, worklet, provider-boundary, SDK and Hub-related source surfaces, but user-facing local start, browser Hub, SDK bridge proof and packaging remain incomplete. A Local Runtime Hub ladder reduces first-product complexity compared with a Windows App first path while keeping Windows as a later optional shell.

## Consequences

- REAL-GH-PR-01..03 are treated as current baseline because PR #4 is merged in the workspace git log.
- REAL-GH-PR-04..08 remain carried forward unless merge receipts appear later.
- Old ladders are mapped, not deleted.
- No legacy moves are performed without review.

## Evidence and claim labels

This rebaseline uses these evidence labels only:

- **Verified now** = command run in this workspace.
- **Repo-grounded** = current file content inspected.
- **Diff-grounded** = current PR diff.
- **Prior-context** = handoff/source-chat memory, not reverified.
- **Inference** = architecture inference, not proof.

Proof boundaries: no production readiness proof, no Windows app proof, no Windows service/tray/installer proof, no live model inference proof, no model quality proof, no security certification proof, no external send proof, no app-state mutation proof.

