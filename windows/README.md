# Odin Windows Convenience Layer

**Claim boundary:** `windows_convenience_candidate_only_not_service_not_tray_not_installer_not_signed`

This directory provides Windows convenience documentation and helper metadata for the Odin Local Runtime Hub.

---

## What this is

- Windows convenience layer (LRH-PR-16)
- Manual start/check/stop helper documentation
- Optional shortcut notes
- Convenience smoke notes
- Candidate-only, local-only documentation

---

## What this is not

- **Not a full Windows app**
- **Not Windows service proof**
- **Not tray proof**
- **Not installer proof**
- **Not signed installer proof**
- **Not target-host proof**
- **Not Microsoft Store readiness**
- **Not production readiness**
- **Not security certification**
- **No app apply authority**
- **No external send authority**
- **No live model inference proof**
- **No model quality proof**

service/tray/signing/installer remains a proof gap, deferred to LRH-PR-26.

---

## Manual Start / Check / Stop

| Action | Helper |
|--------|--------|
| Start Odin locally | `scripts\start_odin.bat` |
| Check Odin health | `scripts\check_odin.bat` |
| Stop Odin locally | `scripts\stop_odin.bat` |

Run each from the repo root. Working directory must be the repo root.

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `README.md` | This file — overview and boundaries |
| `manual_start.md` | Step-by-step manual start/check/stop guide |
| `shortcut_notes.md` | Optional user-created shortcut notes |
| `convenience_smoke_notes.md` | Manual local convenience smoke notes |
| `NO_SERVICE_TRAY_INSTALLER_PROOF.md` | Explicit no-claim guard |
| `helper_manifest_v1.json` | Machine-readable helper manifest |

---

## App-Owned Boundaries

The app owns apply, state, and external sends. Odin outputs candidates only.
All Windows helper scripts invoke `python -m odin.cli` and do not mutate app state.

---

## Known Non-Proofs

- `production_readiness`
- `live_model_inference`
- `app_state_mutation`
- `external_send_authority`
- `windows_service`
- `windows_tray`
- `windows_installer`
- `signed_distribution`
- `target_host_validation`
- `microsoft_store_readiness`
- `security_certification`

---

## Next

Full Windows target-host validation, service, tray, and installer proof are deferred to LRH-PR-26.
