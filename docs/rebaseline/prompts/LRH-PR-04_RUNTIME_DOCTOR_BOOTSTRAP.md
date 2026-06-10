# Codex Prompt — LRH-PR-04 Runtime Doctor, First-Run Bootstrap and Self-Healing

## Branch

Use `codex/lrh-pr-04-runtime-doctor-first-run-bootstrap-and-self-healing`.

## PR title

LRH-PR-04: Runtime Doctor, First-Run Bootstrap and Self-Healing

## Objective

Add deterministic doctor, first-run bootstrap and plan-only repair surfaces for local runtime readiness without silently mutating user state.

## Baseline

Master Architecture v7.1, Master Specs v7.1, the Local Runtime Hub target, the Road-to-100 ladder, candidate-only Odin and app-owned apply/state/external-send boundaries remain authoritative.

## Required intake

Read root canon, Master Architecture, Master Specs, LRH target, current-state audit, build ladder JSON, rebaseline manifest, coverage matrix, Road-to-100 acceptance harness, relevant subsystem docs, schemas, registries and tests.

## Target files
- `odin/doctor/`
- `odin/bootstrap/`
- `docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md`
- `tests/test_lrh_pr_04_runtime_doctor_bootstrap.py`

## Allowed new files
- `odin/doctor/`
- `odin/bootstrap/`
- `docs/RUNTIME_DOCTOR_BOOTSTRAP_V1.md`
- `examples/doctor/`
- `tests/test_lrh_pr_04_runtime_doctor_bootstrap.py`

## Forbidden scope
- no automatic repair without explicit apply gate
- no secret leakage in diagnostics
- no production security claim
- no host validation claim beyond local receipts

## Required behavior
- self-check Python/package/import/config/store/port status
- generate safe first-run config when absent
- emit repair plan without applying changes
- support bundle includes diagnostics without secrets

## Required tests
- doctor success and failure fixtures
- bootstrap idempotence test
- repair plan is plan-only test
- support bundle redaction test

## Required commands
- `future target: python -m odin.cli doctor`
- `future target: python -m odin.cli first-run-bootstrap`
- `future target: python -m odin.cli repair-local-runtime --plan-only`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

## Acceptance gates
- self-checks Python/package/imports/config/store/port
- first-run config generated safely
- repair is plan-only unless explicit apply gate exists
- support bundle includes diagnostics without secrets

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
