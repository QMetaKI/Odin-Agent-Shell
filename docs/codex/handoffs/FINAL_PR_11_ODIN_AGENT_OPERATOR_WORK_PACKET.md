# FINAL-PR-11 Odin Agent Operator Work Packet

**Claim boundary:** `final_pr_11_provider_receipt_critic_thor_compiler_not_release_closure`
**candidate_only:** true
**app_owned_apply:** true

## Objective

Implement FINAL-PR-11: Local Provider Receipt Harness + Critic Runtime Binding + Thor Handoff Compiler v0.
Move Release Closure to FINAL-PR-12.

## Inputs

- odin/operational_spine/provider_seam.py — existing disabled-by-default provider seam
- odin/release_boundaries/ — existing PR10 release boundary evidence
- reports/final_pr_10_boundary_release_proof_packet.json
- reports/final_pr_09_operational_spine_proof_packet.json

## Allowed Edits

- odin/local_provider_receipts/ (create new module)
- odin/critic_runtime/ (create new module)
- odin/route_evaluation/ (create new module)
- odin/thor_handoff_compiler/ (create new module)
- odin/cli.py (add PR11 validators and commands)
- odin/local_hub/server.py (add PR11 endpoints)
- odin/local_hub/ui.py (add PR11 REQUIRED_IDS)
- docs/ (create PR11 docs)
- reports/ (create PR11 reports)
- registries/ (create PR11 registries)
- schemas/ (create PR11 schemas)
- examples/final_pr_11/ (create PR11 examples)
- SYSTEM_MAP.json (add PR11 entry)
- FILE_MANIFEST.json (add PR11 files)
- tools/rebaseline/check_final_pr_11_provider_critic_thor.py (create validator)
- tests/test_final_pr_11_provider_critic_thor.py (create tests)

## Forbidden Edits

- odin/operational_spine/ (preserved as-is)
- odin/release_boundaries/ (preserved as-is)
- tests/test_final_pr_10_boundary_release.py (not modified)
- tests/test_final_pr_09_operational_spine.py (not modified)
- tests/test_final_pr_09_10_qshabang_smallmodel_prep.py (not modified)
- Any existing tests (do not weaken)

## Implementation Order

1. New modules (odin/local_provider_receipts/, odin/critic_runtime/, odin/route_evaluation/, odin/thor_handoff_compiler/)
2. Validator tool (tools/rebaseline/check_final_pr_11_provider_critic_thor.py)
3. Tests (tests/test_final_pr_11_provider_critic_thor.py)
4. CLI updates (odin/cli.py)
5. Local Hub updates (odin/local_hub/server.py, ui.py)
6. Registries, schemas, examples
7. Reports and proof packet
8. Docs
9. SYSTEM_MAP.json, FILE_MANIFEST.json
10. Validation run

## Acceptance Gates

1. python -m odin.cli validate-local-provider-receipt-harness → OK
2. python -m odin.cli validate-critic-runtime-binding → OK
3. python -m odin.cli validate-route-evaluation-receipts → OK
4. python -m odin.cli validate-thor-handoff-compiler → OK
5. python -m odin.cli validate-final-pr-11-provider-critic-thor → OK
6. python -m pytest tests/test_final_pr_11_provider_critic_thor.py → all pass
7. python -m odin.cli validate-all → OK
8. python -m pytest tests/ → all pass

## Proof Boundary

claim_boundary: `final_pr_11_provider_receipt_critic_thor_compiler_not_release_closure`

## Return Report Contract

Required sections:
- branch
- base_commit
- PR51/PR50/PR49/PR48 merge confirmations
- files_created
- files_modified
- tests_run
- full_suite_result (exact output)
- claim_boundary
- not_proven

## Risk Controls

- Provider execution disabled by default (no env var, no flag)
- No shell=True in executor
- No public network calls
- No API keys
- No app apply
- No external send
- Critic is advisory only

## Not Proven

- production_readiness
- security_certification
- release_certification
- general_live_model_inference
- real_model_benchmark
- model_quality_superiority
- provider_execution_without_explicit_receipt
- app_apply
- app_state_mutation
- external_send
- public_network

## Expected PR Title

FINAL-PR-11: Local Provider Receipt Harness + Critic Runtime Binding + Thor Handoff Compiler v0
