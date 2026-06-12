# FINAL-PR-06 Odin Agent Operator Work Packet

**Claim boundary:** `operational_seed_spine_routes_work_not_authority`
**candidate_only:** true
**app_owned_apply:** true

This packet was derived from repo cognition + PR44 prep registry + PR06 baseline prompt + current repo shape. It is designed to be useful for a later Thor chat as evidence of how repo-cognition-to-worker-packet compilation should work.

---

## objective

Implement `odin/operational_seed_spine/` — a deterministic seed routing layer that maps work contexts to intent seeds, role profiles, and bounded work capsules. Produce registries, schemas, examples, CLI commands, local hub endpoint, validator, tests, reports, and documentation.

## scope

- `odin/operational_seed_spine/` (9 files: `__init__`, `intent_seeds`, `role_profiles`, `seed_packs`, `selector`, `work_capsule`, `qirc_hints`, `token_budget`, `proof`)
- `odin/cli.py` — add 3 CLI commands
- `odin/local_hub/server.py` — add 1 endpoint
- `odin/local_hub/ui.py` — add 1 UI section
- `registries/final_pr_06_operational_seed_spine_registry.json`
- `schemas/final_pr_06_operational_seed_spine_proof_packet.schema.json`
- `examples/final_pr_06/` (4 example files)
- `tools/rebaseline/check_final_pr_06_operational_seed_spine.py`
- `tests/test_final_pr_06_operational_seed_spine.py`
- `reports/final_pr_06_*.json` (2 files)
- `SYSTEM_MAP.json` — PR06 entry only
- `FILE_MANIFEST.json` — PR06 files only
- Docs, audits, handoffs (new files only)
- `tools/rebaseline/check_prep_final_pr_06_08.py` — update to acknowledge PR06 implemented

## non_scope

- `odin/field_selection_spine/` — FINAL-PR-07 only
- `odin/projection_candidate_spine/` — FINAL-PR-08 only
- FINAL-PR-09 Release Closure
- Modifying `odin/y_pattern_spine/`, `odin/execution_gate/`, `odin/proof_chain/`, `odin/final_pr_ladder/`, `odin/seeds/`, `odin/patterns/`
- Autonomous reasoning, model inference, provider execution
- App apply, external send, public network

## allowed_files

- `odin/operational_seed_spine/*.py` (create new)
- `odin/cli.py` (add commands only)
- `odin/local_hub/server.py` (add endpoint only)
- `odin/local_hub/ui.py` (add section only)
- `registries/final_pr_06_*.json` (create new)
- `schemas/final_pr_06_*.json` (create new)
- `examples/final_pr_06/*.json` (create new)
- `tools/rebaseline/check_final_pr_06_operational_seed_spine.py` (create new)
- `tools/rebaseline/check_prep_final_pr_06_08.py` (update skip list)
- `tests/test_final_pr_06_operational_seed_spine.py` (create new)
- `reports/final_pr_06_*.json` (create new)
- `SYSTEM_MAP.json` (add PR06 entry only)
- `FILE_MANIFEST.json` (add PR06 files only)
- `docs/` (create new PR06 docs only)

## forbidden_files

- `odin/y_pattern_spine/*.py`
- `odin/execution_gate/*.py`
- `odin/proof_chain/*.py`
- `odin/final_pr_ladder/*.py`
- `odin/seeds/*.py`
- `odin/patterns/*.py`
- `odin/field_selection_spine/` (do not create)
- `odin/projection_candidate_spine/` (do not create)

## implementation_order

1. Repo cognition docs
2. This work packet
3. Module code: intent_seeds → role_profiles → seed_packs → selector → work_capsule → qirc_hints → token_budget → proof → __init__
4. Registry, schema, examples
5. CLI integration
6. Local Hub endpoint + UI
7. Validator tool
8. Tests
9. Reports + proof packet
10. Senior reviews
11. Fixes from reviews
12. Full validation run
13. PR body

## acceptance_gates

- `python -m odin.cli validate-operational-seed-spine` exits 0
- `python -m odin.cli explain-seed-route --demo` prints valid JSON with `candidate_only: true`
- `python -m odin.cli prove-operational-seed-spine` exits 0
- `python -m odin.cli validate-all` exits 0
- `python -m pytest -q tests/test_final_pr_06_operational_seed_spine.py` — all pass
- Full pytest suite passes

## proof_boundary

`operational_seed_spine_routes_work_not_authority`

## test_commands

```
python -m odin.cli validate-operational-seed-spine
python -m odin.cli explain-seed-route --demo
python -m odin.cli prove-operational-seed-spine
python -m odin.cli validate-prep-final-pr-06-08
python -m odin.cli validate-y-pattern-spine
python -m odin.cli validate-all
python -m pytest -q tests/test_final_pr_06_operational_seed_spine.py -p no:cacheprovider
python -m pytest -q -p no:cacheprovider
```

## return_report_contract

`docs/codex/reports/FINAL_PR_06_OPERATIONAL_SEED_SPINE_RETURN_REPORT.md` — must include branch, base commit, files created/modified, validators run, tests run, full suite result, known gaps, claim boundary, not-proven list, senior reviewer fixes, code reviewer fixes, Thor/Odin/Y findings, recommendation for PR07.

## known_non_claims

- autonomous_reasoning
- model_inference
- provider_execution
- app_apply
- app_state_mutation
- external_send
- production_readiness
- security_certification
- live_model_inference
- external_send_authority
- seeds_are_intelligent_agents
- role_profiles_are_runtime_personas
- qirc_hints_authorize_anything
