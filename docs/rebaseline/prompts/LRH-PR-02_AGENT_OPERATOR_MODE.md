# Codex Prompt — LRH-PR-02 Odin Agent Operator Mode

## Branch

Use `codex/lrh-pr-02-odin-agent-operator-mode`.

## PR title

LRH-PR-02: Odin Agent Operator Mode

## Objective

Create the CLI/file-protocol planning surface that lets Codex, Claude Code and future coding agents use Odin as a repo-local handoff, plan, guard, proof and return-report layer, with Thor-compatible packet normalization where verified.

## Baseline

Master Architecture v7.1, Master Specs v7.1, the Local Runtime Hub target, the Road-to-100 ladder, candidate-only Odin and app-owned apply/state/external-send boundaries remain authoritative.

## Required intake

Read root canon, Master Architecture, Master Specs, LRH target, current-state audit, build ladder JSON, rebaseline manifest, coverage matrix, Road-to-100 acceptance harness, relevant subsystem docs, schemas, registries and tests.

## Target files
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
- `docs/AGENT_OPERATOR_MODE_V1.md`

## Allowed new files
- `odin/agent_operator/`
- `schemas/v7_1/odin_agent_work_packet.schema.json`
- `schemas/v7_1/odin_agent_return_report.schema.json`
- `schemas/v7_1/odin_agent_permission_card.schema.json`
- `registries/agent_operator_profile_registry.json`
- `registries/thor_compatibility_registry.json`
- `examples/agent_operator/`
- `tests/test_lrh_pr_02_agent_operator_mode.py`
- `docs/AGENT_OPERATOR_MODE_V1.md`

## Forbidden scope
- no autonomous external execution
- no hidden tool execution
- no network send by default
- no app apply authority
- no provider API integration claim
- no full Thor protocol support claim without verified mapping
- no replacement of Local Runtime Hub

## Required behavior
- support Codex, Claude Code and generic CLI agent profiles
- define Agent Work Packet, Permission Card and Return Report contracts
- normalize Thor-style handoff concepts only where verified
- record Thor incompatibilities as protocol gaps
- keep agents as external workers, not providers or app authority

## Required tests
- valid and invalid Agent Work Packet fixtures
- permission card rejects hidden tool use and external send
- Codex, Claude Code and generic CLI profiles exist
- Thor compatibility registry labels verified mappings and gaps
- return report remains candidate-only

## Required commands
- `future target: python -m odin.cli agent-handoff --agent codex`
- `future target: python -m odin.cli agent-handoff --agent claude-code`
- `future target: python -m odin.cli agent-plan`
- `future target: python -m odin.cli agent-guard`
- `future target: python -m odin.cli agent-check`
- `future target: python -m odin.cli agent-proof`
- `future target: python -m odin.cli agent-return`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_lrh_pr_02_agent_operator_mode.py -p no:cacheprovider`

## Acceptance gates
- Codex profile exists
- Claude Code profile exists
- generic CLI profile exists
- Thor-compatible mapping exists with verified/gap labels
- no hidden tool execution
- no autonomous external execution
- no app apply
- no provider API claim
- validate-all and pytest pass

## Proof boundaries
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof
- no agent autonomy proof
- no full Thor protocol support proof
- Codex and Claude Code remain external workers

## Final response format

Summary, Testing, Proof boundaries, Skipped implementation claims, Ready yes/no, Next recommended PR.
