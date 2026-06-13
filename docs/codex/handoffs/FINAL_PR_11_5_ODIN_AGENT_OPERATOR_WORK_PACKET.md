# FINAL-PR-11.5: Odin Agent Operator Work Packet

**Claim boundary:** final_pr_11_5_semantic_kernel_coverage_not_release_closure
**candidate_only:** true
**app_owned_apply:** true

## Work Packet Type

Claude Code Implementation Worker

## Task

Implement FINAL-PR-11.5: Odin Semantic Kernel Closure + v7.1.1 Coverage Compiler

## Scope

New modules:
- odin/v711_coverage_compiler/
- odin/semantic_kernel_closure/
- odin/y_pattern_operationalization_index/
- odin/claims_compiler/
- odin/agent_operator_modes/

CLI commands (validate, build, explain, list, compile)
Local Hub endpoints and UI sections
Validator: tools/rebaseline/check_final_pr_11_5_semantic_kernel_coverage.py
Tests: tests/test_final_pr_11_5_semantic_kernel_coverage.py (86 tests)
Docs: rebaseline, release, codex handoffs/audits/reports
Reports, examples, registries, schemas
SYSTEM_MAP and FILE_MANIFEST updates

## Forbidden Actions

- app_state_apply
- external_send
- hidden_tool_execution
- provider_api_call_without_receipt
- claiming_proof_without_receipt
- domain_state_mutation
- implementing FINAL-PR-13
- implementing Release Closure
- weakening PR06/07/08/09/10/11 validators or tests

## Global Invariants

- candidate_only: true
- app_owned_apply: true
- local_only_default: true
- no_hidden_authority: true
- final_pr_13_remains_deferred: true
- no_production_readiness: true
- no_security_certification: true
- no_release_certification: true

## Validator Expectations

All validators pass: validate-v711-coverage-compiler, validate-semantic-kernel-closure, validate-y-pattern-operationalization-index, validate-claims-compiler, validate-agent-operator-modes, validate-final-pr-11-5-semantic-kernel-coverage, validate-all

## Return Report

docs/codex/reports/FINAL_PR_11_5_SEMANTIC_KERNEL_COVERAGE_RETURN_REPORT.md
