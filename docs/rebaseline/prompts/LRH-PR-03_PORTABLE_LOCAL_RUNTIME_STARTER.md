# Codex Prompt — LRH-PR-03 Portable Local Runtime Starter

## Branch

Use `codex/lrh-pr-03-portable-local-runtime-starter`.

## PR title

LRH-PR-03: Portable Local Runtime Starter

## Objective

Add portable start, stop, check and one-shot smoke surfaces for a localhost-only Odin runtime without claiming Windows service, tray, installer or production deployment proof.

## Baseline

Master Architecture v7.1, Master Specs v7.1, the Local Runtime Hub target, the Road-to-100 ladder, candidate-only Odin and app-owned apply/state/external-send boundaries remain authoritative.

## Required intake

Read root canon, Master Architecture, Master Specs, LRH target, current-state audit, build ladder JSON, rebaseline manifest, coverage matrix, Road-to-100 acceptance harness, relevant subsystem docs, schemas, registries and tests.

## Target files
- `scripts/start_odin.bat`
- `scripts/stop_odin.bat`
- `scripts/check_odin.bat`
- `scripts/start_odin.sh`
- `scripts/stop_odin.sh`
- `scripts/check_odin.sh`
- `odin/local_runtime/`
- `docs/LOCAL_RUNTIME_STARTER_V1.md`
- `examples/local_runtime/portable_runtime_config.valid.json`
- `tests/test_lrh_pr_03_portable_local_runtime_starter.py`

## Allowed new files
- `scripts/start_odin.bat`
- `scripts/stop_odin.bat`
- `scripts/check_odin.bat`
- `scripts/start_odin.sh`
- `scripts/stop_odin.sh`
- `scripts/check_odin.sh`
- `odin/local_runtime/`
- `docs/LOCAL_RUNTIME_STARTER_V1.md`
- `examples/local_runtime/`
- `tests/test_lrh_pr_03_portable_local_runtime_starter.py`

## Forbidden scope
- no Windows service implementation
- no tray app
- no installer claim
- no WAN/LAN binding by default
- no production readiness claim

## Required behavior
- one start command binds only to 127.0.0.1 by default
- stop command shuts down only the portable local runtime
- check command reports health and proof gaps
- lockfile prevents ambiguous duplicate runtime starts
- port-in-use handling returns structured guidance

## Required tests
- start/check smoke with local-only host fixture
- port-in-use handling test
- lockfile creation/removal test
- WAN/LAN binding rejection test
- no service/tray/installer claim test

## Required commands
- `future target: python -m odin.cli start --portable --host 127.0.0.1 --port 8877`
- `future target: python -m odin.cli stop --portable`
- `future target: python -m odin.cli check --portable`
- `future target: python -m odin.cli prove-local-runtime --once-smoke`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`

## Acceptance gates
- one clear start command exists
- localhost only by default
- runtime lockfile exists
- port-in-use handling exists
- health endpoint smoke works
- no WAN/LAN binding by default
- no Windows service/tray/installer claim

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
