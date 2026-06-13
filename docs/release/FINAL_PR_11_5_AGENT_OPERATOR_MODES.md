# FINAL-PR-11.5: Agent Operator Mode Presets

**Claim boundary:** agent_operator_modes_define_bounded_worker_presets_not_agent_autonomy
**candidate_only:** true

## What It Does

Agent Operator Mode Presets define bounded worker presets for Claude Code and Codex workflows. They improve workflow shaping without granting autonomy, merge authority, or app apply.

## Available Modes

| Mode ID | Tool Target | Best For |
|---------|-------------|----------|
| claude_code_implementation_worker | Claude Code CLI | Implementing bounded PRs |
| claude_code_runtime_integrator | Claude Code CLI | Integrating modules into CLI/Hub |
| codex_repo_planner | Codex | Planning repo changes |
| codex_patch_reviewer | Codex | Reviewing patches |
| release_boundary_reviewer | Claude Code / Codex | Reviewing release boundaries |
| senior_code_reviewer | Claude Code | Code review simulation |
| senior_architecture_reviewer | Claude Code | Architecture review simulation |
| thor_handoff_compiler_mode | Claude Code | Compiling Thor handoff bundles |
| pr_release_closure_worker | Claude Code | PR13 release closure work |

## Rules

- Agent Operator Mode is a work-shaping preset
- It grants NO autonomy
- It grants NO merge authority
- It grants NO app apply
- agent_autonomy: false on all modes
- app_apply: false on all modes
- external_send: false on all modes

## Not Proven

- production_readiness
- live_model_inference
- app_state_mutation
- external_send_authority
