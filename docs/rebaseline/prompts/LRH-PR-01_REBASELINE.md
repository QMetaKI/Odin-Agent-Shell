# Codex Prompt — LRH-PR-01 Rebaseline, Legacy Quarantine, Local Runtime Hub Target

## Branch

Use `codex/rebaseline-local-runtime-hub`.

## PR title

REBASELINE: Local Runtime Hub Target, Legacy Quarantine and 100% Build Ladder

## Objective

Finalize the repo-real control-plane rebaseline, preserve Master Architecture v7.1, define the Local Runtime Hub target, classify current coverage, and publish the executable LRH Road-to-100 ladder without changing runtime behavior.

## Baseline

Master Architecture v7.1, Master Specs v7.1, the Local Runtime Hub target, the Road-to-100 ladder, candidate-only Odin and app-owned apply/state/external-send boundaries remain authoritative.

## Required intake

Read root canon, Master Architecture, Master Specs, LRH target, current-state audit, build ladder JSON, rebaseline manifest, coverage matrix, Road-to-100 acceptance harness, relevant subsystem docs, schemas, registries and tests.

## Target files
- `docs/rebaseline/`
- `registries/local_runtime_hub_build_ladder_v1.json`
- `registries/rebaseline_manifest_v1.json`
- `registries/rebaseline_coverage_matrix_v1.json`
- `registries/road_to_100_acceptance_harness_v1.json`
- `legacy/LEGACY_MAP.json`
- `tests/test_local_runtime_hub_rebaseline.py`
- `SYSTEM_MAP.json`
- `FILE_MANIFEST.json`

## Allowed new files
- `docs/rebaseline/`
- `docs/rebaseline/prompts/`
- `registries/local_runtime_hub_build_ladder_v1.json`
- `registries/rebaseline_manifest_v1.json`
- `registries/rebaseline_coverage_matrix_v1.json`
- `registries/road_to_100_acceptance_harness_v1.json`
- `legacy/LEGACY_INDEX.md`
- `legacy/LEGACY_MAP.json`
- `tests/test_local_runtime_hub_rebaseline.py`

## Forbidden scope
- no runtime behavior changes
- no webapp implementation
- no SDK bridge implementation
- no provider execution
- no app bridge implementation
- no packaging implementation
- no agent commands

## Required behavior
- publish neutral Road-to-100 artifacts
- preserve candidate-only and app-owned apply boundaries
- record proof gaps rather than closing them by documentation
- keep legacy quarantine as quarantine-not-delete

## Required tests
- test required rebaseline docs exist
- test ladder IDs and dependencies are deterministic
- test no stale current-state values remain
- test public naming neutrality in rebaseline artifacts
- test harness JSON is valid

## Required commands
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_local_runtime_hub_rebaseline.py -p no:cacheprovider`
- `python -m odin.cli run-golden-flow`

## Acceptance gates
- current-state audit matches PR #5 branch/head policy
- LRH-PR-01..17 ladder is deterministic
- all rebaseline registries parse as JSON
- no live source file is moved to legacy
- validate-all and pytest pass

## Proof boundaries
- no production readiness proof
- no Windows service/tray/installer proof
- no signed installer proof
- no live model inference proof
- no model quality proof
- no security certification proof
- no public network API proof
- no app-state mutation proof
- no external send authority proof

## Final response format

Summary, Testing, Proof boundaries, Skipped implementation claims, Ready yes/no, Next recommended PR.
