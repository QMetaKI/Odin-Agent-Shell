# REAL-PR-13 — Shadow Runtime Compiler and Runtime Pack System

## Objective

Add Shadow Runtime IR formalization, runtime pack manifests, validators, AOT/cached compilers, loader security and generated gates.

## Internal Tasks Covered

- PR-31
- PR-32
- PR-33
- PR-34
- PR-35
- PR-36
- PR-37

## Primary Files

- `docs/FAIRY_DSL_V7_1.md`
- `docs/YSTAR_NATIVE_DSL_V7_1.md`
- `docs/NARRATIVE_AORTA_V7_1.md`
- `odin/shadow_runtime/`
- `odin/compiler/`
- `schemas/v7_1/`
- `registries/`
- `tests/`

## Required Behavior

- Preserve all v7.1 invariants.
- Add typed narrative/compiler prelude only.
- Keep Fairy prose non-executable.
- Keep Y* mediation non-authoritative.
- Keep runtime packs validation-first.
- Update system map, file manifest and tests.

## Forbidden Scope

- No hot-path live runtime generation.
- No unvalidated runtime pack load.
- No app state mutation.
- No external send.
- No prose-only execution.
- No model-generated executable code.

## Definition of Done

- All covered internal task docs exist.
- `python -m odin.cli validate-all` succeeds.
- `python -m pytest -q -p no:cacheprovider` succeeds.
- New registries and schemas are valid JSON.
- Bundle registry covers all internal tasks.
- Narrative/compiler red lines are enforced by tests or validators.

## Codex PR Summary Template

- Real PR: {bid}
- Internal tasks covered:
- Runtime invariants preserved:
- Narrative compiler artifacts added:
- Validation result:
- Remaining bounded holes:

## Review Notes

This bundle integrates the Narrative Aorta / Y* compiler layer into v7.1. It is not a separate architecture fork. It adds a typed meta-authoring and compiler-prelude layer while keeping v7.1 runtime semantics intact.


## Bundle-Level Review Contract

This real PR bundle is a later Codex pull-request unit. It groups several internal tasks so the actual GitHub review surface remains coherent. The internal tasks remain the fine-grained ladder, but the real bundle is what reviewers should see as one implementable PR.

The reviewer must check three planes simultaneously:

1. Canon plane: Master Architecture v7.1, Master Specs v7.1, claim boundary and app authority remain unchanged.
2. Mechanical plane: schemas, registries, fixtures, tests and validation CLI all agree.
3. Runtime-prelude plane: shadow/compiler artifacts remain preparation artifacts unless a later validated runtime pack loader explicitly implements them.

The bundle may add new docs, schemas, registries, shadow modules, compiler-prelude modules and tests. It may not add unbounded runtime generation, hot-path codegen, direct app mutation, external send capability or model-generated executable code.

## Required Review Evidence

The PR summary must list internal tasks covered, new files, updated registries, validation commands, known holes and explicit boundary preservation. If a runtime behavior is deferred, it must be marked as deferred and bounded rather than implied.

## Merge Criteria

Merge only if all covered internal tasks are satisfied, all validation commands succeed, all added artifacts are represented in FILE_MANIFEST, and the real PR bundle registry still covers every internal task in order.
