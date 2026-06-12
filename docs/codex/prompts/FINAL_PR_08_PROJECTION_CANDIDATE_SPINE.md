# FINAL-PR-08 — Projection / Candidate Graph / Materialization Spine

**Claim boundary:** `projection_candidate_spine_prepares_candidates_not_runtime_execution`
**candidate_only:** true
**app_owned_apply:** true
**generated_at_utc:** 2026-01-01T00:00:00Z
**depends_on:** FINAL-PR-07 (Field Selection Spine merged)

---

## Purpose

This prompt instructs a new Claude Code session to implement the Projection Candidate Spine:
a deterministic layer that organizes inputs into projection sets, builds candidate graphs,
manages materialization levels, compiles expression packets, and links trace receipts.
Nothing in this module executes models, applies patches, or mutates runtime state.
All outputs are candidate artifacts suitable for app consumption and QIRC recording.

---

## 0. Repo-Real Intake Steps (MANDATORY — do before any edit)

1. `git status` — confirm clean working tree on the designated branch.
2. `git log --oneline -10` — confirm base includes FINAL-PR-07 merge commit.
3. Inspect: `odin/field_selection_spine/`, `odin/operational_seed_spine/`, `odin/y_pattern_spine/`.
4. Inspect: `odin/candidates/`, `odin/packets/`, `odin/output/`, `odin/shadow_runtime/`.
5. Read: `registries/y_materialization_ladder.v1.json`.
6. Read: `registries/final_pr_07_field_selection_spine_registry.json`.
7. Read: `registries/prep_final_pr_06_08_plan.v1.json` — confirm PR08 entry.
8. Read: `docs/codex/handoffs/PREP_FINAL_PR_06_08_REPO_REALITY_INTAKE.md`.
9. Run: `python -m odin.cli validate-field-selection-spine` — must pass before starting.
10. Run: `python -m pytest -q tests/test_final_pr_07_field_selection_spine.py -p no:cacheprovider` — must pass.

Do NOT proceed if validate-field-selection-spine fails.

---

## 1. Scope

Implement a deterministic Projection Candidate Spine module with:

- ProjectionSet: organizes multiple candidate expressions from a context.
- CandidateNode: a single candidate artifact node with materialization level.
- CandidateGraph: directed graph linking candidate nodes.
- MaterializationLevel: enum/constant set for M0–M9 ladder rungs.
- ExpressionPacket: a compiled, near-code/near-artifact candidate package.
- CandidateComparison: deterministic comparison of two candidate nodes.
- ReceiptLink: links a candidate to a trace/receipt record.
- Proof module: records proof boundaries and not-proven list.

---

## 2. Non-Scope

- Do NOT execute models, generate code via model calls, or call external APIs.
- Do NOT apply patches or mutate app state.
- Do NOT send external messages.
- Do NOT imply hidden runtime or shadow execution.
- Do NOT claim generated code is production-proven unless validated by tests.
- Do NOT import Q Metamodell / cutk1 as runtime truth.
- Do NOT add new Q-style runtime names.
- Do NOT connect to public networks.
- Do NOT implement Release Closure (PR09) in this PR.
- Do NOT break existing PR06 or PR07 modules.

---

## 3. Allowed Files

**Create (new):**
- `odin/projection_candidate_spine/__init__.py`
- `odin/projection_candidate_spine/projection_set.py`
- `odin/projection_candidate_spine/candidate_graph.py`
- `odin/projection_candidate_spine/materialization.py`
- `odin/projection_candidate_spine/expression_packet.py`
- `odin/projection_candidate_spine/compare.py`
- `odin/projection_candidate_spine/receipt_link.py`
- `odin/projection_candidate_spine/proof.py`
- `schemas/final_pr_08_projection_candidate_spine_proof_packet.schema.json`
- `registries/final_pr_08_projection_candidate_spine_registry.json`
- `examples/final_pr_08/projection_set.example.json`
- `examples/final_pr_08/candidate_graph.example.json`
- `examples/final_pr_08/expression_packet.example.json`
- `examples/final_pr_08/projection_proof_packet.example.json`
- `docs/rebaseline/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE.md`
- `docs/codex/audits/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE_AUDIT.md`
- `docs/codex/audits/FINAL_PR_08_SENIOR_REVIEW.md`
- `docs/codex/reports/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE_RETURN_REPORT.md`
- `docs/codex/handoffs/FINAL_PR_08_REPO_COGNITION_SUMMARY.md`
- `docs/codex/handoffs/FINAL_PR_08_ODIN_AGENT_OPERATOR_WORK_PACKET.md`
- `reports/final_pr_08_projection_candidate_spine_report.json`
- `reports/final_pr_08_projection_candidate_spine_proof_packet.json`
- `tests/test_final_pr_08_projection_candidate_spine.py`
- `tools/rebaseline/check_final_pr_08_projection_candidate_spine.py`

**Update (existing):**
- `odin/cli.py` — add `validate-projection-candidate-spine`, `explain-projection-candidate`, `prove-projection-candidate-spine`
- `odin/local_hub/server.py` — add `GET /demo/projection-candidate.json` endpoint
- `odin/local_hub/ui.py` — add Dev Mode projection candidate section
- `SYSTEM_MAP.json` — add `final_pr_08_projection_candidate_spine` entry
- `FILE_MANIFEST.json` — add new files

---

## 4. Forbidden Changes

- Do NOT modify: `odin/operational_seed_spine/`, `odin/field_selection_spine/`, `odin/y_pattern_spine/`
- Do NOT modify: `odin/execution_gate/`, `odin/proof_chain/`, `odin/final_pr_ladder/`
- Do NOT modify: existing schemas, registries, or tests unless adding precise new entries.
- Do NOT delete any existing file.
- Do NOT introduce new `q_*` named modules, keys, or CLI commands.

---

## 5. Required Concepts

### MaterializationLevel (constants)
Required levels (must match the Y Pattern Spine materialization ladder):
- `M0_raw_input`
- `M1_handoff_context`
- `M2_universal_work`
- `M3_seed_route`
- `M4_field_selection`
- `M5_projection_set`
- `M6_candidate_artifact`
- `M7_response_packet`
- `M8_trace_receipt`
- `M9_release_evidence`

### ProjectionSet (dataclass)
Fields:
- `projection_id: str`
- `source_context: dict`
- `candidate_nodes: list[CandidateNode]`
- `materialization_level: str`
- `candidate_only: bool = True`
- `claim_boundary: str`

### CandidateNode (dataclass)
Fields:
- `node_id: str`
- `label: str`
- `materialization_level: str`
- `content_summary: str`
- `proof_boundary: str`
- `receipt_link_id: str | None`

### CandidateGraph (dataclass)
Fields:
- `graph_id: str`
- `nodes: list[CandidateNode]`
- `edges: list[dict]`  — list of `{from_node_id, to_node_id, relation}`
- `entry_node_id: str`
- `candidate_only: bool = True`

### ExpressionPacket (dataclass)
Fields:
- `packet_id: str`
- `candidate_node: CandidateNode`
- `near_code: str | None`  — near-code text, NOT executed
- `near_artifact: str | None`  — near-artifact description, NOT applied
- `proof_boundary: str`
- `trace_receipt_id: str | None`
- `candidate_only: bool = True`
- `claim_boundary: str`

### CandidateComparison (dataclass)
Fields:
- `comparison_id: str`
- `node_a_id: str`
- `node_b_id: str`
- `winner_id: str | None`
- `comparison_axes: list[str]`
- `not_proven: list[str]`

### ReceiptLink (dataclass)
Fields:
- `link_id: str`
- `candidate_node_id: str`
- `trace_record_ref: str`
- `qirc_event_ref: str | None`
- `bound_at_utc: str`

### ProjectionProofBoundary (dataclass)
Fields:
- `boundary_id: str`
- `proven: list[str]`
- `not_proven: list[str]`
- `claim_boundary: str`

---

## 6. Required Local Hub Surfaces

### Endpoint
```
GET /demo/projection-candidate.json
```
Returns a demo `ProjectionSet` JSON with `candidate_only: true` and `claim_boundary`.

### Dev Mode UI section
Label: `"Projection Candidate Spine: available"`
Dev Mode copy: `"Projection Candidate Spine organizes candidate artifacts on the materialization ladder and links them to trace receipts."`
Normal user copy: `"Odin organizes candidate work into structured sets."`

---

## 7. Required CLI Commands

```
python -m odin.cli validate-projection-candidate-spine
python -m odin.cli explain-projection-candidate --demo
python -m odin.cli prove-projection-candidate-spine
```

All three must be wired into `odin/cli.py`.
`validate-projection-candidate-spine` must be called from `validate_all()`.

---

## 8. Required Validator

File: `tools/rebaseline/check_final_pr_08_projection_candidate_spine.py`

Requirements:
- stdlib only
- accepts `--repo-root`, `--out`, optional `--generated-at-utc`
- validates all required module files exist
- validates all 10 materialization levels defined
- validates registry JSON parses
- validates schema file exists
- validates example files have `candidate_only: true`
- validates ExpressionPacket near_code does NOT claim execution
- validates proof packet has `not_proven` list including `hidden_runtime` and `model_inference`
- validates no forbidden Q-style names in new files
- writes `reports/final_pr_08_projection_candidate_spine_report.json`

---

## 9. Required Tests

File: `tests/test_final_pr_08_projection_candidate_spine.py`

Minimum 12 tests covering:
1. Module `odin/projection_candidate_spine/__init__.py` importable
2. All 10 materialization levels defined
3. ProjectionSet can be constructed with candidate nodes
4. ProjectionSet has `candidate_only: True`
5. ProjectionSet has `claim_boundary`
6. CandidateGraph has nodes and edges
7. ExpressionPacket near_code field is a string or None (not executed)
8. CandidateComparison has `not_proven` list
9. ReceiptLink has `bound_at_utc`
10. Proof module not_proven includes `hidden_runtime` and `model_inference`
11. Validator returns ok (no errors)
12. CLI `validate-projection-candidate-spine` returns 0

---

## 10. Required Reports

- `reports/final_pr_08_projection_candidate_spine_report.json`
- `reports/final_pr_08_projection_candidate_spine_proof_packet.json`

Both must include `candidate_only: true`, `claim_boundary`, `not_proven` list.

---

## 11. Proof Packet Expectations

```json
{
  "proven": ["materialization_levels_defined", "projection_set_candidate_only", "candidate_graph_structured", "expression_packet_near_code_not_executed", "receipt_link_traceable"],
  "not_proven": ["hidden_runtime", "model_inference", "provider_execution", "app_apply", "app_state_mutation", "external_send", "generated_code_correctness", "production_readiness", "security_certification"],
  "claim_boundary": "projection_candidate_spine_prepares_candidates_not_runtime_execution",
  "candidate_only": true
}
```

---

## 12. Not-Proven List

- hidden_runtime
- model_inference
- provider_execution
- app_apply
- app_state_mutation
- external_send_authority
- generated_code_correctness_unless_tested
- public_network_access
- production_readiness
- security_certification

---

## 13. Senior Reviewer Checklist

- [ ] All 10 materialization levels present and match Y Pattern Spine ladder
- [ ] ExpressionPacket near_code field is text only — no execution implied
- [ ] CandidateGraph edges have explicit from/to/relation structure
- [ ] ReceiptLink has bound_at_utc timestamp
- [ ] ProjectionSet always has `candidate_only: True`
- [ ] CandidateComparison has `not_proven` list
- [ ] Proof packet not_proven includes `hidden_runtime` and `generated_code_correctness`
- [ ] No shadow runtime or hidden execution implied
- [ ] No new q_* runtime names introduced
- [ ] validate_all() calls validate_projection_candidate_spine()

---

## 14. Code Reviewer Checklist

- [ ] No runtime module execution
- [ ] No provider API calls
- [ ] No app state mutation
- [ ] No public network access
- [ ] No hidden authority
- [ ] No forbidden naming drift
- [ ] Validator is stdlib-only
- [ ] Tests deterministic
- [ ] Existing PR06 and PR07 tests still pass
- [ ] FILE_MANIFEST and SYSTEM_MAP updated

---

## 15. Acceptance Gates

1. `python -m odin.cli validate-projection-candidate-spine` exits 0
2. `python -m odin.cli explain-projection-candidate --demo` prints valid JSON
3. `python -m odin.cli prove-projection-candidate-spine` exits 0
4. `python -m odin.cli validate-all` exits 0
5. `python -m pytest -q tests/test_final_pr_08_projection_candidate_spine.py -p no:cacheprovider` passes all tests
6. `python -m pytest -q -p no:cacheprovider` full suite passes
7. `reports/final_pr_08_projection_candidate_spine_proof_packet.json` exists with valid structure

---

## 16. Claim Boundary

`projection_candidate_spine_prepares_candidates_not_runtime_execution`

This PR does NOT claim:
- hidden runtime or shadow execution
- model inference or provider execution
- app apply, app state mutation, or external send
- generated code correctness unless validated by explicit tests
- public network access
- production readiness
- security certification
- that projection sets are executed work products
