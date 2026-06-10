# Legacy Quarantine Plan — Local Runtime Hub

## Policy

Quarantine obsolete planning artifacts instead of deleting them. This PR does not move runtime/source files and does not move validator-dependent files. If unsure, mark `review_required`.

## Allowed future move candidates

- Old Codex overlay docs that conflict with the current REAL-GH ladder.
- Old task/bundle plans that present obsolete current status.
- Historical generated prompt packs not referenced by validators.
- Obsolete reports superseded by merged REAL-GH reports.
- Duplicate planning indexes after a validator review.

## Do not move

`odin/`, `odin_app_sdk/`, current schemas, current registries, passing tests, Master Architecture v7.1, Master Specs v7.1, v0.8.7 handoff docs, current REAL-GH reports, root canon entry files, `SYSTEM_MAP.json`, and `FILE_MANIFEST.json`.

## LRH-PR-01 move decision

No files were moved to legacy in LRH-PR-01. `legacy/LEGACY_MAP.json` is intentionally empty because every candidate found during intake either remains current, validator-dependent, or review-required.

## Evidence and claim labels

This rebaseline uses these evidence labels only:

- **Verified now** = command run in this workspace.
- **Repo-grounded** = current file content inspected.
- **Diff-grounded** = current PR diff.
- **Prior-context** = handoff/source-chat memory, not reverified.
- **Inference** = architecture inference, not proof.

Proof boundaries: no production readiness proof, no Windows app proof, no Windows service/tray/installer proof, no live model inference proof, no model quality proof, no security certification proof, no external send proof, no app-state mutation proof.

