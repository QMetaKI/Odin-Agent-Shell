# FINAL-PR-11.5: v7.1.1 Coverage Compiler

**Claim boundary:** v711_coverage_compiler_maps_target_to_repo_evidence_not_runtime_completion
**candidate_only:** true

## What It Does

The v7.1.1 Coverage Compiler maps v7.1.1 target canon to repo-real evidence. It does NOT claim runtime completion.

## How It Works

1. `load_v711_targets()` — returns all 26 target areas from v7.1.1 canon
2. `map_targets_to_repo_evidence()` — checks repo for evidence files per target
3. `build_v711_coverage_matrix()` — builds full coverage matrix with status per target
4. `build_v711_gap_index()` — extracts targets that are not fully implemented
5. `recommend_next_prs_from_v711_gaps()` — recommends FINAL-PR-13 as Release Closure

## Coverage Statuses

| Status | Meaning |
|--------|---------|
| implemented | Fully implemented with tests |
| implemented_candidate_only | Implemented but candidate-only, no app apply |
| implemented_plan_only | Plan only, no runtime code |
| implemented_disabled_by_default | Implemented but disabled by default |
| implemented_structural_evidence | Module exists, structural evidence |
| host_scoped_local_receipt_path | Host-scoped receipt only, not external |
| partial | Partially implemented |
| doc_only | Documentation only |
| target_only | Target spec only, no implementation |
| external_receipt_required | Requires external receipt not yet implemented |
| not_repo_real_yet | Not yet in repo |

## Not Proven

- runtime completion
- production_readiness
- live_model_inference
- app_state_mutation
- external_send_authority
