# Skill: Odin Agent Operator

**Trigger:** When working on an Odin Agent Operator Mode task.
**Claim boundary:** skill_instructions_not_runtime_proof

## Workflow

1. Read AGENTS.md, CODEX_START_HERE.md, CLAIM_BOUNDARY.md
2. Read docs/AGENT_OPERATOR_MODE_V1.md
3. Run: `python -m odin.cli agent-handoff --agent claude-code --task <task>`
4. Review the generated Agent Work Packet — check allowed_files, forbidden_actions, acceptance_gates
5. Plan before editing — confirm file scope, commands, guards
6. Edit only allowed files
7. Run: `python -m odin.cli validate-agent-operator-mode`
8. Run: `python -m odin.cli validate-all`
9. Run: `python -m pytest -q -p no:cacheprovider`
10. Run: `python -m odin.cli agent-return --packet <packet_file>` to scaffold return report
11. Fill in return report — include senior reviewer and senior code reviewer simulation

## Boundaries

- candidate_only: true
- app_owned_apply: true
- No external send
- No hidden tools
- No provider API calls
- Show command evidence — do not assert success without receipts
