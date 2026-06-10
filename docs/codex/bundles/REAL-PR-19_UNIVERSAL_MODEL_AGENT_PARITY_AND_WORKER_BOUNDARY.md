# REAL-PR-19 — Universal Model / Agent Parity and Worker Boundary

## Objective

Generalize the ChatGPT/Odin twin metaphor into a universal model/agent parity architecture. Every model, hosted model, local model, coding agent, browser agent, workflow agent, IDE assistant, app-native assistant, and future worker enters Odin through the same capability, permission, candidate, semantic diff and why trace boundary.

## Internal Tasks Covered

- PR-66 — Universal Model / Agent Parity Matrix
- PR-67 — Model / Agent Capability Cards
- PR-68 — Work Capsules and Capability Packs for Agents
- PR-69 — External Agent Adapter Boundary
- PR-70 — Universal Agent Candidate Protocol
- PR-71 — Agent Permission Cards and Apply Boundary
- PR-72 — Universal Agent Why Trace and Archetype Roles

## Primary Files

- docs/UNIVERSAL_MODEL_AGENT_PARITY_V7_1.md
- docs/MODEL_AGENT_CAPABILITY_CARDS_V7_1.md
- docs/MODEL_AGENT_WORK_CAPSULES_V7_1.md
- docs/UNIVERSAL_AGENT_CANDIDATE_PROTOCOL_V7_1.md
- docs/MODEL_AGENT_PERMISSION_CARD_SYSTEM_V7_1.md
- docs/EXTERNAL_MODEL_AGENT_ADAPTER_BOUNDARY_V7_1.md
- docs/UNIVERSAL_AGENT_ORCHESTRATION_MATRIX_V7_1.md
- docs/MODEL_AGENT_WHY_TRACE_V7_1.md
- schemas/v7_1/
- registries/
- odin/shadow_runtime/
- tests/

## Required Behavior

- All workers require capability cards.
- All workers require permission cards.
- All worker output normalizes to Candidate Artifacts.
- Action attempts downgrade to Action Card Candidates or are blocked.
- Why Trace explains selected and rejected worker choices.
- Semantic Diff preserves reviewability.
- App-owned Apply remains the only path to real state changes.

## Forbidden Scope

- No autonomous agent action.
- No model/agent-specific bypass of Odin gates.
- No app state mutation by Odin.
- No external send through Odin.
- No unvalidated worker adapter.
- No provider-specific authority promotion.

## Definition of Done

- All docs exist and include red lines.
- Schemas validate as JSON.
- Registries include worker classes and permission levels.
- Shadow Runtime modules exist.
- Test file verifies the universal model/agent parity lock.
- Codex task registry covers PR-66 through PR-72.
- Real PR bundle registry covers PR-66 through PR-72.
- validate-all and pytest pass.

## Codex PR Summary Template

- Scope:
- Internal tasks covered:
- Worker classes added:
- Capability/permission cards changed:
- Candidate-only gates preserved:
- Tests run:
- Non-claims:

## Senior Review Notes

REAL-PR-19 is approved only if it reduces model/agent special cases. It is rejected if it creates generic autonomous agent behavior. The point is not to make Odin an agent swarm. The point is to make all agent/model work versioned, candidate-only, traceable, diffable and app-sovereign.


## Bundle Review Depth

This real PR bundle is the universal worker-boundary consolidation. Reviewers must verify that every model and agent class enters through the same normalized Odin path. This includes local models, hosted models, coding agents, browser/research agents, IDE assistants, workflow agents, app-native assistants and future worker surfaces. The bundle is incomplete if any worker type can bypass capability cards, permission cards, candidate protocol, why trace, semantic diff or app-owned apply.

The implementation must be tested as a boundary layer, not as a real agent execution layer. No test may rely on an actual external agent. Fixtures must show selected and rejected workers, blocked action attempts, permission downgrades and Why Trace decisions. The bundle must also preserve prior v7.1 invariants from Pre-LLM Intelligence, QIRC Gold Spine, Odin Core/QLI/DFAS, Bug6/Q7, AI-Git Safety and Shadow Runtime Compiler.

## Bundle Non-Claims

REAL-PR-19 does not claim real provider integration, real browser actions, real coding-agent application, live tool execution, remote hosted model verification, security audit completion, production readiness or app-state mutation. It is a Codex build boundary for universal candidate-worker parity.
