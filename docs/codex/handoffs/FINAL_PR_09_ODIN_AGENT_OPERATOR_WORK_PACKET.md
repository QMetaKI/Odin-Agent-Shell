# FINAL-PR-09 Odin Agent Operator Work Packet

claim_boundary: final_pr_09_operational_spine_candidate_kernel_not_live_model_proof_not_app_apply

## Objective

Implement FINAL-PR-09++: Functional Small-Model Operational Spine + Odin Work Kernel.

Connect the repo-real system into a runnable operational spine that accepts bounded work, creates handoff/context/work packets, validates and routes, prepares ModelWorkPackets, creates deterministic/no-model/mock/local-provider-seam candidate packets, organizes small-model role plans, and returns Candidate Artifacts and Response Packets with trace/receipt/proof surfaces.

## Inputs

- PR49 prep package (merged, confirmed)
- PR48 pre-release super audit (merged, confirmed)
- PR08 Projection Candidate Spine (merged, confirmed)
- PR07 Field Selection Spine (merged, confirmed)
- PR06 Operational Seed Spine (merged, confirmed)
- odin/precompute/route_score.py (score_pre_llm_route)
- odin/operational_seed_spine/selector.py (select_seed_route)
- odin/field_selection_spine/selector.py (select_field_route_from_seed_route)
- odin/projection_candidate_spine/ (build_projection_set_from_field_selection, build_candidate_graph)

## Allowed Edits

- Create: odin/operational_spine/ (all 11 module files)
- Create: registries/final_pr_09_operational_spine_registry.json
- Create: schemas/final_pr_09_operational_spine_report.schema.json
- Create: examples/final_pr_09/ (7 example files)
- Create: reports/final_pr_09_*.json (9 report files)
- Create: tools/rebaseline/check_final_pr_09_operational_spine.py
- Create: tests/test_final_pr_09_operational_spine.py
- Create: docs/codex/handoffs/FINAL_PR_09_*.md (3 files)
- Create: docs/codex/audits/FINAL_PR_09_*.md (4 files)
- Create: docs/codex/reports/FINAL_PR_09_OPERATIONAL_SPINE_RETURN_REPORT.md
- Create: docs/release/FINAL_PR_09_*.md (4 files)
- Create: docs/rebaseline/FINAL_PR_09_OPERATIONAL_SPINE.md
- Update: odin/cli.py (add new commands and validator)
- Update: odin/local_hub/server.py (add new endpoints)
- Update: odin/local_hub/ui.py (add REQUIRED_IDS, REQUIRED_COPY, HTML section)
- Update: SYSTEM_MAP.json (add final_pr_09_operational_spine entry)
- Update: FILE_MANIFEST.json (add all new PR09 files)
- Update: tools/rebaseline/check_final_pr_09_10_qshabang_smallmodel_prep.py (if needed)
- Update: tests/test_final_pr_09_10_qshabang_smallmodel_prep.py (if needed)

## Forbidden Edits

- Do NOT modify: odin/operational_seed_spine/ (existing PR06 code)
- Do NOT modify: odin/field_selection_spine/ (existing PR07 code)
- Do NOT modify: odin/projection_candidate_spine/ (existing PR08 code)
- Do NOT use: eval(), exec(), subprocess, urllib.request, requests, socket in new operational_spine modules
- Do NOT use: uuid.uuid4(), random, datetime.now(), time.time() for IDs
- Do NOT implement: FINAL-PR-10++, FINAL-PR-11, release closure
- Do NOT use: broad q_* runtime namespaces
- Do NOT claim: live model inference, production readiness, security certification

## Implementation Order

1. odin/operational_spine/ module files (11 files)
2. Registry, schema, examples (8 files)
3. Reports and proof packet (9 files)
4. Validator tool (1 file)
5. Tests (1 file)
6. CLI update (odin/cli.py)
7. Local Hub update (server.py, ui.py)
8. SYSTEM_MAP.json + FILE_MANIFEST.json
9. Docs (handoffs, audits, reports, release, rebaseline)

## Acceptance Gates

1. `python -m odin.cli validate-operational-spine` returns 0
2. `python -m odin.cli run-operational-spine --demo` prints valid JSON with candidate_only: true
3. `python tools/rebaseline/check_final_pr_09_operational_spine.py --repo-root . --out reports/final_pr_09_operational_spine_report.json` returns status: ok
4. `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_final_pr_09_operational_spine.py` passes all 76 tests
5. `python -m odin.cli validate-all` returns OK
6. All prior PR tests still pass

## Proof Boundary

proven: operational_spine_module_exists, operational_spine_demo_returns_candidate_packet, modelworkpacket_enforces_boundaries, small_model_route_plan_defined, qshabang_operational_map_defined, deferred_system_lift_classified, provider_seam_disabled_by_default, cli_surfaces_registered, hub_surfaces_registered, trace_receipt_surfaces_present

not_proven: live_model_inference, real_model_benchmark, provider_execution, app_apply, app_state_mutation, external_send, public_network, production_readiness, security_certification, release_certification

## Return Report Contract

docs/codex/reports/FINAL_PR_09_OPERATIONAL_SPINE_RETURN_REPORT.md must include:
- Branch and base commit
- PR merge confirmations
- Files created/modified
- Full test suite result (exact commands and output)
- Claim boundary and not-proven list

## Risk Controls

- Import all odin sub-modules with try/except to handle ImportError gracefully
- Use only stdlib in operational_spine modules
- Use deterministic SHA256 for all IDs
- Validate provider seam returns execution_allowed: false by default
- Run full test suite before marking complete

## Not-Proven List

- live_model_inference
- real_model_benchmark
- provider_execution
- app_apply
- app_state_mutation
- external_send
- public_network
- production_readiness
- security_certification
- release_certification

## Expected PR Title and Body

Title: FINAL-PR-09++: Functional Small-Model Operational Spine + Odin Work Kernel

Body: See prompt section 29 for full PR body template.
