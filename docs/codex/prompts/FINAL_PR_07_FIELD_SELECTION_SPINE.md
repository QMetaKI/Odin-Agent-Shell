# FINAL-PR-07 — DFAS / Field Selection Spine + Coherence / Review Axes

**Claim boundary:** `field_selection_scores_routes_not_truth`
**candidate_only:** true
**app_owned_apply:** true
**generated_at_utc:** 2026-01-01T00:00:00Z
**depends_on:** FINAL-PR-06 (Operational Seed Spine merged)

---

## Purpose

This prompt instructs a new Claude Code session to implement the Field Selection Spine:
a deterministic layer that selects dominant fields, scores coherence, identifies holes,
and produces route recommendations with review axes. The output is a ranked candidate
routing recommendation — not a final decision, not autonomous authority.

DFAS (Dominant Field Activation / Selection) is referenced in the title for continuity
with source pattern terminology. New runtime module names use neutral operational terms.

---

## 0. Repo-Real Intake Steps (MANDATORY — do before any edit)

1. `git status` — confirm clean working tree on the designated branch.
2. `git log --oneline -10` — confirm base includes FINAL-PR-06 merge commit.
3. Inspect: `odin/operational_seed_spine/`, `odin/y_pattern_spine/`.
4. Inspect: `odin/why_trace/`, `odin/quality/`, `odin/precompute/`.
5. Read: `registries/final_pr_06_operational_seed_spine_registry.json`.
6. Read: `registries/prep_final_pr_06_08_plan.v1.json` — confirm PR07 entry.
7. Read: `docs/codex/handoffs/PREP_FINAL_PR_06_08_REPO_REALITY_INTAKE.md`.
8. Run: `python -m odin.cli validate-operational-seed-spine` — must pass before starting.
9. Run: `python -m pytest -q tests/test_final_pr_06_operational_seed_spine.py -p no:cacheprovider` — must pass.

Do NOT proceed if validate-operational-seed-spine fails.

---

## 1. Scope

Implement a deterministic Field Selection Spine module with:

- Field signal definitions: dominant field, suppressed fields.
- Review axes: named scoring dimensions.
- Coherence scorer: scores a context against review axes.
- Hole density: measures evidence gaps.
- Selector: selects dominant field from a work context.
- Why-trace: records why a field was selected.
- Proof module: records proof boundaries and not-proven list.

The output is always a route recommendation / candidate ranking, never a final truth.

---

## 2. Non-Scope

- Do NOT implement autonomous decision authority.
- Do NOT execute providers or call external APIs.
- Do NOT mutate app state, apply patches, or send external messages.
- Do NOT claim field selection scores are final truth.
- Do NOT import Q Metamodell / cutk1 as runtime truth.
- Do NOT add new Q-style runtime names.
- Do NOT connect to public networks.
- Do NOT implement Projection (PR08) or Release Closure (PR09) in this PR.
- Do NOT break existing Operational Seed Spine (PR06).

---

## 3. Allowed Files

**Create (new):**
- `odin/field_selection_spine/__init__.py`
- `odin/field_selection_spine/fields.py`
- `odin/field_selection_spine/review_axes.py`
- `odin/field_selection_spine/coherence.py`
- `odin/field_selection_spine/hole_density.py`
- `odin/field_selection_spine/selector.py`
- `odin/field_selection_spine/why_trace.py`
- `odin/field_selection_spine/proof.py`
- `schemas/final_pr_07_field_selection_spine_proof_packet.schema.json`
- `registries/final_pr_07_field_selection_spine_registry.json`
- `examples/final_pr_07/field_signal.example.json`
- `examples/final_pr_07/field_selection.example.json`
- `examples/final_pr_07/coherence_score.example.json`
- `examples/final_pr_07/field_why_trace.example.json`
- `docs/rebaseline/FINAL_PR_07_FIELD_SELECTION_SPINE.md`
- `docs/codex/audits/FINAL_PR_07_FIELD_SELECTION_SPINE_AUDIT.md`
- `docs/codex/audits/FINAL_PR_07_SENIOR_REVIEW.md`
- `docs/codex/reports/FINAL_PR_07_FIELD_SELECTION_SPINE_RETURN_REPORT.md`
- `docs/codex/handoffs/FINAL_PR_07_REPO_COGNITION_SUMMARY.md`
- `docs/codex/handoffs/FINAL_PR_07_ODIN_AGENT_OPERATOR_WORK_PACKET.md`
- `reports/final_pr_07_field_selection_spine_report.json`
- `reports/final_pr_07_field_selection_spine_proof_packet.json`
- `tests/test_final_pr_07_field_selection_spine.py`
- `tools/rebaseline/check_final_pr_07_field_selection_spine.py`

**Update (existing):**
- `odin/cli.py` — add `validate-field-selection-spine`, `explain-field-selection`, `prove-field-selection-spine`
- `odin/local_hub/server.py` — add `GET /demo/field-selection.json` endpoint
- `odin/local_hub/ui.py` — add Dev Mode field selection section
- `SYSTEM_MAP.json` — add `final_pr_07_field_selection_spine` entry
- `FILE_MANIFEST.json` — add new files

---

## 4. Forbidden Changes

- Do NOT modify: `odin/operational_seed_spine/`, `odin/y_pattern_spine/`, `odin/execution_gate/`, `odin/proof_chain/`
- Do NOT modify: existing schemas, registries, or tests unless adding precise new entries.
- Do NOT delete any existing file.
- Do NOT add files outside the allowed list.
- Do NOT introduce new `q_*` named modules, keys, or CLI commands.

---

## 5. Required Concepts

### FieldSignal (dataclass)
Fields:
- `field_id: str` — unique field identifier
- `field_name: str`
- `signal_weight: float` — 0.0 to 1.0
- `evidence_list: list[str]`
- `suppression_reason: str | None`

### DominantField (dataclass)
Fields:
- `field_id: str`
- `confidence: float`
- `review_axes_applied: list[str]`
- `why_trace_id: str`

### SuppressedField (dataclass)
Fields:
- `field_id: str`
- `suppression_reason: str`

### ReviewAxis (dataclass)
Fields:
- `axis_id: str`
- `description: str`
- `scoring_method: str`

Required review axes (axis_id values):
- `scope`
- `claim_boundary`
- `repo_reality`
- `runtime_truth`
- `locality`
- `candidate_integrity`
- `evidence`
- `token_efficiency`
- `app_authority`
- `release_readiness`

### CoherenceScore (dataclass)
Fields:
- `overall_score: float`
- `axis_scores: dict[str, float]`
- `hole_density: float`
- `evidence_requirement_met: bool`
- `route_confidence: float`

### HoleDensity
Float 0.0–1.0 measuring ratio of missing evidence to required evidence.

### FieldSelection (dataclass)
Output of selector. Fields:
- `dominant_field: DominantField`
- `suppressed_fields: list[SuppressedField]`
- `coherence_score: CoherenceScore`
- `review_axes_applied: list[str]`
- `why_trace: FieldWhyTrace`
- `route_recommendation: str`
- `candidate_only: bool = True`
- `claim_boundary: str`

### FieldWhyTrace (dataclass)
Fields:
- `trace_id: str`
- `field_id: str`
- `reason_tokens: list[str]`
- `evidence_items: list[str]`
- `not_proven: list[str]`

---

## 6. Required Local Hub Surfaces

### Endpoint
```
GET /demo/field-selection.json
```
Returns a demo `FieldSelection` JSON with `candidate_only: true` and `claim_boundary`.

### Dev Mode UI section
Label: `"Field Selection Spine: available"`
Dev Mode copy: `"Field Selection Spine scores work context against review axes and recommends a dominant routing field."`
Normal user copy: `"Odin ranks candidate routes by coherence."`

---

## 7. Required CLI Commands

```
python -m odin.cli validate-field-selection-spine
python -m odin.cli explain-field-selection --demo
python -m odin.cli prove-field-selection-spine
```

All three must be wired into `odin/cli.py`.
`validate-field-selection-spine` must be called from `validate_all()`.

---

## 8. Required Validator

File: `tools/rebaseline/check_final_pr_07_field_selection_spine.py`

Requirements:
- stdlib only
- accepts `--repo-root`, `--out`, optional `--generated-at-utc`
- validates all required module files exist
- validates registry JSON parses with required review axis IDs
- validates field concept definitions are present
- validates schema file exists
- validates example files have `candidate_only: true`
- validates proof packet has `not_proven` list
- validates no forbidden Q-style names
- writes `reports/final_pr_07_field_selection_spine_report.json`

---

## 9. Required Tests

File: `tests/test_final_pr_07_field_selection_spine.py`

Minimum 12 tests covering:
1. Module `odin/field_selection_spine/__init__.py` importable
2. All required review axes defined
3. Selector returns a FieldSelection for a test input
4. FieldSelection has `candidate_only: True`
5. FieldSelection has `claim_boundary`
6. CoherenceScore fields present
7. HoleDensity is float in [0.0, 1.0]
8. WhyTrace has `not_proven` list
9. Suppressed fields list is not None
10. Proof module not_proven includes required entries
11. Validator returns ok (no errors)
12. CLI `validate-field-selection-spine` returns 0

---

## 10. Required Reports

- `reports/final_pr_07_field_selection_spine_report.json`
- `reports/final_pr_07_field_selection_spine_proof_packet.json`

Both must include `candidate_only: true`, `claim_boundary`, `not_proven` list.

---

## 11. Proof Packet Expectations

```json
{
  "proven": ["review_axes_defined", "coherence_scorer_deterministic", "field_selection_candidate_only", "why_trace_recorded"],
  "not_proven": ["autonomous_decision_authority", "final_truth_claim", "model_inference", "provider_execution", "app_apply", "app_state_mutation", "external_send", "production_readiness", "security_certification"],
  "claim_boundary": "field_selection_scores_routes_not_truth",
  "candidate_only": true
}
```

---

## 12. Not-Proven List

- autonomous_decision_authority
- final_truth_claim
- model_inference
- provider_execution
- app_apply
- app_state_mutation
- external_send_authority
- public_network_access
- production_readiness
- security_certification

---

## 13. Senior Reviewer Checklist

- [ ] FieldSelection output always has `candidate_only: True`
- [ ] Selector is purely deterministic (no model calls, no randomness beyond seed inputs)
- [ ] CoherenceScore is a number between 0.0 and 1.0, not a probability claim
- [ ] All 10 required review axes present with non-empty descriptions
- [ ] WhyTrace records evidence items, not fabricated reasoning
- [ ] Route recommendation is a string hint, not an authority command
- [ ] No new q_* runtime names introduced
- [ ] DFAS title reference is only in doc/title, not in module names
- [ ] Proof packet not_proven includes autonomous_decision_authority and final_truth_claim
- [ ] validate_all() calls validate_field_selection_spine()

---

## 14. Code Reviewer Checklist

- [ ] No runtime module execution (no subprocess to models)
- [ ] No provider API calls
- [ ] No app state mutation
- [ ] No public network access
- [ ] No hidden authority
- [ ] No forbidden naming drift
- [ ] Validator is stdlib-only
- [ ] Tests deterministic (no random, network, model calls)
- [ ] Existing PR06 tests still pass
- [ ] FILE_MANIFEST and SYSTEM_MAP updated

---

## 15. Acceptance Gates

1. `python -m odin.cli validate-field-selection-spine` exits 0
2. `python -m odin.cli explain-field-selection --demo` prints valid JSON
3. `python -m odin.cli prove-field-selection-spine` exits 0
4. `python -m odin.cli validate-all` exits 0
5. `python -m pytest -q tests/test_final_pr_07_field_selection_spine.py -p no:cacheprovider` passes all tests
6. `python -m pytest -q -p no:cacheprovider` full suite passes
7. `reports/final_pr_07_field_selection_spine_proof_packet.json` exists with valid structure

---

## 16. Claim Boundary

`field_selection_scores_routes_not_truth`

This PR does NOT claim:
- autonomous decision authority
- final truth about routing
- model inference or provider execution
- app apply, app state mutation, or external send
- public network access
- production readiness
- security certification
- that DFAS is a mystical system
- that coherence scores are probabilities or guarantees
