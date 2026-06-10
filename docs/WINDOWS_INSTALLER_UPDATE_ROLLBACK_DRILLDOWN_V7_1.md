# Windows Installer, Update and Rollback Drilldown v7.1

## Purpose

Define packaging and lifecycle rules before product implementation.

## Installer profiles

### Portable ZIP

First development target. No machine-wide service. Stores data under a user-local directory. Good for Codex and early testers.

### MSIX candidate

Future signed package profile. Requires stricter path, permissions, update and identity rules.

### Winget candidate

Future distribution metadata. Not required for MVP.

## Directory posture

- binaries: local install directory;
- configuration: user app data;
- database: user app data;
- model cache: configurable user path;
- runtime packs: versioned pack directory;
- support bundles: explicit user export path.

## Update lifecycle

```text
UPDATE_AVAILABLE
→ DOWNLOAD_CANDIDATE
→ VERIFY_HASH
→ VERIFY_SIGNATURE_IF_PRESENT
→ STOP_ACCEPTING_WORK
→ SNAPSHOT_STATE
→ APPLY_UPDATE
→ MIGRATE_PACKS
→ START_SAFE_CHECK
→ ACTIVATE | ROLLBACK
```

## Rollback lifecycle

```text
FAILURE_DETECTED
→ STOP_NEW_WORK
→ RESTORE_PREVIOUS_PACK
→ RESTORE_CONFIG_SNAPSHOT
→ START_SAFE_MODE
→ EMIT_WHY_TRACE
→ USER_REVIEW
```

## Migration rule

No migration may delete user data without an explicit backup. No migration may silently weaken claim boundary or permission cards.

## Required artifacts

- install manifest;
- previous version manifest;
- pack manifest;
- migration plan;
- rollback plan;
- support bundle reference;
- user-visible status.
