# Codex Public Build Ready Gate v7.1

## Purpose

This gate tells Codex when the repository is ready to transition from architecture prep to implementation PRs.

## Required before implementation

- validate-all succeeds;
- test suite succeeds;
- FILE_MANIFEST is refreshed;
- SYSTEM_MAP points to all current canon docs;
- root docs are current-canon first;
- Codex real PR bundles are complete;
- GPL-2.0-only files are present;
- no positive overclaim phrases;
- Windows implementation drilldown exists;
- MVP/V1/Power boundaries exist;
- Seed/Pattern Pack security certification exists.

## Implementation entry rule

Codex starts with the first real PR bundle that has no unmet dependency. Codex may not skip ahead to UI richness, provider adapters or Power Mode before foundation gates exist.

## Review rule

Every implementation PR must update tests and the corresponding docs, schemas, registries or System Map when it changes behavior.
