# PREP FINAL-PR-06..08 — Operational Seed / DFAS / Projection Plan

**Claim boundary:** `prep_final_pr_06_08_prepares_future_prs_not_runtime_execution`
**candidate_only:** true
**generated_at_utc:** 2026-01-01T00:00:00Z

---

## Why FINAL-PR-06, PR-07, and PR-08 Are Separated

Each PR implements one operational spine layer. They are separated because:

1. **Testability:** Each spine can be validated independently before the next builds on it.
2. **Reviewability:** Each PR is small enough for a single focused review session.
3. **Failure isolation:** If PR07 has issues, PR08 is not blocked; PR06 is clean.
4. **Token efficiency:** Claude Code sessions can implement one spine per task without context overflow.
5. **Proof clarity:** Each spine has its own proof packet and not-proven list.

The three spines build on each other:
- PR06 (Seed Spine) produces `SeedWorkCapsule` — consumed by PR07.
- PR07 (Field Selection) produces `FieldSelection` — consumed by PR08.
- PR08 (Projection) produces `ProjectionSet` / `CandidateGraph` — consumed by apps and PR09.

---

## Why Release Moves to FINAL-PR-09

Release / Closure was previously positioned after Y Pattern Spine as the next ladder step.

It is moved to FINAL-PR-09 because:

1. **Incompleteness:** The operational routing spines (PR06–08) are the primary intelligence
   layer of the Odin system. Releasing without them would leave the main operational
   routing capability unimplemented.

2. **Evidence requirement:** A proper release closure requires evidence from all spines:
   seed routing metrics, field selection evidence, candidate materialization records.
   These only exist after PR06–08.

3. **Not-proven lock:** The system-wide not-proven lock must enumerate all three spine
   claim boundaries. It cannot be complete until all three spines exist.

4. **Acceptance gate:** "Full acceptance" means all Odin surfaces pass validation.
   Surfaces that don't exist yet cannot be validated.

**Historical PRs are not renumbered.** FINAL-PR-01 through PR-05 and Y-Pattern-Spine
retain their names and merge order. Only the forward-looking roadmap is updated.

---

## PR-by-PR Objectives

### FINAL-PR-06 — Operational Seed Spine + Role Profiles + Seed-to-Work Capsule Compiler

**Objective:** Implement a deterministic seed-routing layer.

**Deliverables:**
- `odin/operational_seed_spine/` module (9 files)
- 12 seed packs defined
- 10 role profiles defined
- Selector routing test: given a context, produces a SeedWorkCapsule
- Local Hub: `GET /demo/seed-route.json`
- CLI: `validate-operational-seed-spine`, `explain-seed-route --demo`, `prove-operational-seed-spine`
- Tests: 12+ tests, all deterministic
- Validator: stdlib-only, integrated into validate-all
- Reports: proof packet + report JSON

**Success metric:** `validate-operational-seed-spine` passes and `explain-seed-route --demo`
returns a valid SeedWorkCapsule with `candidate_only: true`.

### FINAL-PR-07 — DFAS / Field Selection Spine + Coherence / Review Axes

**Objective:** Implement deterministic field selection and coherence scoring.

**Deliverables:**
- `odin/field_selection_spine/` module (8 files)
- 10 review axes defined
- Coherence scorer: given a context, returns CoherenceScore with hole_density
- Field selector: routes to dominant field
- Why-trace: records selection evidence
- Local Hub: `GET /demo/field-selection.json`
- CLI: `validate-field-selection-spine`, `explain-field-selection --demo`, `prove-field-selection-spine`
- Tests: 12+ tests, all deterministic
- Validator: stdlib-only, integrated into validate-all
- Reports: proof packet + report JSON

**Success metric:** `validate-field-selection-spine` passes and `explain-field-selection --demo`
returns a valid FieldSelection with `candidate_only: true` and CoherenceScore.

### FINAL-PR-08 — Projection / Candidate Graph / Materialization Spine

**Objective:** Implement deterministic projection and candidate graph preparation.

**Deliverables:**
- `odin/projection_candidate_spine/` module (8 files)
- 10 materialization levels (M0–M9, matching Y Pattern Spine)
- ProjectionSet with multiple CandidateNodes
- CandidateGraph with edges
- ExpressionPacket with near_code (text only, not executed)
- ReceiptLink with timestamp
- Local Hub: `GET /demo/projection-candidate.json`
- CLI: `validate-projection-candidate-spine`, `explain-projection-candidate --demo`, `prove-projection-candidate-spine`
- Tests: 12+ tests, all deterministic
- Validator: stdlib-only, integrated into validate-all
- Reports: proof packet + report JSON

**Success metric:** `validate-projection-candidate-spine` passes and
`explain-projection-candidate --demo` returns a valid ProjectionSet with `candidate_only: true`.

### FINAL-PR-09 — Release Closure / Full Acceptance / Claim Boundary Lock

**Objective:** Perform final release closure with full evidence record.

**Deliverables:**
- Release readiness matrix (all 9 surfaces)
- Final not-proven lock (system-wide)
- Claim boundary inventory
- CLI validation inventory
- Release evidence packet
- Final return report

**Success metric:** All validators pass, release evidence packet exists,
not-proven lock explicitly names production_readiness and security_certification as not proven.

---

## Interdependencies

```
FINAL-PR-05 (Execution Gate) [merged]
    ↓
Y-PATTERN-SPINE [merged]
    ↓
PREP PR (this PR) — scaffold for PR06–08
    ↓
FINAL-PR-06 (Operational Seed Spine)
    ↓
FINAL-PR-07 (Field Selection Spine)
    ↓
FINAL-PR-08 (Projection Candidate Spine)
    ↓
FINAL-PR-09 (Release Closure)
```

Each arrow means: the latter PR can only start after the former passes all its validators.

---

## Non-Overlap Rules

- PR06 does NOT implement field selection or projection.
- PR07 does NOT implement seed routing or projection.
- PR08 does NOT implement seed routing or field selection.
- PR09 does NOT implement new runtime features (except closure plumbing).
- No PR may modify another PR's primary module directory.
- QIRC core is not extended in PR06–08; only hints are added.
- Y Pattern Spine is not modified in PR06–08; only extended by reference.
- Execution Gate is not modified in PR06–08.

---

## Acceptance Gates (Per PR)

### PR06 Gates:
- `validate-operational-seed-spine` exits 0
- `explain-seed-route --demo` returns valid JSON
- `validate-all` exits 0
- All 12+ tests pass
- Proof packet has `not_proven` list

### PR07 Gates:
- `validate-field-selection-spine` exits 0
- `explain-field-selection --demo` returns valid JSON
- `validate-all` exits 0
- All 12+ tests pass
- Proof packet has `not_proven` list

### PR08 Gates:
- `validate-projection-candidate-spine` exits 0
- `explain-projection-candidate --demo` returns valid JSON
- `validate-all` exits 0
- All 12+ tests pass
- Proof packet has `not_proven` list

### PR09 Gates:
- All PR06–08 validators pass before starting
- `validate-final-pr-09-release-closure` exits 0
- `validate-all` exits 0
- All 10+ tests pass
- Release evidence packet exists

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| PR06 module name collision with `odin/seeds/` | Low | Medium | Create `odin/operational_seed_spine/` as new module; do not modify `odin/seeds/` |
| PR07 coherence score interpreted as probability | Medium | High | Explicitly bound to [0.0,1.0]; add `not_proven: final_truth_claim` to proof packet |
| PR08 ExpressionPacket near_code treated as executable | Medium | High | Field is `str | None`, documented as text only; validator checks no execution claim |
| Forbidden Q-style naming drift | Low | Medium | Validator checks all new prep files; test #14 checks no forbidden names in disallowed sections |
| PR09 started before PR06–08 merged | Low | High | PR09 prompt has mandatory intake step checking merge history |
| validate-all regression | Low | Medium | Each PR adds to validate_all() and runs full suite before merge |

---

## Proof Strategy

Each PR produces a proof packet with:
- `proven`: list of specific structural facts that can be verified by tests
- `not_proven`: list of items that are explicitly not claimed
- `claim_boundary`: a string name identifying the scope

The system-wide proof strategy:
1. Each spine proves its own structural correctness (files exist, data structures parse, selector deterministic).
2. No spine proves runtime intelligence, model inference, or production readiness.
3. PR09 aggregates all spine proof packets into a release evidence packet.
4. The release evidence packet is itself candidate-only — it records evidence, not certification.

---

## Roadmap Amendment

The following roadmap items are updated FORWARD-LOOKING only (no historical renaming):

**Before this prep PR:**
```
... Y-PATTERN-SPINE → RELEASE-CLOSURE
```

**After this prep PR:**
```
... Y-PATTERN-SPINE → PREP PR → FINAL-PR-06 → FINAL-PR-07 → FINAL-PR-08 → FINAL-PR-09 (Release Closure)
```

Affected documents:
- `docs/rebaseline/INSERT_Y_PATTERN_SPINE.md` — NOT modified (historical)
- `registries/prep_final_pr_06_08_plan.v1.json` — NEW (forward-looking)
- This document — NEW (forward-looking)

---

## Regression Prevention

1. Each PR must run `python -m pytest -q -p no:cacheprovider` (full suite) before marking ready.
2. Each PR's validator is called by `validate_all()` — a regression in a new spine fails the global check.
3. Each PR's tests are deterministic — no flakiness permitted.
4. PR06–08 must not modify existing module directories.
5. The prep validator checks no forbidden Q-style names were introduced in new prep files.
6. SYSTEM_MAP.json and FILE_MANIFEST.json updates are validated by `validate-system-map`.

---

## Operating Formula

"Handoff orients. Universal Work bounds. Odin gates. Y Pattern Spine structures.
Operational Seeds route. Field Selection ranks. Projection prepares candidates.
QIRC records. Apps decide. Receipts bind claims."

This formula guides every implementation decision in PR06–PR09.
If an implementation step would give Odin authority over an app decision, it violates this formula.
