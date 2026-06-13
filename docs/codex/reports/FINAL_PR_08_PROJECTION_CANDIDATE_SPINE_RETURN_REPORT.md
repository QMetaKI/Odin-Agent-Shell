# FINAL-PR-08 Projection Candidate Spine — Return Report

**Branch:** `claude/projection-candidate-spine-pr08-52nvl2`
**Claim boundary:** `projection_candidate_spine_prepares_candidates_not_runtime_execution`
**candidate_only:** true
**generated_at_utc:** 2026-01-01T00:00:00Z

---

## Base Commit

```
5b10d10 Merge pull request #46 from QMetaKI/codex/implement-final-pr-07-field-selection-spine
```

## PR46 / FINAL-PR-07 Merge Confirmation

PR #46 (FINAL-PR-07 Field Selection Spine) confirmed merged into main.
`git log --oneline -15` shows `5b10d10` as HEAD: "Merge pull request #46".

## PR45 / FINAL-PR-06 Merge Confirmation

PR #45 (FINAL-PR-06 Operational Seed Spine) confirmed merged: `590e28c` in git log.

---

## Files Created

### New Module: odin/projection_candidate_spine/

- `odin/projection_candidate_spine/__init__.py`
- `odin/projection_candidate_spine/materialization.py` — MATERIALIZATION_LEVELS M0–M9, validate_materialization_level(), materialization_index()
- `odin/projection_candidate_spine/candidate_graph.py` — CandidateNode, CandidateGraph, build_candidate_graph()
- `odin/projection_candidate_spine/projection_set.py` — ProjectionSet, build_projection_set(), build_projection_set_from_field_selection()
- `odin/projection_candidate_spine/expression_packet.py` — ExpressionPacket, build_expression_packet()
- `odin/projection_candidate_spine/compare.py` — CandidateComparison, compare_candidate_nodes()
- `odin/projection_candidate_spine/receipt_link.py` — ReceiptLink, build_receipt_link()
- `odin/projection_candidate_spine/proof.py` — ProjectionProofBoundary, build_proof_packet(), persist_proof_packet()

### Registry / Schema / Examples

- `registries/final_pr_08_projection_candidate_spine_registry.json`
- `schemas/final_pr_08_projection_candidate_spine_proof_packet.schema.json`
- `examples/final_pr_08/projection_set.example.json`
- `examples/final_pr_08/candidate_graph.example.json`
- `examples/final_pr_08/expression_packet.example.json`
- `examples/final_pr_08/projection_proof_packet.example.json`

### Validator / Tests / Reports

- `tools/rebaseline/check_final_pr_08_projection_candidate_spine.py`
- `tests/test_final_pr_08_projection_candidate_spine.py` (40 tests)
- `reports/final_pr_08_projection_candidate_spine_proof_packet.json`
- `reports/final_pr_08_projection_candidate_spine_report.json`

### Docs / Handoffs / Audits

- `docs/rebaseline/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE.md`
- `docs/codex/handoffs/FINAL_PR_08_REPO_COGNITION_SUMMARY.md`
- `docs/codex/handoffs/FINAL_PR_08_THOR_STYLE_FIELD_TO_PROJECTION_HANDOFF.md`
- `docs/codex/handoffs/FINAL_PR_08_ODIN_AGENT_OPERATOR_WORK_PACKET.md`
- `docs/codex/audits/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE_AUDIT.md`
- `docs/codex/audits/FINAL_PR_08_SENIOR_REVIEW.md`
- `docs/codex/audits/FINAL_PR_08_CODE_REVIEW.md`
- `docs/codex/audits/FINAL_PR_08_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md`
- `docs/codex/reports/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE_RETURN_REPORT.md` (this file)

---

## Files Modified

- `odin/cli.py` — Added validate_projection_candidate_spine(), 3 CLI subparsers, 3 early-return handlers, validate_all() call
- `odin/local_hub/server.py` — Added build_projection_candidate_payload(), GET /demo/projection-candidate.json endpoint
- `odin/local_hub/ui.py` — Added REQUIRED_IDS entry, REQUIRED_COPY entries, HTML section
- `tools/rebaseline/check_prep_final_pr_06_08.py` — Added odin/projection_candidate_spine to IMPLEMENTED_PR_MODULE_DIRS and 2 JSON artifacts to IMPLEMENTED_PR_JSON_ARTIFACTS
- `tests/test_prep_final_pr_06_08.py` — Added odin/projection_candidate_spine to implemented_dirs in 2 test functions
- `SYSTEM_MAP.json` — Added final_pr_08_projection_candidate_spine entry
- `FILE_MANIFEST.json` — Added all 27 new PR08 files with sha256 and size

---

## Repo Cognition Summary

- Base: PR#46 merged (FINAL-PR-07 Field Selection Spine), PR#45 merged (FINAL-PR-06 Operational Seed Spine)
- Working branch: claude/projection-candidate-spine-pr08-52nvl2
- Clean working tree before edits confirmed
- All 4 preflight validators passed: field-selection-spine, operational-seed-spine, prep-final-pr-06-08, y-pattern-spine
- PR07 public interface consumed without modification: select_field_route(), FieldSelection.to_dict()
- PR06 public interface consumed without modification: select_seed_route(), select_field_route_from_seed_route()
- Y materialization ladder from registries/y_materialization_ladder.v1.json: 10 levels M0–M9 used directly
- Local hub pattern: GET /demo/*.json → build_*_payload() → status/candidate_only/claim_boundary/payload
- CLI pattern: validate_*() -> list[str] errors, early-return before elif chain, add to validate_all()

---

## Implementation Summary

FINAL-PR-08 implements the Projection Candidate Spine:

- **Materialization levels M0–M9** defined as constants in materialization.py, used for CandidateNode validation
- **CandidateNode** organizes candidate artifacts with materialization_level, content_summary (text only), proof_boundary
- **CandidateGraph** links CandidateNodes with explicit from/to/relation edges; builds deterministic derived_from chains
- **ProjectionSet** organizes candidate_nodes at M5_projection_set level from source_context metadata
- **ExpressionPacket** carries near_code/near_artifact as text only; near_code_execution=False explicit
- **CandidateComparison** deterministic comparison with winner_id as recommendation only; not_proven includes generated_code_correctness_unless_tested
- **ReceiptLink** links candidates to trace records with deterministic link_id; bound_at_utc=2026-01-01T00:00:00Z
- **ProjectionProofBoundary** and build_proof_packet() with required proven/not_proven lists
- All IDs deterministic via canonical JSON + SHA256 (no uuid4, no random, no datetime.now)

---

## PR07 Integration Summary

`build_projection_set_from_field_selection(field_selection)` accepts both FieldSelection objects and dicts (via hasattr/isinstance adapter). It:
1. Extracts dominant_field, why_trace_id, field_confidence from FieldSelection
2. Builds source_context with field_selection_available=True, preserves field_id and why_trace evidence
3. Creates a CandidateNode at M6_candidate_artifact level
4. Returns a ProjectionSet at M5_projection_set with candidate_only=True and correct claim_boundary

No modifications to odin/field_selection_spine/.

---

## PR06 Upstream Chain Summary

Full chain confirmed via test_pr06_pr07_pr08_chain_works():
```python
seed = select_seed_route({"trigger_shape": "repo", "work_type": "repo"})
fs = select_field_route_from_seed_route(seed)
ps = build_projection_set_from_field_selection(fs)
assert ps.candidate_only is True
assert ps.claim_boundary == CLAIM_BOUNDARY
```
All outputs are candidate_only=True at each stage. No model/provider/app apply.

---

## Validators Run

```
python -m odin.cli validate-projection-candidate-spine   → OK
python -m odin.cli explain-projection-candidate --demo   → valid JSON (candidate_only: true)
python -m odin.cli prove-projection-candidate-spine      → OK
python -m odin.cli validate-field-selection-spine        → OK
python -m odin.cli validate-operational-seed-spine       → OK
python -m odin.cli validate-prep-final-pr-06-08          → OK
python -m odin.cli validate-y-pattern-spine              → OK
python -m odin.cli validate-all                          → OK
python tools/rebaseline/check_final_pr_08_projection_candidate_spine.py --repo-root . --out reports/final_pr_08_projection_candidate_spine_report.json --generated-at-utc 2026-01-01T00:00:00Z → ok
```

---

## Tests Run — Full Suite Result

```
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

Result: **40 passed** (test_final_pr_08_projection_candidate_spine.py) + 20 passed (test_prep_final_pr_06_08.py) + 22 passed (test_final_pr_07_field_selection_spine.py) + 20 passed (test_final_pr_06_operational_seed_spine.py)

Full suite exact result:

```
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider --tb=no
2353 passed, 2 skipped in 304.68s (0:05:04)
```

---

## Known Gaps

None. All acceptance gates passed.

---

## Claim Boundary

`projection_candidate_spine_prepares_candidates_not_runtime_execution`

---

## Not-Proven List

- hidden_runtime
- model_inference
- provider_execution
- app_apply
- app_state_mutation
- external_send
- generated_code_correctness
- production_readiness
- security_certification

---

## Senior Reviewer Fixes Applied

None required. All senior review checklist items passed on first implementation.

## Senior Code Reviewer Fixes Applied

None required. All code review checklist items passed on first implementation.

---

## Thor/Odin/Y Findings

See `docs/codex/audits/FINAL_PR_08_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md` for full findings.

Key findings:
1. Y materialization ladder reuse was the highest-value artifact — all 10 levels directly used for CandidateNode validation
2. near_code_execution=False explicit field is the most important single design decision — makes not-execution boundary machine-checkable
3. PR07 FieldSelection adapter pattern (hasattr/isinstance) preserved clean integration without modifying PR07

---

## Recommendation for FINAL-PR-09

Before running the PR09 Release Closure prompt:
1. Add explicit gate: "Input must include a valid PR08 ProjectionSet from build_projection_set_from_field_selection()"
2. PR09 validator must confirm reports/final_pr_08_projection_candidate_spine_proof_packet.json exists
3. Thor handoff must compile PR06+PR07+PR08 chain evidence before specifying release closure work
4. PR09 target: M9_release_evidence on Y materialization ladder
5. All PR06/PR07/PR08 module directories must be in PR09 forbidden_edits list
