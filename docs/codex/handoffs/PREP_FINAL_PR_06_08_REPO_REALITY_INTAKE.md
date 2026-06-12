# PREP FINAL-PR-06..08 — Repo Reality Intake

**Claim boundary:** `prep_final_pr_06_08_prepares_future_prs_not_runtime_execution`
**candidate_only:** true
**generated_at_utc:** 2026-01-01T00:00:00Z

---

## Purpose

This document records the repo-real current state relevant to FINAL-PR-06 through PR-08.
It is the ground truth for Claude Code sessions implementing PR06, PR07, and PR08.

---

## 1. Current Ladder State

| PR Slot | ID | Description | Status |
|---------|-----|-------------|--------|
| 1 | FINAL-PR-01 | Simple Local Hub / Browser UI | Merged |
| 2 | FINAL-PR-02 | Model Picker / Connected Apps / Demo Universal Work | Merged |
| 3 | FINAL-PR-03 | QIRC Core First Slice / Activity Trace Receipt Dev Mode | Merged |
| 4 | FINAL-PR-04 | Provider Policy / Local Candidate Probe / Runtime Security Smoke | Merged |
| 5 | FINAL-PR-05 | Execution Gate / Deterministic Mock Provider / Proof Chain / Ladder Scaffold | Merged |
| 6 | Y-PATTERN-SPINE | Y Pattern Spine — Neutral Operational Pattern Layer | Merged |
| 7 | PREP PR | This prep PR — prepares PR06..08, moves Release to PR09 | This PR |
| 8 | FINAL-PR-06 | Operational Seed Spine + Role Profiles + Work Capsule Compiler | Future |
| 9 | FINAL-PR-07 | Field Selection Spine + Coherence / Review Axes | Future |
| 10 | FINAL-PR-08 | Projection / Candidate Graph / Materialization Spine | Future |
| 11 | FINAL-PR-09 | Release Closure / Full Acceptance / Claim Boundary Lock | Future |

---

## 2. Existing Handoff / Universal Work Surfaces

**Location:** `odin/universal_work/`

Status: Implemented in prior PRs.

Key artifact: `UniversalWork` — the bounded work representation passed from handoff to execution.

Relevant to PR06: Seed spine will route work into Universal Work structures.
Relevant to PR07: Field selection will score Universal Work context.
Relevant to PR08: Projection sets will expand from Universal Work.

---

## 3. Existing Local Hub Surfaces

**Location:** `odin/local_hub/`

Files:
- `server.py` — FastAPI (or similar) hub server with `/demo/*` endpoints
- `ui.py` — UI rendering for Dev Mode and normal mode
- `model_picker.py`, `connected_apps.py`, `demo_universal_work.py`
- `policy.py`, `proof.py`, `proof_pr02.py`, `proof_pr03.py`
- `surface_registry.py`

Demo endpoints already present:
- From PR02: `/demo/universal-work.json`
- From PR03: `/qirc/activity-trace.json`, `/qirc/receipts.json`
- From PR04: `/local-candidate/probe.json`
- From PR05: `/execution-gate/status.json`, `/execution-gate/mock`, `/final-pr-ladder/scaffold.json`
- From Y Pattern Spine: `/demo/y-route-hint.json`, `/demo/y-work-capsule.json`, `/demo/y-projection-set.json`

Future PR06 must add: `GET /demo/seed-route.json`
Future PR07 must add: `GET /demo/field-selection.json`
Future PR08 must add: `GET /demo/projection-candidate.json`

---

## 4. Existing QIRC Surfaces

**Location:** `odin/qirc_core/`

Files: `__init__.py`, `bus.py`, `channels.py`, `events.py`, `policy.py`, `proof.py`

QIRC is the semantic event bus. It coordinates and records — it does not authorize or mutate.

Relevant to PR06: Seed QircHints will suggest event emissions. QIRC does not execute them.
Relevant to PR07: Field selection may emit `field_selected` events as hints.
Relevant to PR08: Projection candidate materalization hints go to QIRC.

Existing event type registry: `registries/qirc_event_type_registry.json`
Existing channel registry: `registries/qirc_channel_registry.json`

---

## 5. Existing Y Pattern Spine Surfaces

**Location:** `odin/y_pattern_spine/`

Files:
- `__init__.py`, `patterns.py`, `profiles.py`, `materialization.py`
- `scoring.py`, `explain.py`, `proof.py`, `token_budget.py`, `capsules.py`

Y Pattern Spine provides:
- Pattern families (14 total including orientation, token_efficiency, review, route_selection, etc.)
- Materialization ladder: M0–M9
- Projection set schema: `schemas/y_projection_set.schema.json`
- Work capsule schema: `schemas/y_work_capsule.schema.json`
- Token budget modes: `registries/y_token_budget_registry.v1.json`
- Source pattern mine: `registries/y_source_pattern_mine.v1.json`

**Important for PR06–08:** The Y Pattern Spine materialization ladder M0–M9 must be respected by all future spines. PR08 must use the same level names.

Existing demo endpoints: `/demo/y-route-hint.json`, `/demo/y-work-capsule.json`, `/demo/y-projection-set.json`

---

## 6. Existing Execution Gate Surfaces

**Location:** `odin/execution_gate/`

Files: `__init__.py`, `gateway.py`, `local_candidate_policy.py`, `mock_provider.py`, `policy.py`, `proof.py`

Execution Gate allows deterministic mock execution only.
No real model/provider execution in any future PR unless the gate policy is explicitly updated.

CLI commands: `validate-final-pr-05-execution-gate`, `prove-final-pr-05-execution-gate`

**Important for PR06–08:** Seed spine and field selection do NOT use the execution gate.
Only explicit mock execution scenarios go through the gate.

---

## 7. Existing Proof Chain / Final PR Ladder Surfaces

**Location:** `odin/proof_chain/`, `odin/final_pr_ladder/`

Proof chain: `registry.py`, `builder.py`
Final PR ladder: `compiler.py`, `templates.py`, `proof.py`

The ladder scaffold is built from `registries/final_pr_ladder_scaffold*` patterns.
Each new PR must produce a proof packet with `proven`, `not_proven`, `claim_boundary`.

---

## 8. Existing Seeds / Patterns Surfaces (Legacy)

**Location:** `odin/seeds/`, `odin/patterns/`

These are pre-existing modules from the legacy build ladder.
`odin/seeds/` — app-level seed packs (not to be confused with the new Operational Seed Spine).
`odin/patterns/` — pattern intake and compilation.

**Important:** PR06 creates a NEW `odin/operational_seed_spine/` module.
It does NOT replace or rename `odin/seeds/`.
These coexist as different abstraction layers.

Existing relevant registries:
- `registries/operational_seed_function_registry.json`
- `registries/operational_seed_substrate_registry.json`
- `registries/seed_registry.json`
- `registries/app_seed_pack_type_registry.json`
- `registries/seed_pack_capability_profile_registry.json`

---

## 9. Existing Why-Trace Surface

**Location:** `odin/why_trace/`

Why-trace provides structured reasoning records. PR07 will extend this pattern for field selection traces.

---

## 10. Current Release / Closure Position

**Before this prep PR:** Release / Closure was the next item after Y Pattern Spine.

**After this prep PR:** Release / Closure moves to FINAL-PR-09, after PR06, PR07, and PR08.

The reason: PR06–08 implement the operational seed, field selection, and projection layers
that are required for a complete system acceptance. Releasing before these would leave the
primary operational routing spine unimplemented.

---

## 11. Known Non-Claims at Prep Stage

- No model inference capability implemented yet (Execution Gate only provides mock).
- No production deployment capability.
- No security certification.
- No external send capability.
- No app state authority.
- Odin outputs candidates; apps decide.
- QIRC coordinates; it does not authorize.
- Execution Gate gates mock execution; it does not gate real models.

---

## 12. Constraints for PR06–PR09

**PR06 constraints:**
- Must not use `odin/seeds/` as runtime parent — creates new `odin/operational_seed_spine/`.
- Selector must be deterministic — no model calls.
- Work capsule must always have `candidate_only: true`.
- Token budget must be per-seed, not global.

**PR07 constraints:**
- Must not claim field selection scores are final truth.
- Review axes must be explicit named constants, not computed.
- Why-trace must record evidence items, not fabricated reasoning.
- CoherenceScore must be bounded [0.0, 1.0].

**PR08 constraints:**
- Materialization levels must match Y Pattern Spine M0–M9 exactly.
- ExpressionPacket near_code is text only — not executed.
- CandidateGraph edges must have explicit from/to/relation structure.
- ReceiptLink must have bound_at_utc timestamp.

**PR09 constraints:**
- Must not start until PR06, PR07, PR08 are merged and all validators pass.
- Must not claim production readiness or security certification.
- Must not introduce new runtime features unless required for closure plumbing.

---

## 13. Recommended Base Strategy

**For PR06:** Start from `odin/y_pattern_spine/capsules.py` as a structural reference.
Use `registries/operational_seed_function_registry.json` and `registries/seed_registry.json`
as the seed taxonomy source. Do not blindly copy — read them as source pattern mines.

**For PR07:** Start from `odin/why_trace/` as a structural reference for why-trace patterns.
Use `registries/resonance_band_registry.json` and `registries/y_core_posture_registry.json`
as field taxonomy sources.

**For PR08:** Start from `odin/y_pattern_spine/materialization.py` and the Y materialization
ladder registry. Extend, do not replace.

**For PR09:** Do not start until all validators pass. Treat as a final audit, not a new feature.
