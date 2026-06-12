# FINAL-PR-04 Compiled Thor/Y Handoff

**compiled_handoff_id:** final_pr_04_compiled_thor_y_handoff
**source:** FINAL_PR_04_THOR_Y_HANDOFF_REQUEST.md

---

## WARNING

> Probe readiness is not model execution.
> Provider status is not provider proof.
> Local candidate provider discovery is not live inference.
> No API key, no external network, no provider run.

---

## Provider Probe Scope

- Implement `odin/providers/policy.py` with ProviderPolicy dataclass
- Implement `odin/providers/registry.py` with PROVIDER_REGISTRY dict
- Implement `odin/providers/probe.py` with probe_provider, probe_all_providers, build_provider_status_packet
- Use `shutil.which` for binary discovery; optional `--version` with 2s timeout
- Probe result shape: provider_id, status, probe_allowed, execution_allowed, candidate_only, local_only, remote, requires_api_key, binary_found, model_inference, provider_execution, claim_boundary

## Provider Policy Scope

- Four providers: none, mock, ollama_candidate, llama_cpp_candidate
- All: execution_allowed=False, candidate_only=True
- ollama_candidate/llama_cpp_candidate: remote=False, requires_api_key=False
- Policy only describes gates; does not execute

## Runtime Security Smoke Scope

- Implement `odin/runtime_security/smoke.py`
- Static scan of odin/providers/ and odin/runtime_security/ for forbidden markers
- Check provider registry: all execution_allowed=False
- scan_content() public API for test use
- Result shape: status, forbidden_findings, provider_execution_default, model_inference_default, api_key_reads, external_network, public_bind

## Forbidden Actions

- ollama run, generate, chat, embed
- llama-cli model execution
- API key reads (OPENAI_API_KEY, ANTHROPIC_API_KEY)
- external network calls
- subprocess with model arguments
- app apply/state/external-send
- public QIRC/network/federation
- remote providers

## Files to Touch

- odin/providers/__init__.py (new)
- odin/providers/policy.py (new)
- odin/providers/registry.py (new)
- odin/providers/probe.py (new)
- odin/providers/proof.py (new)
- odin/runtime_security/__init__.py (new)
- odin/runtime_security/smoke.py (new)
- odin/qirc_core/channels.py (add #odin.model)
- odin/local_hub/ui.py (add REQUIRED_IDS + HTML + copy)
- odin/local_hub/server.py (add endpoints)
- odin/cli.py (add commands + validator)
- tests/test_final_pr_04_provider_probe_security.py (new)
- tools/rebaseline/check_final_pr_04_provider_probe_security.py (new)
- schemas/final_pr_04_*.schema.json
- examples/final_pr_04/*.example.json
- registries/final_pr_04_*.registry.json
- docs/codex/handoffs/FINAL_PR_04_*.md
- docs/codex/audits/FINAL_PR_04_*.md
- docs/codex/reports/FINAL_PR_04_*.md
- docs/rebaseline/FINAL_PR_04_*.md
- reports/final_pr_04_*.json

## Files to Avoid

- odin/models/providers/ (not disturbed)
- odin/local_hub/policy.py (not disturbed)
- odin/local_hub/surface_registry.py (not disturbed)
- odin/daemon/ (not disturbed)
- Ports 8877/8878 (not disturbed)

## Acceptance Gates

1. provider policy exists with all four provider IDs
2. all providers have execution_allowed=False
3. local candidate providers have remote=False, requires_api_key=False
4. probe_all_providers() returns candidate_only/local_only results
5. missing binary results in status=not_found (not error)
6. probe does not perform model inference
7. probe does not read API keys
8. runtime security smoke returns ok
9. runtime security smoke detects forbidden marker in synthetic input
10. QIRC #odin.model channel exists
11. provider probe emits QIRC provider-status events
12. local hub exposes /providers.json, /providers/probe.json, POST /providers/probe, /security/runtime-smoke.json
13. UI contains all eight FINAL-PR-04 required IDs
14. proof packet has provider_execution=false, model_inference=false, api_key_reads=false, external_network=false
15. proof packet persisted to reports/
16. validate-final-pr-04-provider-probe-security passes
17. validate-all passes
18. all previous tests pass
19. full pytest passes

## Known Gaps

- Model execution deferred to FINAL-PR-05
- Remote providers explicitly forbidden in this PR
- FINAL-PR Ladder Compiler deferred

## Return Contract

- validate-final-pr-04-provider-probe-security: OK
- prove-final-pr-04-provider-probe-security: packet with status=ok_with_known_gaps
- validate-all: OK
- Full pytest: all pass
- Reports persisted: final_pr_04_provider_probe_security_proof_packet.json
