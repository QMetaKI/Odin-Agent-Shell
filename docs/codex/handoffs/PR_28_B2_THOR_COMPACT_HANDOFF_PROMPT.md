# PR-28 B2 Thor Compact Handoff Prompt

claim_boundary: thor_compact_handoff_prompt_is_task_description_not_runtime_proof

## Compact Master Prompt

**Repo:** Odin-Agent-Shell  
**Base commit:** 02f27ae (Add B1 app boundary and semantic bus contracts)  
**Branch:** claude/pr-28-b2-context-lenses-worklets-3osowv  
**B2 slice range:** V711-R100-048..075 (exactly 28 IDs)  
**Absorbed families:** PR-29-CONTEXT-LENSES, PR-30-WORKLETS-SLOTS-GAPTEXT

## Hard Scope Boundaries

- NEVER claim runtime completion, provider execution, live model inference, QIRC server
- NEVER mutate app state or claim external-send authority
- ALL schemas must have claim_boundary and candidate_only: true
- ALL examples must have claim_boundary and candidate_only: true
- Static validator must fail closed on missing files
- FILE_MANIFEST must not include .pyc, __pycache__, .odin_runtime/, egg-info artifacts
- Exactly 28 slices (V711-R100-048..V711-R100-075)

## Thor Repo Cognition Task

1. Clone https://github.com/QMetaKI/Thor-Agent-Kit.git to /tmp/odin_pr28_b2_external_refs/Thor-Agent-Kit
2. Run `find . -maxdepth 5 -type f | sort` in Thor-Agent-Kit
3. Check for runnable repo cognition tool (none found — apply manual method)
4. Document SHA and clone status in PR_28_B2_THOR_REPO_COGNITION_HANDOFF.md

## Y Handoff Task

1. Clone https://github.com/QMetaKI/YNode-prep.git — document BLOCKED if fails
2. Scan YNode-prep structure (if found) for handoff protocol patterns
3. Document findings in PR_28_B2_Y_HANDOFF_INTAKE_SUMMARY.md
4. Note: YNode-prep clone BLOCKED in automated environment — proceed with conservative conventions

## Odin Work Kernel Task

Apply the Odin universal work kernel:
- transformation_verb: "compile_semantic_work_contracts"
- output_contract: "candidate_only_static_contracts"
- candidate_only: true
- No app state mutation, no external send, no provider execution

## Expected B2 Artifacts

### Schemas (8)
- v7_1_1_artifact_family.schema.json
- v7_1_1_artifact_lens.schema.json
- v7_1_1_output_contract.schema.json
- v7_1_1_context_capsule.schema.json
- v7_1_1_worklet_graph.schema.json
- v7_1_1_slot_contract.schema.json
- v7_1_1_gaptext.schema.json
- v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.schema.json

### Registries (8)
- v7_1_1_artifact_family_registry.json (8 families required)
- v7_1_1_artifact_lens_registry.json (13 lenses required)
- v7_1_1_output_contract_registry.json
- v7_1_1_context_distillery_contract.json
- v7_1_1_worklet_graph_contract.json
- v7_1_1_slot_forge_contract_registry.json (5 route classes)
- v7_1_1_gaptext_contract.json
- v7_1_1_llm_work_audit_findings_registry.json

### Examples (7)
- artifact_family.example.json
- artifact_lens.example.json
- output_contract.example.json
- context_capsule.example.json
- worklet_graph.example.json
- slot_contract.example.json
- gaptext.example.json

### Tools / Reports / Tests
- tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py
- reports/v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.json
- tests/test_v7_1_1_b2_context_lenses_worklets_slot_gaptext.py (49 tests)

## Commands to Run

```bash
cd /home/user/Odin-Agent-Shell
python -m pip install -e . -q
python tools/v7_1_1/check_b2_context_lenses_worklets_slot_gaptext.py \
  --repo-root . \
  --out reports/v7_1_1_b2_context_lenses_worklets_slot_gaptext_report.json \
  --generated-at-utc 2026-01-01T00:00:00Z
python -m pytest -q tests/test_v7_1_1_b2_context_lenses_worklets_slot_gaptext.py -p no:cacheprovider
python -m pytest -q -p no:cacheprovider
python -m odin.cli validate-all
```

## Acceptance Criteria

- B2 validator exits 0
- B2 report hard_violations == []
- 49 B2 tests pass
- Prior PR tests (PR-25, PR-26, PR-27/B1) pass
- validate-all passes
- Git commit pushed to claude/pr-28-b2-context-lenses-worklets-3osowv
- Return report complete

## claim_boundary

thor_compact_handoff_prompt_is_task_description_not_runtime_proof
