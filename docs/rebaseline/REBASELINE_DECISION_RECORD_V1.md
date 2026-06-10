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



## Amendment: Agent Operator Mode as LRH-PR-02

Decision: insert Odin Agent Operator Mode as the early LRH-PR-02 build slice and shift the portable local runtime starter to LRH-PR-03. Rationale: future Codex, Claude Code and local-agent work should enter through Odin's own handoff/plan/guard/proof/return discipline before later Local Runtime Hub implementation PRs depend on agent-authored changes. This is a planning decision only; it does not implement `odin agent-*` commands.

Boundaries: Agent Operator Mode does not replace the Local Runtime Hub, does not create autonomous execution, does not add provider API integration, does not grant app-apply authority, and does not claim full Thor protocol compatibility without verified packet evidence.

## Final Road-to-100 normalization

Decision: normalize the LRH ladder to LRH-PR-01..17 with Agent Operator Mode as LRH-PR-02, Portable Local Runtime Starter as LRH-PR-03, Neutral External App Bridge Pack as LRH-PR-12, and Generic App Bridge Examples and Golden Harness as LRH-PR-13. The dependency graph follows the amend prompt because Agent Operator Mode is a build/workflow foundation and the API/Hub/bridge/package slices depend on progressively stronger local runtime, API and safety surfaces.

Decision: add a Road-to-100 acceptance harness model as future target proof commands. The harness is not current runtime proof; it lists expected outputs, proof boundaries and known non-proofs for future acceptance PRs.

Decision: neutralize public external app naming in LRH artifacts. Public examples use external app, host app, client app, reference app, generic app bridge and neutral app fixture language rather than concrete external app/project names.
