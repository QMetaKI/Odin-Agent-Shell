# FINAL-PR-04 Thor/Y Handoff Request

```yaml
handoff_request_id: final_pr_04_provider_probe_security_smoke
primary_profile: thor
secondary_profiles:
  - generic
  - y
  - mjolnir
task_intent: >
  Build Local Candidate Provider Probe + Provider Policy + Runtime Security Smoke.
  Odin must detect and display local provider readiness without executing models,
  loading API keys, or connecting to external networks.
repo_cognition_input: docs/codex/handoffs/FINAL_PR_04_REPO_COGNITION_SUMMARY.md
source_truth:
  - Odin v7.1.1 Local Runtime Hub target
  - PR #37 simple local hub (base)
  - PR #38 model picker/apps/demo
  - PR #39 QIRC/devmode/hub convergence
allowed_scope:
  - provider policy (none, mock, ollama_candidate, llama_cpp_candidate)
  - provider registry
  - local candidate provider probe (binary availability check only)
  - mock provider probe (always available, no model)
  - Ollama availability probe without inference (shutil.which + --version only)
  - llama.cpp availability probe without inference (shutil.which + --version/--help only)
  - provider status UI sections and IDs
  - QIRC provider-status events on #odin.model
  - runtime security smoke checks
  - proof packet and report persistence
  - validators/tests/docs/reports/schemas/examples/registries
forbidden_scope:
  - provider execution (ollama run, generate, chat, embed)
  - model inference of any kind
  - API key reads (OPENAI_API_KEY, ANTHROPIC_API_KEY, any credentials)
  - external network calls
  - remote providers
  - app apply/state/external-send
  - public QIRC/network/federation
handoff_output_required:
  - compiled handoff
  - provider policy plan
  - runtime security smoke plan
  - acceptance gates
  - validator expectations
  - proof commands
  - return report contract
quality_goal: >
  Detect and report provider readiness without executing models or leaking secrets.
  Probe does not execute. Policy gates provider readiness.
  QIRC records local status. Odin keeps candidate boundaries. Apps decide.
token_goal: >
  Reuse PR-02/03 cognition and audits; avoid broad repo rereads.
  Focus on provider/security scope only.
```
