# FINAL-PR-05 Odin Agent Operator Work Packet

**task_id:** `final_pr_05_execution_gate_ladder_scaffold`
**intent:** Implement FINAL-PR-05 Controlled Execution Gate + Deterministic Mock Execution + Local Candidate Policy + Proof Chain + FINAL-PR Ladder Scaffold
**input_handoff:** `docs/codex/handoffs/FINAL_PR_05_COMPILED_THOR_Y_HANDOFF.md`
**candidate_only:** true
**local_only:** true
**claim_boundary:** `final_pr_05_work_packet_candidate_only_no_app_apply_no_external_send`

## Allowed Actions

- create new Python modules in `odin/execution_gate/`, `odin/proof_chain/`, `odin/final_pr_ladder/`
- extend `odin/local_hub/server.py` with new endpoints
- extend `odin/local_hub/ui.py` with new IDs and copy
- extend `odin/runtime_security/smoke.py` with execution gate checks
- add CLI commands to `odin/cli.py`
- create tests in `tests/test_final_pr_05_execution_gate.py`
- create validator in `tools/rebaseline/check_final_pr_05_execution_gate.py`
- create docs, handoffs, audits, reports, schemas, registries, examples
- update `SYSTEM_MAP.json` and `FILE_MANIFEST.json`
- run `python -m pytest -q -p no:cacheprovider`
- run `python -m odin.cli validate-all`

## Forbidden Actions

- `app_state_apply`
- `external_send`
- `hidden_tool_execution`
- `provider_api_call_without_receipt`
- `claiming_proof_without_receipt`
- `domain_state_mutation`
- real provider execution (Ollama, llama.cpp, remote APIs)
- real model inference
- API key reads
- external network calls
- subprocess for mock execution
- production readiness claims
- security certification claims
- writing `.env`, credentials, or API key files

## Expected Artifacts

### Code Modules
- `odin/execution_gate/__init__.py`
- `odin/execution_gate/policy.py`
- `odin/execution_gate/gateway.py`
- `odin/execution_gate/mock_provider.py`
- `odin/execution_gate/local_candidate_policy.py`
- `odin/execution_gate/proof.py`
- `odin/proof_chain/__init__.py`
- `odin/proof_chain/registry.py`
- `odin/proof_chain/builder.py`
- `odin/final_pr_ladder/__init__.py`
- `odin/final_pr_ladder/compiler.py`
- `odin/final_pr_ladder/templates.py`
- `odin/final_pr_ladder/proof.py`

### Modified Files
- `odin/local_hub/server.py`
- `odin/local_hub/ui.py`
- `odin/runtime_security/smoke.py`
- `odin/cli.py`

### Tests and Tools
- `tests/test_final_pr_05_execution_gate.py`
- `tools/rebaseline/check_final_pr_05_execution_gate.py`

### Docs and Handoffs
- `docs/codex/handoffs/FINAL_PR_05_REPO_COGNITION_SUMMARY.md`
- `docs/codex/handoffs/FINAL_PR_05_THOR_Y_HANDOFF_REQUEST.md`
- `docs/codex/handoffs/FINAL_PR_05_COMPILED_THOR_Y_HANDOFF.md`
- `docs/codex/handoffs/FINAL_PR_05_ODIN_AGENT_OPERATOR_WORK_PACKET.md`
- `docs/codex/handoffs/FINAL_PR_05_HANDOFF_QUALITY_GATE.md`
- `docs/codex/audits/FINAL_PR_05_EXECUTION_GATE_AUDIT.md`
- `docs/codex/audits/FINAL_PR_05_THOR_EFFECTIVENESS_AUDIT.md`
- `docs/codex/audits/FINAL_PR_05_ODIN_EFFECTIVENESS_AUDIT.md`
- `docs/codex/reports/FINAL_PR_05_EXECUTION_GATE_RETURN_REPORT.md`
- `docs/rebaseline/FINAL_PR_05_EXECUTION_GATE_LADDER.md`

### Reports and Data
- `reports/final_pr_05_execution_gate_report.json`
- `reports/final_pr_05_execution_gate_proof_packet.json`
- `reports/final_pr_05_proof_chain.json`
- `reports/final_pr_05_ladder_scaffold_report.json`
- `reports/final_pr_05_thor_effectiveness_audit.json`
- `reports/final_pr_05_odin_effectiveness_audit.json`
- `schemas/final_pr_05_execution_gate_proof_packet.schema.json`
- `schemas/final_pr_ladder_worker_packet_scaffold.schema.json`
- `registries/final_pr_05_execution_gate_registry.json`
- `examples/final_pr_05/execution_gate_proof_packet.example.json`
- `examples/final_pr_05/final_pr_ladder_worker_packet_scaffold.example.json`

## Validators

- `python -m odin.cli validate-final-pr-05-execution-gate`
- `python -m odin.cli validate-all`
- `python tools/rebaseline/check_final_pr_05_execution_gate.py --repo-root . --out reports/final_pr_05_execution_gate_report.json --generated-at-utc 2026-01-01T00:00:00Z`

## Tests

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_final_pr_05_execution_gate.py -p no:cacheprovider`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

## Proof Packets

- `python -m odin.cli prove-final-pr-05-execution-gate`
- `python -m odin.cli prove-final-pr-proof-chain`
- `python -m odin.cli prove-final-pr-ladder-scaffold`

## Return Report

`docs/codex/reports/FINAL_PR_05_EXECUTION_GATE_RETURN_REPORT.md`

Must include:
- Thor Audit: Observation → Cause → Finding → Improvement → Priority → Evidence
- Odin Audit: Primitive → Where → Effect → Evidence → Missing → Next Injection → Decision
- Senior Reviewer Simulation
- Senior Code Reviewer Simulation
- Known gaps and FINAL-PR-06 decision

## Failure Policy

If any of the following fails, do not mark ready:
- `validate-all` has errors
- `pytest` has failures
- `runtime-security-smoke` finds forbidden markers in execution gate source
- Proof packet is missing or malformed

## Token Minimization Policy

- Reuse PR-01..04 cognition
- Read only focused files needed for FINAL-PR-05 surfaces
- Do not re-read all provider/QIRC files unless needed for integration

## Odin PR-40 Findings Injected

- Runtime policy check before any subprocess (gateway checks policy first)
- Model availability probe when gate opens (probe via existing probe module)
- `#odin.model` events with model loading/execution gate status (gateway emits these)
- Dynamic subprocess allowlist enforcement (mock execution uses no subprocess)
- Proof chain cross-reference to all proof packets (proof_chain module)
- SYSTEM_MAP auto-check / coverage check (validator checks)
- FINAL-PR Ladder Compiler scaffolding (final_pr_ladder module)
