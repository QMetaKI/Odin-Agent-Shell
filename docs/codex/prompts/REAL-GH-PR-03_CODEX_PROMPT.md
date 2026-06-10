# Codex Prompt — REAL-GH-PR-03 — Model Provider Runtime, Pre-LLM Intelligence and Universal Worker Boundary — Provider-Ready

## Base state

You are working in `Odin-Agent-Shell` after:

```text
v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
```

This is a running runtime candidate. Do not restart from architecture-only assumptions.

## Objective

Build the model/agent worker layer: scale ladder, mock/local provider seams, low-memory strict behavior, pre-LLM intelligence, model-work avoidance, output composer, model/agent cards, permission cards and local/remote parity boundary. Post-v0.8.6 focus: complete and harden the direct runtime candidate already materialized by ChatGPT.

## Already materialized by ChatGPT

- provider base classes
- MockProvider
- Null/Echo-like stub cards
- provider registry/list-providers
- model route inside runtime engine
- candidate-only worker boundary docs

## Codex completion focus

- finish provider contract isolation
- add Ollama/llama.cpp/OpenAI-compatible/Claude-compatible adapters as disabled-by-default stubs or optional integrations
- harden provider config redaction
- strengthen pre-LLM routing and model-work-avoidance tests
- ensure every provider return is candidate-only and gate-checked

## Expected deliverables

- provider interface tests
- provider config fixtures
- disabled-by-default real provider adapters
- pre-LLM route-selection tests
- redaction and secret-boundary tests

## Existing files to preserve and inspect first

- `odin/models/`
- `odin/precompute/`
- `registries/universal_llm_worker_registry.json`
- `registries/remote_worker_boundary_registry.json`
- `docs/PRE_LLM_INTELLIGENCE_LAYER_V7_1.md`
- `docs/UNIVERSAL_LLM_WORK_CONSTRUCT_V7_1.md`
- `tests/`

## Target/new paths allowed for this PR

- `odin/agents/`
- `odin/output/`
- `registries/model_*`

## Forbidden scope

- no remote provider credentials
- no unreviewed tool use by agents
- no model output accepted as truth
- no app state ownership by Odin
- no production performance claim

## Required behavior

- Odin does deterministic/precompute work before model dispatch
- smallest sufficient worker is selected from declared capability cards
- remote workers are candidate workers only
- permission cards block apply, external send and authority escalation

## Acceptance gates

- All modified registries and schemas remain JSON-valid
- Codex return report separates implemented, prepared, skipped and blocked work
- No host/model/provider proof is claimed without a receipt produced in that environment
- PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
- agent permission fixtures block apply/tool escalation
- all proof gaps and non-claims are stated in the PR summary
- every created or updated artifact is registered in FILE_MANIFEST.json
- model routing negative cases fail closed
- pre-LLM direct-apply example remains invalid
- python -m odin.cli validate-all
- remote worker boundary fixtures validate

## Required commands

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `python -m odin.cli list-providers`
- `python -m odin.cli run-golden-flow`
- `python -m odin.cli validate-all`

## Must preserve

- no_llm_in_app
- candidate_only
- local_first
- app_owns_state
- semantic_bus_local_only
- app_owns_apply
- pre_model_admissibility
- truthful_perceived_intelligence
- universal_worker_boundary
- why_trace
- same_boundary_for_all_workers
- gpl_2_0_only

## Proof boundaries

- ChatGPT-built runtime candidate is not a substitute for host-real Codex proof
- Codex must keep app-owned apply boundary intact
- Codex must preserve GPL-2.0-only policy and no-hidden-authority posture
- no_app_apply_authority_for_odin
- no_app_state_ownership_by_odin
- no_external_send_by_odin
- no_model_inference_proof_without_actual_model_receipts
- no_model_output_accepted_as_truth
- no_network_qirc_by_default
- no_production_performance_claim
- no_production_readiness_claim
- no_remote_provider_credentials
- no_runtime_proof_without_host_receipts
- no_unreviewed_tool_use_by_agents

## Senior reviewer focus

- provider cannot become authority
- no secret leakage
- no claim that real inference was proven unless Codex actually proves it
- remote optional and disabled by default

## Return format

```text
PR: REAL-GH-PR-03
Branch:
Implemented:
Changed files:
Commands run:
Results:
Skipped:
Blocked:
Proof boundaries:
Next recommended PR:
```
