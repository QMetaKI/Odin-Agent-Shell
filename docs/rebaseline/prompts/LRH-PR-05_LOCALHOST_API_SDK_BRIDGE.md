# Codex Prompt — LRH-PR-05 Localhost API Contract Hardening and SDK Bridge v1

## Branch

Use `codex/lrh-pr-05-localhost-api-contract-hardening-and-sdk-bridge-v1`.

## PR title

LRH-PR-05: Localhost API Contract Hardening and SDK Bridge v1

## Objective

Harden the localhost-only API contract and SDK Bridge so host apps can health-check Odin, submit Universal Work and read Candidate Artifacts without giving Odin apply/state/external-send authority.

## Baseline

Master Architecture v7.1, Master Specs v7.1, the Local Runtime Hub target, the Road-to-100 ladder, candidate-only Odin and app-owned apply/state/external-send boundaries remain authoritative.

## Required intake

Read root canon, Master Architecture, Master Specs, LRH target, current-state audit, build ladder JSON, rebaseline manifest, coverage matrix, Road-to-100 acceptance harness, relevant subsystem docs, schemas, registries and tests.

## Target files
- `odin/daemon/local_api.py`
- `odin_app_sdk/client.py`
- `sdk/python/`
- `sdk/typescript/`
- `docs/LOCALHOST_API_CONTRACT_V1.md`
- `docs/SDK_BRIDGE_V1.md`
- `tests/test_lrh_pr_05_localhost_api_sdk_bridge.py`

## Allowed new files
- `odin/daemon/local_api.py`
- `odin_app_sdk/client.py`
- `sdk/python/`
- `sdk/typescript/`
- `docs/LOCALHOST_API_CONTRACT_V1.md`
- `docs/SDK_BRIDGE_V1.md`
- `examples/sdk_bridge/`
- `tests/test_lrh_pr_05_localhost_api_sdk_bridge.py`

## Forbidden scope
- no WAN/LAN API by default
- no app apply endpoint
- no external send endpoint
- no raw app state sent to models
- no provider credential defaults

## Required behavior
- GET /v1/health
- GET /v1/status
- GET /v1/providers
- POST /v1/universal-work
- GET /v1/sessions/{id}
- GET /v1/candidates/{id}
- GET /v1/events
- GET /v1/proof-gaps
- SDK health check
- SDK submit universal work
- SDK read candidate
- structured errors

## Required tests
- API contract positive and negative tests
- localhost-only binding test
- SDK health check test
- SDK Universal Work submit test
- candidate read test
- structured error test
- no apply/external-send endpoint test

## Required commands
- `future target: python -m odin.cli prove-sdk-bridge`
- `python -m pip install -e .`
- `python -m odin.cli validate-current-public-canon`
- `python -m odin.cli validate-all`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider`
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_lrh_pr_05_localhost_api_sdk_bridge.py -p no:cacheprovider`

## Acceptance gates
- localhost-only default
- schema-backed request/response
- SDK health check
- SDK submit universal work
- SDK read candidate
- errors are structured
- no app apply
- no external send

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
