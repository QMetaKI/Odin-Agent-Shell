# LRH-PR-02 Agent Operator Mode Prompt

## Branch

`codex/lrh-pr-02-agent-operator-mode`

## PR title

`LRH-PR-02: Odin Agent Operator Mode`

## Objective

Create the CLI/file-protocol planning surface that lets Codex, Claude Code and future coding agents use Odin as a repo-local handoff, plan, guard, proof and return-report layer, with Thor-compatible packet normalization where verified.

## Baseline

Master Architecture v7.1, Local Runtime Hub target v1, and the LRH-PR-01 rebaseline remain authoritative. This is a candidate-only repository workflow protocol slice, not a runtime autonomy slice.

## Required intake

Read `START_HERE.md`, `CANON_ENTRY.md`, `SYSTEM_MAP.json`, `docs/MASTER_ARCHITECTURE_V7_1.md`, `docs/MASTER_SPECS_V7_1.md`, `docs/THOR_INTEGRATION.md`, `docs/BOUNDED_CODE_WORK.md`, this build ladder, relevant schemas and registries, and the current AGENTS.md instructions.

## Target files

- `docs/AGENT_OPERATOR_MODE_V1.md`
- `odin/agent_operator/`
- `schemas/v7_1/odin_agent_work_packet.schema.json`
- `schemas/v7_1/odin_agent_return_report.schema.json`
- `schemas/v7_1/odin_agent_permission_card.schema.json`
- `registries/agent_operator_profile_registry.json`
- `registries/thor_compatibility_registry.json`
- `examples/agent_operator/codex_work_packet.valid.json`
- `examples/agent_operator/claude_code_work_packet.valid.json`
- `examples/agent_operator/thor_compatible_packet.valid.json`
- `tests/test_lrh_pr_02_agent_operator_mode.py`

## Allowed new files

Only add isolated docs, schemas, registries, examples, tests and minimal CLI/file-protocol scaffolding required for Agent Operator Mode.

## Forbidden scope

No real agent autonomy. No network send. No app apply. No hidden tool execution. No provider API integration. No claim that Codex or Claude Code are integrated providers. No full Thor protocol claim without verified mapping. Do not replace the Local Runtime Hub target.

## Required behavior

Future commands must be designed around:

- `odin agent-handoff --agent codex`
- `odin agent-handoff --agent claude-code`
- `odin agent-plan`
- `odin agent-guard`
- `odin agent-check`
- `odin agent-proof`
- `odin agent-return`

The protocol must include Agent Work Packet, Agent Permission Card, Allowed Files / Forbidden Scope, Acceptance Gates, Proof Boundary Packet and Return Report Packet. Thor-compatible mapping must label verified mappings and gaps.

## Required tests

Add deterministic tests for valid/invalid Agent Work Packets, permission cards, Codex and Claude Code profiles, generic CLI profile, Thor-compatible mapping gaps, no hidden apply authority, no external send by default, and candidate-only return reports.

## Required commands

- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_lrh_pr_02_agent_operator_mode.py -p no:cacheprovider`

## Acceptance gates

Agent packet schemas validate, Codex/Claude/generic profiles exist, Thor-compatible mapping exists with explicit gaps, agent commands are scaffolded or documented without hidden execution, tests prove candidate-only and no app-apply boundaries, and `validate-all` plus pytest pass.

## Proof boundaries

Agent Operator Mode is repository-local workflow protocol, not live LLM provider proof. Codex and Claude Code remain external workers. Odin validates and constrains but does not secretly execute app actions. Thor compatibility is evidence-bound and gap-labeled.

## Final response format

Summarize files changed, tests run, proof boundaries retained, skipped implementation claims, and whether the slice is ready for review.
