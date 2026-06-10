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

## LRH Development Conventions

Added in LRH-PR-05. Subordinate to AGENTS.md and Master Architecture.

**artifact_kind naming:** `odin_<subsystem>_<artifact_type>` (e.g. `odin_localhost_api_health`)

**claim_boundary naming:** `<subsystem>_candidate_only_no_<forbidden>` (e.g. `local_api_candidate_only_no_app_apply_no_external_send_no_wan_lan_claim`)

**known_non_proofs required list:** Every proof function must include `not_proven` list. Required entries:
- `production_readiness`
- `live_model_inference`
- `app_state_mutation`
- `external_send_authority`

**fixture structure:** `examples/<subsystem>/<name>.<valid|invalid>.json` — response fixtures must include `candidate_only: true`, `claim_boundary`.

**CLI parser/dispatch insertion pattern:**
1. Add subparser in `main()` argument parser block
2. Add early-return handler before the validate_all fallback
3. Add to validate_all() if a new validate_* function
4. For prove_* commands: return a proof packet dict with `proven`, `not_proven`, `claim_boundary`

**validate_* integration pattern:** Each `validate_<feature>()` function returns `list[str]` errors. Add call to `validate_all()`. Add `validate-<feature>` subparser and early handler.

**Return Report audit requirements:** Every LRH PR must include `docs/codex/reports/LRH-PR-NN_RETURN_REPORT.md` with Thor audit, Odin Agent Operator audit, Claude Code worker audit, proof boundaries, skipped items, and next recommended PR.

## Skills

See `.claude/skills/odin-agent-operator/SKILL.md` for the agent operator skill.
