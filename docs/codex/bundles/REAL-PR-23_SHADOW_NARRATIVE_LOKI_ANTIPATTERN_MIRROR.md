# REAL-PR-23 — Shadow Narrative / Loki / Anti-Pattern Mirror

## Objective
Implement the Shadow Narrative, Anti-Fairy DSL, Loki mediation and narrative anti-pattern mirror as the negative twin to Fairy DSL and Shadow Runtime. This real PR bundle makes Odin able to compile failure stories into gates, negative fixtures, repair routes and Why Trace notes without granting Loki authority or executing prose.

## Internal Tasks Covered
- PR-93
- PR-94
- PR-95
- PR-96
- PR-97

## Primary Files
- docs/SHADOW_NARRATIVE_V7_1.md
- docs/ANTI_FAIRY_DSL_V7_1.md
- docs/LOKI_MEDIATION_LAYER_V7_1.md
- docs/NARRATIVE_ANTIPATTERN_MIRROR_V7_1.md
- docs/SHADOW_NARRATIVE_TO_GATES_V7_1.md
- docs/NARRATIVE_RED_TEAM_COMPILER_V7_1.md
- schemas/v7_1/odin_shadow_narrative.schema.json
- registries/narrative_antipattern_registry.json
- odin/shadow_runtime/shadow_narrative_shadow.py
- tests/test_shadow_narrative_loki_antipattern.py

## Required Behavior
- Shadow Narrative is typed negative IR.
- Anti-Fairy DSL mirrors Fairy DSL with machine-readable mappings.
- Loki emits risk candidates only.
- Anti-patterns map to gates, repairs, fixtures and why-trace notes.
- Runtime behavior remains candidate-only and app-owned apply is preserved.

## Forbidden Scope
- No prose-only execution.
- No Loki authority.
- No app mutation.
- No external send.
- No receipt issuance.
- No unvalidated runtime pack load.
- No hidden negative-policy expansion outside declared gates.

## Definition of Done
- python -m odin.cli validate-all passes.
- pytest suite completes successfully.
- PR-93 through PR-97 are covered in task registry.
- REAL-PR-23 covers PR-93 through PR-97.
- Shadow runtime contract registry contains mappings for all new shadow modules.
- SYSTEM_MAP and FILE_MANIFEST are updated.

## Codex PR Summary Template
```text
REAL-PR-23 — Shadow Narrative / Loki / Anti-Pattern Mirror
Summary:
Validation:
Changed files:
Boundaries preserved:
Known follow-ups:
```

## Senior Review Notes
This bundle is approved only as a typed anti-pattern mirror and red-team compiler. If implementation turns Loki into a decision-maker, executes narrative prose, weakens Odin Final Gate, or treats anti-patterns as fear theatre rather than typed gates, the PR must be rejected.


## Bundle Expansion Notes
REAL-PR-23 is the point where Odin gains a symmetrical negative narrative layer. The bundle should be reviewed as a safety, quality and Codex-buildability improvement, not as a new user-facing persona. The reviewer must verify that each anti-pattern family can produce a negative fixture or remains explicitly documentation-only. The reviewer must also verify that Loki cannot grant permission, cannot accept claims, cannot issue receipts and cannot call tools. All returned values are candidate records for Odin Core and the relevant gate. This bundle should improve Thor handoff safety, QIRC Gold Spine precompute, App Seed Pack security, Universal Model/Agent adapter safety and Runtime Pack validation. The work is complete only when the tests demonstrate that an authority-escalating Loki packet is blocked.

## Additional Definition of Done
- Anti-pattern mirror is trace-linked to Why Trace.
- Shadow-to-gate mapping includes repair routes.
- Failure Story Registry includes severity bands and gate mappings.
- Red-team compiler produces invalid fixture plans.
- REAL-PR-23 remains after REAL-PR-22 and does not disturb previous bundles.
