# Manual Windows Start / Check / Stop

**Claim boundary:** `windows_convenience_candidate_only_not_service_not_tray_not_installer_not_signed`

This guide covers the manual start path for Windows users of Odin Local Runtime Hub.

---

## Prerequisites

1. Python 3.10+ installed and on PATH
2. Repo cloned locally
3. `python -m pip install -e .` run from repo root

---

## Manual Start

Open a command prompt in the repo root directory, then run:

```bat
scripts\start_odin.bat
```

Or set custom host/port:

```bat
set ODIN_HOST=127.0.0.1
set ODIN_PORT=8877
scripts\start_odin.bat
```

This is a manual start. It is candidate-only. It is local-only.
It is not a full Windows app. It is not Windows service proof.
It is not tray proof. It is not installer proof. It is not target-host proof.

---

## Manual Check

Open a command prompt in the repo root directory, then run:

```bat
scripts\check_odin.bat
```

This is a manual check. It checks localhost only. It is candidate-only.

---

## Manual Stop

Open a command prompt in the repo root directory, then run:

```bat
scripts\stop_odin.bat
```

---

## Convenience Smoke Sequence

For a quick manual local smoke, run in order:

```bat
scripts\start_odin.bat
scripts\check_odin.bat
scripts\stop_odin.bat
```

This is manual local convenience smoke. It is not target-host validation. It is not CI proof.
It is not installer/service/tray proof.

---

## Optional: CLI Validation

```bat
python -m odin.cli validate-windows-convenience-layer
python -m odin.cli prove-windows-convenience-layer
python -m odin.cli validate-all
```

---

## Known Non-Proofs

- not a full Windows app
- not Windows service proof
- not tray proof
- not installer proof
- not signed installer proof
- not target-host proof
- not Microsoft Store readiness
- not production readiness
- not security certification
- no app apply
- no external send
- no live model inference
- no model quality proof
- service/tray/signing/installer remains a proof gap
