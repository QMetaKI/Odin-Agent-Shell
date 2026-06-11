# No Service / Tray / Installer Proof

**Claim boundary:** `windows_convenience_candidate_only_not_service_not_tray_not_installer_not_signed`

This file is an explicit claim guard for LRH-PR-16.

---

## Explicit Non-Claims

The following are **not proven** by this PR or this directory:

| Item | Status |
|------|--------|
| Windows service | not Windows service proof — deferred to LRH-PR-26 |
| Windows tray app | not tray proof — deferred to LRH-PR-26 |
| Windows installer | not installer proof — deferred to LRH-PR-26 |
| Signed installer | not signed installer proof — deferred to LRH-PR-25 |
| Full Windows app | not a full Windows app — deferred to LRH-PR-26 |
| Microsoft Store | not Microsoft Store readiness — deferred later |
| Target-host validation | not target-host proof — deferred to LRH-PR-26 |
| Production readiness | not production readiness — future |
| Security certification | not security certification — future |
| App apply authority | no app apply — app-owned |
| External send | no external send — app-owned |
| Live model inference | no live model inference — candidate-only |
| Model quality | no model quality proof — candidate-only |

---

## What Is Provided

- Windows convenience layer (candidate-only, local-only)
- Manual start/check/stop helper scripts
- Optional shortcut documentation
- Convenience smoke notes
- No system mutation by default
- service/tray/signing/installer remains a proof gap

---

## Carry-Forward

- `LRH-PR-25` — Packaging / Distribution / Signed Release Readiness
- `LRH-PR-26` — Windows Target-Host Installer / Service / Tray Proof Pack
