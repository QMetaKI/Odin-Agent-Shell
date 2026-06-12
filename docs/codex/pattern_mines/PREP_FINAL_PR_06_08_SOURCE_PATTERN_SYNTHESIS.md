# PREP FINAL-PR-06..08 — Source Pattern Synthesis

**Claim boundary:** `prep_final_pr_06_08_prepares_future_prs_not_runtime_execution`
**candidate_only:** true
**generated_at_utc:** 2026-01-01T00:00:00Z

---

## Purpose

This document synthesizes Q Metamodell / cutk1 / permanent-memory source concepts into
neutral Odin operational patterns for use in FINAL-PR-06 through PR-08.

Source pattern concepts are treated as a PATTERN MINE ONLY. They are not imported as
runtime truth. Each source concept is neutralized into an operational Odin concept
with a well-defined scope, claim boundary, and implementation target.

---

## 1. Source Pattern Categories

The following source pattern domains are relevant to PR06–PR08:

### A. Seed / Intent Layer
Source concepts: seeds, archetypes, intent routing, center-first routing, operator pattern mining.
Odin role: Seed spine (PR06).

### B. Field / Dominance Layer
Source concepts: DFAS, dominant field activation, suppressed fields, hole density, resonance bands,
field coherence, ring systems, wheel/rad systems.
Odin role: Field selection spine (PR07).

### C. Projection / Shadow / Materialization Layer
Source concepts: shadow runtime, materialization ladders, precompute / AI-without-AI,
projection sets, near-code, near-artifact, narrative compute, Q* narrative structures,
Fairy DSL, middle-out compression.
Odin role: Projection candidate spine (PR08).

### D. Proof / Receipt / QIRC Layer
Source concepts: QIRC, semantic event fabric, proof/receipt discipline,
source-to-candidate derivation, balance/care-force axes.
Odin role: All PRs, via proof modules and QIRC hints.

---

## 2. Why Raw Source Import Is Forbidden

Raw source concept import into Odin runtime is forbidden for these reasons:

1. **Naming ambiguity:** Q Metamodell concepts like "DFAS", "resonance", "archetype"
   carry domain-specific connotations that could be misread as mystical or authority claims.

2. **Scope creep:** Source patterns are broader than Odin's role. Importing them wholesale
   would blur the boundary between Odin (candidate prep) and App (authority/apply).

3. **Religious / mystical naming risk:** Names like "Q Shabang", "Q*", "qmath" could imply
   capabilities beyond what Odin can claim.

4. **Proof contamination:** Source patterns may include claims about intelligence, truth,
   or authority that Odin explicitly does not make.

5. **Runtime confusion:** Names like "shadow runtime" or "narrative aorta" imply hidden
   execution that contradicts Odin's candidate-only posture.

---

## 3. Operational Neutralizations

Each source concept has been neutralized into a neutral Odin operational concept:

| Source Concept | Forbidden Direct Use | Neutral Odin Concept | Why Safe |
|----------------|---------------------|----------------------|----------|
| seed | OK as general term | `IntentSeed` (dataclass) | Explicit fields, no authority |
| archetype | NOT as runtime persona | `RoleProfile` (dataclass) | Neutral behavioral contract |
| DFAS | NOT as module name | `field_selection_spine` (module) | Operational routing, not authority |
| dominant field | OK as term | `DominantField` (dataclass) | Bounded struct, not truth |
| resonance | NOT as score name | `CoherenceScore` (dataclass) | Bounded [0.0,1.0] float |
| mirror axis | NOT as axis name | `ReviewAxis` (dataclass) | Named scoring dimension |
| ring/wheel system | NOT as module name | seed pack groupings | Neutral domain groupings |
| shadow runtime | NOT as module name | `ExpressionPacket` (near-code) | Text only, not executed |
| materialization ladder | OK as concept | `MaterializationLevel` (enum) | Named levels, M0–M9 |
| projection set | OK as concept | `ProjectionSet` (dataclass) | Candidate container |
| narrative aorta | NOT as module name | `ExpressionPacket.near_code` | Text field, not execution |
| Fairy DSL | NOT as runtime | expression packet content format | Text format hint only |
| Q* | NEVER as name | (no equivalent) | Forbidden naming |
| precompute/AI-without-AI | OK as pattern | deterministic selector | No model calls |
| QIRC | OK as existing | QIRC hints (existing module) | Already an Odin surface |
| proof/receipt | OK as concept | proof module + ReceiptLink | Standard Odin pattern |
| care-force axis | NOT as axis name | `review_axes` field | Neutral naming |
| hole density | OK as metric | `HoleDensity` (float) | Bounded 0.0–1.0 |
| center-first routing | OK as concept | `selector.center_first_route()` | Deterministic method |

---

## 4. Seed System Extraction

**Source concept:** Seeds are intent activators in Q Metamodell. They carry trigger patterns,
resonance conditions, and routing preferences.

**Neutralization:**
- Seeds become `IntentSeed` dataclasses with explicit fields.
- Trigger patterns become `trigger_shapes: list[str]` — explicit string matchers.
- Resonance conditions become `qirc_event_hints: list[str]` — suggestions, not activations.
- Routing preferences become `preferred_surfaces: list[str]` — not guaranteed routes.
- Intelligence claims are replaced by `validator_expectations: list[str]` — checked at test time.

**Forbidden:** Seeds do not have personalities, autonomous goals, or memory.

**Target PR:** FINAL-PR-06.

**Source pattern mine references:**
- `registries/seed_registry.json`
- `registries/operational_seed_function_registry.json`
- `registries/app_seed_pack_type_registry.json`

---

## 5. Archetype-to-Role-Profile Extraction

**Source concept:** Archetypes in Q Metamodell carry behavioral traits, style preferences,
and operational tendencies. Examples: builder, guardian, navigator.

**Neutralization:**
- Archetypes become `RoleProfile` dataclasses.
- Style preferences become `allowed_use: list[str]` and `forbidden_use: list[str]`.
- Behavioral traits become `review_axes: list[str]` — scored dimensions, not personalities.
- No runtime persona. No name implies intelligence or identity.

**Required role profiles (neutral names):**
`builder`, `reviewer`, `guard`, `router`, `materializer`,
`proof_binder`, `scope_compressor`, `lineage_tracker`, `devmode_explainer`, `risk_scanner`

**Forbidden role profile names:** Thor, Odin, Loki, Mjolnir, Tyr, any mythological name.
These belong only in historical docs where already present.

**Target PR:** FINAL-PR-06.

**Source pattern mine references:**
- `registries/archetype_role_registry.json`
- `registries/agent_twin_archetype_registry.json`

---

## 6. DFAS-to-Field-Selection Extraction

**Source concept:** DFAS (Dominant Field Activation / Selection) is a Q Metamodell pattern
for selecting which conceptual field dominates a reasoning space. It uses ring-system
resonance, hole density, and balance axes.

**Neutralization:**
- DFAS becomes `field_selection_spine` module (not `dfas` module).
- Ring/wheel resonance becomes `CoherenceScore` with bounded float axes.
- Balance axes become `ReviewAxis` dataclasses with neutral operational names.
- Hole density stays as `HoleDensity` float — already a neutral metric term.
- "DFAS" may appear in PR title and docs for continuity, but NOT in module names or API.

**Key constraint:** Field selection output is a RECOMMENDATION, not a final decision.
The `FieldSelection` struct always has `candidate_only: True` and a `not_proven` list.

**Target PR:** FINAL-PR-07.

**Source pattern mine references:**
- `registries/resonance_band_registry.json`
- `registries/y_core_posture_registry.json`
- `registries/qmath_score_registry.json` (read as pattern mine only; never import as runtime)

---

## 7. Resonance/Mirror/Ring/Wheel-to-Review-Axis Extraction

**Source concept:** Q Metamodell uses resonance bands, mirror axes, ring systems, and
wheel/rad structures to organize field relationships. These are rich conceptual frameworks.

**Neutralization:**
- Resonance bands become review axis IDs: `scope`, `claim_boundary`, `repo_reality`, etc.
- Mirror axes become paired review dimensions (e.g., `candidate_integrity` vs `app_authority`).
- Ring systems become seed pack groupings — no ring names in code.
- Wheel/rad structures become materialization level groupings.
- All resonance scoring is done via CoherenceScore with bounded floats.

**Forbidden:** Do not create modules named `ring_system.py`, `resonance.py`, `wheel.py`, or `rad.py`.

**Target PR:** FINAL-PR-07.

---

## 8. Q*/Narrative/Fairy/Shadow-to-Projection Extraction

**Source concept:** Q* narrative compute, Fairy DSL, and shadow runtime describe
a system for generating, projecting, and materializing candidate expressions.
Shadow runtime implies near-code execution without visible side effects.

**Neutralization:**
- Shadow runtime becomes `ExpressionPacket` — a text container for near-code/near-artifacts.
- Near-code text is a string field, never executed by Odin.
- Fairy DSL becomes a hint format: `ExpressionPacket.near_code` format spec in a comment.
- Narrative aorta becomes `CandidateGraph` — directed acyclic graph of candidate nodes.
- Q* narrative structure becomes `ProjectionSet` — organized candidate container.
- Materialization ladder (M0–M9) is already implemented in Y Pattern Spine; PR08 extends it.

**Key constraint:** Projection candidate spine prepares candidates only. It does NOT execute
shadow code, apply patches, or mutate runtime state.

**Forbidden:** Do not create modules named `shadow_projection.py` or reference hidden execution.

**Target PR:** FINAL-PR-08.

---

## 9. QIRC / AI-without-AI Implications

**Source concept:** QIRC is the semantic event coordination fabric. AI-without-AI refers to
deterministic intelligence patterns that do not require live model inference.

**Odin mapping:**
- QIRC is already implemented in `odin/qirc_core/`. PR06–08 add QIRC hints but do not extend QIRC core.
- AI-without-AI pattern is expressed through deterministic selectors: seed selector, field selector,
  candidate comparator — all run without model calls.
- The proof modules in PR06–08 explicitly document `model_inference` in their `not_proven` lists.

**Implication for PR06:** SeedQircHint produces QIRC event suggestions; QIRC does not execute them.
**Implication for PR07:** FieldWhyTrace is a deterministic trace record; no AI reasoning implied.
**Implication for PR08:** ExpressionPacket near-code is precomputed text; no AI generation implied.

---

## 10. Explicit Forbidden Runtime Import List

The following source pattern names MUST NOT appear as:
- new Python module names
- new Python function names (top-level public)
- new JSON registry keys (top-level)
- new CLI command names
- new schema property names (top-level)

Forbidden names:
- `q_shabang`, `Q_Shabang`, `Q Shabang`
- `qmath`, `q_math`, `qMath`
- `q_state`, `qstate`
- `qgit`, `q_git`
- `qcode`, `q_code`
- `qli`, `q_li`
- `qstar`, `q_star`, `Q*`, `qstar_*`
- Any `q_*` prefix on NEW runtime-facing identifiers

Allowed (existing):
- `QIRC` — already an Odin surface
- `qirc_*` — existing QIRC module prefixes
- `qmath_score_registry.json` — existing registry file (read-only pattern mine reference)

---

## 11. Mapping Table: Source Concept → Neutral Odin Concept → Target PR → Target Surface

| Source Concept | Neutral Odin Concept | Target PR | Target Surface |
|----------------|---------------------|-----------|----------------|
| seed (intent trigger) | `IntentSeed` dataclass | PR06 | `odin/operational_seed_spine/intent_seeds.py` |
| archetype (behavioral) | `RoleProfile` dataclass | PR06 | `odin/operational_seed_spine/role_profiles.py` |
| seed pack (domain group) | `SeedPack` registry | PR06 | `odin/operational_seed_spine/seed_packs.py` |
| center-first routing | `selector.center_first_route()` | PR06 | `odin/operational_seed_spine/selector.py` |
| work capsule (context wrapper) | `SeedWorkCapsule` dataclass | PR06 | `odin/operational_seed_spine/work_capsule.py` |
| token budget (context efficiency) | `SeedTokenBudget` dataclass | PR06 | `odin/operational_seed_spine/token_budget.py` |
| DFAS dominant field | `DominantField` dataclass | PR07 | `odin/field_selection_spine/fields.py` |
| resonance band | `ReviewAxis` dataclass | PR07 | `odin/field_selection_spine/review_axes.py` |
| coherence (field agreement) | `CoherenceScore` dataclass | PR07 | `odin/field_selection_spine/coherence.py` |
| hole density (evidence gap) | `HoleDensity` float | PR07 | `odin/field_selection_spine/hole_density.py` |
| balance / care-force axis | `review_axes` field | PR07 | `odin/field_selection_spine/review_axes.py` |
| why-trace (selection record) | `FieldWhyTrace` dataclass | PR07 | `odin/field_selection_spine/why_trace.py` |
| projection set (candidate org.) | `ProjectionSet` dataclass | PR08 | `odin/projection_candidate_spine/projection_set.py` |
| narrative aorta / candidate graph | `CandidateGraph` dataclass | PR08 | `odin/projection_candidate_spine/candidate_graph.py` |
| materialization ladder (M0–M9) | `MaterializationLevel` constants | PR08 | `odin/projection_candidate_spine/materialization.py` |
| near-code / Fairy DSL | `ExpressionPacket.near_code` (text) | PR08 | `odin/projection_candidate_spine/expression_packet.py` |
| shadow runtime (hidden exec.) | (NOT IMPLEMENTED — candidate text only) | PR08 | `ExpressionPacket` — text field only |
| candidate comparison (tournament) | `CandidateComparison` dataclass | PR08 | `odin/projection_candidate_spine/compare.py` |
| receipt / proof binding | `ReceiptLink` dataclass | PR08 | `odin/projection_candidate_spine/receipt_link.py` |
| QIRC (event coordination) | QIRC hints (existing surface) | PR06 | `odin/operational_seed_spine/qirc_hints.py` |
| AI-without-AI | Deterministic selectors (no model) | PR06–08 | All selector modules |
| proof / receipt discipline | Proof modules + `not_proven` lists | PR06–09 | All `*/proof.py` modules |
