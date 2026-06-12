# FINAL-PR-04 Odin Agent Operator Work Packet

```yaml
task_id: final_pr_04_provider_probe_security_smoke
intent: >
  Implement Local Candidate Provider Probe, Provider Policy, and Runtime Security Smoke.
  Odin must detect local provider readiness without executing models or leaking secrets.
input_handoff: docs/codex/handoffs/FINAL_PR_04_COMPILED_THOR_Y_HANDOFF.md
candidate_only: true
local_only: true

allowed_actions:
  - create odin/providers/ module (policy, registry, probe, proof)
  - create odin/runtime_security/ module (smoke)
  - update odin/qirc_core/channels.py (add #odin.model)
  - update odin/local_hub/ui.py (add REQUIRED_IDS, HTML sections, copy)
  - update odin/local_hub/server.py (add FINAL-PR-04 endpoints)
  - update odin/cli.py (add commands and validator function)
  - create tests/test_final_pr_04_provider_probe_security.py
  - create tools/rebaseline/check_final_pr_04_provider_probe_security.py
  - create schemas, examples, registries, reports, docs

forbidden_actions:
  - provider_execution
  - model_inference
  - api_key_reads
  - external_network_calls
  - remote_provider_connections
  - app_apply
  - app_state_mutation
  - external_send
  - public_qirc_network
  - qirc_federation
  - disturbing_ports_8877_8878
  - modifying_odin_models_providers

expected_artifacts:
  - odin/providers/__init__.py
  - odin/providers/policy.py
  - odin/providers/registry.py
  - odin/providers/probe.py
  - odin/providers/proof.py
  - odin/runtime_security/__init__.py
  - odin/runtime_security/smoke.py
  - tests/test_final_pr_04_provider_probe_security.py
  - tools/rebaseline/check_final_pr_04_provider_probe_security.py
  - reports/final_pr_04_provider_probe_security_proof_packet.json
  - reports/final_pr_04_provider_probe_security_report.json
  - schemas/final_pr_04_provider_probe_security_proof_packet.schema.json
  - examples/final_pr_04/provider_probe_security_proof_packet.example.json
  - registries/final_pr_04_provider_probe_security_registry.json
  - docs/codex/handoffs/FINAL_PR_04_*.md (all required)
  - docs/codex/audits/FINAL_PR_04_*.md (all required)
  - docs/codex/reports/FINAL_PR_04_PROVIDER_PROBE_SECURITY_RETURN_REPORT.md
  - docs/rebaseline/FINAL_PR_04_PROVIDER_PROBE_SECURITY.md

validators:
  - python -m odin.cli validate-final-pr-04-provider-probe-security
  - python -m odin.cli validate-all
  - python tools/rebaseline/check_final_pr_04_provider_probe_security.py --repo-root . --out reports/final_pr_04_provider_probe_security_report.json --generated-at-utc 2026-01-01T00:00:00Z

tests:
  - PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_final_pr_04_provider_probe_security.py -p no:cacheprovider
  - PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider

proof_packets:
  - python -m odin.cli prove-final-pr-04-provider-probe-security

return_report: docs/codex/reports/FINAL_PR_04_PROVIDER_PROBE_SECURITY_RETURN_REPORT.md

failure_policy: >
  If validate-all or pytest fails, do not mark ready.
  Record exact failure, classify as baseline/scoped/blocker.
  Continue only if unrelated to FINAL-PR-04 scope.

token_minimization_policy: >
  Reuse PR-02/03 cognition. Do not reread unrelated modules.
  Focus only on provider/security scope.

pr03_findings_injected:
  - QIRC Core exists; provider probe must emit #odin.model events
  - Hub surface ownership intact (8765/8877/8878); do not disturb
  - Proof packet auto-persistence pattern from PR-03; extend for PR-04
  - Candidate/app-owned apply boundary must remain explicit
  - Runtime security smoke must scan provider/security files for forbidden markers
  - FINAL-PR Ladder Compiler remains too large; defer to FINAL-PR-05
```
