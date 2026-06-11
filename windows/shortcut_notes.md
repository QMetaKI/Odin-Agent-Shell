# Optional Shortcut Notes

**Claim boundary:** `windows_convenience_candidate_only_not_service_not_tray_not_installer_not_signed`

Users may optionally create a Windows shortcut to the manual start helper.

---

## Creating a Shortcut (Optional, Manual)

A user may manually create a shortcut to `scripts\start_odin.bat`.

Steps:
1. Right-click the Desktop (or any folder) → New → Shortcut
2. Target: `<repo root>\scripts\start_odin.bat`
3. Set working directory (Start in): `<repo root>`
4. Name it: `Start Odin`

This shortcut is convenience only.

---

## Shortcut Boundaries

- Shortcut is **not installer proof**
- Shortcut is **not Windows service proof**
- Shortcut is **not tray proof**
- Shortcut is **not target-host proof**
- Shortcut is **not production readiness**
- Shortcut is **not Microsoft Store readiness**
- Creating a shortcut does not constitute deployment
- Creating a shortcut does not constitute release readiness
- App owns apply/state/external-send; shortcut invokes helper only

---

## Shortcut is Optional

Odin does not create, install, or manage shortcuts automatically.
This document describes what a user may do manually.
No shortcut is created by default by any Odin script.

---

## Known Non-Proofs

- not a full Windows app
- not Windows service proof
- not tray proof
- not installer proof
- not signed installer proof
- not target-host proof
- service/tray/signing/installer remains a proof gap
