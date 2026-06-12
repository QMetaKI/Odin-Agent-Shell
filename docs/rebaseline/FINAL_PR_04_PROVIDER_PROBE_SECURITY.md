# FINAL-PR-04: Provider Probe + Provider Policy + Runtime Security Smoke

**Claim boundary:** `final_pr_04_provider_probe_readiness_not_model_execution_not_security_certification`
**candidate_only:** true
**local_only:** true

## Purpose

FINAL-PR-04 implements the fourth final Local Runtime Hub build slice: Local Candidate Provider Probe, Provider Policy, and Runtime Security Smoke.

Provider probe readiness is NOT model execution. Provider status is NOT provider proof. Local candidate discovery does NOT imply inference.

## What Is Done

- Provider policy (`odin/providers/policy.py`): none, mock, ollama_candidate, llama_cpp_candidate
- Provider registry (`odin/providers/registry.py`): maps all required provider IDs
- Provider probe (`odin/providers/probe.py`): safe binary availability check, no model run
- Runtime security smoke (`odin/runtime_security/smoke.py`): boundary checks, static scan
- QIRC `#odin.model` channel added (`odin/qirc_core/channels.py`)
- Provider probe emits local QIRC events on `#odin.model`
- Local Hub endpoints: `/providers.json`, `/providers/probe.json`, `POST /providers/probe`, `/security/runtime-smoke.json`
- UI IDs: provider-policy-status, provider-probe-panel, provider-probe-results, provider-execution-boundary, runtime-security-smoke-status, secret-scan-status, network-boundary-status, qirc-provider-events-status
- Proof packet: `odin/providers/proof.py` + `reports/final_pr_04_provider_probe_security_proof_packet.json`
- CLI: validate-final-pr-04-provider-probe-security, prove-final-pr-04-provider-probe-security, provider-status, provider-probe, runtime-security-smoke
- Validator: `tools/rebaseline/check_final_pr_04_provider_probe_security.py`
- Tests: `tests/test_final_pr_04_provider_probe_security.py`

## Not Proven / Not Done

- No model inference
- No provider text generation
- No provider model quality
- No remote provider API
- No API key reads
- No external network
- No app apply / state / external-send authority
- No production readiness
- No security certification

## Known Gaps to FINAL-PR-05

- Actual model execution (gated by policy; deferred to FINAL-PR-05)
- Model quality proofs
- Remote provider routing (explicitly forbidden in this PR)
- Full FINAL-PR Ladder Compiler (deferred)

## Claim Boundary

Provider probe readiness is not model execution. Runtime security smoke is not security certification.
