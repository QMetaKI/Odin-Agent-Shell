# Odin Agent Operator Mode V1

**Version:** 1.0
**Status:** Candidate specification — schemas, registries, guards, proofs, and CLI surfaces defined. Implementation targets: Codex-first, Claude-Code-equivalent, generic-agent-capable.
**Claim boundary:** architecture_specified_not_runtime_verified

---

## Purpose

Agent Operator Mode is Odin's repository-local handoff/plan/guard/proof/return workflow protocol for coding agents. It creates a deterministic, candidate-only workflow layer that lets agents work under Odin's handoff, scope, guard, proof, and return discipline.

This is NOT:
- A live LLM integration
- An autonomous agent swarm
- A hidden executor
- An app-apply authority
- A provider API
- A remote orchestration daemon
- A network transport

---

## Architecture Split

```
Odin for Apps:
  Universal Work → Candidate Artifact

Odin for Coding Agents:
  Agent Task → Agent Work Packet → Guarded Patch/PR → Return Report

Odin for Agent Systems:
  Agent Packet → Permission Gate → Candidate Work → Proof / Return Packet
```

Agents remain external workers. Odin provides:
- handoff (Agent Work Packet)
- plan (plan envelope in packet)
- guard (guard checks)
- check (packet validation)
- proof (proof boundary summary, does not close gaps)
- return (Return Report skeleton)
- schemas, registries, examples
- permission cards
- profile registry (Codex, Claude Code, generic, Thor-compatible, future-local)
- Thor-compatible mapping (where verified, gap-labeled where not)
- senior-review structure
- senior-code-review structure

---

## Agent Profile Registry

See `registries/agent_operator_profile_registry.json`.

Required profiles:
- `codex` — GitHub PR workflow, repo-scoped diffs, deterministic tests
- `claude-code` — explore-plan-implement, CLAUDE.md, hooks, skills, subagent-style review
- `generic-cli-agent` — tool-neutral, minimal
- `thor-compatible` — gap-labeled, not full Thor protocol
- `future-local-agent` — candidate-only, permission-card-bound, no external send

All profiles share hard forbidden actions:
- `app_state_apply`
- `external_send`
- `hidden_tool_execution`
- `unbounded_file_edit`
- `provider_api_call_without_receipt`
- `claiming_proof_without_receipt`
- `secret_exfiltration`
- `network_transport_by_default`
- `domain_state_mutation`

All permission cards have hard defaults false:
- `may_apply_app_state: false`
- `may_send_external: false`
- `may_call_provider_api: false`
- `may_use_hidden_tools: false`
- `may_mutate_domain_state: false`

---

## Claude Code Profile

The Claude Code profile preserves these workflow traits:
- explore first
- plan before editing
- use concrete file context
- run deterministic checks
- use concise persistent project instructions (CLAUDE.md)
- prefer hooks/guards for non-negotiable checks
- support reusable workflow skills
- support subagent-style review boundaries
- keep context lean
- show command evidence instead of asserting success

The Claude Code profile does NOT require Claude Code to be installed, does NOT call Claude Code, and does NOT claim Claude Code provider integration.

Optional Claude-facing files:
- `CLAUDE.md` — project instructions
- `.claude/skills/odin-agent-operator/SKILL.md` — reusable skill definition
- `.claude/agents/senior-reviewer.md` — senior reviewer subagent
- `.claude/agents/senior-code-reviewer.md` — senior code reviewer subagent

These files are concise and subordinate to AGENTS.md, Master Architecture v7.1, and Odin claim boundaries.

---

## Thor Compatibility

See `registries/thor_compatibility_registry.json`.

Thor-Agent-Kit is used as a temporary external handoff/compiler aid, not as a vendored dependency and not as Odin authority.

Thor compatibility mapping:
- Thor handoff → Odin Agent Work Packet (partial)
- Thor plan → Odin Agent Plan Envelope (conceptual)
- Thor guard → Odin Agent Guard Check (partial, implemented)
- Thor expected → Odin Acceptance Gates (partial)
- Thor return-plan → Odin Agent Return Report (partial)
- Thor pack/agent codex → Odin codex profile packet (partial)
- Thor repo cognition → Odin context packet candidate (conceptual, gap)
- Thor repo intent → Odin context packet candidate (conceptual, gap)
- Thor repo semantic-inputs → Odin context packet candidate (conceptual, gap)

Claim language:
- `Thor-compatible where verified`
- `Thor-inspired where conceptual`
- `Thor-bound only when actual file/protocol evidence exists`

---

## Schemas

- `schemas/v7_1/odin_agent_work_packet.schema.json`
- `schemas/v7_1/odin_agent_return_report.schema.json`
- `schemas/v7_1/odin_agent_operator_permission_card.schema.json`

Hard invariants in Agent Work Packet:
- `candidate_only: true`
- `app_owned_apply: true`
- `external_send_default: false`
- `network_transport_default: false`
- `hidden_tool_execution_allowed: false`

---

## CLI Commands

```
python -m odin.cli agent-handoff --agent codex --task <path>
python -m odin.cli agent-handoff --agent claude-code --task <path>
python -m odin.cli agent-handoff --agent generic-cli-agent --task <path>
python -m odin.cli agent-plan --packet <path>
python -m odin.cli agent-guard --packet <path>
python -m odin.cli agent-check --packet <path>
python -m odin.cli agent-proof --packet <path>
python -m odin.cli agent-return --packet <path>
python -m odin.cli validate-agent-operator-mode
```

No command modifies app state, sends externally, calls remote provider APIs, uses hidden tools, grants apply authority, or claims runtime proof without receipts.

---

## Required Files

```
odin/agent_operator/__init__.py
odin/agent_operator/packets.py
odin/agent_operator/profiles.py
odin/agent_operator/guards.py
odin/agent_operator/proofs.py
odin/agent_operator/returns.py
schemas/v7_1/odin_agent_work_packet.schema.json
schemas/v7_1/odin_agent_return_report.schema.json
schemas/v7_1/odin_agent_operator_permission_card.schema.json
registries/agent_operator_profile_registry.json
registries/thor_compatibility_registry.json
examples/agent_operator/codex_work_packet.valid.json
examples/agent_operator/claude_code_work_packet.valid.json
examples/agent_operator/generic_cli_agent_work_packet.valid.json
examples/agent_operator/future_local_agent_work_packet.valid.json
examples/agent_operator/thor_compatible_packet.valid.json
examples/agent_operator/agent_work_packet.invalid.hidden_apply.json
examples/agent_operator/agent_work_packet.invalid.external_send.json
examples/agent_operator/agent_permission_card.invalid.provider_api.json
tests/test_lrh_pr_02_agent_operator_mode.py
```

---

## Proof Boundaries

- No app apply by agent
- No external send by agent
- No hidden tool execution
- Candidate-only output
- No runtime proof claimed
- Thor output is advisory and did not replace Odin repo-real validation

---

## Forbidden Scope

This PR does NOT implement:
- Portable Local Runtime Starter (LRH-PR-03)
- Browser Hub
- SDK Bridge
- External App Bridge
- Provider/live model integration
- Network transport
- Windows service/tray/installer
- App-state mutation
- External send
- Autonomous agents
- Hidden tools

---

## Next Recommended PR

**LRH-PR-03 — Portable Local Runtime Starter**
