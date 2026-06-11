# Windows Convenience Layer V1

**Claim boundary:** `windows_convenience_candidate_only_not_full_windows_app_not_service_not_tray_not_installer_not_signed`

**LRH-PR:** LRH-PR-16
**Status:** candidate-only, local-only

---

## 1. What This Is

This is the Windows convenience layer for Odin Local Runtime Hub.

It provides:
- Manual start/check/stop helper scripts for Windows users
- Windows convenience documentation
- Optional shortcut notes
- Convenience smoke notes
- No-claim guard for service/tray/installer/signing
- Reuse of portable start/check path from LRH-PR-15

This is a **Windows convenience layer** — candidate-only, local-only.
It makes Windows users' manual local start/check flow easier after LRH-PR-15 portable packaging.

---

## 2. What This Is Not

| Claim | Status |
|-------|--------|
| Full Windows app | **not a full Windows app** |
| Windows service proof | **not Windows service proof** |
| Tray app proof | **not tray proof** |
| Installer proof | **not installer proof** |
| Signed installer proof | **not signed installer proof** |
| Target-host proof | **not target-host proof** |
| Microsoft Store readiness | **not Microsoft Store readiness** |
| Production readiness | **not production readiness** |
| Security certification | **not security certification** |
| App apply authority | **no app apply** |
| External send | **no external send** |
| Live model inference | **no live model inference** |
| Model quality proof | **no model quality proof** |

service/tray/signing/installer remains a proof gap, deferred to LRH-PR-25 and LRH-PR-26.

---

## 3. Manual Windows Start

Open a command prompt with working directory set to the repo root, then run:

```bat
scripts\start_odin.bat
```

Environment variables (optional):

```bat
set ODIN_HOST=127.0.0.1
set ODIN_PORT=8877
scripts\start_odin.bat
```

The start helper invokes `python -m odin.cli start --portable --host ... --port ...`.
It binds localhost only by default. It is candidate-only.

---

## 4. Manual Windows Check

manual check path: open a command prompt with working directory set to the repo root, then run:

```bat
scripts\check_odin.bat
```

The check helper invokes `python -m odin.cli check --portable --host ... --port ...`.
It checks localhost only. It is candidate-only.

---

## 5. Manual Windows Stop

manual stop path: open a command prompt with working directory set to the repo root, then run:

```bat
scripts\stop_odin.bat
```

The stop helper invokes `python -m odin.cli stop --portable`.
It is candidate-only.

---

## 6. Optional Shortcut Notes

A user may manually create a shortcut to `scripts\start_odin.bat`.

- Target: `<repo root>\scripts\start_odin.bat`
- Working directory (Start in): `<repo root>`

The shortcut is convenience only. The shortcut is not installer proof. The shortcut is not
Windows service proof. The shortcut is not tray proof. No shortcut is created automatically.

See `windows/shortcut_notes.md` for full details.

---

## 7. Convenience Smoke Notes

Manual local convenience smoke sequence:

```
scripts\start_odin.bat
scripts\check_odin.bat
scripts\stop_odin.bat
```

This is manual local convenience smoke. It is not target-host validation. It is not CI proof.
It is not installer/service/tray proof.

See `windows/convenience_smoke_notes.md` for full details.

---

## 8. Reuse of Portable Package / Start-Check Path

LRH-PR-15 established the portable start/check path via `python -m odin.cli start --portable`
and `python -m odin.cli check --portable`. LRH-PR-16 reuses this path for Windows.

The `.bat` helper scripts are thin wrappers around the same `python -m odin.cli` commands
used by the POSIX `.sh` scripts.

---

## 9. No Service / Tray / Signing / Installer Claim Guard

This PR explicitly does not claim:

- Windows service installation, registration, or management
- Windows tray application implementation or proof
- Installer creation, packaging, or proof
- Code signing or signed distribution proof
- MSIX packaging or Microsoft Store submission
- Admin elevation or UAC bypass
- Registry modification
- Task scheduler modification

service/tray/signing/installer remains a proof gap.
See `windows/NO_SERVICE_TRAY_INSTALLER_PROOF.md` for details.

---

## 10. Proof Boundaries

- `not_windows_service_proof`
- `not_tray_proof`
- `not_installer_proof`
- `not_signed_installer_proof`
- `not_full_windows_app_proof`
- `not_target_host_proof`
- `not_microsoft_store_readiness`
- `not_production_readiness_certification`
- `not_security_certification`
- `not_public_network_api_proof`
- `not_live_model_inference_proof`
- `not_model_quality_proof`
- `not_app_apply_proof`
- `not_app_state_mutation_proof`
- `not_external_send_authority_proof`

---

## 11. Known Non-Proofs

- `windows_service`
- `windows_tray`
- `windows_installer`
- `signed_distribution`
- `target_host_validation`
- `microsoft_store_readiness`
- `full_windows_app`
- `production_readiness`
- `security_certification`
- `public_network_api`
- `live_model_inference`
- `model_quality`
- `app_apply_authority`
- `app_state_mutation`
- `external_send_authority`

---

## 12. Claim Discipline

All outputs from this layer are candidates only. The app owns apply, state, and external sends.
Odin outputs candidates only. No hidden tool execution. No provider API calls without receipt.

This is a Windows convenience layer. It is candidate-only. It is local-only.

---

## 13. PR-18+ / Later Windows Carry-Forward

| Item | Deferred To |
|------|-------------|
| Full acceptance/E2E harness | LRH-PR-17 |
| Agent proof boundary closure | LRH-PR-18 |
| Signed distribution | LRH-PR-25 |
| Windows service/tray/installer target-host proof | LRH-PR-26 |
| Microsoft Store / app store readiness | later |

service/tray/signing/installer remains a proof gap.
