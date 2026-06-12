# PREP FINAL-PR-06..08 — Senior Review Audit

**Claim boundary:** `prep_final_pr_06_08_prepares_future_prs_not_runtime_execution`
**candidate_only:** true
**generated_at_utc:** 2026-01-01T00:00:00Z

---

## Senior Reviewer: Findings and Implementation Record

This audit records specific senior reviewer findings for the PREP FINAL-PR-06..08 task.
Each finding is addressed by specific prep artifacts.

---

## Finding 1 — Seeds Must Be Operational, Not Vocabulary

**Problem:** Previous approaches to seed concepts treated them as vocabulary items
("add seed names", "mention resonance"). This produces documentation artifacts with
no implementation value.

**Required fix:** Each seed must be a fully operational `IntentSeed` dataclass with:

| Field | Type | Purpose |
|-------|------|---------|
| `seed_id` | str | Unique identifier |
| `family` | str | Domain grouping |
| `trigger_shapes` | list[str] | Input patterns that activate this seed |
| `input_requirements` | list[str] | Required context fields |
| `output_shape` | str | Describes the output structure |
| `preferred_surfaces` | list[str] | Odin surfaces this seed routes to |
| `allowed_use` | list[str] | Permitted contexts |
| `forbidden_use` | list[str] | Prohibited contexts |
| `qirc_event_hints` | list[str] | Suggested QIRC event emissions |
| `validator_expectations` | list[str] | What validators will check |
| `proof_boundary` | str | Claim boundary for this seed |
| `token_budget_key` | str | References a token budget entry |
| `fallback_behavior` | str | What to do if seed does not match |

**Implementation:** `docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE.md` section 5 fully specifies `IntentSeed`.

**Verification:** `tests/test_prep_final_pr_06_08.py` test #1 verifies prompt file exists with required sections.

---

## Finding 2 — Archetypes Must Become Role Profiles

**Problem:** "Archetype" terminology carries connotations of personality, identity, and
potentially mythological/mystical associations. Runtime personas cause several problems:
- They imply Odin has opinions and preferences beyond its bounded role.
- They create expectation of behavior not verifiable by tests.
- They blur the boundary between Odin (candidate prep) and human operator.

**Required fix:** Represent archetype-like behavior as neutral `RoleProfile` dataclasses.

Required role profiles (neutral operational names):

| Role Profile ID | Family | Purpose |
|----------------|--------|---------|
| `builder` | construction | Builds candidate artifacts |
| `reviewer` | review | Reviews and scores candidates |
| `guard` | safety | Checks claim boundaries and forbidden operations |
| `router` | routing | Routes work to appropriate surfaces |
| `materializer` | materialization | Manages materialization level transitions |
| `proof_binder` | proof | Binds proof packets and not-proven lists |
| `scope_compressor` | compression | Reduces context to essential tokens |
| `lineage_tracker` | lineage | Tracks candidate artifact provenance |
| `devmode_explainer` | explanation | Produces Dev Mode explanations |
| `risk_scanner` | safety | Scans for risk patterns in candidates |

Each role profile must have:
- `role_profile_id`, `family`, `allowed_use`, `forbidden_use`, `review_axes`, `output_shape`, `claim_boundary`

**Forbidden role profile names:** Thor, Odin, Loki, Mjolnir, Tyr, or any mythological name
not already present in historical documents.

**Implementation:** `docs/codex/prompts/FINAL_PR_06_OPERATIONAL_SEED_SPINE.md` sections 5 and 6.

---

## Finding 3 — DFAS Must Not Become Authority

**Problem:** DFAS (Dominant Field Activation / Selection) could be implemented as an
autonomous decision-maker, which would contradict the core Odin law that apps own authority.

**Required fix:** FINAL-PR-07 must implement DFAS purely as deterministic selection support:

What DFAS/Field Selection MUST produce:
- dominant field (candidate recommendation)
- suppressed fields (what was de-prioritized and why)
- center-first routing (deterministic, not probabilistic)
- coherence score (bounded float, not probability)
- hole density (evidence gap metric)
- evidence requirement (what evidence was present)
- route confidence (bounded float)
- review axes (named scoring dimensions)
- why-trace (deterministic evidence record)
- not-proven list (explicit scope limitation)

What DFAS/Field Selection MUST NOT do:
- make final routing decisions on behalf of the app
- claim its output is truth
- execute model calls to generate scores
- apply routes without app confirmation
- use "resonance" as a module name or API key

**Implementation:** `docs/codex/prompts/FINAL_PR_07_FIELD_SELECTION_SPINE.md` section 2 (Non-Scope) and section 5 (Required Concepts).

**Verification:** `registries/prep_final_pr_06_08_plan.v1.json` — PR07 `forbidden_scope` includes `autonomous_decision_authority` and `final_truth_claims`.

---

## Finding 4 — Projection / Shadow Must Be Candidate-Only

**Problem:** The shadow runtime concept from Q Metamodell implies hidden execution —
code that runs invisibly in the background. Implementing this in Odin would create:
- Unverifiable side effects.
- Hidden authority claims.
- Inability to prove candidate-only posture.

**Required fix:** FINAL-PR-08 must implement projection as text-only near-code preparation:

What Projection MUST add:
- `ProjectionSet` — organizes candidate expressions (text, not executable)
- `CandidateGraph` — directed graph of candidate nodes (structure, not execution)
- `MaterializationLevel` — M0–M9 ladder rungs (position tracking, not execution)
- `ExpressionPacket` — near-code as a `str | None` text field (NOT executed by Odin)
- `CandidateComparison` — deterministic comparison (no model scoring)
- `ReceiptLink` — trace linkage (bookkeeping, not authority)
- `ProjectionProofBoundary` — explicit not-proven list

What Projection MUST NOT do:
- execute models
- apply patches to any file
- mutate files outside planned candidate artifacts
- claim real runtime intelligence
- claim generated code is production-proven unless validated by explicit tests
- create hidden background processes

**Implementation:** `docs/codex/prompts/FINAL_PR_08_PROJECTION_CANDIDATE_SPINE.md` section 2 (Non-Scope) and section 11 (Proof Packet).

---

## Finding 5 — Release Must Move to FINAL-PR-09

**Problem:** Release / Closure was positioned immediately after Y Pattern Spine.
Releasing then would skip the primary operational layers (PR06–08), leaving
the system functionally incomplete while claiming full acceptance.

**Required fix:** Update all forward-looking roadmap documents to show Release as FINAL-PR-09.

**Constraints:**
- Historical merged PRs (PR-01 through Y-Pattern-Spine) are NOT renumbered.
- Historical document names are NOT changed.
- Only forward-looking plan documents and the prep registry are updated.

**Implementation artifacts:**
- `docs/rebaseline/PREP_FINAL_PR_06_08_OPERATIONAL_SEED_DFAS_PROJECTION_PLAN.md` — section "Why Release Moves to FINAL-PR-09"
- `registries/prep_final_pr_06_08_plan.v1.json` — PR09 entry with `depends_on: [pr06, pr07, pr08]`
- `docs/codex/audits/PREP_FINAL_PR_06_08_ROADMAP_AUDIT.md` — explicit roadmap audit

**Verification:** `tests/test_prep_final_pr_06_08.py` test #6 verifies PR09 exists with release closure title.
Test #7 verifies PR09 depends_on includes PR06, PR07, and PR08.

---

## Senior Review Verdict: PREP PR

**Overall assessment:** This prep PR correctly addresses all five senior reviewer findings.

| Finding | Status | Evidence |
|---------|--------|----------|
| Seeds must be operational | Addressed | PR06 prompt specifies full IntentSeed dataclass |
| Archetypes must become role profiles | Addressed | PR06 prompt specifies 10 neutral RoleProfiles |
| DFAS must not become authority | Addressed | PR07 prompt specifies candidate-only FieldSelection |
| Projection / Shadow must be candidate-only | Addressed | PR08 prompt specifies text-only ExpressionPacket |
| Release must move to PR09 | Addressed | Registry and plan docs updated |

**Remaining risks (not blocking):**
1. PR06–08 implementations may introduce naming drift — mitigated by validator test #14.
2. PR09 start condition must be enforced — mitigated by mandatory intake step in PR09 prompt.
3. Coherence scores may be misread as probabilities — mitigated by explicit `[0.0,1.0]` bound and `not_proven: final_truth_claim`.

**Recommendation:** Merge this prep PR. Implement PR06 as the next Claude Code session.

---

## Non-Claims

This prep PR does NOT claim:
- FINAL-PR-06 through PR-08 are implemented (they are future PRs).
- Production readiness.
- Security certification.
- Model inference or provider execution.
- App apply or external send.
- Hidden authority.
- Source-pattern runtime import.
