# Convenience Smoke Notes

**Claim boundary:** `windows_convenience_candidate_only_not_service_not_tray_not_installer_not_signed`

---

## What These Notes Cover

Manual local convenience smoke for Windows users.
This is not target-host validation. This is not CI proof.
This is not installer/service/tray proof.

---

## Convenience Smoke Sequence

```
scripts\start_odin.bat
scripts\check_odin.bat
scripts\stop_odin.bat
```

Run each from repo root. Working directory must be repo root.

---

## What a Local Smoke Verifies (Candidate-Only)

- Python is on PATH and can run `python -m odin.cli`
- Odin start helper returns without error (locally, manually)
- Odin check helper returns without error (locally, manually)
- Odin stop helper returns without error (locally, manually)

---

## What This Smoke Does Not Verify

- **Not target-host validation** — this is manual, local, convenience only
- **Not CI proof** — not run in CI; manual local receipt only
- **Not installer/service/tray proof** — scripts are manual helpers
- **Not signed distribution** — no signing claimed
- **Not production readiness** — candidate-only
- **Not security certification** — no security audit
- **Not Microsoft Store readiness** — not an app package
- **No app apply** — app owns apply/state/external-send
- **No external send** — local only
- **No live model inference** — candidate-only
- **No model quality proof** — not proven

---

## Known Non-Proofs

service/tray/signing/installer remains a proof gap, deferred to LRH-PR-25 and LRH-PR-26.
