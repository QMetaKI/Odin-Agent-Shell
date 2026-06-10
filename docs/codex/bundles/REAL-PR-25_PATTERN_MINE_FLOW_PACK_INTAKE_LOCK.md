# REAL-PR-25 — Pattern Mine Flow Pack Intake Lock

## Objective
Add compile-only Pattern Mine and Flow Pack intake so external pattern mines become seed/flow/runtime-pack candidates.

## Internal Tasks Covered
- PR-103
- PR-104
- PR-105
- PR-106
- PR-107

## Primary Files
- docs/PATTERN_MINE_FLOW_PACK_INTAKE_LOCK_V7_1.md
- docs/FLOW_PACK_TO_SEED_PACK_V7_1.md
- registries/pattern_mine_type_registry.json

## Required Behavior
- Build the lock as candidate-only, local-first, GPL-2.0-only architecture/runtime prep.
- Preserve app-owned apply and Odin Final Gate.
- Add schemas, registries, shadow runtime, fixtures and tests for every new surface.
- Connect documentation, SYSTEM_MAP, FILE_MANIFEST and Codex task registry.

## Forbidden Scope
- No direct app mutation.
- No external send.
- No public network expansion.
- No runtime proof or host validation claim.
- No Pattern Mine, Work Atom or Hub path may bypass Candidate Artifact boundaries.

## Definition of Done
- Internal task documents pass validate-all.
- Bundle registry covers all internal tasks.
- Tests pass.
- Negative fixtures block boundary violations.
- Docs explain how this bundle preserves v7.1.

## Codex PR Summary Template
- Bundle:
- Internal tasks:
- Files changed:
- Validation:
- Boundary review:
- Remaining gaps:

## Senior Review Notes
This bundle is intentionally scoped as preparation and lock-in, not as runtime proof. Codex should implement the smallest useful layer first: schemas, registries, shadow modules, fixtures and tests. Only after those artifacts exist should real runtime handlers be added. Any behavior that would allow app mutation, external send, hidden agent execution, or unvalidated runtime pack loading is outside this bundle.

## Bundle Acceptance Evidence
The final PR for this bundle must include validation output, registry coverage evidence, negative fixture evidence, and a brief explanation of how the bundle keeps Odin as the LLM/agent candidate instance while apps remain sovereign over state and apply.

## Migration Notes
This bundle extends v7.1 without replacing any prior lock. Existing apps, seed packs, QIRC events, Thor handoffs and Candidate Artifacts remain valid. New runtime/product/pattern/atom/hub surfaces must degrade safely when unsupported.

## Additional Bundle Detail
The bundle must be implemented in two phases. Phase one is documentation, schema, registry and shadow runtime. Phase two may add real module stubs and adapters but only after negative tests exist. Every bundle item must update SYSTEM_MAP, FILE_MANIFEST, codex task registry and the real bundle registry. The bundle must be reviewed as a coherent unit because these surfaces are mutually reinforcing: Windows Product Runtime supplies operational reality, Pattern Mine Intake supplies reusable intelligence priors, Work Atom Runtime supplies micro-execution structure, and Odin Hub supplies operational visibility.

The bundle must also document the intended fallback behavior. If a Windows process contract is unsupported, Odin enters safe mode. If a pattern mine cannot be validated, Odin ignores it and records a Why Trace. If a Work Atom graph exceeds budget, Odin splits, holds, or asks context. If Odin Hub cannot show a panel, the daemon remains safe and the user can export a support bundle.
