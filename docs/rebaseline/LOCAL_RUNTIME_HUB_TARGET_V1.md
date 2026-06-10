# Odin Local Runtime Hub Target v1

Odin Local Runtime Hub is the new practical product target for the next build ladder. It preserves Master Architecture v7.1 as the semantic and technical baseline while replacing “Windows App first” as the immediate execution target. The Windows app remains a later optional shell.

## Definition

Odin as a portable local runtime, localhost-only API, browser-based Odin Hub/local webapp surface, SDK Bridge for external apps and host apps, easy start/stop/check flow, candidate-only Odin behavior, and app-owned apply/state/external send.


## Odin Agent Operator Mode

Odin Agent Operator Mode is an early repository-local build/workflow surface for the Local Runtime Hub ladder. It lets coding agents and compatible agent systems use Odin as an orchestration, handoff, planning, guard, proof and return-report layer while preserving Odin's candidate-only and permission-gated architecture.

It is **not** a live LLM provider API, autonomous agent swarm, hidden executor, app-apply authority, remote orchestration daemon, network transport by default, or replacement for the Local Runtime Hub. It is a CLI/file-protocol and packet-contract layer for agent-guided repository work.

### Conceptual split

- **Odin for Apps:** Universal Work → Candidate Artifact.
- **Odin for Coding Agents:** Agent Task → Agent Work Packet → Guarded Patch/PR → Return Report.
- **Odin for Agent Systems:** Agent Packet → Permission Gate → Candidate Work → Proof / Return Packet.

### Coding Agent Operator Surface

Primary target agents are Codex and Claude Code. Additional compatible targets include Gemini CLI, Cursor-style agents, Aider-style agents, OpenHands-style agents, and future local coding agents. Future canonical commands are `odin agent-handoff`, `odin agent-plan`, `odin agent-guard`, `odin agent-check`, `odin agent-proof`, and `odin agent-return`, with profiles such as `--agent codex`, `--agent claude-code`, and `--agent generic-cli-agent`. Codex- and Claude-specific aliases may be added later, but the canonical surface remains `agent-*`.

### Thor-compatible protocol surface

Thor compatibility is a reference/interoperability layer. Future Odin should read Thor handoff material, normalize Thor-style task/handoff packets into Odin Agent Work Packets, emit Odin return packets that Thor-compatible tooling can consume, preserve Thor guard/plan/expected/return concepts when useful, and record incompatibilities as protocol gaps rather than silent assumptions. This PR only uses the labels **Thor-compatible where verified**, **Thor-inspired where conceptual**, and **Thor-bound only when actual file/protocol evidence exists**. It does not claim full Thor protocol support.

### General agent boundary

Future agent systems must enter through Agent Work Packet, Agent Permission Card, Allowed Files / Forbidden Scope, Acceptance Gates, Proof Boundary Packet, and Return Report Packet. No agent may apply app state, send externally, mutate domain state, claim proof without receipt, use tools invisibly, or escape declared scope.

Agent Operator Mode is intended to make Codex, Claude Code and future agents work under Odin's scope/proof discipline. It does not create agent autonomy, provider API integration, hidden tool use, or app-apply authority.

## Required end-user behavior

1. User downloads/clones repo or release package.
2. User runs one start command.
3. Odin validates itself.
4. Odin starts a localhost-only runtime API.
5. Browser Hub opens or is available locally.
6. Hub shows health, providers, sessions, candidates, bus events, worklets, proof gaps.
7. External apps and host apps connect via SDK Bridge.
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


## Public naming neutrality

The Local Runtime Hub Road-to-100 artifacts use neutral external app terminology: external app, host app, client app, reference app, generic app bridge, external app bridge, client bridge, host app bridge, integration fixture and neutral app fixture. No concrete external app/product/project name is required for Odin public architecture.
