# Odin Agent Shell — Claude Code Project Instructions

**Claim boundary:** project_instructions_not_runtime_proof

This file provides concise project instructions for Claude Code operating under Odin Agent Operator Mode.

## Required Reads (in order)

1. README.md
2. AGENTS.md
3. CODEX_START_HERE.md
4. CLAIM_BOUNDARY.md
5. docs/MASTER_ARCHITECTURE_V7_1.md (key sections)
6. docs/AGENT_OPERATOR_MODE_V1.md (for agent operator work)

## Non-Negotiable Boundaries

- Odin outputs candidates only — never apply app state
- App owns apply, state, external sends, storage, domain authority
- No hidden tool execution
- No provider API calls without receipt
- No claiming proof without receipt
- No network transport by default
- candidate_only: true / app_owned_apply: true in all agent work packets

## Agent Operator Mode

For agent operator work, use the Claude Code profile:

```
python -m odin.cli agent-handoff --agent claude-code --task <task_file>
python -m odin.cli validate-agent-operator-mode
```

Workflow: explore → plan → implement (allowed files only) → validate → pytest → return report

## Validation Commands

```
python -m odin.cli validate-all
python -m odin.cli validate-agent-operator-mode
python -m pytest -q -p no:cacheprovider
```

Do not mark ready if validate-all or pytest fails.

## Forbidden

- app_state_apply
- external_send
- hidden_tool_execution
- provider_api_call_without_receipt
- claiming_proof_without_receipt
- domain_state_mutation

## Skills

See `.claude/skills/odin-agent-operator/SKILL.md` for the agent operator skill.
